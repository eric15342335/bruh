# SpamBot
## What is this?
Created just for fun. <br>
This is my first attempt to create a usable (not really) GUI interface for a python script. 
## Functionality
1. SpamBot (Ctrl+V) `not working :(`
2. ClickBot
3. Text-only chat room
4. Updates checking
## Installing
First, create a virtual environment: <br>
```commandline
pip install -U virtualenv
virtualenv venv --clear
venv\scripts\activate
```
Install dependencies: <br>
```commandline
pip install -U -r requirements.txt
```
(Optional) If you want to package the app, install pyinstaller: <br>
```commandline
pip install pyinstaller      
```
Then run!  The source files are located at /src/ <br>
```commandline
commandline interface: python3 src/cli.py
gui interface: python3 src/gui.py
```
## Packaging using PyInstaller
(Optional) Optimize file size by excluding useless packages: <br>
```
set Excludes=--exclude _asyncio --exclude _bz2 --exclude _decimal --exclude _hashlib --exclude _lzma --exclude _multiprocessing --exclude _overlapped --exclude _queue --exclude lib2to3 --exclude difflib --exclude distutils --exclude pickle
```
Set my custom hook for pyinstaller and icons: <br>
```
set Resources=--additional-hooks-dir utils
set Icons=--icon "src/res/riva.ico"
```
Finally, build both the cli and gui versions: <br>
```
pyinstaller -y --clean -n "spambotcli" src/cli.py --version-file "utils/cli.txt" %Excludes% %Resources% %Icons%
pyinstaller -y --clean -n "spambotgui" src/gui.py --version-file "utils/gui.txt" -w %Excludes% %Resources% %Icons%
```
If you want the executable output be one file, add the --onefile flag: <br>
```
pyinstaller -y --clean -n "spambotcli" src/cli.py --version-file "utils/cli.txt" %Excludes% %Resources% %Icons% --onefile
pyinstaller -y --clean -n "spambotgui" src/gui.py --version-file "utils/gui.txt" -w %Excludes% %Resources% %Icons% --onefile
```
(Beta) PyInstaller Splash screen: <br>
Add `--splash riva.ico` to the pyinstaller command <br>

PyInstaller Documentation: [Here](https://pyinstaller.org/en/stable/usage.html)
## File structure
```
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
I would like to thank the following people: <br>
1. PyInstaller devs (specifically bwoodsend, rokm, Legorooj)
2. My friends who helped me to test the program
3. And you, for reading this README.md
