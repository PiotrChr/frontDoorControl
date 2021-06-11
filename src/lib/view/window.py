import tkinter


class Window:
    def __init__(self, title):
        self.master = tkinter.Tk()
        self.master.title(title)

        self.main_frame = self.create_main_frame()
        self.main_frame.pack()

    def create_main_frame(self):
        main_frame = tkinter.Frame()

        return main_frame

    def set_fullscreen(self):
        self.master.overrideredirect(False)
        self.master.attributes('-fullscreen', True)

    def start(self):
        self.master.mainloop()

    def close(self):
        self.master.destroy()
