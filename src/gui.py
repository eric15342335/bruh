"""
gui.py 0.7-dev
"""
# -*- coding:utf-8 -*-
import socket
import threading
import time
import tkinter
import traceback
import webbrowser

import psutil
import pynput
import pyperclip
import requests
from PIL import ImageTk, Image

import utils

"""
Issue: Keyboard listener is not working properly in GUI,
but it works fine in CLI.
Current Solution: Temporarily comment out the keyboard listener code in GUI.
"""
try:
    import pyi_splash

    pyi_splash.close()
except ImportError:
    pyi_splash = None

VERSION = utils.versions["GUI"]["version"]
mouse = pynput.mouse.Controller()
keyboard = pynput.keyboard.Controller()
res = utils.Resources(1)


def exit_program() -> None:
    """A dialog asking user to exit the program or not"""
    exit_ui = tkinter.Toplevel(basic)
    exit_ui.title("Confirm Exit")
    res.sound_effect("notice")
    exit_ui_text = tkinter.Label(exit_ui, text="Do you want to exit the program?")
    exit_ui_text.place(x=30, y=10)

    exit_ui_button_y = tkinter.Button(exit_ui, text="Yes", command=basic.destroy, bd=1.2)
    exit_ui_button_y.place(height=30, width=50, x=50, y=50)

    exit_ui_button_n = tkinter.Button(exit_ui, text="No", command=exit_ui.destroy, bd=1.2)
    exit_ui_button_n.place(height=30, width=50, x=150, y=50)

    exit_ui.geometry("%sx%s+%s+%s" % utils.centre_coordinate(basic, 250, 100, False))
    exit_ui.iconbitmap(res.abspath("res/riva.ico"))
    exit_ui.resizable(False, False)
    exit_ui.focus_force()
    exit_ui.mainloop()


def aboutpage() -> None:
    """About page displays version information and credits"""
    about_page = tkinter.Toplevel(basic)
    about_page.title("About")

    about_page.geometry("%sx%s+%s+%s" % utils.centre_coordinate(basic, 350, 190, False))
    about_page.iconbitmap(res.abspath("res/riva.ico"))
    about_page.focus_force()
    about_page.resizable(False, False)

    version_text = tkinter.Label(
        about_page, font=("Segoe UI Light", 21), fg="#0000bb", text="Spam Bot GUI"
    )
    version_text.place(x=130, y=0)

    version_info = tkinter.Label(
        about_page, font=("TkDefaultFont", 11), text=f"Version: {VERSION}", relief="flat"
    )
    version_info.place(x=125, y=46)
    about_page.update_idletasks()
    version_info.place_configure(
        x=(version_text.winfo_width() - version_info.winfo_width()) / 2 + 130
    )
    # relx=1, x=-1, y=60, anchor=tkinter.E

    legendarybbk = ImageTk.PhotoImage(Image.open(res.abspath("res/legendarybbk.jpg")))
    bbk_display = tkinter.Label(about_page, image=legendarybbk)
    bbk_display.place(height=140, width=80, x=30, y=20)

    copyright_info = tkinter.Message(
        about_page,
        font=("TkDefaultFont", 13),
        text="Copyright (c) 2023 eric15342335",
        justify="center",
        width=195,
    )
    copyright_info.place(x=125, y=70)

    github_page = tkinter.Label(about_page, text="Github Repository", bg="#00ffee", cursor="hand2")
    github_page.bind(
        "<Button-1>",
        lambda e: webbrowser.open("https://github.com/eric15342335/bruh", new=0, autoraise=True),
    )
    github_page.place(x=125, y=120)

    dont_click = tkinter.Label(about_page, text="Don't Click Me ", bg="#ffcc00", cursor="hand2")
    dont_click.bind(
        "<Button-1>",
        lambda e: webbrowser.open(
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ", new=0, autoraise=True
        ),
    )
    dont_click.place(x=240, y=120)

    about_ok_button = tkinter.Button(about_page, text="Close", command=about_page.destroy, bd=2.3)
    about_ok_button.place(height=30, width=65, x=390 / 2 - 65 / 2, y=155)

    about_page.mainloop()


def autopastebot() -> None:
    """Paste-Enter Bot function binded to the Button"""

    def main() -> None:
        try:
            spam = utils.SpamBot(int(paste_times.get()), enable_spam_interval.get(), res, basic)

            # def on_press(key) -> False:
            #    """See pynput documentation"""
            #    if key == pynput.keyboard.Key.shift:
            #        spam.reset()

            def paste() -> None:
                """Simulate LEFT_CONTROL + V"""
                while not spam.finished():
                    spam.increase()
                    keyboard.pressed(pynput.keyboard.Key.ctrl_l, "v", pynput.keyboard.Key.enter)
                    time.sleep(spam.interval)
                # Since user can press shift to stop spamming
                # we help him press shift after the spam ends
                # keyboard.press(pynput.keyboard.Key.shift)
                # keyboard.release(pynput.keyboard.Key.shift)

            paste_thread = threading.Thread(target=paste)
            time.sleep(4)
            paste_thread.start()
            # with pynput.keyboard.Listener(on_press=on_press) as listener:
            #    listener.join()
            paste_thread.join()
            res.sound_effect("finish")
            finished = tkinter.Label(basic, text="Spamming has finished.")
            finished.place(x=250, y=270, anchor="center")
            basic.after(3 * 1000, finished.destroy)
        except ValueError:
            value_error = tkinter.Label(basic, text="You have entered an invalid value.")
            value_error.place(x=250, y=270, anchor="center")
            basic.after(3 * 1000, value_error.destroy)

    paste_times_text = tkinter.Label(basic, text="Paste Times : ")
    paste_times_text.place(x=20, y=140)
    paste_times = tkinter.Entry(basic, bd=4)
    paste_times.place(width=170, x=120, y=140)

    confirm_spam = tkinter.Button(basic, text="Start", command=main)
    confirm_spam.place(height=50, width=100, x=200, y=200)

    def hide_inputs() -> None:
        """Clicking button two times will destroy the input widgets"""
        paste_times_text.destroy()
        paste_times.destroy()
        confirm_spam.destroy()
        button1.configure(text="Paste-Enter Bot", command=autopastebot)

    button1.configure(text="Paste-Enter Bot (O)", command=hide_inputs)


def autoclickbot() -> None:
    """Click Bot function binded to the Button"""

    def click_process() -> None:
        try:
            spam = utils.SpamBot(int(global_click_times.get()), False, res, basic)

            # def on_press(key) -> None:
            #    """pynput.keyboard.listener"""
            #    try:
            #        if key == pynput.keyboard.Key.shift:
            #            spam.reset()
            #    except AttributeError:
            #        print(key)

            def click() -> None:
                """the function we use to spam clicks"""
                while not spam.finished():
                    mouse.click(pynput.mouse.Button.left, 1)
                    print("Clicked")
                    spam.increase()
                # keyboard.press(pynput.keyboard.Key.shift)
                # keyboard.release(pynput.keyboard.Key.shift)

            # basic.after(4000, click)
            time.sleep(4)
            click()
            # with pynput.keyboard.Listener(on_press=on_press) as listener:
            #    listener.join()
            res.sound_effect("finish")
            finished = tkinter.Label(basic, text="Clicking has finished.")
            finished.place(x=250, y=270, anchor="center")
            basic.after(3 * 1000, finished.destroy)
        except ValueError:
            value_error = tkinter.Label(basic, text="You have entered an invalid value.")
            value_error.place(x=250, y=270, anchor="center")
            basic.after(3 * 1000, value_error.destroy)

    click_times_text = tkinter.Label(basic, text="Click Times  :")
    click_times_text.place(x=20, y=140)
    global_click_times = tkinter.Entry(basic, bd=4)
    global_click_times.place(width=170, x=120, y=140)

    confirm_click = tkinter.Button(basic, text="Start", command=click_process)
    confirm_click.place(height=50, width=100, x=200, y=200)

    def hide_inputs2() -> None:
        """Clicking button two times will destroy the input widgets"""
        click_times_text.destroy()
        global_click_times.destroy()
        confirm_click.destroy()
        button2.configure(text="Click Bot", command=autoclickbot)

    button2.configure(text="Click Bot (O)", command=hide_inputs2)


def clipboard_check() -> None:
    """Show user clipboard history"""
    clipboard_display = tkinter.Toplevel(basic)
    clipboard_display.title("Clipboard")

    clipboard_display.geometry("%sx%s+%s+%s" % utils.centre_coordinate(basic, 640, 500, False))
    clipboard_display.iconbitmap(res.abspath("res/riva.ico"))
    clipboard_display.focus_force()
    clipboard_display.resizable(False, False)

    text = str(pyperclip.paste())

    clipboard_list_scrollbar = tkinter.Scrollbar(clipboard_display, bd=10)
    clipboard_list_scrollbar.place(height=350, width=20, x=600, y=60)

    clipboard_list_x_scrollbar = tkinter.Scrollbar(clipboard_display, bd=10, orient="horizontal")
    clipboard_list_x_scrollbar.place(height=20, width=580, x=10, y=420)

    clipboard_list = tkinter.Listbox(
        clipboard_display,
        activestyle="none",
        xscrollcommand=clipboard_list_x_scrollbar.set,
        yscrollcommand=clipboard_list_scrollbar.set,
    )
    for line_texts in list(text.split("\n")):
        clipboard_list.insert(tkinter.END, line_texts)
    clipboard_list.place(height=350, width=580, x=10, y=60)
    clipboard_list_scrollbar.config(command=clipboard_list.yview)
    clipboard_list_x_scrollbar.config(command=clipboard_list.xview)

    cb_exit = tkinter.Button(clipboard_display, text="ok", command=clipboard_display.destroy, bd=2)
    cb_exit.place(height=40, width=80, x=10, y=10)

    cb_len = tkinter.Label(clipboard_display, text=f"Clipboard length: {len(text)}")
    cb_len.place(x=95, y=10)

    def cb_experimental_msg() -> None:
        """Experimental Tkinter interface for chatroom, currently sticked to clipboard_display window"""
        clipboard_list.delete(0, tkinter.END)
        clipboard_list.insert(
            tkinter.END,
            f"Current clock: {time.strftime('%H:%M:%S', time.localtime())}",
            "Loading available servers... Please wait",
            "",
        )
        clipboard_display.update_idletasks()
        try:
            server_get = requests.get(utils.SERVER_URL)
            if server_get.status_code != 200:
                clipboard_list.insert(
                    tkinter.END,
                    f"Status code {server_get.status_code}, do the repo exist?",
                )
            else:
                server_get = server_get.json()
                # testing
                # import json
                # server_get = json.load(open(file="E:/bruh/get/server.json", mode='br'))
                clipboard_list.insert(tkinter.END, "List of available servers:")
                try:
                    for index, json in enumerate(server_get):
                        clipboard_list.insert(
                            tkinter.END,
                            f"{index + 1}) {json} "
                            f"{server_get[json]['address']} {server_get[json]['port']}",
                        )
                except IndexError:
                    clipboard_list.insert(tkinter.END, "Error: No server found.")
                clipboard_display.update_idletasks()
                # get self ip address
                ip_address = requests.get("https://httpbin.org/ip").json()["origin"]
                clipboard_list.insert(tkinter.END, "", f"Your IP address is {ip_address}")

                def connect_initialize() -> None:
                    try:
                        selected = int(message_sent.get())
                        if 0 < selected < len(list(server_get)) + 1:
                            selected_server = server_get[list(server_get)[selected - 1]]
                            address, port = (
                                selected_server["address"],
                                selected_server["port"],
                            )
                            try:
                                s_test = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                s_test.close()
                            except socket.error:
                                pass
                            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            sock.settimeout(3)
                            cb_exp_msg_button.configure(text="Connecting...")
                            clipboard_list.insert(tkinter.END, f"\nConnecting to {address}:{port}")
                            clipboard_display.update_idletasks()
                            try:
                                sock.connect((address, port))
                                sock.settimeout(None)
                                clipboard_list.insert(
                                    tkinter.END, "Successfully connected to the server."
                                )
                                cb_exp_msg_button.configure(text="Success")
                                message_sent.delete(0, tkinter.END)

                                def receivemsg() -> None:
                                    """Thread for receive incoming TCP packet"""
                                    while True:
                                        try:
                                            message = sock.recv(utils.BUFFER)
                                            clipboard_list.insert(
                                                tkinter.END,
                                                message.decode(utils.ENCODING),
                                            )
                                            clipboard_list.yview(tkinter.END)
                                            res.sound_effect("receive")
                                        except socket.error:
                                            break

                                username = f"GUI Client <{VERSION}>"
                                sock.send(
                                    f"{utils.return_time(False)}[{username}]{utils.PING_MESSAGE}".encode(
                                        utils.ENCODING
                                    )
                                )
                                rmsg_cb = threading.Thread(target=receivemsg)
                                rmsg_cb.start()

                                def disconnect() -> None:
                                    """Disconnect the TCP connection"""
                                    try:
                                        sock.close()
                                        cb_exp_msg_button.configure(text="Disconnected")
                                        clipboard_list.insert(tkinter.END, "You are disconnected.")
                                    except socket.error:
                                        pass

                                def sentmsg_sent() -> None:
                                    """Thread for sending outgoing TCP packet"""
                                    send_message_button.configure(text="Send")
                                    clipboard_display.update_idletasks()
                                    try:
                                        sock.send(
                                            f"{utils.return_time(False)}[{username}]{message_sent.get()}".encode(
                                                utils.ENCODING
                                            )
                                        )
                                    except socket.error as sending_error:
                                        clipboard_list.insert(
                                            tkinter.END,
                                            "Cannot send message to server.",
                                        )
                                        clipboard_list.yview(tkinter.END)
                                        clipboard_list.insert(tkinter.END, str(sending_error))
                                        for line_send_error in list(
                                            traceback.format_exc().split("\n")
                                        ):
                                            clipboard_list.insert(
                                                clipboard_list.size() + 1,
                                                line_send_error,
                                            )
                                    res.sound_effect("send")
                                    time.sleep(0.2)
                                    send_message_button.configure(text="Send", command=sentmsg_sent)
                                    message_sent.delete(0, tkinter.END)
                                    clipboard_display.update_idletasks()

                                cb_exp_msg_button.configure(text="Disconnect", command=disconnect)
                                send_message_button.configure(text="Send", command=sentmsg_sent)
                                clipboard_display.update_idletasks()
                            except socket.error:
                                clipboard_list.insert(
                                    tkinter.END,
                                    "Connection Failed. Server is not online: timeout",
                                )
                        else:
                            clipboard_list.insert(tkinter.END, "Please enter a valid server.")
                    except ValueError:
                        clipboard_list.insert(tkinter.END, "Please enter a valid value.")

                message_sent = tkinter.Entry(clipboard_display, bd=3)
                message_sent.place(width=540, x=10, y=450)
                send_message_button = tkinter.Button(
                    clipboard_display, text="Connect", command=connect_initialize
                )
                send_message_button.place(height=28, width=70, x=560, y=450)

                clipboard_list.insert(tkinter.END, "\nWhich server would you like to connect?")
                clipboard_list.insert(
                    tkinter.END,
                    f"Enter {list(range(1, len(server_get) + 1))} " "in the text box below.",
                    "",
                )

        except OSError as network_error:
            clipboard_list.insert(tkinter.END, str(network_error))
            for line_error in list(traceback.format_exc().split("\n")):
                clipboard_list.insert(tkinter.END, line_error)
            cb_exp_msg_button.configure(text="Connection failed")
            clipboard_display.update_idletasks()

    cb_exp_msg_button = tkinter.Button(
        clipboard_display, text="Experimental Chatroom", command=cb_experimental_msg
    )
    cb_exp_msg_button.place(height=40, width=210, x=410, y=10)

    clipboard_display.mainloop()


def check_update() -> None:
    """Small window for checking updates (HTTP get raw file)"""
    update = tkinter.Toplevel(basic)
    update.title("Check for updates")

    update_info_scrollbar = tkinter.Scrollbar(update, bd=10)
    update_info_scrollbar.place(height=170, width=15, x=360, y=10)

    update_info_x_scrollbar = tkinter.Scrollbar(update, bd=10, orient="horizontal")
    update_info_x_scrollbar.place(height=15, width=350, x=10, y=170)
    update_info = tkinter.Listbox(
        update,
        activestyle="none",
        xscrollcommand=update_info_x_scrollbar.set,
        yscrollcommand=update_info_scrollbar.set,
    )
    update_info.place(height=160, width=350, x=10, y=10)
    update_info_scrollbar.config(command=update_info.yview)
    update_info_x_scrollbar.config(command=update_info.xview)
    try:
        update_info.insert(tkinter.END, "Checking for updates...")
        newest_version = requests.get(utils.UPDATE_URL)
        if newest_version.status_code != 200:
            update_info.insert(
                tkinter.END,
                f"Status code {newest_version.status_code}, do the repo exist?",
            )
        else:
            newest_version = newest_version.json()
            res.sound_effect("notice")
            for imp in list(newest_version):
                update_info.insert(tkinter.END, f'{imp}: {newest_version[imp]["version"]}')
            if newest_version["GUI"]["version"] != VERSION:
                update_info.insert(
                    tkinter.END,
                    "",
                    f"New version {newest_version['GUI']['version']} is available!",
                )
            else:
                update_info.insert(tkinter.END, "Program is up-to-date!")
    except OSError:
        update_info.insert(tkinter.END, traceback.format_exc())
    update.geometry("%sx%s+%s+%s" % utils.centre_coordinate(basic, 380, 190, False))
    update.iconbitmap(res.abspath("res/riva.ico"))
    update.focus_force()
    update.resizable(False, False)
    update.mainloop()


def keylogger() -> None:
    """Displaying user keyboard input data"""
    keylog_window = tkinter.Toplevel(basic)
    keylog_window.title("Key input detection")
    keylog_list_scrollbar = tkinter.Scrollbar(keylog_window, bd=10)
    keylog_list_scrollbar.place(height=170, width=15, x=360, y=10)

    keylog_list_x_scrollbar = tkinter.Scrollbar(keylog_window, bd=10, orient="horizontal")
    keylog_list_x_scrollbar.place(height=15, width=350, x=10, y=170)
    keylog_list = tkinter.Listbox(
        keylog_window,
        activestyle="none",
        xscrollcommand=keylog_list_x_scrollbar.set,
        yscrollcommand=keylog_list_scrollbar.set,
    )
    keylog_list.place(height=160, width=350, x=10, y=10)
    keylog_list_scrollbar.config(command=keylog_list.yview)
    keylog_list_x_scrollbar.config(command=keylog_list.xview)

    def on_press(key) -> None:
        keylog_list.insert(tkinter.END, "Key pressed: " + str(key).strip("'"))
        keylog_list.yview(tkinter.END)
        if key == pynput.keyboard.Key.shift:
            keylog_window.destroy()

    listener = pynput.keyboard.Listener(on_press=on_press)
    listener.start()
    keylog_list.insert(tkinter.END, "Output pressed key in this window. (Exit: Press Shift)")
    keylog_window.geometry("%sx%s+%s+%s" % utils.centre_coordinate(basic, 380, 190, False))
    keylog_window.iconbitmap(res.abspath("res/riva.ico"))
    keylog_window.focus_force()
    keylog_window.resizable(False, False)
    keylog_window.mainloop()


print(f"Spam Bot GUI v{VERSION} by eric15342335 (c) 2020-2023")
basic = tkinter.Tk()
basic.title("Spam Bot GUI")

height = basic.winfo_screenheight()
width = basic.winfo_screenwidth()

welcome_version = tkinter.Label(basic, font=("TkDefaultFont", 10), text=VERSION)
welcome_version.place(rely=1.0, relx=1.0, x=0, y=0, anchor=tkinter.SE)
welcome_msg = tkinter.Label(basic, font=("Calibri", 14), text="Welcome to Spam Bot GUI !!")
welcome_msg.place(x=20, y=30)

neko_vanilla = ImageTk.PhotoImage(Image.open(res.abspath("res/vanilla.png")))
neko_vanilla_display = tkinter.Label(basic, image=neko_vanilla)
neko_vanilla_display.place(x=300, y=15)

cat_noob = ImageTk.PhotoImage(Image.open(res.abspath("res/cat.png")))
cat_noob_background = tkinter.Label(basic, image=cat_noob)
cat_noob_background.place(rely=1.0, relx=1.0, x=0, y=-25, anchor=tkinter.SE)

button1 = tkinter.Button(basic, text="Paste-Enter Bot", command=autopastebot)
button1.place(height=40, width=120, x=20, y=70)

button2 = tkinter.Button(basic, text="Click Bot", command=autoclickbot)
button2.place(height=40, width=100, x=150, y=70)

button3 = tkinter.Button(basic, text="Clipboard / Chatroom", command=clipboard_check)
button3.place(height=40, width=160, x=320, y=70)


class Clock:
    """Display CPU load and current time"""

    interval = 500  # refresh rate, in millisecond
    enabled = tkinter.BooleanVar()
    enabled.set(False)

    def __init__(self) -> None:
        """Initialize the Clock() process"""
        self.text = "Loading..."
        self.label = tkinter.Label(basic, text=self.get_update())
        self.label.place(relx=1, y=-5, anchor=tkinter.NE)
        threading.Thread(target=self.update).start()

    def get_update_thread(self) -> None:
        """Defining a thread for getting CPU load by psutil"""
        self.text = str(
            f"CPU: {psutil.cpu_percent(1)}% {time.strftime('%H:%M:%S', time.localtime())}"
        )

    def get_update(self) -> str:
        """Execute the thread and return value"""
        threading.Thread(target=self.get_update_thread).start()
        return self.text

    def update(self) -> None:
        """Checking whether the user has enabled the 'update clock' option"""
        if self.enabled.get():
            # see 'Stop the clock pls'
            basic.after(self.interval, self.update)
        else:
            self.label.configure(text=self.get_update())
            basic.after(self.interval, self.update)
            basic.update_idletasks()


Clock()

enable_spam_interval = tkinter.BooleanVar()
enable_spam_interval.set(False)

sound_enabled = tkinter.BooleanVar()
sound_enabled.set(True)

menu_file = tkinter.Menu(basic)
menu_view = tkinter.Menu(menu_file, tearoff=0)
file_item = tkinter.Menu(menu_file, tearoff=0)
about_infos = tkinter.Menu(menu_file, tearoff=0)
menu_view.add_command(label="Exit", command=exit_program)
file_item.add_checkbutton(
    label="Enable Spam Interval",
    onvalue=True,
    offvalue=False,
    variable=enable_spam_interval,
)
file_item.add_checkbutton(
    label="Enable Sound", onvalue=True, offvalue=False, variable=sound_enabled
)
file_item.add_checkbutton(
    label="Pause the Clock", onvalue=True, offvalue=False, variable=Clock.enabled
)
about_infos.add_command(label="Check for updates", command=check_update)
about_infos.add_command(label="Debug (Keyboard)", command=keylogger)
about_infos.add_command(label="About", command=aboutpage)
menu_file.add_cascade(label="File", menu=menu_view)
menu_file.add_cascade(label="Options", menu=file_item)
menu_file.add_cascade(label="Help", menu=about_infos)
basic.config(menu=menu_file)
basic.geometry("%sx%s+%s+%s" % utils.centre_coordinate(basic, 500, 290, True))
basic.iconbitmap(res.abspath("res/riva.ico"))
basic.focus_force()
basic.resizable(False, False)
basic.update_idletasks()
basic.mainloop()
