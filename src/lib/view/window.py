import tkinter


class Window:
    def __init__(self):
        self.tkinter = tkinter
        self.master = tkinter.Tk()
        self.main_frame = self.create_main_frame(self.master)
        self.main_frame.pack(expand=True)

    def init(self, title):
        self.master.title(title)

    def create_main_frame(self, container):
        main_frame = self.tkinter.Frame(container)

        return main_frame

    def set_fullscreen(self):
        self.master.overrideredirect(False)
        self.master.attributes('-fullscreen', True)
        # self.master.attributes('-zoomed', True)

    def start(self):
        self.master.mainloop()

    def close(self):
        self.master.quit()
        # self.master = None
        # self.main_frame = None
        # self.tkinter = None
