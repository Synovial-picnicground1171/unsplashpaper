[Setup]
AppName=UnsplashPaper
AppVersion=1.0
AppPublisher=UnsplashPaper
AppPublisherURL=https://github.com/Teyk0o
DefaultDirName={autopf}\UnsplashPaper
DefaultGroupName=UnsplashPaper
UninstallDisplayIcon={app}\UnsplashPaper.exe
OutputDir=installer_output
OutputBaseFilename=UnsplashPaper_Setup
Compression=lzma2
SolidCompression=yes
PrivilegesRequired=lowest
SetupIconFile=
WizardStyle=modern
DisableProgramGroupPage=yes

[Files]
Source: "dist\UnsplashPaper.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\UnsplashPaper"; Filename: "{app}\UnsplashPaper.exe"
Name: "{autodesktop}\UnsplashPaper"; Filename: "{app}\UnsplashPaper.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Shortcuts:"
Name: "autostart"; Description: "Start UnsplashPaper with Windows"; GroupDescription: "Options:"

[Registry]
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "UnsplashPaper"; ValueData: """{app}\UnsplashPaper.exe"""; Flags: uninsdeletevalue; Tasks: autostart

[Run]
Filename: "{app}\UnsplashPaper.exe"; Description: "Launch UnsplashPaper"; Flags: nowait postinstall skipifsilent
