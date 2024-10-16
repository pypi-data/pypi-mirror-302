import typing
import abc
from .xrange import XRange


class _ColorIterator:
    def __init__(self):
        self.colors = ["#00f", "#0f0", "#f00", "#0ff", "#f0f", "#ff0"]
        self.index = 0

    def __next__(self):
        result = self.colors[self.index]
        self.index = (self.index + 1) % len(self.colors)
        return result


class MathFunctionBase(abc.ABC):
    __colorizer = _ColorIterator()

    def __init__(
        self,
        *,
        series_name: str | None = None,
        color: str | None = None,
        line_style: str = "-",
    ):
        self.series_name = series_name if series_name is not None else "?"
        if color is None:
            self.color = next(type(self).__colorizer)
        else:
            self.color = color
        self.line_style = line_style

    @abc.abstractmethod
    def __call__(xs: XRange) -> XRange:
        """
        the __call__ function should accept a range of x values and return their resulting y values
        """
        raise NotImplementedError(
            "Subclass must implement __call__ or use MathFunction concrete class"
        )


class MathFunction(MathFunctionBase):
    def __init__(
        self,
        relation: typing.Callable[[XRange], XRange],
        series_name: str | None = None,
        color: str | None = None,
        line_style: str = "-",
    ):
        super().__init__(series_name=series_name, color=color, line_style=line_style)
        self.relation = relation

    def __call__(self, *args, **kwargs) -> XRange:
        return self.relation(*args, **kwargs)

    @property
    def __name__(self) -> str:
        return (
            self.series_name if self.series_name is not None else self.relation.__name__
        )
