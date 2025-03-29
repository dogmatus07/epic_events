import os
import sys


def clear_console():
    if os.getenv("TERM") is not None and sys.stdout.isatty():
        os.system("clear" if os.name != "nt" else "cls")
    else:
        print("\n" * 100)
