import typing
import numpy as np

from .mathfunction import MathFunction
from .xrange import XRange
from .axes import Axes

import matplotlib.pyplot as plt


class Graph:
    def __init__(
        self,
        *funcs: MathFunction | typing.Callable[[XRange], XRange],
        xs: XRange,
        show_legend: bool = True,
        title: str | None = None,
        axes: Axes = Axes(x_label="x", y_label="y"),
        plotter=plt,
    ) -> None:
        self.funcs = funcs
        self._xvals = xs
        self.axes = axes
        self.show_legend = show_legend
        self.title = title
        self.plotter = plotter

        self.grid = True

        self._yvals: list[XRange] | None = None

    def compute(self) -> list[XRange]:
        """
        @postcondition: self._yvals is iterable
        """
        self._yvals = [f(self._xvals) for f in self.funcs]
        return self._yvals

    @property
    def x_min(self) -> float:
        return min(self._xvals)

    @property
    def x_max(self) -> float:
        return max(self._xvals)

    @property
    def delta(self) -> float:
        return (max(self._xvals) - min(self._xvals)) / len(self._xvals)

    @property
    def last_computed_result(self):
        return self._yvals

    def show(self):
        self.compute()
        # always assigns [...] to self._yvals

        # Plot the function

        for index, y_val in enumerate(typing.cast(list[np.ndarray], self._yvals)):
            if isinstance(self.funcs[index], MathFunction):
                fn = typing.cast(MathFunction, self.funcs[index])
                self.plotter.plot(
                    self._xvals,
                    y_val,
                    label=f"{fn.series_name}",
                    color=f"{fn.color}",
                    linestyle=f"{fn.line_style}",
                )
            else:
                self.plotter.plot(
                    self._xvals,
                    y_val,
                    label=f"{self.funcs[index].__name__}",
                )
        self.plotter.xlabel(self.axes.x_label)
        self.plotter.ylabel(self.axes.y_label)
        self.plotter.title(
            f"Plot of {self.funcs[0].__name__} with bounds {(self.x_min, self.x_max)}"
            if self.title is None
            else self.title
        )
        if self.show_legend:
            self.plotter.legend()
        self.plotter.grid(self.grid)
        self.plotter.show()
