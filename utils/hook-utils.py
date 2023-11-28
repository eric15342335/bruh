import os
from os import path

res_folder = path.join(path.dirname(path.abspath(__file__)), os.pardir, "src", "res")

# hiddenimports = ["winsound", "tkinter", "os", "sys", "time"]
datas = [(res_folder, "res")]
