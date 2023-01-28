from flask import request
from Scheduler import app, db
from sqlite3 import Error

@app.route('/createtutor', methods=['POST'])
def createtutor():
    try:
        attributes = ['name', 'nickname', 'primary_phone', 'personal_email', 'work_email', 'hire_date', 'dob', 'comment']

        new_tutor_attributes = []
        args = []

        for attribute in attributes:
            if attribute in request.json:
                if request.json[attribute] != '':
                    new_tutor_attributes.append(attribute)
                    args.append(request.json[attribute])

        sql = """
            INSERT INTO Tutor({})
            VALUES({})
            """.format(', '.join(new_tutor_attributes), ', '.join(['?'] * len(new_tutor_attributes)))

        db.execute(sql, args)

        db.commit()

    except Error as e:
        print(e)

    return ''

@app.route('/edittutor/<id>', methods=['PUT'])
def editTutor(id):
    try:
        attributes = ['name', 'nickname', 'primary_phone', 'personal_email', 'work_email', 'hire_date', 'dob', 'comment']

        setStmt = ''
        args = []

        for attribute in attributes:
            if attribute in request.json:
                if request.json[attribute] != '':
                    setStmt += attribute + ' = ?, '
                    args.append(request.json[attribute])

        setStmt = setStmt[:len(setStmt)-2]

        sql = """
            UPDATE Tutor
            SET {}
            WHERE id = ?;""".format(setStmt)

        args.append(id)

        db.execute(sql, args)
        db.commit()

    except Error as e:
        print(e)

    return ''

@app.route('/deletetutor/<id>', methods=['DELETE'])
def deleteTutor(id):
    try:
        sql = """
            DELETE FROM Tutor
            WHERE id = ?;"""

        db.execute(sql, [id])
        db.commit()

    except Error as e:
        print(e)

    return ''

@app.route('/addtutoravailability/<id>', methods=['POST'])
def addTutorAvailability(id):
    try:
        sql= """
            INSERT INTO Tutor_Availability
            VALUES(?, ?, ?, ?);
        """

        args = [id, request.json['day'], request.json['start'], request.json['finish']]

        db.execute(sql, args)
        db.commit()

    except Error as e:
        print(e)
    
    return ''

@app.route('/edittutoravailability/<id>', methods=['PUT'])
def editTutorAvailability(id):
    try:
        oldStart = request.json['oldStart']
        oldFinish = request.json['oldFinish']
        newStart = request.json['newStart']
        newFinish = request.json['newFinish']
        day = request.json['day']

        sql = """
            UPDATE Tutor_Availability
            SET start = ? AND finish = ?
            WHERE tutor_id = ? AND day = ? AND start = ? AND finish = ?;"""

        args = [newStart, newFinish, id, day, oldStart, oldFinish]

        db.execute(sql, args)
        db.commit()

    except Error as e:
        print(e)    

    return ''

@app.route('/removetutoravailability/<id>', methods=['DELETE'])
def removeTutorAvailability(id):
    try:
        day = request.json['day']
        start = request.json['start']
        finish = request.json['finish']

        sql = """
            DELETE FROM Tutor_Availability
            WHERE tutor_id = ? AND day = ? AND start = ? AND finish = ?;"""

        args = [id, day, start, finish]

        db.execute(sql, args)
        db.commit()

    except Error as e:
        print(e)

@app.route('/tutorswithavailability', methods=['GET'])
def tutorsWithAvailability():
    try:
        start = request.json['start']
        day = request.json['day']
        student = request.json['student_id']

        sql = """
            SELECT available_tutors.tid as Tutor_id, day, start, finish, IFNULL(num_sessions, 0) as times_with_student
            FROM
                (SELECT Tutor.id as tid, day, start, finish
                FROM
                    Tutor, Tutor_Availability
                WHERE
                    Tutor.id = Tutor_Availability.tutor_id AND
                    start <= ? AND
                    finish > ? AND
                    day = ?) available_tutors
                LEFT OUTER JOIN
                (SELECT Tutor.id as tid, Student.id as sid, count() as num_sessions
                FROM
                    Session, Student, Tutor
                WHERE
                    Session.student_id = Student.id AND
                    Session.tutor_id = Tutor.id AND
                    sid = ?
                GROUP BY
                    tid, Student.name) session_counts
                ON available_tutors.tid = session_counts.tid
            ORDER BY times_with_student DESC;"""

        cur = db.cursor()
        cur.execute(sql, [start, start, day, student])

        rows = cur.fetchall()

        return rows

    except Error as e:
        print(e)


    return ''