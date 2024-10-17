
import json
import os
import tempfile
from typing import List

from odrive._internal_utils import transform_odrive_objects
from odrive.async_tree import AsyncProperty
from odrive.libodrive import DeviceLostException
from odrive.runtime_device import RuntimeDevice
from odrive.ui import OperationAbortedException, yes_no_prompt

def _flatten(prefix: List[str], config: dict):
    for k, v in config.items():
        if isinstance(v, dict):
            yield from _flatten(prefix + [k], v)
        else:
            yield '.'.join(prefix + [k]), v

@transform_odrive_objects
async def restore_config(device: RuntimeDevice, config: dict):
    """
    Restores the configuration of the ODrive from a dictionary.

    :param device: The ODrive to write the config to.
    :param config: A dictionary of the form {path: value}
    """
    errors = []

    # flatten config dict for legacy compatibility
    config = {k: v for k, v in _flatten([], config)}

    for name, v in config.items():
        try:
            prop_info = device.properties[name]
            if isinstance(v, str) and prop_info.codec_name == 'endpoint_ref':
                v = AsyncProperty(device, prop_info)
            await device.write(name, v)
        except Exception as ex:
            errors.append("Could not restore {}: {}".format(name, str(ex)))

    return errors

@transform_odrive_objects
async def backup_config(device: RuntimeDevice) -> dict:
    """
    Returns a dict of the form {path: value} containing all properties on the
    ODrive that have "config" in their path.

    :param device: The device to read from
    """
    config_properties = [(name, prop) for name, prop in device.properties.items() if ".config." in f".{name}."]

    vals = await device.read_multiple([p for _, p in config_properties])

    return {
        config_properties[i][0]: device.path_of(val._info) if isinstance(val, AsyncProperty) else val
        for i, val in enumerate(vals)
    }


def get_temp_config_filename(device: RuntimeDevice):
    serial_number = device.serial_number
    safe_serial_number = ''.join(filter(str.isalnum, serial_number))
    return os.path.join(tempfile.gettempdir(), 'odrive-config-{}.json'.format(safe_serial_number))

@transform_odrive_objects
async def backup_config_ui(device: RuntimeDevice, filename, logger):
    """
    Exports the configuration of an ODrive to a JSON file.
    If no file name is provided, the file is placed into a
    temporary directory.
    """

    if filename is None:
        filename = get_temp_config_filename(device)

    logger.info("Saving configuration to {}...".format(filename))

    if os.path.exists(filename):
        if not yes_no_prompt("The file {} already exists. Do you want to override it?".format(filename), True):
            raise OperationAbortedException()

    data = await backup_config(device)
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2)
    logger.info("Configuration saved.")

@transform_odrive_objects
async def restore_config_ui(device: RuntimeDevice, filename, logger):
    """
    Restores the configuration stored in a file 
    """

    if filename is None:
        filename = get_temp_config_filename(device)

    with open(filename) as file:
        data = json.load(file)

    logger.info("Restoring configuration from {}...".format(filename))
    errors = await restore_config(device, data)

    for error in errors:
        logger.info(error)
    if errors:
        logger.warn("Some of the configuration could not be restored.")
    
    try:
        await device.call_function('save_configuration')
    except DeviceLostException:
        pass # Saving configuration makes the device reboot
    logger.info("Configuration restored.")
