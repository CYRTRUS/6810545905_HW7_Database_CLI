import mysql.connector # type: ignore
from lib.utils import get_connection, print_table


def report(db_config):
    print("Available reports:\n1. Student transcript\n2. Average score per course")
    choice = input("Choose a report: ").strip()

    if choice == "1":
        student_transcript(db_config)
    elif choice == "2":
        average_score_per_course(db_config)
    else:
        print("> Invalid selection.")


def student_transcript(db_config):
    sid = input("Enter student ID (sID): ").strip()
    connection = None

    try:
        connection = get_connection(db_config)
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT sID FROM Student WHERE sID = %s", (sid,))
            if not cursor.fetchone():
                print(f"> No student found with sID = {sid}.")
                return

            cursor.execute("""
                SELECT c.cName, e.score, e.pass_or_not
                FROM Enroll e
                JOIN Course c ON e.cID = c.cID
                WHERE e.sID = %s
            """, (sid,))
            rows = cursor.fetchall()
        finally:
            cursor.close()

        print_table(["Course", "Score", "Pass"], rows)
    except mysql.connector.Error as error:
        print(f"> Database error: {error}")
    finally:
        if connection and connection.is_connected():
            connection.close()


def average_score_per_course(db_config):
    connection = None
    try:
        connection = get_connection(db_config)
        cursor = connection.cursor()
        try:
            cursor.execute("""
                SELECT c.cName, ROUND(AVG(e.score), 2)
                FROM Enroll e
                JOIN Course c ON e.cID = c.cID
                GROUP BY c.cID, c.cName
            """)
            rows = cursor.fetchall()
        finally:
            cursor.close()

        print_table(["Course", "Average Score"], rows)
    except mysql.connector.Error as error:
        print(f"> Database error: {error}")
    finally:
        if connection and connection.is_connected():
            connection.close()
