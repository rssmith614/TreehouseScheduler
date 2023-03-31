from flask import request, send_from_directory, render_template, jsonify
from Scheduler import app, db
from sqlite3 import Error

import csv
import os

student_table_header = [
    'id', 
    'name', 
    'nickname', 
    'parent_id', 
    'grade', 
    'school', 
    'dob', 
    'reason', 
    'subjects',
    'mode',
    'status', 
    'gpa', 
    'address', 
    'email', 
    'e_contact_name', 
    'e_contact_relation', 
    'e_contact_phone', 
    'pickup_person', 
    'pickup_relation', 
    'pickup_phone', 
    'medical_comment', 
    'comment'
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/manage_students')
def manageStudents():
    return render_template('manage_students.html')

@app.route('/downloadstudentdata', methods=['GET'])
def downloadStudentData():
    try:
        cur = db.cursor()
        data = cur.execute("SELECT * FROM Student")

        export_loc = app.root_path
        filename = 'students_export.csv'

        with open(os.path.join(export_loc, filename), 'w') as f:
            writer = csv.writer(f)
            writer.writerow(student_table_header)
            writer.writerows(data)
            f.close()

        return send_from_directory(os.path.join(export_loc), os.path.join(filename), as_attachment=True)

    except Error as e:
        print(e)
        return e.args[0], 500

@app.route('/createstudent', methods=['POST'])
def createStudent():
    try:
        # id is automatically assigned
        attributes = student_table_header[1:]

        new_student_attributes = []
        args = []

        for attribute in attributes:
            if attribute in request.json:
                if request.json[attribute] != '':
                    new_student_attributes.append(attribute)
                    args.append(request.json[attribute])

        sql = """
            INSERT INTO Student({})
            VALUES({})
            """.format(', '.join(new_student_attributes), ', '.join(['?'] * len(new_student_attributes)))

        db.execute(sql, args)

        db.commit()

        return {}, 201
        
    except Error as e:
        print(e)
        return e.args[0], 500
    
@app.route('/searchstudents', methods=['GET'])
def searchStudents():
    try:
        res = []

        sql = """
            SELECT * FROM Student
            WHERE name LIKE ?;
        """

        name = request.args.get('name')

        cur = db.cursor()
        rows = cur.execute(sql, ['%'+name+'%'])

        for student in rows:
            cur = {}
            for name, att in zip(student_table_header, student):
                if att:
                    cur.update({name: att})
                else:
                    cur.update({name: ''})
            res.append(cur)

        return jsonify(res), 200

    except Error as e:
        print(e)
        return e.args[0], 500
    
@app.route('/studentinfo/<studentid>', methods=['GET'])
def studentInfo(studentid):
    try:
        res = {}

        sql = """
            SELECT * FROM Student
            WHERE id = ?"""
        
        cur = db.cursor()
        cur.execute(sql, [studentid])

        for name, att in zip(student_table_header, cur.fetchone()):
            if att:
                res.update({name: att})
            else:
                res.update({name: ''})

        return render_template('student_info.html', student=res)
    
    except Error as e:
        print(e)
        return e.args[0], 500

@app.route('/editstudent/<id>', methods=['PUT'])
def editStudent(id):
    try:
        # id is automatically assigned, cannot be changed
        attributes = student_table_header[1:]

        setStmt = ''
        args = []

        for attribute in attributes:
            if attribute in request.json:
                setStmt += attribute + ' = ?, '
                args.append(request.json[attribute])

        setStmt = setStmt[:len(setStmt)-2]

        sql = """
            UPDATE Student
            SET {}
            WHERE id = ?;""".format(setStmt)

        args.append(id)

        db.execute(sql, args)
        db.commit()

        return {}, 201

    except Error as e:
        print(e)
        return e.args[0], 500

@app.route('/deletestudent/<id>', methods=['DELETE'])
def deleteStudent(id):
    try:
        sql = """
            DELETE FROM Student
            WHERE id = ?;"""

        db.execute(sql, [id])
        db.commit()

        return {}, 200

    except Error as e:
        print(e)
        return e.args[0], 500

@app.route('/addstudentavailability/<id>', methods=['POST'])
def addStudentAvailability(id):
    try:
        sql= """
            INSERT INTO Student_Availability
            VALUES(?, ?, ?, ?);
        """

        args = [id, request.json['day'], request.json['start'], request.json['finish']]

        db.execute(sql, args)
        db.commit()

        return {}, 201

    except Error as e:
        print(e)
        return e.args[0], 500

@app.route('/editstudentavailability/<id>', methods=['PUT'])
def editStudentAvailability(id):
    try:
        oldStart = request.json['oldStart']
        oldFinish = request.json['oldFinish']
        newStart = request.json['newStart']
        newFinish = request.json['newFinish']
        day = request.json['day']

        sql = """
            UPDATE Student_Availability
            SET start = ? AND finish = ?
            WHERE student_id = ? AND day = ? AND start = ? AND finish = ?;"""

        args = [newStart, newFinish, id, day, oldStart, oldFinish]

        db.execute(sql, args)
        db.commit()

        return {}, 201

    except Error as e:
        print(e)
        return e.args[0], 500

@app.route('/removestudentavailability/<id>', methods=['DELETE'])
def removeStudentAvailability(id):
    try:
        day = request.json['day']
        start = request.json['start']
        finish = request.json['finish']

        sql = """
            DELETE FROM Student_Availability
            WHERE student_id = ? AND day = ? AND start = ? AND finish = ?;"""

        args = [id, day, start, finish]

        db.execute(sql, args)
        db.commit()

        return {}, 200

    except Error as e:
        print(e)
        return e.args[0], 500
    
@app.route('/studentavailability/<studentid>', methods=['GET'])
def studentAvailability(studentid):
    try:
        res = []

        header = ['day', 'start', 'finish']
        sql = """
            SELECT day, start, finish
            FROM Student_Availability
            WHERE student_id = ?
            ORDER BY start;"""
        
        cur = db.cursor()
        cur.execute(sql, [studentid])

        for availability in cur.fetchall():
            current = {}
            for att, val in zip(header, availability):
                current.update({att: val})
            res.append(current)

        return jsonify(res), 200

    except Error as e:
        print(e)
        return e.args[0], 500
    
@app.route('/studentsessionhistory/<studentid>', methods=['GET'])
def studentSessionHistory(studentid):
    try:
        res = []
        header = ['tutor_name', 'date', 'start', 'finish']
        sql = """
            SELECT Tutor.name, date, start, finish
            FROM Session, Tutor
            WHERE
                Session.tutor_id = Tutor.id AND
                student_id = ?
            ORDER BY date DESC;"""
        
        cur = db.cursor()
        cur.execute(sql, [studentid])
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