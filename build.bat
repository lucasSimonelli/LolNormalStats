pyinstaller main.spec --onefile
@echo off
mkdir "dist/img"
mkdir "dist/templates"
xcopy img "dist/img" /E /Q
xcopy templates "dist/templates" /E /Q
rmdir build /S /Q