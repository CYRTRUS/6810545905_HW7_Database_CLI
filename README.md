# 6810545905_HW7_Database_CLI

**Selected Practical Database Use Option: Option C - Simple Database Application**

This project implements a command-line application using Python and MySQL. It allows users to manage university departments, students, courses, and enrollments through database operations and meaningful reports.

## 1. Project Overview

The University Enrollment System is a command-line application designed to manage university enrollment information.

The system stores and manages:

- Department information
- Student information
- Course information
- Student course enrollments, including scores and enrollment dates

Users can perform database operations through a simple command-line interface without directly writing SQL statements.

## 2. Technologies Used

| Technology             | Purpose                                         |
| ---------------------- | ----------------------------------------------- |
| Python                 | Application development                         |
| MySQL                  | Relational database management                  |
| mysql-connector-python | Connects Python to MySQL                        |
| SQL                    | Database creation, queries, and data management |

## 3. Database Design

The database is named `hw7_6810545905` and contains four tables.

| Table     | Description                                                         |
| --------- | ------------------------------------------------------------------- |
| `Dept`    | Stores department names and building information                    |
| `Student` | Stores student information and department membership                |
| `Course`  | Stores course information and department membership                 |
| `Enroll`  | Stores student enrollments, semesters, scores, and enrollment dates |

### Business Rules

1. A department can have many students, but each student belongs to exactly one department.

2. A department can offer many courses, but each course belongs to exactly one department.

3. A student can enroll in many courses, and a course can have many students enrolled in it.

4. For each enrollment, the semester, score, and pass/fail status are recorded specifically for that student-course pair.

5. A student cannot enroll in the same course more than once in the system (each student-course pair is unique).

6. A course must belong to an existing department; a course cannot exist without a valid department.

7. A student's enrollment score, if given, must be between 0 and 100.

## 4. Application Features

The application provides the following commands:

| Command  | Description                                                              |
| -------- | ------------------------------------------------------------------------ |
| `add`    | Add a new record to a selected table                                     |
| `view`   | Display records from a selected table                                    |
| `search` | Search for records using a selected field                                |
| `edit`   | Update an existing record                                                |
| `delete` | Delete a record, reset a table, reset the database, or drop the database |
| `report` | Generate student transcripts or average course scores                    |
| `cls`    | Clear the terminal                                                       |
| `quit`   | Exit the application                                                     |

### Reports

The application provides two reports:

1. **Student Transcript** - Displays a student's enrolled courses, scores, and pass results.
2. **Average Score per Course** - Calculates and displays the average score for each course.

Both reports retrieve information from multiple related tables.

## 5. Project Structure

```text
6810545905_HW7_Database_CLI/
├── 01_Report/
│   └── 6810545905_HW7_Report.pdf
├── 02_Database/
│   └── 6810545905_HW7.sql
├── 03_Practical_Database_Use/
│   ├── lib/
│   │   ├── __init__.py
│   │   ├── add.py
│   │   ├── config.py
│   │   ├── delete.py
│   │   ├── edit.py
│   │   ├── report.py
│   │   ├── search.py
│   │   ├── utils.py
│   │   └── view.py
│   ├── main.py
│   ├── requirements.txt
│   ├── run.bat
│   ├── run.command
│   └── run.sh
├── 04_Screenshots/
└── README.md
```

## 6. Requirements

Before running the application, make sure you have:

- Python 3.14 installed
- MySQL 8.0 installed and running
- A MySQL account with permission to create and modify the project database
- A terminal or command prompt

## 7. Installation and Setup

### Step 1: Clone the repository and open the application folder

Clone the project from GitHub and navigate to the `03_Practical_Database_Use` directory, which contains the application source code.

**Windows:**

```bat
git clone https://github.com/CYRTRUS/6810545905_HW7_Database_CLI.git
cd 6810545905_HW7_Database_CLI\03_Practical_Database_Use
```

**macOS / Linux:**

```bash
git clone https://github.com/CYRTRUS/6810545905_HW7_Database_CLI.git
cd 6810545905_HW7_Database_CLI/03_Practical_Database_Use
```

### Step 2: Create a virtual environment

Create a virtual environment to keep the project's Python dependencies separate from other Python projects.

**Windows:**

```bat
py -m venv .venv
```

**macOS / Linux:**

```bash
python3 -m venv .venv
```

### Step 3: Install dependencies

Install the required Python packages using the provided `requirements.txt` file.

**Windows:**

```bat
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

**macOS / Linux:**

```bash
./.venv/bin/python -m pip install -r requirements.txt
```

### Step 4: Start MySQL Server

Make sure MySQL Server is installed and running before starting the application.

### Step 5: Run the application

**Windows:**

Run the following command:

```bat
run.bat
```

Alternatively, double-click `run.bat` in File Explorer or run the application directly:

```bat
.venv\Scripts\python.exe main.py
```

**macOS / Linux:**

Make the launch scripts executable, then run `run.sh`:

```bash
chmod +x run.sh run.command
./run.sh
```

Alternatively, run the application directly:

```bash
./.venv/bin/python main.py
```

On macOS, you can also double-click `run.command` in Finder. On Linux, you can run `run.sh` from a terminal or use your file manager's option to execute the script, if supported.

### Step 6: Usage

Continue reading the instructions in the `README.md` file located in the `03_Practical_Database_Use` folder.

## 8. Connecting to MySQL

When the application starts, enter the following information:

1. MySQL host, such as `localhost`
2. MySQL username
3. MySQL password

The password is entered using masked characters.

After a successful connection, the application automatically executes the SQL setup script located at:

```text
02_Database/6810545905_HW7.sql
```

The setup process creates the database and tables if they do not already exist. It also inserts the sample data when the corresponding tables are empty.

The database name is configured in `lib/config.py`:

```python
DATABASE_NAME = "hw7_6810545905"
```

## 9. Using the Application

After the database setup is completed, the main menu displays the available commands.

For example:

```text
Available commands: add / delete / edit / report / search / view / cls / quit
```

Enter a command to perform the corresponding operation.

### Adding an Enrollment

When adding an enrollment, enter the following information:

- Student ID
- Course ID
- Semester
- Enrollment date

The enrollment date must use the following format:

```text
DD-MM-YYYY
```

For example:

```text
15-01-2026
```

The database automatically handles the enrollment's score and pass result as nullable fields.

### Generating a Report

Enter:

```text
report
```

Then select one of the available reports:

```text
1. Student transcript
2. Average score per course
```

For a student transcript, enter the student's ID when prompted.

## 10. Database Reset and Deletion

The `delete` command provides three options:

| Option  | Description                                                           |
| ------- | --------------------------------------------------------------------- |
| `row`   | Delete a selected record                                              |
| `reset` | Delete all records from a selected table or reset the entire database |
| `drop`  | Permanently delete the project database                               |

The application requests confirmation before performing destructive operations.

**Warning:** Resetting or dropping the database can permanently remove data. Use these options carefully.

**Recovering a dropped database:** If the database has been dropped, any other command will report that it cannot find the database. Run `delete` → `reset` → option `2` (reset the entire database) to recreate it from `02_Database/6810545905_HW7.sql`, or restart the application, which also recreates it automatically on startup.

## 11. Screenshots and Demonstration

[placeholder]

## 12. Notes

- The application uses MySQL as its database management system.
- The SQL schema and sample data are provided in `02_Database/6810545905_HW7.sql`.
- The database name is configured in `03_Practical_Database_Use/lib/config.py`.
- The application is implemented using Python and a command-line interface.
- The project demonstrates Option C: Simple Database Application.
- The application does not require authentication, deployment, or an advanced graphical interface.
