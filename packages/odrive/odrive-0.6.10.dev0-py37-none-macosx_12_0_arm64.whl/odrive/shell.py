import asyncio
import code
import os
import platform
import sys
from typing import List, Optional, Dict, Any

import odrive._backports # needed for asyncio.to_thread
from odrive._matplotlib_asyncio import patch_pyplot_once_imported
from odrive.device_manager import DeviceManager, Subscription
from odrive.libodrive import DeviceLostException
from odrive.runtime_device import RuntimeDevice
from odrive.ui import dont_print_on_last_line
import odrive.utils
from odrive.rich_text import RichText, print_rich_text, Color, to_vt100, Style

def print_banner():
    print("Website: https://odriverobotics.com/")
    print("Docs: https://docs.odriverobotics.com/")
    print("Forums: https://discourse.odriverobotics.com/")
    print("Discord: https://discord.gg/k3ZZ3mS")
    print("GUI: https://gui.odriverobotics.com/")

    print()
    print('Please connect your ODrive.')
    print('You can also type help() or quit().')

def print_help(device_path, have_devices):
    print('')
    if not have_devices:
        print('Connect your ODrive to {} and power it up.'.format(device_path))
        print('After that, the following message should appear:')
        print('  "Connected to ODrive [serial number] as odrv0"')
        print('')
        print('Once the ODrive is connected, type "odrv0." and press <tab>')
    else:
        print('Type "odrv0." and press <tab>')
    print('This will present you with all the properties that you can reference')
    print('')
    print('Examples:')
    print('  "odrv0.axis0.pos_estimate" will print the current encoder position on axis 0.')
    print('  "odrv0.axis0.controller.input_pos = 0.5" will send axis 0 to 0.5 turns.')
    print('')

def _import_from(source):
    return {
        k: getattr(source, k)
        for k in dir(source)
        if not k.startswith("_")
    }

async def launch_shell(args, device_manager: DeviceManager):
    """
    Launches an interactive python or IPython command line
    interface.
    As ODrives are connected they are made available as
    "odrv0", "odrv1", ...
    """
    patch_pyplot_once_imported()

    # Must make this event loop reentrant to enable calling sync ODrive
    # functions on the async loop.
    import odrive._nest_asyncio as nest_asyncio
    nest_asyncio.apply()

    if ".dev" in odrive.__version__:
        print("")
        print_rich_text(RichText("Developer Preview", foreground=Color.YELLOW, style=Style.BOLD))
        print("  If you find issues, please report them")
        print("  on https://github.com/odriverobotics/ODrive/issues")
        print("  or better yet, submit a pull request to fix it.")
        print("")

    # Check if IPython is installed
    if args.no_ipython:
        use_ipython = False
    else:
        try:
            import IPython
            use_ipython = True
        except:
            print("Warning: you don't have IPython installed.")
            print("If you want to have an improved interactive console with pretty colors,")
            print("you should install IPython\n")
            use_ipython = False

    shell = ODriveShell(args.path, use_ipython=use_ipython)

    subscription = Subscription.for_serno(args.serial_number, shell.on_connected_device, shell.on_disconnected_device, debug_name="shell")
    device_manager.subscribe(subscription)
    try:
        await shell.interact()
    finally:
        device_manager.unsubscribe(subscription)

class PlainConsole(code.InteractiveConsole):
    """
    Customized version of the plain Python embedded console code.InteractiveConsole.

    Added features:
    - Prevent printing on the last line while a prompt is active (IPython does this already)
    - Don't print exceptions that match ignore_exception_type
    - Async interaction via interact_async()
    """
    def __init__(self, ignore_exception_type: type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._raw_write = None
        self._ignore_exception_type = ignore_exception_type
        self._interact_loop: Optional[asyncio.AbstractEventLoop] = None

    def raw_input(self, prompt=""):
        with dont_print_on_last_line(sys.stderr) as inner_stderr_write:
            with dont_print_on_last_line(sys.stdout) as inner_write:
                self._raw_write = inner_stderr_write
                try:
                    return super().raw_input(prompt)
                finally:
                    self._raw_write = None

    def write(self, data):
        write = sys.stderr.write if self._raw_write is None else self._raw_write
        write(data)

    async def _runcode_coro(self, code):
        _inner_hook = sys.excepthook
        def except_hook(ex_class, ex, trace):
            if ex_class != DeviceLostException:
                _inner_hook(ex_class, ex, trace)
        sys.excepthook = except_hook
        try:
            super().runcode(code)
        finally:
            sys.excepthook = _inner_hook

    def runcode(self,code):
        # console.interact() will be called on a background thread but we
        # want to run user input on the thread that calls Shell.interact(),
        # so we wrap runcode accordingly.
        asyncio.run_coroutine_threadsafe(self._runcode_coro(code), loop=self._interact_loop).result()

    async def interact_async(self, **kwargs):
        self._interact_loop = asyncio.get_running_loop()
        try:
            await asyncio.to_thread(self.interact, **kwargs)
        finally:
            self._interact_loop = None

# # In case we run into issues with IPython pumping the asyncio loop, we can use this:
# 
# import IPython
# class IPythonShell(IPython.terminal.embed.InteractiveShellEmbed):
#     def __init__(self, *args, **kwargs):
#         # crashes on exit on macOS when not using confirm_exit (because something about input() which is only allowed on the main thread)
#         super().__init__(*args, confirm_exit=False, **kwargs)
#         self._interact_loop: Optional[asyncio.AbstractEventLoop] = None
# 
#     async def _run_cell_coro(self, *args, **kwargs):
#         print("proxying run_cell to", threading.current_thread())
#         super().run_cell(*args, **kwargs)
# 
#     def run_cell(self, *args, **kwargs):
#         print("proxying run_cell from", threading.current_thread())
#         asyncio.run_coroutine_threadsafe(self._run_cell_coro(*args, **kwargs), loop=self._interact_loop).result()
# 
#     async def interact_async(self, **kwargs):
#         self._interact_loop = asyncio.get_running_loop()
#         try:
#             await asyncio.to_thread(self.__call__, **kwargs)
#         finally:
#             self._interact_loop = None
# 

class DummyMod(object):
    """A dummy module used for IPython's interactive module when
    a namespace must be assigned to the module's __dict__."""
    __spec__ = None
    __name__ = "shell"

class Shell():
    def __init__(self, use_ipython: bool, ignore_exception_type: type) -> None:
        self._locals = {}
        self._mod = DummyMod()
        self._interact_loop: Optional[asyncio.AbstractEventLoop] = None

        self.use_ipython = use_ipython

        if use_ipython:
            import IPython

            if IPython.core.getipython.get_ipython() is None:
                console = IPython.terminal.embed.InteractiveShellEmbed.instance(banner1='', user_module=self._mod)
            else:
                console = IPython.terminal.embed.InteractiveShellEmbed(banner1='', user_module=self._mod)

            console.set_custom_exc((ignore_exception_type,), Shell._noop_exception_handler)

        else:
            # Enable tab complete if possible
            try:
                import readline # Works only on Unix
                readline.parse_and_bind("tab: complete")
            except:
                sudo_prefix = "" if platform.system() == "Windows" else "sudo "
                print("Warning: could not enable tab-complete. User experience will suffer.\n"
                    "Run `{}pip install readline` and then restart this script to fix this."
                    .format(sudo_prefix))

            console = PlainConsole(ignore_exception_type=ignore_exception_type, locals=self._locals) # TODO

        self.console = console

    @staticmethod
    def _noop_exception_handler(console, etype, value, tb, tb_offset=None):
        pass

    def add_globals(self, variables: Dict[str, Any]):
        self._locals.update(variables)
        for k, v in variables.items():
            setattr(self._mod, k, v)

    async def interact(self):
        if self.use_ipython:
            # This pumps the event loop internally which is made possible by nest_asyncio.
            # So even though this call blocks, it behaves as if it was an async call and
            # does not prevent other asyncio events from being handled.
            #await self.console.interact_async(local_ns=None, module=self._mod)
            self.console()
        else:
            await self.console.interact_async(banner='')

def print_warning(msg: str):
    print_rich_text(RichText(msg, foreground=Color.YELLOW, style=Style.BOLD))

def print_notification(msg: str):
    print_rich_text(RichText(msg, foreground=Color.CYAN, style=Style.BOLD))

class ODriveShell(Shell):
    def __init__(self, device_path: str, use_ipython: bool = True):
        super().__init__(ignore_exception_type=DeviceLostException, use_ipython=use_ipython)

        self._async_tasks = []

        self._known_serial_numbers: List[str] = []
        interactive_variables: dict = {}

        # Import a bunch of variables and functions from various sources
        interactive_variables.update({'odrive': odrive})
        interactive_variables.update(_import_from(odrive.utils))
        interactive_variables.update(_import_from(odrive.enums))
        interactive_variables["help"] = lambda: print_help(device_path, len(self._known_serial_numbers) > 0)

        private_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'odrive_private')
        if os.path.isfile(os.path.join(private_path, '__init__.py')):
            print("loading private plugins...")
            sys.path.insert(0, private_path)
            import odrive_private
            odrive_private.load_odrivetool_plugins(interactive_variables)

        self.add_globals(interactive_variables)
        self.var_names = {}

    def on_connected_device(self, device: RuntimeDevice):
        serial_number_str = device.serial_number

        if not device.verified:
            print_warning("Device {}: Not a genuine ODrive! Some features may not work as expected.".format(serial_number_str))
            display_name, var_name = ("device " + serial_number_str, "dev")

        else:
            fw_version_str = '???' if device.fw_version is None else 'v{}.{}.{}'.format(*device.fw_version)
            display_name, var_name = (f"{device.board.display_name if not device.board is None else 'device'} {serial_number_str} (firmware {fw_version_str})", "odrv")

        if serial_number_str in self._known_serial_numbers:
            verb = "Reconnected"
            index = self._known_serial_numbers.index(serial_number_str)
        else:
            verb = "Connected"
            self._known_serial_numbers.append(serial_number_str)
            index = len(self._known_serial_numbers) - 1

        var_name = var_name + str(index)

        # Publish new device to interactive console
        sync_wrapper = device.sync_wrapper
        sync_wrapper.__sealed__ = False
        try:
            sync_wrapper.__name__ = var_name
        finally:
            sync_wrapper.__sealed__ = True

        self.var_names[device] = var_name
        self.add_globals({var_name: sync_wrapper})
        print_notification("{} to {} as {}".format(verb, display_name, var_name))

    def on_disconnected_device(self, device: RuntimeDevice):
        if not device in self.var_names:
            return # device was ignored when found or failed to connect
        var_name = self.var_names.pop(device)
        print_warning("Oh no {} disappeared".format(var_name))

    def interact(self):
        print_banner()
        return super().interact()
