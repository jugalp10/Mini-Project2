import os

def clear():
    if os.name == "nt":
        os.system("cls")
    elif os.name == "posix":
        os.system("clear")
    return

def horizontal_line():
    print('=' * os.get_terminal_size().columns)