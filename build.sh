#!/bin/bash
pyinstaller --onefile --add-data="rename.ico:." --clean --noconfirm --log-level WARN --windowed -i rename.ico main.py