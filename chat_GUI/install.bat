@echo off
pip install pyinstaller
pyinstaller --onefile --noconsole --icon=icon.ico --name=AutoClicker.exe main.py