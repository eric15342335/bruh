"""
Functions that shares between cli/gui scripts
"""
# -*- coding:utf-8 -*-
import os
import time
import tkinter

import winsound

UPDATE_URL = "https://raw.githubusercontent.com/eric15342335/bruh/main/get/version.json"
SERVER_URL = "https://raw.githubusercontent.com/eric15342335/bruh/main/get/server.json"
BUFFER = 4096
ENCODING = "utf-8"
PING_MESSAGE = " Client PING"

versions = {"CLI": {"version": "1.3.4"}, "GUI": {"version": "0.6.3"}}

sounds = {
    "send": "send_msg.wav",
    "receive": "receive_msg.wav",
    "finish": "finish.wav",
    "notice": "asterisk.wav",
}


class Resources:
    """Accessing files"""

    def __init__(self, _script: [0, 1]) -> None:
        # self.base_path = getattr(
        #    sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__))
        # )
        # Starting from PyInstaller 4.3, sys._MEIPASS is superseded by __file__
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.sound_enable = True
        if _script == 0:  # cli only need .wav file
            self._initialize(".wav")
        elif _script == 1:  # gui need to preload all files
            self._initialize()

    def _initialize(self, ends: str = "") -> None:
        """Read all files under the "res" folder"""
        for entry in os.scandir(self.abspath("res")).__iter__():
            if entry.is_file() and entry.name.endswith(ends):
                with open(file=entry.path, mode="br") as file:
                    file.read()
                    # todo: should we catch FileNotFoundError?

    def abspath(self, *relative_path: str) -> str:
        """Return the absolute path"""
        return os.path.join(self.base_path, *relative_path)

    def sound_effect(self, which: str) -> None:
        """Provide a handy function to play sounds"""
        if self.sound_enable:
            winsound.PlaySound(self.abspath("res", sounds[which]), winsound.SND_ASYNC)


def return_time(file: bool = False) -> str:
    """Return the current time [12:12:12]"""
    _sp = "-" if file else ":"  # separator as windows does not allow ":" in file name
    now_time = time.strftime(f"%H{_sp}%M{_sp}%S", time.localtime())
    return "[%s]" % now_time


def centre_coordinate(root: tkinter.Tk, width: int, height: int, is_base: bool = True) -> tuple:
    if is_base:
        root_width, root_height = root.winfo_screenwidth(), root.winfo_screenheight()
        return (
            width,
            height,
            int(root_width / 2 - width / 2),
            int(root_height / 2 - height / 2),
        )
    # root.window.update_idletasks()
    base_width = root.winfo_width()
    base_height = root.winfo_height()
    height_coord = (
        root.winfo_rooty() + (base_height - height) / 2 - 20
    )  # -20: modifier of the [-] [X] space
    width_coord = root.winfo_rootx() + (base_width - width) / 2
    print(width, height, int(width_coord), int(height_coord))
    return width, height, int(width_coord), int(height_coord)


class SpamBot:
    """Encapsulate variables into a class to prevent global variable warnings"""

    alert_text = "You now have 4 seconds to prepare. you can press shift to stop."

    def __init__(self, times: int, interval: bool, res: Resources, root: tkinter.Tk = None) -> None:
        """parse variables to SpamBot class"""
        # use for debugging: winsound.PlaySound(("res/finish.wav"), winsound.SND_ASYNC)
        self.times = times
        if interval:
            self.interval = 0.5
        else:
            self.interval = 0.1
        self.times_spammed = 0
        """ Creates a Tkinter window to display warning texts """
        if root:
            notification = tkinter.Toplevel(root)
            self.root = root
        else:
            notification = tkinter.Tk()
            self.root = notification

        notification.title("Spam Bot Ready")
        notification.attributes("-topmost", True)

        notification.geometry("%sx%s+%s+%s" % centre_coordinate(self.root, 350, 100))
        notification.resizable(False, False)
        notification.iconbitmap(res.abspath("res/riva.ico"))
        notification.focus_force()

        notific_text = tkinter.Text(notification, font=("TkDefaultFont", 10))
        notific_text.insert(tkinter.END, self.alert_text)
        notific_text.pack()
        notific_button = tkinter.Button(
            notification, text="Okay", command=notification.quit, bd=1.8
        )
        notific_button.place(height=30, width=90, anchor="center", x=175, y=75)

        winsound.PlaySound("res/finish.wav", winsound.SND_ASYNC)

        notification.mainloop()
        notification.destroy()

    def increase(self, times: int = 1) -> None:
        """record number of times of clicks/paste"""
        self.times_spammed += times

    def reset(self) -> None:
        """Reset the variables"""
        self.times_spammed = self.times

    def finished(self) -> bool:
        """Check if spamming is finished"""
        return self.times_spammed > self.times


# SpamBot(1, True, Resources(GUI))
