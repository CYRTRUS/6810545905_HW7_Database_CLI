import mysql.connector # type: ignore
from mysql.connector import errorcode # type: ignore
from lib.colors import GRAY, error as print_error, paint


def get_connection(db_config):
    try:
        return mysql.connector.connect(**db_config)
    except mysql.connector.Error as error:
        if error.errno == errorcode.ER_BAD_DB_ERROR:
            raise mysql.connector.Error(
                f"Database '{db_config['database']}' not found. Try resetting the database with the delete command."
            ) from None
        raise


def print_table(columns, rows):
    if not rows:
        print_error("> No records found.")
        return

    widths = [len(str(col)) for col in columns]
    for row in rows:
        for i, value in enumerate(row):
            widths[i] = max(widths[i], len(str(value)))

    def format_row(values):
        return "│ " + " │ ".join(str(v).ljust(widths[i]) for i, v in enumerate(values)) + " │"

    def separator(left, middle, right):
        return left + middle.join("─" * (w + 2) for w in widths) + right

    lines = [
        separator("┌", "┬", "┐"),
        format_row(columns),
        separator("├", "┼", "┤"),
        *(format_row(row) for row in rows),
        separator("└", "┴", "┘"),
    ]

    print()
    print(paint("\n".join(lines), GRAY))
