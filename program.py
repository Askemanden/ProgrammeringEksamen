from typing import Tuple

class Program():
    def __init__(self, width : int = 800, height : int = 600) -> None:
        self.screen_size : Tuple[int, int] = (width, height)
        self.running = True

    def quit(self):
        self.running = False