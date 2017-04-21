import os
from cx_Freeze import setup, Executable

os.environ['TCL_LIBRARY'] = r'C:\Users\Remi\AppData\Local\Programs\Python\Python35-32\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\Remi\AppData\Local\Programs\Python\Python35-32\tcl\tk8.6'

setup(name = "graphical_2048",
      version = "3.0",
      description = "Reproduction of 2048 mobile game with Python3",
      executables = [Executable("graphical_2048.py", base="Win32Gui")])
