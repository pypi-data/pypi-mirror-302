"""
Wrappers to allow for pythonic asynchronous usage of libodrive.Device objects.

`AsyncObject` wrappers are not thread-safe.
"""

from typing import List
from odrive.codecs import codecs
from odrive.libodrive import Device
from odrive.runtime_device import FunctionInfo, PropertyInfo, RuntimeDevice

class AsyncObject():
    __sealed__ = False

    def __init__(self, dev: RuntimeDevice, path: str):
        self._dev = dev
        self._path = path

    def __setattr__(self, key, value):
        if self.__sealed__:
            oldval = getattr(self, key, None)
            if isinstance(oldval, AsyncProperty):
                raise AttributeError(f"Property {key} cannot be assigned to directly. Try `await {key}.write(val)`.")
            elif oldval is not None:
                raise AttributeError(f"Attribute {key} cannot be overwritten.")
            else:
                raise AttributeError(f"Attribute {key} not found.")
        object.__setattr__(self, key, value)

    @staticmethod
    def from_json(device: RuntimeDevice, json: list, prefix: List[str] = []):
        generated_type = type('anonymous_interface', (AsyncObject,), {})
        obj = generated_type(device, '.'.join(prefix))

        for child in json:
            codec_name = child['type']
            if codec_name == 'json':
                pass # ignore first endpoint
            elif codec_name == 'function':
                func = AsyncFunction(device, FunctionInfo.from_json(child))
                setattr(obj, child['name'], func)
            elif codec_name == 'object':
                child_obj = AsyncObject.from_json(device, child['members'], prefix + [child['name']])
                setattr(obj, child['name'], child_obj)
            else:
                codec = codecs.get(child['type'], None)
                if codec is None:
                    raise Exception("unsupported codec {}".format(codec_name))
                setattr(obj, child['name'], AsyncProperty(device, PropertyInfo.from_json(child)))

        obj.__sealed__ = True
        return obj

class AsyncProperty():
    def __init__(self, device: RuntimeDevice, info: PropertyInfo):
        self._dev = device
        self._info = info

    def read(self):
        return self._dev.read(self._info)

    def write(self, val):
        return self._dev.write(self._info, val)

class AsyncFunction():
    def __init__(self, device: RuntimeDevice, info: FunctionInfo):
        self._dev = device
        self._info = info

    def __call__(self, *args):
        return self._dev.call_function(self._info, *args)
