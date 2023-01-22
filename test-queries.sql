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