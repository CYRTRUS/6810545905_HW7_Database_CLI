CREATE DATABASE IF NOT EXISTS hw7_6810545905;

USE hw7_6810545905;

CREATE TABLE IF NOT EXISTS Dept (
    dID CHAR(2) PRIMARY KEY,
    dName VARCHAR(30) NOT NULL,
    building CHAR(2) NOT NULL
);

CREATE TABLE IF NOT EXISTS Student (
    sID CHAR(5) PRIMARY KEY,
    sName VARCHAR(30) NOT NULL,
    YEAR INT NOT NULL CHECK (YEAR BETWEEN 1 AND 4),
    dID CHAR(2) NOT NULL,
    FOREIGN KEY (dID) REFERENCES Dept (dID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS Course (
    cID CHAR(6) PRIMARY KEY,
    cName VARCHAR(30) NOT NULL,
    credit INT NOT NULL CHECK (credit > 0),
    dID CHAR(2) NOT NULL,
    FOREIGN KEY (dID) REFERENCES Dept (dID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS Enroll (
    sID CHAR(5),
    cID CHAR(6),
    sem CHAR(2) NOT NULL,
    score INT NULL CHECK (score BETWEEN 0 AND 100),
    pass_or_not CHAR(1) NULL CHECK (pass_or_not IN ("Y", "N")),
    enroll_date DATE NOT NULL,
    PRIMARY KEY (sID, cID),
    FOREIGN KEY (sID) REFERENCES Student (sID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (cID) REFERENCES Course (cID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

INSERT INTO Dept (dID, dName, building) VALUES
("CS", "Computer Science", "K1"),
("IT", "Information Tech", "K2"),
("SE", "Software Engineer", "K3"),
("DS", "Data Science", "K4"),
("AI", "Artificial Intel", "K5");

INSERT INTO Student (sID, sName, YEAR, dID) VALUES
("S1001", "Yua Mikami", 1, "CS"),
("S1002", "Akiho Yoshizawa", 2, "IT"),
("S1003", "Sora Aoi", 3, "SE"),
("S1004", "Maria Ozawa", 4, "DS"),
("S1005", "Rola Takizawa", 2, "AI");

INSERT INTO Course (cID, cName, credit, dID) VALUES
("CS2001", "Database", 3, "CS"),
("IT2001", "Networking", 3, "IT"),
("SE2001", "Software Design", 3, "SE"),
("DS2001", "Data Analysis", 3, "DS"),
("AI2001", "Machine Learning", 3, "AI");

INSERT INTO Enroll
    (sID, cID, sem, score, pass_or_not, enroll_date)
VALUES
("S1001", "CS2001", "1", 85, "Y", "2026-01-01"),
("S1001", "IT2001", "1", 78, "Y", "2026-01-02"),
("S1002", "IT2001", "1", 92, "Y", "2026-01-03"),
("S1002", "SE2001", "1", 68, "N", "2026-01-04"),
("S1003", "SE2001", "1", 88, "Y", "2026-01-05"),
("S1003", "DS2001", "1", 75, "Y", "2026-01-06"),
("S1004", "DS2001", "1", 95, "Y", "2026-01-07"),
("S1004", "AI2001", "1", 82, "Y", "2026-01-08"),
("S1005", "AI2001", "1", 90, "Y", "2026-01-09"),
("S1005", "CS2001", "1", 73, "Y", "2026-01-10");
