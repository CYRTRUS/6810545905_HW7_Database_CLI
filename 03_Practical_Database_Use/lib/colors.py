import os

if os.name == "nt":
    os.system("")

RESET = "\033[0m"
PURPLE = "\033[95m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
GRAY = "\033[38;5;250m"


def paint(text, color):
    return f"{color}{text}{RESET}"


def success(message):
    print(paint(message, GREEN))


def error(message):
    print(paint(message, RED))


def warning(message):
    print(paint(message, YELLOW))


def command_line(message):
    print(paint(message, PURPLE))
