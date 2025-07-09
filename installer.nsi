; NSIS Installer Script

; General
Name "Image Compressor"
OutFile "ImageCompressorSetup_NSIS.exe"
InstallDir "$PROGRAMFILES\ImageCompressor"
RequestExecutionLevel admin

; Pages
Page directory
Page instfiles

; Section
Section "Install"
  SetOutPath $INSTDIR
  File "dist\image_compressor_app.exe"
  
  ; Create Desktop Shortcut
  CreateShortCut "$DESKTOP\Image Compressor.lnk" "$INSTDIR\image_compressor_app.exe"
  
  ; Write the uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"
SectionEnd

; Uninstaller Section
Section "Uninstall"
  Delete "$INSTDIR\image_compressor_app.exe"
  Delete "$INSTDIR\Uninstall.exe"
  Delete "$DESKTOP\Image Compressor.lnk"
  RMDir "$INSTDIR"
SectionEnd
