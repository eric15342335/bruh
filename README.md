# SpamBot

## What is this?

Created just for fun.

This is my first attempt to create a usable (not really) GUI interface for a python script.

## Functionality

1. SpamBot (Ctrl+V)
2. ClickBot
3. Text-only chat room
4. Updates checking

## Installing

First, create a virtual environment:

```bash
pip install -U virtualenv
virtualenv venv --clear
venv\scripts\activate
```

Install dependencies:

```bash
pip install -U -r requirements.txt
```

(Optional) If you want to package the app, install pyinstaller:

```bash
pip install pyinstaller      
```

Then run!  The source files are located at /src/

```bash
python3 src/cli.py  # Command line interface
python3 src/gui.py  # GUI (tkinter)
```

## Packaging using PyInstaller

(Optional) Optimize file size by excluding useless packages:

```cmd
set Excludes=--exclude _asyncio --exclude _bz2 --exclude _decimal --exclude _hashlib --exclude _lzma --exclude _multiprocessing --exclude _overlapped --exclude _queue --exclude lib2to3 --exclude difflib --exclude pickle
```

Set my custom hook for pyinstaller and icons:

```cmd
set Resources=--additional-hooks-dir utils
set Icons=--icon "src/res/riva.ico"
```

Finally, build both the cli and gui versions:

```bash
pyinstaller -y --clean -n "spambotcli" src/cli.py --version-file "utils/cli.txt" %Excludes% %Resources% %Icons%
pyinstaller -y --clean -n "spambotgui" src/gui.py --version-file "utils/gui.txt" -w %Excludes% %Resources% %Icons%
```

If you want the executable output be one file, add the --onefile flag:

```bash
pyinstaller -y --clean -n "spambotcli" src/cli.py --version-file "utils/cli.txt" %Excludes% %Resources% %Icons% --onefile
pyinstaller -y --clean -n "spambotgui" src/gui.py --version-file "utils/gui.txt" -w %Excludes% %Resources% %Icons% --onefile
```

(Beta) PyInstaller Splash screen:
Add `--splash src/res/riva.ico` to the pyinstaller command

PyInstaller Documentation: [Here](https://pyinstaller.org/en/stable/usage.html)

## File structure

```sh
.github/workflows   # Github Actions
src/*.py            # Codes
src/get             # Server lists for chatroom and version lists for checking updates
src/res             # resources(images,audios) for the program 
utils/hook-utils.py # PyInstaller hook
utils/*.iss         # Inno setup scripts
utils/*.txt         # windows metadata for the program 
.gitignore          # gitignore 
LICENSE.txt         # License file
README.md           # This file 
requirements.txt    # Dependencies
```

## Appreciation

I would like to thank the following people:

1. PyInstaller devs (specifically bwoodsend, rokm, Legorooj)
2. My friends who helped me to test the program
3. And you, for reading this README.md
