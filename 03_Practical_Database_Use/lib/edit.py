import mysql.connector  # type: ignore
from lib.utils import get_connection

PK = {"course": ["cID"], "dept": ["dID"], "enroll": ["sID", "cID"], "student": ["sID"]}

EDITABLE_FIELDS = {
    "course": ["cName", "credit", "dID"],
    "dept": ["dName", "building"],
    "enroll": ["sem", "score", "pass_or_not", "enroll_date"],
    "student": ["sName", "YEAR", "dID"]
}

SQL_TABLE = {"course": "Course", "dept": "Dept", "enroll": "Enroll", "student": "Student"}


def edit(db_config):
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

            columns = [description[0] for description in cursor.description]
            record = dict(zip(columns, row))

            print(f"Available fields: {', '.join(EDITABLE_FIELDS[table])}")
            field = input("Choose a field to update: ").strip()

            if field not in EDITABLE_FIELDS[table]:
                print("> Invalid field.")
                return

            current_value = record[field]

            if field == "enroll_date":
                current_value = "-".join(str(current_value).split("-")[::-1])

            new_value = input(f"Current value: {current_value} | Enter new value: ").strip()

            if field == "enroll_date":
                new_value = "-".join(new_value.split("-")[::-1])

            cursor.execute(f"UPDATE {SQL_TABLE[table]} SET {field} = %s WHERE {where}", [new_value] + pk_values)
            connection.commit()
            print("> Record updated successfully.")
        finally:
            cursor.close()
    except mysql.connector.Error as error:
        print(f"> Database error: {error}")
    finally:
        if connection and connection.is_connected():
            connection.close()
