; Tinky Installer Script for Inno Setup 6
; Builds a professional Windows installer that:
;  - Bundles the VC++ 2022 x64 Runtime (installs it silently if missing)
;  - Installs Tinky to %LocalAppData%\Programs\Tinky (NO admin needed)
;  - Creates Desktop + Start Menu shortcuts
;  - Registers in Apps & Features (Programs and Features)
;  - Handles uninstall cleanly

#define AppName        "Tinky"
#define AppVersion     "1.0.0"
#define AppPublisher   "Tinky"
#define AppURL         "https://tinky.app"
#define AppExeName     "Tinky.exe"
#define AppDescription "Your Digital AI Genie"

[Setup]
AppId={{A7F2C3D1-8B4E-4F5A-9C6D-2E3F1A0B8C7D}
AppName={#AppName}
AppVersion={#AppVersion}
AppVerName={#AppName} {#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL={#AppURL}
AppSupportURL={#AppURL}
AppUpdatesURL={#AppURL}
DefaultDirName={localappdata}\Programs\{#AppName}
DefaultGroupName={#AppName}
DisableProgramGroupPage=yes
; No admin required — installs per-user
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=commandline
OutputDir=installer_output
OutputBaseFilename=Tinky-Setup-1.0.0
SetupIconFile=assets\tinky_app_icon.ico
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
DisableWelcomePage=no
WizardImageFile=assets\wizard_sidebar.bmp
WizardSmallImageFile=assets\wizard_small.bmp
UninstallDisplayIcon={app}\{#AppExeName}
UninstallDisplayName={#AppName} {#AppVersion}
VersionInfoVersion={#AppVersion}
VersionInfoCompany={#AppPublisher}
VersionInfoDescription={#AppDescription}
VersionInfoProductName={#AppName}
; Sign the installer if certificate is available (comment out if not signing)
; SignTool=signtool sign /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 $f
MinVersion=10.0.19041

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "startupitem"; Description: "Start {#AppName} automatically with Windows"; GroupDescription: "Windows Startup:"; Flags: unchecked

[Files]
; Main application executable
Source: "dist_release\{#AppExeName}"; DestDir: "{app}"; Flags: ignoreversion

; VC++ 2022 x64 Runtime DLLs (bundled directly — no internet required)
Source: "installer_deps\msvcp140.dll";     DestDir: "{app}"; Flags: ignoreversion onlyifdoesntexist
Source: "installer_deps\vcruntime140.dll";  DestDir: "{app}"; Flags: ignoreversion onlyifdoesntexist
Source: "installer_deps\vcruntime140_1.dll";DestDir: "{app}"; Flags: ignoreversion onlyifdoesntexist
Source: "installer_deps\msvcp140_1.dll";    DestDir: "{app}"; Flags: ignoreversion onlyifdoesntexist
Source: "installer_deps\msvcp140_2.dll";    DestDir: "{app}"; Flags: ignoreversion onlyifdoesntexist

; App icon for shortcuts
Source: "assets\tinky_app_icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{userprograms}\{#AppName}"; Filename: "{app}\{#AppExeName}"; IconFilename: "{app}\tinky_app_icon.ico"; Comment: "{#AppDescription}"
Name: "{userprograms}\Uninstall {#AppName}"; Filename: "{uninstallexe}"
Name: "{userdesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; IconFilename: "{app}\tinky_app_icon.ico"; Tasks: desktopicon

[Registry]
; Add to startup if user selected the task
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "Tinky"; ValueData: """{app}\{#AppExeName}"""; Flags: uninsdeletevalue; Tasks: startupitem

; Register in Apps & Features properly
Root: HKCU; Subkey: "Software\{#AppPublisher}\{#AppName}"; ValueType: string; ValueName: "InstallPath"; ValueData: "{app}"; Flags: uninsdeletekey

[Run]
; Launch Tinky after install (optional — user can uncheck)
Filename: "{app}\{#AppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(AppName, '&', '&&')}}"; \
    Flags: nowait postinstall skipifsilent

[UninstallRun]
; Kill Tinky before uninstalling
Filename: "taskkill.exe"; Parameters: "/F /IM {#AppExeName}"; Flags: runhidden; RunOnceId: "KillTinky"

[UninstallDelete]
; Clean up the AppData runtime cache on uninstall
Type: filesandordirs; Name: "{localappdata}\Tinky"

[Code]
// No VC++ installer check needed — DLLs are bundled directly
