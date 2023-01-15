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
    student_id  REFERENCES Student(id),
    day         VARCHAR,
    start       VARCHAR,
    finish      VARCHAR,
    CHECK (
        start LIKE '__:__' AND
        finish LIKE '__:__'
    )
);

CREATE TABLE Tutor (
    id              INTEGER PRIMARY KEY  AUTOINCREMENT,
    name            VARCHAR,
    nickname        VARCHAR,
    primary_phone   VARCHAR,
    personal_email  VARCHAR,
    work_email      VARCHAR,
    hire_date       DATE,
    dob             DATE,
    comment         VARCHAR
);

CREATE TABLE Tutor_Availability (
    tutor_id  REFERENCES Tutor(id),
    day         VARCHAR,
    start       VARCHAR,
    finish      VARCHAR,
    CHECK (
        start LIKE '__:__' AND
        finish LIKE '__:__'
    )
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
        start LIKE '__:__'  AND
        finish LIKE '__:__'
    )
);

CREATE TABLE Evaluation (
    session_id  REFERENCES Session(id),
    attendance  VARCHAR,
    comment     VARCHAR
);