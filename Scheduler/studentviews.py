from flask import request
from Scheduler import app, db
from sqlite3 import Error

@app.route('/')
def index():
    return None

@app.route('/createstudent', methods=['POST'])
def createStudent():
    try:
        attributes = ['name', 'nickname', 'parent_name', 'primary_phone', 'grade', 'school', 'dob', 'reason', 'subjects', 'gpa', 'address', 'email', 'e_contact_name', 'e_contact_relation', 'e_contact_phone', 'pickup_person', 'pickup_relation', 'pickup_phone', 'medical_comment', 'comment']

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
        
    except Error as e:
        print(e)

    return ''

@app.route('/deletestudent/<id>', methods=['DELETE'])
def deleteStudent(id):
    try:
        sql = """
            DELETE FROM Student
            WHERE id = ?"""

        db.execute(sql, id)
        db.commit()

    except Error as e:
        print(e)

    return ''

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

    except Error as e:
        print(e)
    
    return ''