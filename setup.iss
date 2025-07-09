[Setup]
AppId={B4F2A5B3-7B5A-4F9E-B0B4-7A6C8D9E0F1B}
AppName=Image Compressor
AppVersion=1.0
DefaultDirName={autopf}\ImageCompressor
DefaultGroupName=Image Compressor
OutputBaseFilename=ImageCompressorSetup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "dist\image_compressor_app.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Image Compressor"; Filename: "{app}\image_compressor_app.exe"
Name: "{autodesktop}\Image Compressor"; Filename: "{app}\image_compressor_app.exe"

[Run]
Filename: "{app}\image_compressor_app.exe"; Description: "Launch Image Compressor"; Flags: nowait postinstall skipifsilent
