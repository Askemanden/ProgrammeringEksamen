from typing import Callable, Generic, TypeVarTuple, Unpack, List

Args = TypeVarTuple("Args")

class Signal(Generic[Unpack[Args]]):
    def __init__(self):
        self._subscribers: List[Callable[[Unpack[Args]], None]] = []

    def connect(self, callback: Callable[[Unpack[Args]], None]) -> None:
        if callback not in self._subscribers:
            self._subscribers.append(callback)

    def disconnect(self, callback: Callable[[Unpack[Args]], None]) -> None:
        if callback in self._subscribers:
            self._subscribers.remove(callback)

    def emit(self, *args: Unpack[Args]) -> None:
        for callback in self._subscribers:
            callback(*args)
