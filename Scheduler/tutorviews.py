from flask import request, render_template, jsonify, abort
from Scheduler import app, db
from sqlite3 import Error

@app.route('/manage_tutors')
def manageTutors():
    return render_template('manage_tutors.html')

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

@app.route('/searchtutors', methods=['GET'])
def searchTutors():
    try:
        res = []
        header = ['id', 'name', 'nickname', 'primary_phone', 'personal_email', 'work_email', 'hire_date', 'dob', 'comment']

        sql = """
            SELECT * FROM Tutor
            WHERE name LIKE ?;
        """

        name = request.args.get('name')

        cur = db.cursor()
        rows = cur.execute(sql, ['%'+name+'%'])

        for tutor in rows:
            cur = {}
            for name, att in zip(header, tutor):
                if att:
                    cur.update({name: att})
                else:
                    cur.update({name: ''})
            res.append(cur)

        return jsonify(res), 200

    except Error as e:
        print(e)
        return abort(404)
    
@app.route('/tutorinfo/<tutorid>', methods=['GET'])
def tutorInfo(tutorid):
    try:
        res = {}
        header = ['id', 'name', 'nickname', 'primary_phone', 'personal_email', 'work_email', 'hire_date', 'dob', 'comment']

        sql = """
            SELECT * FROM Tutor
            WHERE id = ?"""
        
        cur = db.cursor()
        cur.execute(sql, [tutorid])

        for name, att in zip(header, cur.fetchone()):
            if att:
                res.update({name: att})
            else:
                res.update({name: ''})

        return render_template('tutor_info.html', tutor=res)
    
    except Error as e:
        print(e)
        return abort(404)

@app.route('/edittutor/<id>', methods=['PUT'])
def editTutor(id):
    try:
        attributes = ['name', 'nickname', 'primary_phone', 'personal_email', 'work_email', 'hire_date', 'dob', 'comment']

        setStmt = ''
        args = []

        for attribute in attributes:
            if attribute in request.json:
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

        return {}, 201

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

@app.route('/tutoravailability/<tutorid>', methods=['GET'])
def tutorAvailability(tutorid):
    try:
        res = []

        header = ['day', 'start', 'finish']
        sql = """
            SELECT day, start, finish
            FROM Tutor_Availability
            WHERE tutor_id = ?
            ORDER BY start;"""
        
        cur = db.cursor()
        cur.execute(sql, [tutorid])

        for availability in cur.fetchall():
            current = {}
            for att, val in zip(header, availability):
                current.update({att: val})
            res.append(current)

        return jsonify(res), 200

    except Error as e:
        print(e)
        return abort(404)

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

@app.route('/tutorsessionhistory/<tutorid>', methods=['GET'])
def tutorSessionHistory(tutorid):
    try:
        res = []
        header = ['student_name', 'date', 'start', 'finish']
        sql = """
            SELECT Student.name, date, start, finish
            FROM Session, Student
            WHERE
                Session.student_id = Student.id AND
                tutor_id = ?
            ORDER BY date DESC;"""
        
        cur = db.cursor()
        cur.execute(sql, [tutorid])
        rows = cur.fetchall()

        for session in rows:
            cur = {}
            for att, val in zip(header, session):
                cur.update({att: val})
            res.append(cur)

        return jsonify(res), 200

    except Error as e:
        print(e)
        return abort(404)