[Setup]
AppName=spambotgui
AppVersion=0.7.1
WizardStyle=classic
DefaultDirName={autodesktop}\spambotgui
DefaultGroupName=Spam Bot Graphical-User Interface
UninstallDisplayIcon={app}\spambotgui.exe

Compression=lzma2/ultra64
InternalCompressLevel=ultra64
LZMANumBlockThreads=8
LZMANumFastBytes=273
LZMAUseSeparateProcess=yes
LZMADictionarySize=65536
SolidCompression=yes

SourceDir=..\
OutputDir=.
OutputBaseFilename=spambotgui-install

ArchitecturesAllowed=x64
PrivilegesRequired=lowest
DisableWelcomePage=no
LicenseFile=LICENSE.txt

[Files]
Source: "dist\spambotgui\*"; DestDir: "{app}"; Flags: recursesubdirs

[Icons]
Name: "{group}\Launch"; Filename: "{app}\spambotgui.exe"
Name: "{group}\Uninstall"; Filename: "{app}\unins000.exe"

[Run]
Filename: "{app}\spambotgui.exe"; Description: "Launch"; Flags: postinstall nowait skipifsilent

