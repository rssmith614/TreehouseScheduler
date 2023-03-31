################
# studentviews.py
# author: Robert Smith
# 
# This script manages the flask app routes for any functions relating to modifications on student data
################

from flask import request, send_from_directory, render_template, jsonify
from Scheduler import app, db
from sqlite3 import Error

import csv
import os

# this is the header for the Student table in the database
# if the database changes, this needs to change
# the rest of this script refers to this list
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
    # Temporary home page
    return render_template('index.html')

@app.route('/manage_students')
def manageStudents():
    # Page to display all student data
    return render_template('manage_students.html')

@app.route('/downloadstudentdata', methods=['GET'])
def downloadStudentData():
    # Materialize the Student table in the database as it is now
    # Create a download as a .csv file
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
    # Generate a new record for a student
    # request should contain json with assignment for every attribute in
    # student_table_header (except for id)
    # if the request doesn't have every value, empty strings are assigned
    # this may throw errors when database constraints fail
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
    # Query the database for every student based on their name
    # request may have 'name' argument as a search parameter
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
    # Collect all attributes on a specific student, identified by unique id attribute
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
    # Edit any attributes for a specific student, identified by unique id
    # request json should contain keys from student_table_header whose values are to be changed
    # {"name": "New Name"} when id = 1 will change student 1's name to "New Name" 
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
    # Remove a specific student from the database, identified by unique id
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
    # Create an availability for a specific student
    # request json needs keys "day", "start", and "finish"
    # database constraints will make this throw errors, so be careful
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
    # Change an availability entry in the database for a specific student
    # since day, start, and finish times are unique to each student, all are needed to do edits
    # you can see the required json keys on the following few lines
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
    # Delete a specific student availability from the database
    # availability is unique based on id, day, start, and finish, so all are needed
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
    # Get every availability for a specific student, unique student id
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
    # Get every session involving a specific student
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
        cur.execute(sql, [int(studentid)])
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