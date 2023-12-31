[Setup]
AppName=spambotcli
AppVersion=1.4.1
WizardStyle=classic
DefaultDirName={autodesktop}\spambotcli
DefaultGroupName=Spam Bot Command-Line Interface
UninstallDisplayIcon={app}\spambotcli.exe

Compression=lzma2/ultra64
InternalCompressLevel=ultra64
LZMANumBlockThreads=8
LZMANumFastBytes=273
LZMAUseSeparateProcess=yes
LZMADictionarySize=65536
SolidCompression=yes

SourceDir=..\
OutputDir=.
OutputBaseFilename=spambotCLI

ArchitecturesAllowed=x64
PrivilegesRequired=lowest
DisableWelcomePage=no
LicenseFile=LICENSE.txt

[Files]
Source: "dist\spambotcli\*"; DestDir: "{app}"; Flags: recursesubdirs

[Icons]
Name: "{group}\Launch"; Filename: "{app}\spambotcli.exe"
Name: "{group}\Uninstall"; Filename: "{app}\unins000.exe"

[Run]
Filename: "{app}\spambotcli.exe"; Description: "Launch"; Flags: postinstall nowait skipifsilent

