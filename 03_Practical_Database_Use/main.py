import os
import sys
from pathlib import Path

import mysql.connector  # type: ignore
from lib.config import DATABASE_NAME

if os.name == "nt":
    import msvcrt
else:
    import termios
    import tty


def get_password():
    print("Enter database password: ", end="", flush=True)
    password = ""

    if os.name == "nt":
        while True:
            char = msvcrt.getwch()
            if char == "\r":
                print()
                break
            elif char == "\b":
                if password:
                    password = password[:-1]
                    print("\b \b", end="", flush=True)
            elif char == "\003":
                raise KeyboardInterrupt
            else:
                password += char
                print("*", end="", flush=True)
    else:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                char = sys.stdin.read(1)
                if char in ("\r", "\n"):
                    print()
                    break
                elif char in ("\x7f", "\b"):
                    if password:
                        password = password[:-1]
                        print("\b \b", end="", flush=True)
                elif char == "\x03":
                    raise KeyboardInterrupt
                else:
                    password += char
                    print("*", end="", flush=True)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return password


def setup_database(host, user, password):
    project_root = Path(__file__).resolve().parent.parent
    sql_path = project_root / "02_Database" / "6810545905_HW7.sql"
    connection = cursor = None

    try:
        if not sql_path.is_file():
            print(f"> SQL file not found: {sql_path}")
            return False

        connection = mysql.connector.connect(host=host, user=user, password=password)
        cursor = connection.cursor()

        with open(sql_path, "r", encoding="utf-8") as file:
            statements = file.read().split(";")

        for statement in statements:
            statement = statement.strip()
            if not statement:
                continue

            if statement.upper().startswith("INSERT INTO"):
                table = statement.split()[2].strip("`")
                cursor.execute(f"SELECT COUNT(*) FROM `{table}`")
                if cursor.fetchone()[0] > 0:
                    continue

            cursor.execute(statement)

        connection.commit()
        print("> Database setup completed.")
        return True

    except (mysql.connector.Error, OSError) as error:
        if connection:
            connection.rollback()
        print(f"> Database setup error: {error}")
        return False

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def main():
    from lib import add, delete, edit, report, search, view

    while True:
        print("┌─────────────────────────┐")
        print("│   Database Connection   │")
        print("└─────────────────────────┘")

        host = input("Enter database host: ").strip()
        user = input("Enter database username: ").strip()
        password = get_password()

        try:
            connection = mysql.connector.connect(host=host, user=user, password=password)
            connection.close()
            break
        except mysql.connector.Error as error:
            print("> Access denied. Please try again." if error.errno == 1045 else f"> Connection failed: {error}")
            print()

    if not setup_database(host, user, password):
        print("> Database setup failed.")
        return

    db_config = {"host": host, "user": user, "password": password, "database": DATABASE_NAME}
    os.system("cls" if os.name == "nt" else "clear")

    actions = {
        "add": add.add,
        "delete": delete.delete,
        "edit": edit.edit,
        "report": report.report,
        "search": search.search,
        "view": view.view
    }

    print()
    print("          ┌────────────────────────────────────────────────────────┐")
    print("          │              University Enrollment System              │")
    print("          └────────────────────────────────────────────────────────┘")
    print("\n──────────────────────────────────────────────────────────────────────────────")

    while True:
        print()
        print("Available commands: add / delete / edit / report / search / view / cls / quit")

        command = input("Choose a command: ").strip().lower()
        print()

        if command in actions:
            actions[command](db_config)
        elif command == "cls":
            os.system("cls" if os.name == "nt" else "clear")
            print()
            print("          ┌────────────────────────────────────────────────────────┐")
            print("          │              University Enrollment System              │")
            print("          └────────────────────────────────────────────────────────┘")
            print("\n──────────────────────────────────────────────────────────────────────────────")
            continue
        elif command in ["quit", "q"]:
            print("> Goodbye!")
            break
        else:
            print("> Invalid command. Please try again.")

        print("\n──────────────────────────────────────────────────────────────────────────────")


if __name__ == "__main__":
    main()
