import os

def clear_console():
    """
    Clear the console
    """
    os.system("cls" if os.name == "nt" else "clear")