
import asyncio
import functools
from typing import List, Tuple

import numpy as np
import numpy.ma as ma
from odrive.device_manager import DeviceManager, Subscription
from odrive.libodrive import DeviceLostException, DiscoveryDelegate
from odrive.runtime_device import PropertyInfo, RuntimeDevice

_codecs = {
    'int8': np.int8,
    'uint8': np.uint8,
    'int16': np.int16,
    'uint16': np.uint16,
    'int32': np.int32,
    'uint32': np.uint32,
    'int64': np.int64,
    'uint64': np.uint64,
    'bool': np.bool_,
    'float': np.float32,
}

async def _noop_fetcher(frame):
    pass

async def _read_single_dev(dev: RuntimeDevice, indices: List[int], props: List[PropertyInfo], frame):
    try:
        vals = await dev.read_multiple(props)
        for i, val in enumerate(vals):
            frame[indices[i]] = val
    except DeviceLostException:
        pass # This should only happen once, after that the fetcher is replaced by _noop_fetcher

class Recorder(DiscoveryDelegate):
    """
    Utility for continuous recording of data from one or multiple ODrives.
    Takes care of disappearing and reappearing ODrives.

    properties: (name, serial_number, property_name, codec_name)
        name is used as column name in the numpy array
        serial_number and property_name are used to identify the property across reboots
        codec_name defines the data type of the numpy array
    """
    def __init__(self, properties: List[Tuple[str, str, str, str]], interval: float = 0.01):
        self.properties = properties
        self.interval = interval

        for _, _, path, codec_name in properties:
            if not codec_name in _codecs:
                raise Exception(f"Cannot plot property {path} of type {codec_name}")

        self._dt = np.dtype([
            (name, _codecs[codec_name])
            for name, _, _, codec_name in properties
        ])
        self.data = ma.zeros(0, dtype=self._dt)
        self.total_samples = 0
        self._devices = list(set(sn for _, sn, _, _ in properties))
        self._fetchers = [_noop_fetcher for _ in range(len(self._devices))]

    def on_connected(self, dev: RuntimeDevice):
        indices_and_props = [
            (i, dev.get_prop_info(path, codec_name))
            for i, (_, sn, path, codec_name) in enumerate(self.properties)
            if sn == dev.serial_number
        ]
        indices = [i for i, p in indices_and_props if not p is None]
        props = [p for i, p in indices_and_props if not p is None]
        self._fetchers[self._devices.index(dev.serial_number)] = functools.partial(_read_single_dev, dev, indices, props)

    def on_disconnected(self, dev: RuntimeDevice):
        self._fetchers[self._devices.index(dev.serial_number)] = _noop_fetcher

    def prune(self, n_retain: int):
        self.data = self.data[-n_retain:]

    def _append(self, frame):
        self.data = ma.concatenate([self.data, frame])
        self.total_samples += len(frame)

    async def run(self, device_manager: DeviceManager):
        """
        Runs the recorder until the coroutine is cancelled.
        """
        subscription = Subscription.for_serno(self._devices, self.on_connected, self.on_disconnected, debug_name="Recorder.run()")
        device_manager.subscribe(subscription)
        try:

            while True:
                frame = ma.masked_all(1, dtype=self._dt)
                frame0 = frame[0]

                fetch_interval_awaitable = asyncio.create_task(asyncio.sleep(self.interval))
                await asyncio.gather(
                    *[fetcher(frame0) for fetcher in self._fetchers]
                )
                self._append(frame)

                await fetch_interval_awaitable

        finally:
            device_manager.unsubscribe(subscription)
