BEGIN;
-- PRAGMA foreign_keys = ON;
DROP TABLE Student;
DROP TABLE Student_Availability;
DROP TABLE Tutor;
DROP TABLE Tutor_Availability;
DROP TABLE Assessment;
DROP TABLE Session;
DROP TABLE Evaluation;

CREATE TABLE Student (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    name                VARCHAR,
    nickname            VARCHAR,
    parent_name         VARCHAR,
    primary_phone       VARCHAR,
    grade               INTEGER,
    school              VARCHAR,
    dob                 DATE,
    reason              VARCHAR,
    subjects            VARCHAR,
    gpa                 VARCHAR,
    address             VARCHAR,
    email               VARCHAR,
    e_contact_name      VARCHAR,
    e_contact_relation  VARCHAR,
    e_contact_phone     VARCHAR,
    pickup_person       VARCHAR,
    pickup_relation     VARCHAR,
    pickup_phone        VARCHAR,
    medical_comment     VARCHAR,
    comment             VARCHAR
);

CREATE TABLE Student_Availability (
    student_id  INTEGER REFERENCES Student(id),
    day         VARCHAR,
    start       VARCHAR,
    finish      VARCHAR,
    CHECK (start LIKE '_:__'),
    CHECK (finish LIKE '_:__'),
    CHECK (day IN ('M', 'T', 'W', 'R', 'F')),
    UNIQUE (student_id, day, start, finish)
);

CREATE TABLE Tutor (
    id              INTEGER PRIMARY KEY  AUTOINCREMENT,
    name            TEXT,
    nickname        TEXT,
    primary_phone   TEXT,
    personal_email  TEXT,
    work_email      TEXT,
    hire_date       DATE,
    dob             DATE,
    avail_calendar  TEXT,
    sched_calendar  TEXT,
    comment         TEXT
);

CREATE TABLE Tutor_Availability (
    tutor_id    INTEGER REFERENCES Tutor(id),
    day         VARCHAR,
    start       VARCHAR,
    finish      VARCHAR,
    CHECK (start LIKE '_:__'),
    CHECK (finish LIKE '_:__'),
    CHECK (day IN ('M', 'T', 'W', 'R', 'F')),
    UNIQUE (tutor_id, day, start, finish)
);

CREATE TABLE Assessment (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id  REFERENCES Student(id),
    tutor_id    REFERENCES Tutor(id),
    subject     VARCHAR,
    date        DATE,
    score       FLOAT
);

CREATE TABLE Session (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id  REFERENCES Student(id),
    tutor_id    REFERENCES Tutor(id),
    date        DATE,
    start       VARCHAR,
    finish      VARCHAR,
    CHECK  (
        start LIKE '_:__'  AND
        finish LIKE '_:__'
    )
);

CREATE TABLE Evaluation (
    session_id  REFERENCES Session(id),
    attendance  VARCHAR,
    comment     VARCHAR
);
COMMIT;
PRAGMA foreign_keys = ON;

CREATE VIEW View_Student_Availability(name, day, start, finish) AS
SELECT name, day, start, finish
FROM Student, Student_Availability
WHERE
    student_id = id;

CREATE VIEW View_Tutor_Availability(name, day, start, finish) AS
SELECT name, day, start, finish
FROM Tutor, Tutor_Availability
WHERE
    tutor_id = id;