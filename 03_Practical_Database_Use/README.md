# University Enrollment System - Usage Guide

This guide explains how to use each command in the CLI once the program is running. For installation and setup, see `README.md`.

## Starting the Program

Run the program using `run.bat` (Windows), `run.sh` / `run.command` (macOS/Linux), or directly with `python main.py`.

You will be prompted for:

1. **Database host** - e.g. `localhost`
2. **Database username**
3. **Database password** - entered masked (shown as `*`)

If the credentials are wrong, you'll be asked to try again. Once connected, the program automatically creates the database and tables (if they don't already exist) and loads the sample data, then shows the main menu:

```text
Available commands: add / delete / edit / report / search / view / cls / quit
```

Type a command name and press Enter to use it.

## Reference: Tables and Fields

All four tables are referred to by these lowercase names throughout the program: `dept`, `student`, `course`, `enroll`.

| Table     | Fields                                                    | Primary Key   | Notes                                                                 |
| --------- | ---------------------------------------------------------- | ------------- | ---------------------------------------------------------------------- |
| `dept`    | `dID`, `dName`, `building`                                  | `dID`         | `dID` is 2 characters (e.g. `CS`)                                     |
| `student` | `sID`, `sName`, `YEAR`, `dID`                                | `sID`         | `YEAR` must be 1–4; `dID` must exist in `dept`                       |
| `course`  | `cID`, `cName`, `credit`, `dID`                              | `cID`         | `credit` must be greater than 0; `dID` must exist in `dept`          |
| `enroll`  | `sID`, `cID`, `sem`, `score`, `pass_or_not`, `enroll_date`  | `sID` + `cID` | `sID`/`cID` must exist in `student`/`course`; `score` 0–100; `pass_or_not` is `Y` or `N` |

`score` and `pass_or_not` aren't set when you `add` an enrollment - they start empty and are filled in later with `edit` (e.g. once a course is graded).

## `add` - Add a New Record

1. Choose a table: `course`, `dept`, `enroll`, or `student`.
2. Enter a value for each field, in order, as prompted.
3. For `enroll`, the enrollment date must be typed as `DD-MM-YYYY` (e.g. `15-01-2026`).

**Example - adding a student:**

```text
Choose a table (course/dept/enroll/student): student
Enter sID: S1006
Enter sName: Grace Kim
Enter YEAR: 1
Enter dID: CS
> Record added successfully.
```

If a value violates a rule - a duplicate ID, a `dID`/`sID`/`cID` that doesn't exist, an out-of-range `YEAR`/`credit`/`score`, or a badly formatted enrollment date - the program shows an error and the record is not added.

## `view` - Display All Records in a Table

Choose a table and every row is printed in a formatted table.

```text
Choose a table (course/dept/enroll/student): dept
```

## `search` - Search a Table by Field

1. Choose a table.
2. Choose which field to search by (the available fields are listed).
3. Enter a search value.

The search matches partial text anywhere in the field (a "contains" search), not just exact matches - searching `course` by `cName` for `Data` will match `Data Analysis`.

```text
Choose a table (course/dept/enroll/student): course
Available fields: cID, cName, credit, dID
Search by field: cName
Enter search value: Data
```

If nothing matches, the program tells you no records were found.

## `edit` - Update an Existing Record

1. Choose a table.
2. Enter the primary key value(s) to identify the record - `enroll` needs both `sID` and `cID`, since together they form its primary key; the other tables need just one ID.
3. Choose which field to update (only certain fields are editable per table - the ID/primary-key fields themselves cannot be changed this way).
4. Enter the new value. The current value is shown for reference first.

**Editable fields per table:**

| Table     | Editable fields                                  |
| --------- | ------------------------------------------------- |
| `dept`    | `dName`, `building`                                |
| `student` | `sName`, `YEAR`, `dID`                             |
| `course`  | `cName`, `credit`, `dID`                           |
| `enroll`  | `sem`, `score`, `pass_or_not`, `enroll_date`       |

**Note on dates:** when editing `enroll_date`, both the current value shown and the new value you type use `DD-MM-YYYY` - the same format as `add` - even though the database stores it differently.

**Example - recording a score after a course is graded:**

```text
Choose a table (course/dept/enroll/student): enroll
Enter sID: S1006
Enter cID: CE2001
Available fields: sem, score, pass_or_not, enroll_date
Choose a field to update: score
Current value: None | Enter new value: 88
> Record updated successfully.
```

If the record doesn't exist, or the new value would break a constraint (e.g. a `score` outside 0–100), the program shows an error and nothing changes.

## `delete` - Delete Records, Reset a Table, or Drop the Database

Choosing `delete` asks which action you want: `row`, `reset`, or `drop`.

### `row` - delete one record

Choose a table and enter its primary key value(s), same as `edit`. The matching record is shown and you must confirm with `Y` before it's deleted.

```text
Choose an action (row/reset/drop): row
Choose a table (course/dept/enroll/student): enroll
Enter sID: S1006
Enter cID: CE2001
> Warning: This will delete the following record: (S1006, CE2001, ...)
Are you sure? (Y/N): Y
> Record deleted successfully.
```

Deleting a `dept` or `course` also deletes any `student`/`enroll` or `enroll` rows that reference it (cascading delete) - the foreign keys are set to cascade.

### `reset` - clear a table or reset the whole database

```text
Choose an action (row/reset/drop): reset
1. Reset a table
2. Reset the entire database
Choose an option: 1
Choose a table (course/dept/enroll/student): enroll
Warning: This will delete all records from Enroll.
Are you sure? (Y/N): Y
```

Option 2 drops and recreates the entire database from the SQL schema, restoring the original sample data. This is also how you recover if the database was previously dropped (see below).

### `drop` - permanently delete the database

This removes the entire database, tables and all. You must type the exact database name (`hw7_6810545905`) to confirm.

```text
Choose an action (row/reset/drop): drop
> WARNING: This will permanently delete the entire database 'hw7_6810545905'.
Type 'hw7_6810545905' to confirm: hw7_6810545905
> Database dropped successfully.
```

**After a drop**, every other command will report that the database can't be found. To get back to a working state, either:
- run `delete` → `reset` → option `2`, or
- restart the program - it recreates the database automatically on startup.

## `report` - Generate a Report

```text
report
1. Student transcript
2. Average score per course
Choose a report: 1
Enter student ID (sID): S1001
```

1. **Student transcript** - shows every course a given student is enrolled in, with their score and pass/fail result.
2. **Average score per course** - shows the average score across all students, grouped by course.

## `cls` - Clear the Screen

Clears the terminal and redraws the menu header. Has no effect on the database.

## `quit` - Exit the Program

Closes the application. Type `quit` or `q`.
