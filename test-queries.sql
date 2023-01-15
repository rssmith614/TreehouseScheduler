-- What tutors has tutor X worked with
SELECT DISTINCT Tutor.name
FROM
    Session,
    Student,
    Tutor
WHERE
    Session.student_id = Student.id AND
    Session.tutor_id = Tutor.id AND
    Student.name = 'X';

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

SELECT Tutor.name, Tutor_Availability.*
FROM
    Tutor,
    Tutor_Availability
WHERE
    Tutor.id = Tutor_Availability.tutor_id;