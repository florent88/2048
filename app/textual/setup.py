from cx_Freeze import setup, Executable

setup(name = "textual_2048",
      version = "3.0",
      description = "Reproduction of 2048 mobile game with Python3",
      executables = [Executable("textual_2048.py")])
