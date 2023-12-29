from os import path, pardir

# you must run pyinstaller command from the root directory bruh/
# if you don't want to change this
res_folder = path.join(path.dirname(path.abspath(__file__)), pardir, "src", "res")
version_file = path.join(path.dirname(path.abspath(__file__)), pardir, "src", "get", "version.json")

# hiddenimports = ["winsound", "tkinter", "os", "sys", "time"]
# is it necessary to include hiddenimports?

datas = [(res_folder, "res"), (version_file, "get")]
