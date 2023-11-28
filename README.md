# SpamBot
## What is this?
Initially created just for fun, this is my first attempt to create a usable GUI interface for a python script. 
## Functionality
1. SpamBot (Ctrl+V)
2. ClickBot
3. Plaintext chatroom
4. Check for updates
## Installing
First, create a virtual environment: <br>
```commandline
pip install -U virtualenv
virtualenv venv --clear
venv\scripts\activate
```
Install the dependencies: <br>
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
## Packaging instructions
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
pyinstaller -y --clean -n "spambotcli" src/cli.py --version-file "src/metadata/cli.version" %Excludes% %Resources% %Icons%
pyinstaller -y --clean -n "spambotgui" src/gui.py --version-file "src/metadata/gui.version" -w %Excludes% %Resources% %Icons%
```
If you want the executable output be one file, add the --onefile flag: <br>
```
pyinstaller -y --clean -n "spambotcli" src/cli.py --version-file "src/metadata/cli.version" %Excludes% %Resources% %Icons% --onefile
pyinstaller -y --clean -n "spambotgui" src/gui.py --version-file "src/metadata/gui.version" -w %Excludes% %Resources% %Icons% --onefile
```
(Beta) PyInstaller Splash screen: <br>
Add `--splash riva.ico` to the pyinstaller command <br>

PyInstaller Documentation: [Here](https://pyinstaller.org/en/stable/usage.html)
## File structure
```
.github/workflows   # Github actions for CodeQL analysis 
get                 # Server lists for chatroom and version lists for checking updates 
src                 # files crucial for running the program 
src/metadata        # windows metadata for the program 
src/res             # resources(images,audios) for the program 
utils               # utilities for packaging the program 
.gitignore          # gitignore 
LICENSE.txt         # License file
README.md           # this file 
requirements.txt    # dependencies 
```
## Appreciation
I would like to thank the following people: <br>
1. PyInstaller developers (bwoodsend, rokm, Legorooj, and many more), for teaching me how to package my app in a friendly minder
2. My friends who helped me to test the program
3. And you, for reading this README.md
