from typing import Callable, Generic, TypeVarTuple, Unpack, List

Type = TypeVarTuple("Type")

class Signal(Generic[Unpack[Type]]):
    def __init__(self):
        self._subscribers: List[Callable[[Unpack[Type]], None]] = []

    def connect(self, callback: Callable[[Unpack[Type]], None]) -> None:
        self._subscribers.append(callback)

    def disconnect(self, callback: Callable[[Unpack[Type]], None]) -> None:
        if callback in self._subscribers:
            self._subscribers.remove(callback)

    def emit(self, *args: Unpack[Type]) -> None:
        for callback in self._subscribers:
            callback(*args)
