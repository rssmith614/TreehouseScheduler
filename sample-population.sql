INSERT INTO Student(name, parent_name, grade, subjects)
VALUES('X', 'X Parent', 5, 'Math');

INSERT INTO Tutor(name)
VALUES('Y');

INSERT INTO Session(student_id, tutor_id, date, start, finish)
VALUES(1, 1, '2023-01-16', '02:30', '03:30');

INSERT INTO Student_Availability(student_id, day, start, finish)
VALUES(1, 'Mon', '02:30', '03:30');

INSERT INTO Tutor_Availability(tutor_id, day, start, finish)
VALUES(1, 'Mon', '02:30', '03:30');

UPDATE Tutor_Availability
SET finish = '06:30'
WHERE tutor_id = 1;

-- reset autoincrement
update sqlite_sequence set seq=1 where name = 'Student';