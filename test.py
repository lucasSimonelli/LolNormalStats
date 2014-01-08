import os, winshell
from win32com.client import Dispatch

desktop = winshell.programs()
path = os.path.join(desktop, "startup/LolNormalStats.lnk")
target = os.getcwd()+"/dist/main.exe"
wDir = r"D:\Users\Myself\My Music"
icon = r"D:\Users\Myself\My Music\some_file.mp3"

shell = Dispatch('WScript.Shell')
shortcut = shell.CreateShortCut(path)
shortcut.Targetpath = target
shortcut.WorkingDirectory = wDir
shortcut.IconLocation = icon
shortcut.save()