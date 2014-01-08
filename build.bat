pyinstaller main.py --onefile
@echo off
mkdir "dist/img"
mkdir "dist/templates"
xcopy img "dist/img" /E
xcopy templates "dist/templates" /E