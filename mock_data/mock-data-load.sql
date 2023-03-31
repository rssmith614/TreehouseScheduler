-- load all mock data into the database
.mode csv
.separator ','

BEGIN;
CREATE TABLE student_import (name TEXT);
.import --skip 1 students.csv student_import
INSERT INTO Student(name) SELECT * FROM student_import;
DROP TABLE student_import;

.import --skip 1 student_avail.csv Student_Availability
DELETE FROM Student_Availability WHERE start >= finish;

CREATE TABLE tutor_import (name TEXT);
.import --skip 1 tutors.csv tutor_import
INSERT INTO Tutor(name) SELECT * FROM tutor_import;
DROP TABLE tutor_import;

.import --skip 1 tutor_avail.csv Tutor_Availability
DELETE FROM Tutor_Availability WHERE start >= finish;

CREATE TABLE session_import (student_id INTEGER, tutor_id INTEGER, date DATE, start TEXT, finish TEXT);
.import --skip 1 session.csv session_import
INSERT INTO Session (student_id, tutor_id, date, start, finish) SELECT * FROM session_import;
DROP TABLE session_import;

COMMIT;

.exit