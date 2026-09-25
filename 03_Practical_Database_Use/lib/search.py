import mysql.connector # type: ignore
from lib.utils import get_connection, print_table

FIELDS = {
    "course": ["cID", "cName", "credit", "dID"],
    "dept": ["dID", "dName", "building"],
    "enroll": ["sID", "cID", "sem", "score", "pass_or_not", "enroll_date"],
    "student": ["sID", "sName", "YEAR", "dID"]
}

SQL_TABLE = {"course": "Course", "dept": "Dept", "enroll": "Enroll", "student": "Student"}


def search(db_config):
    table = input("Choose a table (course/dept/enroll/student): ").strip().lower()
    if table not in FIELDS:
        print("> Invalid table.")
        return

    print(f"Available fields: {', '.join(FIELDS[table])}")
    field = input("Search by field: ").strip()

    if field not in FIELDS[table]:
        print("> Invalid field.")
        return

    value = input("Enter search value: ").strip()
    connection = None

    try:
        connection = get_connection(db_config)
        cursor = connection.cursor()
        try:
            cursor.execute(f"SELECT * FROM {SQL_TABLE[table]} WHERE {field} LIKE %s", (f"%{value}%",))
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
        finally:
            cursor.close()

        if not rows:
            print(f"> No records found where {field} matches '{value}'.")
            return

        print_table(columns, rows)
    except mysql.connector.Error as error:
        print(f"> Database error: {error}")
    finally:
        if connection and connection.is_connected():
            connection.close()
