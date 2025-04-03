import os
import sys
import pathlib

if hasattr(sys, '_MEIPASS'):
    # Running from the .exe (temp folder created by PyInstaller)
    base_path = pathlib.Path(sys._MEIPASS)
else:
    # Running as a normal Python script
    base_path = pathlib.Path(__file__).parent.resolve()

# Build the full path to Finance.py
finance_app = base_path / "Finance.py"

# Wrap the path in quotes to handle spaces
os.system(f'streamlit run "{finance_app}"')

input("Press Enter to exit...")
