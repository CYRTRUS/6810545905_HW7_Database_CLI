import mysql.connector  # type: ignore
from pathlib import Path
from lib.config import DATABASE_NAME
from lib.utils import get_connection

PK = {"course": ["cID"], "dept": ["dID"], "enroll": ["sID", "cID"], "student": ["sID"]}
SQL_TABLE = {"course": "Course", "dept": "Dept", "enroll": "Enroll", "student": "Student"}


def delete(db_config):
    mode = input("Choose an action (row/reset/drop): ").strip().lower()

    if mode == "row":
        delete_row(db_config)
    elif mode == "reset":
        reset_menu(db_config)
    elif mode == "drop":
        drop_database(db_config)
    else:
        print("> Invalid mode.")


def delete_row(db_config):
    table = input("Choose a table (course/dept/enroll/student): ").strip().lower()
    if table not in PK:
        print("> Invalid table.")
        return

    pk_fields = PK[table]
    pk_values = [input(f"Enter {key}: ").strip() for key in pk_fields]
    connection = None

    try:
        connection = get_connection(db_config)
        cursor = connection.cursor()
        try:
            where = " AND ".join(f"{key} = %s" for key in pk_fields)
            cursor.execute(f"SELECT * FROM {SQL_TABLE[table]} WHERE {where}", pk_values)
            row = cursor.fetchone()

            if not row:
                print("> No matching record found.")
                return

            print("> Warning: This will delete the following record: "
                  f"({', '.join(str(value) for value in row)})")

            if input("Are you sure? (Y/N): ").strip().upper() != "Y":
                print("> Deletion cancelled.")
                return

            cursor.execute(f"DELETE FROM {SQL_TABLE[table]} WHERE {where}", pk_values)
            connection.commit()
            print("> Record deleted successfully.")
        finally:
            cursor.close()
    except mysql.connector.Error as error:
        print(f"> Database error: {error}")
    finally:
        if connection and connection.is_connected():
            connection.close()


def reset_menu(db_config):
    print("1. Clear a table\n2. Reset the entire database")
    choice = input("Choose an option: ").strip()

    if choice == "1":
        table = input("Choose a table (course/dept/enroll/student): ").strip().lower()
        if table not in SQL_TABLE:
            print("> Invalid table.")
            return

        print(f"Warning: This will delete all records from {SQL_TABLE[table]}.")
        if input("Are you sure? (Y/N): ").strip().upper() == "Y":
            reset_table(db_config, SQL_TABLE[table])
        else:
            print("> Reset cancelled.")

    elif choice == "2":
        print("> Warning: This will reset the entire database.")
        if input("Are you sure? (Y/N): ").strip().upper() == "Y":
            reset_all(db_config)
        else:
            print("> Reset cancelled.")

    else:
        print("> Invalid selection.")


def reset_table(db_config, table):
    connection = None
    try:
        connection = get_connection(db_config)
        cursor = connection.cursor()
        try:
            cursor.execute(f"DELETE FROM {table}")
            connection.commit()
            print(f"> All records deleted from {table}.")
        finally:
            cursor.close()
    except mysql.connector.Error as error:
        print(f"> Database error: {error}")
    finally:
        if connection and connection.is_connected():
            connection.close()


def reset_all(db_config):
    sql_path = Path(__file__).resolve().parents[2] / "02_Database" / "6810545905_HW7.sql"
    connection = None

    try:
        connection = mysql.connector.connect(
            host=db_config["host"], user=db_config["user"], password=db_config["password"]
        )
        cursor = connection.cursor()
        try:
            cursor.execute(f"DROP DATABASE IF EXISTS `{DATABASE_NAME}`")

            with open(sql_path, "r", encoding="utf-8") as file:
                statements = file.read().split(";")

            for statement in statements:
                if statement.strip():
                    cursor.execute(statement.strip())

            connection.commit()
            print("> Database reset successfully.")
        finally:
            cursor.close()
    except (mysql.connector.Error, OSError) as error:
        if connection:
            connection.rollback()
        print(f"> Database error: {error}")
    finally:
        if connection and connection.is_connected():
            connection.close()


def drop_database(db_config):
    print(f"> WARNING: This will permanently delete the entire database '{DATABASE_NAME}'.")

    if input(f"Type '{DATABASE_NAME}' to confirm: ").strip() != DATABASE_NAME:
        print("> Database deletion cancelled.")
        return

    connection = None
    try:
        connection = mysql.connector.connect(
            host=db_config["host"], user=db_config["user"], password=db_config["password"]
        )
        cursor = connection.cursor()
        try:
            cursor.execute(f"DROP DATABASE IF EXISTS `{DATABASE_NAME}`")
            print("> Database dropped successfully.")
        finally:
            cursor.close()
    except mysql.connector.Error as error:
        print(f"> Database error: {error}")
    finally:
        if connection and connection.is_connected():
            connection.close()
