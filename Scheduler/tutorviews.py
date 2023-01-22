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

@app.route('/deletetutor/<id>', methods=['DELETE'])
def deleteTutor(id):
    try:
        sql = """
            DELETE FROM Tutor
            WHERE id = ?"""

        db.execute(sql, id)
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

@app.route('/tutorswithavailability', methods=['GET'])
def tutorsWithAvailability():
    try:
        start = request.json['start']
        day = request.json['day']

        sql = """
            SELECT * FROM View_Tutor_Availability
            WHERE
                start = ? AND
                day = ?;"""

        cur = db.cursor()
        cur.execute(sql, [start, day])

        rows = cur.fetchall()

        return rows

    except Error as e:
        print(e)


    return ''