' Specimen Tracker Launcher
' This script launches the Flask application and opens the browser
' Save this as a .vbs file and create a shortcut to it on your desktop

Option Explicit

Dim objShell, objFSO, strPath, strPythonPath, strCommand

' Get the directory where this script is located
strPath = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)

' Python executable path
strPythonPath = "C:\Users\findl\AppData\Local\Programs\Python\Python313\python.exe"

' Create shell object
Set objShell = CreateObject("WScript.Shell")

' Change to the project directory
objShell.CurrentDirectory = strPath

' Start the Flask application in background
strCommand = """" & strPythonPath & """ wsgi.py"
objShell.Run strCommand, 0, False

' Wait a moment for the server to start
WScript.Sleep 3000

' Open the browser
objShell.Run "http://localhost:5000", 1, False

' Clean up
Set objShell = Nothing
