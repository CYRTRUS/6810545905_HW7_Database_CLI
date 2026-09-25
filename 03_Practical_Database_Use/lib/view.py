import mysql.connector # type: ignore
from lib.utils import get_connection, print_table

SQL_TABLE = {"course": "Course", "dept": "Dept", "enroll": "Enroll", "student": "Student"}


def view(db_config):
    table = input("Choose a table (course/dept/enroll/student): ").strip().lower()
    if table not in SQL_TABLE:
        print("> Invalid table.")
        return

    connection = None
    try:
        connection = get_connection(db_config)
        cursor = connection.cursor()
        try:
            cursor.execute(f"SELECT * FROM {SQL_TABLE[table]}")
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
        finally:
            cursor.close()

        print_table(columns, rows)
    except mysql.connector.Error as error:
        print(f"> Database error: {error}")
    finally:
        if connection and connection.is_connected():
            connection.close()
