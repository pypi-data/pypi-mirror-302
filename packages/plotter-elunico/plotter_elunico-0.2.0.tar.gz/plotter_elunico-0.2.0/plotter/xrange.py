import typing

F = typing.TypeVar("F", covariant=True)


class IndexedIterator(typing.Iterator[F], typing.Sized):
    pass


class XRange(typing.Protocol[F]):
    def __len__(self) -> int:
        ...

    def __iter__(self) -> IndexedIterator[F]:
        ...

    def __add__(self, other: object) -> "XRange[F]":
        ...

    def __sub__(self, other: object) -> "XRange[F]":
        ...

    def __mul__(self, other: object) -> "XRange[F]":
        ...

    def __div__(self, other: object) -> "XRange[F]":
        ...
