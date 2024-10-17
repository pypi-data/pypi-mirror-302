import asyncio
import matplotlib.pyplot as plt
import numpy as np
from typing import Callable, List, Tuple

from odrive._internal_utils import await_first
from odrive._matplotlib_asyncio import patch_pyplot, wait_for_close, make_animation
from odrive.async_tree import AsyncProperty
from odrive.recorder import Recorder
from odrive.device_manager import get_device_manager

patch_pyplot(plt) # make plt.show(block=False) work on asyncio threads

class LivePlotter():
    """
    Utility for showing a live plot of ODrive properties.
    """
    def __init__(self, labels: List[List[str]], getter: Callable, window_size: int = 500):
        """
        Must only be called on the main thread.

        :param labels: A nested list of labels that also defines the subplots and the ordering of data.
            Each sublist corresponds to one subplot and can contain multiple lines.
            This must have the same shape as the data returned by ``getter``.
        :param getter: A callable that is invoked at each timestep to get the
            data for plotting.
            The output must have the form ``[[y_series_1, y_series_2, ...], ...]``
            and must have the same shape as ``labels``.
        :param window_size: The x-axis window size (in number of samples) of the plotter.
        """
        self.getter = getter
        self.window_size = window_size

        n_subplots = len(labels)
        self._fig, axes = plt.subplots(n_subplots, 1, sharex=True)
        self._axes = [axes] if n_subplots == 1 else axes
        
        self._lines = [
            [ax.plot([], label=label)[0] for label in labels[i]]
            for i, ax in enumerate(self._axes)
        ]

        # We're not using matplotlib.animation.FuncAnimation because it was
        # causing freezes on some platforms. See notes in function below.
        self._anim = make_animation(self._fig, self._animate, blit=False)

    async def show(self):
        """
        Shows the liveplotter. The figure can be closed by cancelling this
        coroutine.
        """
        plt.show(block=False)
        try:
            await wait_for_close(self._fig, self._anim)
        finally:
            plt.close(self._fig)

    def _animate(self, *fargs):
        x, data = self.getter()

        for lines, lines_data in zip(self._lines, data):
            for line, line_data in zip(lines, lines_data):
                line.set_data(x, line_data)

        x_max = np.max(x)
        for ax in self._axes:
            ax.set_xlim(x_max - self.window_size, x_max)
            ax.relim()
            ax.autoscale_view()
            if len(ax.get_legend_handles_labels()[0]):
                ax.legend(loc='upper left')

def start_liveplotter(properties: List[AsyncProperty], labels: List[List[str]], transform: Callable, window_size: int = 500):
    """
    Starts the liveplotter.

    Returns an awaitable that completes when the plotting window is closed or
    plotting is interrupted by a KeyboardInterrupt.

    The liveplotter can be closed by cancelling the awaitable.

    Parameters documented on odrive.utils.start_liveplotter().
    """

    # Transform list of properties into list of unique keys that will be used to
    # reference data from the recorder.
    single_device = len(set((p._dev for p in properties))) == 1
    if single_device:
        def get_label(p: AsyncProperty): return p._dev.path_of(p._info)
    else:
        def get_label(p: AsyncProperty): return p._dev.sync_wrapper.__name__ + "." + p._dev.path_of(p._info)
    names = [get_label(p) for p in properties]

    # Auto-infer optional arguments
    if transform is None:
        transform = lambda *args: [list(args)]
        if labels is None:
            labels = [names]
    elif labels is None:
        raise ValueError("labels must be given if transform is given")

    recorder = Recorder([
        (get_label(prop), prop._dev.serial_number, [k for k, v in prop._dev.properties.items() if v == prop._info][0], prop._info.codec_name)
        for prop in properties
    ])

    def getter():
        recorder.prune(window_size)
        data = recorder.data
        x = np.arange(recorder.total_samples - len(data), recorder.total_samples)
        y = [data[key] for key in names]
        transformed = transform(*y)
        return x, transformed

    plotter = LivePlotter(labels, getter, window_size=window_size)

    return await_first(
        asyncio.create_task(recorder.run(get_device_manager())),
        asyncio.create_task(plotter.show())
    )

async def run_liveplotter(properties: List[List[Tuple[str, AsyncProperty]]]):
    await start_liveplotter(properties)
