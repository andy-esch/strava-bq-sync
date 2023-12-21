from typing import Callable, TypeVar

T = TypeVar("T")

Supplier = Callable[[], T]
