-- What tutors has tutor X worked with
SELECT DISTINCT Tutor.name
FROM
    Session, Student, Tutor
WHERE
    Session.student_id = Student.id AND
    Session.tutor_id = Tutor.id AND
    Student.name = 'Ramsay Melby';

-- On which days are Student X scheduled
SELECT Session.date
FROM
    Session,
    Student
WHERE
    Session.student_id = Student.id AND
    Student.name = 'X' AND
    -- sessions after today
    Session.date > DATE();

-- On which days are Tutor Y scheduled
SELECT Session.date
FROM
    Session,
    Tutor
WHERE
    Session.tutor_id = Tutor.id AND
    Tutor.name = 'Y' AND
    -- sessions after today
    Session.date > DATE();

-- How many times has each Tutor worked with each Student
SELECT Tutor.name as Tutor, Student.name as Student, count()
FROM
    Session, Student, Tutor
WHERE
    Session.student_id = Student.id AND
    Session.tutor_id = Tutor.id
GROUP BY
    Tutor.name, Student.name;

-- How many times has each Student worked with each Tutor
SELECT Student.name as Student, Tutor.name as Tutor, count()
FROM
    Session, Student, Tutor
WHERE
    Session.student_id = Student.id AND
    Session.tutor_id = Tutor.id
GROUP BY
    Student.name, Tutor.name;

SELECT *
FROM View_Tutor_Availability
WHERE
    start <= ? AND
    finish > ? AND
    day = ?;

SELECT available_tutors.tid as Tutor_id, day, start, finish, IFNULL(num_sessions, 0) as times_with_student
FROM
    (SELECT Tutor.id as tid, day, start, finish
    FROM
        Tutor, Tutor_Availability
    WHERE
        Tutor.id = Tutor_Availability.tutor_id AND
        start <= '6:30' AND
        finish > '6:30' AND
        day = 'T') available_tutors
    LEFT OUTER JOIN
    (SELECT Tutor.id as tid, Student.id as sid, count() as num_sessions
    FROM
        Session, Student, Tutor
    WHERE
        Session.student_id = Student.id AND
        Session.tutor_id = Tutor.id AND
        sid = 18
    GROUP BY
        tid, Student.name) session_counts
    ON available_tutors.tid = session_counts.tid
ORDER BY times_with_student DESC;

SELECT Student.name, date, start, finish
FROM Session, Student
WHERE
    Session.student_id = Student.id AND
    tutor_id = ?;