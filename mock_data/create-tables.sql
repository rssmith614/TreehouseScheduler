-- define database schema
BEGIN;
DROP TABLE IF EXISTS Parent;
DROP TABLE IF EXISTS Student;
DROP TABLE IF EXISTS Student_Availability;
DROP TABLE IF EXISTS Tutor;
DROP TABLE IF EXISTS Tutor_Availability;
DROP TABLE IF EXISTS Assessment;
DROP TABLE IF EXISTS Session;
DROP TABLE IF EXISTS Evaluation;

CREATE TABLE Parent (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    name                TEXT,
    primary_phone       TEXT,
    address             TEXT,
    email               TEXT,
    comment             TEXT
);

CREATE TABLE Student (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    name                TEXT,
    nickname            TEXT,
    parent_id           INTEGER REFERENCES Parent(id),
    grade               INTEGER,
    school              TEXT,
    dob                 DATE,
    reason              TEXT,
    subjects            TEXT,
    mode                TEXT,
    status              TEXT,
    gpa                 TEXT,
    address             TEXT,
    email               TEXT,
    e_contact_name      TEXT,
    e_contact_relation  TEXT,
    e_contact_phone     TEXT,
    pickup_person       TEXT,
    pickup_relation     TEXT,
    pickup_phone        TEXT,
    medical_comment     TEXT,
    comment             TEXT,
    CHECK (mode IN ('IN PERSON', 'ONLINE', 'HYBRID')),
    CHECK (status IN ('CURRENT', 'PAST', 'PAUSED'))
);

CREATE TABLE Student_Availability (
    student_id  INTEGER REFERENCES Student(id),
    day         TEXT,
    start       TEXT,
    finish      TEXT,
    CHECK (start LIKE '_:__'),
    CHECK (finish LIKE '_:__'),
    CHECK (day IN ('M', 'T', 'W', 'R', 'F')),
    UNIQUE (student_id, day, start, finish)
);

CREATE TRIGGER no_student_avail_overlaps
BEFORE INSERT ON Student_Availability
WHEN EXISTS (SELECT *
             FROM Student_Availability
             WHERE student_id = NEW.student_id AND day = NEW.day
               AND start <= NEW.finish
               AND finish >= NEW.start)
BEGIN
    SELECT RAISE(FAIL, "overlapping intervals");
END;

CREATE TABLE Tutor (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT,
    nickname        TEXT,
    primary_phone   TEXT,
    personal_email  TEXT,
    work_email      TEXT,
    mode            TEXT,
    status          TEXT,
    zoom_room_id    TEXT,
    zoom_room_pwd   TEXT,
    hire_date       DATE,
    dob             DATE,
    avail_calendar  TEXT,
    sched_calendar  TEXT,
    comment         TEXT,
    CHECK (mode IN ('IN PERSON', 'ONLINE', 'HYBRID')),
    CHECK (status IN ('CURRENT', 'PAST', 'PAUSED'))
);

CREATE TABLE Tutor_Availability (
    tutor_id    INTEGER REFERENCES Tutor(id),
    day         TEXT,
    start       TEXT,
    finish      TEXT,
    CHECK (start LIKE '_:__'),
    CHECK (finish LIKE '_:__'),
    CHECK (day IN ('M', 'T', 'W', 'R', 'F')),
    UNIQUE (tutor_id, day, start, finish)
);

CREATE TRIGGER no_tutor_avail_overlaps
BEFORE INSERT ON Tutor_Availability
WHEN EXISTS (SELECT *
             FROM Tutor_Availability
             WHERE tutor_id = NEW.tutor_id AND day = NEW.day
               AND start <= NEW.finish
               AND finish >= NEW.start)
BEGIN
    SELECT RAISE(FAIL, "overlapping intervals");
END;

CREATE TABLE Assessment (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id  REFERENCES Student(id),
    tutor_id    REFERENCES Tutor(id),
    subject     TEXT,
    date        DATE,
    score       FLOAT
);

CREATE TABLE Session (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id  REFERENCES Student(id),
    tutor_id    REFERENCES Tutor(id),
    date        DATE,
    start       TEXT,
    finish      TEXT,
    CHECK  (
        start LIKE '_:__'  AND
        finish LIKE '_:__'
    )
);

CREATE TABLE Evaluation (
    session_id  REFERENCES Session(id),
    attendance  TEXT,
    comment     TEXT
);
COMMIT;
PRAGMA foreign_keys = ON;