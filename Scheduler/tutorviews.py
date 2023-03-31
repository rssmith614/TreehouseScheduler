###############
# tutorviews.py
# author: Robert Smith

# This script manages all flask routes for interactions with and modifications on tutor data
###############

from flask import request, render_template, jsonify, abort, make_response
from Scheduler import app, db, updateTutorAvailability
from sqlite3 import Error

# this list is the header of the Tutor table in the database
# if the database schema changes, this must change
# the rest of this script refers to this list
tutor_table_header = [
    'id',
    'name', 
    'nickname', 
    'primary_phone', 
    'personal_email', 
    'work_email', 
    'mode',
    'status',
    'zoom_room_id',
    'zoom_room_pwd',
    'hire_date', 
    'dob', 
    'avail_calendar', 
    'sched_calendar', 
    'comment'
]

@app.route('/fetchtutoravailability/<id>', methods=['GET'])
def fetchAvailability(id):
    # call the Google Calendar API to get all availability for a specific tutor for the week
    # then push the new availability into the database
    # this is DESTRUCTIVE, if the API call is successful, all of the tutor's current availability is DELETED
    return updateTutorAvailability.DBFromEvents(id)

@app.route('/pushtutoravailability/<id>', methods=['POST'])
def pushAvailability(id):
    # call the Google Calendar API to create events in a specific tutor's calendar next week based on
    # the availability currently stored in the database
    return updateTutorAvailability.eventsFromDB(id)

@app.route('/manage_tutors')
def manageTutors():
    # Page to display all tutor data
    return render_template('manage_tutors.html')

@app.route('/createtutor', methods=['POST'])
def createtutor():
    # Generate a new record for a tutor
    # request should contain json with assignment for every attribute in
    # tutor_table_header (except for id)
    # if the request doesn't have every value, empty strings are assigned
    # this may throw errors when database constraints fail
    try:
        # id is automatically generated
        attributes = tutor_table_header[1:]

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
        return e.args[0], 500

    return '', 201

@app.route('/searchtutors', methods=['GET'])
def searchTutors():
    # Query the database for every tutor based on their name
    # request may have 'name' argument as a search parameter
    try:
        res = []

        sql = """
            SELECT * FROM Tutor
            WHERE name LIKE ?;
        """

        name = request.args.get('name')

        cur = db.cursor()
        rows = cur.execute(sql, ['%'+name+'%'])

        for tutor in rows:
            cur = {}
            for name, att in zip(tutor_table_header, tutor):
                if att:
                    cur.update({name: att})
                else:
                    cur.update({name: ''})
            res.append(cur)

        return jsonify(res), 200

    except Error as e:
        print(e)
        return e.args[0], 500
    
@app.route('/tutorinfo/<tutorid>', methods=['GET'])
def tutorInfo(tutorid):
    # Collect all attributes on a specific student, identified by unique id attribute
    try:
        res = {}

        sql = """
            SELECT * FROM Tutor
            WHERE id = ?"""
        
        cur = db.cursor()
        cur.execute(sql, [tutorid])

        for name, att in zip(tutor_table_header, cur.fetchone()):
            if att:
                res.update({name: att})
            else:
                res.update({name: ''})

        return render_template('tutor_info.html', tutor=res), 200
    
    except Error as e:
        print(e)
        return e.args[0], 500

@app.route('/edittutor/<id>', methods=['PUT'])
def editTutor(id):
    # Edit any attributes for a specific tutor, identified by unique id
    # request json should contain keys from tutor_table_header whose values are to be changed
    # {"name": "New Name"} when id = 1 will change tutor 1's name to "New Name" 
    try:
        # id is automatically assigned, cannot be changed
        attributes = tutor_table_header[1:]

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
        return e.args[0], 500

@app.route('/deletetutor/<id>', methods=['DELETE'])
def deleteTutor(id):
    # Remove a specific tutor from the database, identified by unique id
    try:
        sql = """
            DELETE FROM Tutor
            WHERE id = ?;"""

        db.execute(sql, [id])
        db.commit()

    except Error as e:
        print(e)
        return e.args[0], 500

    return '', 200

@app.route('/addtutoravailability/<id>', methods=['POST'])
def addTutorAvailability(id):
    # Create an availability for a specific tutor
    # request json needs keys "day", "start", and "finish"
    # database constraints will make this throw errors, so be careful
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
        return e.args[0], 500
    
    return '', 201

@app.route('/edittutoravailability/<id>', methods=['PUT'])
def editTutorAvailability(id):
    # Change an availability entry in the database for a specific tutor
    # since day, start, and finish times are unique to each tutor, all are needed to do edits
    # you can see the required json keys on the following few lines
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
        return e.args[0], 500

    return '', 201

@app.route('/removetutoravailability/<id>', methods=['DELETE'])
def removeTutorAvailability(id):
    # Delete a specific tutor availability from the database
    # availability is unique based on id, day, start, and finish, so all are needed
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
        return e.args[0], 500
    
    return '', 200

@app.route('/tutoravailability/<tutorid>', methods=['GET'])
def tutorAvailability(tutorid):
    # Get every availability for a specific tutor, unique tutor id
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
        return e.args[0], 500

@app.route('/tutorswithavailability', methods=['GET'])
def tutorsWithAvailability():
    # Proof of concept query
    # get tutors with a specified availability (request json "day" and "start")
    # show how many times each tutor has worked with a specified student (request json "student_id")
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

        return jsonify(rows), 200

    except Error as e:
        print(e)
        return e.args[0], 500

@app.route('/tutorsessionhistory/<tutorid>', methods=['GET'])
def tutorSessionHistory(tutorid):
    # Get every session involving a specific tutor
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
        cur.execute(sql, [int(tutorid)])
        rows = cur.fetchall()

        for session in rows:
            cur = {}
            for att, val in zip(header, session):
                cur.update({att: val})
            res.append(cur)

        return jsonify(res), 200

    except Error as e:
        print(e)
        return e.args[0], 500