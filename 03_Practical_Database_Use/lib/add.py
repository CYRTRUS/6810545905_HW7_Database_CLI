import mysql.connector # type: ignore
from datetime import datetime
from lib.utils import get_connection

INSERT_FIELDS = {
    "course": ["cID", "cName", "credit", "dID"],
    "dept": ["dID", "dName", "building"],
    "enroll": ["sID", "cID", "sem", "enroll_date"],
    "student": ["sID", "sName", "YEAR", "dID"]
}

SQL_TABLE = {"course": "Course", "dept": "Dept", "enroll": "Enroll", "student": "Student"}


def add(db_config):
    table = input("Choose a table (course/dept/enroll/student): ").strip().lower()
    if table not in INSERT_FIELDS:
        print("> Invalid table.")
        return

    fields = INSERT_FIELDS[table]
    values = [input(f"Enter {field}: ").strip() for field in fields]

    if table == "enroll":
        try:
            values[3] = datetime.strptime(values[3], "%d-%m-%Y").date()
        except ValueError:
            print("> Invalid date. Please use DD-MM-YYYY.")
            return

    columns = ", ".join(fields)
    placeholders = ", ".join(["%s"] * len(fields))
    sql = f"INSERT INTO {SQL_TABLE[table]} ({columns}) VALUES ({placeholders})"

    connection = None
    try:
        connection = get_connection(db_config)
        cursor = connection.cursor()
        try:
            cursor.execute(sql, values)
            connection.commit()
            print("> Record added successfully.")
        finally:
            cursor.close()
    except mysql.connector.Error as error:
        print(f"> Database error: {error}")
    finally:
        if connection and connection.is_connected():
            connection.close()
