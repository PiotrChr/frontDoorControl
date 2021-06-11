from src.lib.screen import screen as libscreen


class DisplayController:
    def __init__(
            self,
            screen: libscreen.Screen
    ) -> None:
        self.screen = screen

