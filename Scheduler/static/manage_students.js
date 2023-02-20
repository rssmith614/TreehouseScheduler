function createStudent() {
    var name = document.getElementById("name").value;
    var nickname = document.getElementById("nickname").value;
    var parent_name = document.getElementById("parent_name").value;
    var primary_phone = document.getElementById("primary_phone").value;
    var grade = document.getElementById("grade").value;
    var school = document.getElementById("school").value;
    var dob = document.getElementById("dob").value;
    var reason = document.getElementById("reason").value;
    var subjects = document.getElementById("subjects").value;
    var gpa = document.getElementById("gpa").value;
    var address = document.getElementById("address").value;
    var email = document.getElementById("email").value;
    var e_contact_name = document.getElementById("e_contact_name").value;
    var e_contact_relation = document.getElementById("e_contact_relation").value;
    var e_contact_phone = document.getElementById("e_contact_phone").value;
    var pickup_person = document.getElementById("pickup_person").value;
    var pickup_relation = document.getElementById("pickup_relation").value;
    var pickup_phone = document.getElementById("pickup_phone").value;
    var medical_comment = document.getElementById("medical_comment").value;
    var comment = document.getElementById("comment").value;

    var student = {
        "name": name,
        "nickname": nickname,
        "parent_name": parent_name,
        "primary_phone": primary_phone,
        "grade": grade,
        "school": school,
        "dob": dob,
        "reason": reason,
        "subjects": subjects,
        "gpa": gpa,
        "address": address,
        "email": email,
        "e_contact_name": e_contact_name,
        "e_contact_relation": e_contact_relation,
        "e_contact_phone": e_contact_phone,
        "pickup_person": pickup_person,
        "pickup_relation": pickup_relation,
        "pickup_phone": pickup_phone,
        "medical_comment": medical_comment,
        "comment": comment
    };
  
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/createstudent", false);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

    xhr.onload = function() {
        searchStudentsByName();
    }

    xhr.send(JSON.stringify(student));
}

function searchStudentsByName() {
    var xhr = new XMLHttpRequest();
    var name = document.getElementById("search_name").value;
    xhr.open("GET", "/searchstudents?name=" + encodeURIComponent(name), false);

    xhr.onload = function() {
        data = JSON.parse(this.response);
        res = "";
        header = ['name', 'nickname', 'parent_name', 'primary_phone', 'grade', 'school', 'dob', 'reason', 'subjects', 'gpa', 'address', 'email', 'e_contact_name', 'e_contact_relation', 'e_contact_phone', 'pickup_person', 'pickup_relation', 'pickup_phone', 'medical_comment', 'comment'];

        data.forEach(student => {
            res += "<tr>";
            res += "<td><button onclick=\"deleteStudent(" + student['id'] + ")\">Delete</button></td>";
            res += "<td><a href=\"studentinfo/" + student['id'] + "\">" + student['id'] + "</a></td>";
            header.forEach(att => {
                res += "<td>" + student[att] + "</td>";
            });
            res += "</td>";
        });

        document.getElementById("students_table").innerHTML = res;
    }

    xhr.send();
}

function deleteStudent(id) {
    var xhr = new XMLHttpRequest();
    xhr.open("DELETE", "/deletestudent/" + id);

    xhr.onload = function() {
        searchStudentsByName();
    }

    xhr.send();
}

function updateStudent() {
    var xhr = new XMLHttpRequest();
    xhr.open("PUT", "/editstudent/" + document.getElementById("studentid").innerHTML);
    data = {};
    attributes = ['name', 'nickname', 'parent_name', 'primary_phone', 'grade', 'school', 'dob', 'reason', 'subjects', 'gpa', 'address', 'email', 'e_contact_name', 'e_contact_relation', 'e_contact_phone', 'pickup_person', 'pickup_relation', 'pickup_phone', 'medical_comment', 'comment'];
    attributes.forEach(att => {
        data[att] = document.getElementById(att).value;
    });

    xhr.onload = function() {
        document.getElementById("updateResult").innerHTML = "Done!";
    }

    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify(data));
}

function showSessions() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/studentsessionhistory/" + document.getElementById("studentid").innerHTML);

    xhr.onload = function() {
        data = JSON.parse(this.response);
        console.log(data);
        res = "";
        header = ['tutor_name', 'date', 'start', 'finish'];

        data.forEach(session => {
            res += "<tr>";
            header.forEach(att => {
                res += "<td>" + session[att] + "</td>";
            });
            res += "</tr>";
        });

        document.getElementById("sessions").innerHTML = res;
    }

    xhr.send();
}

function showAvailability() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/studentavailability/" + document.getElementById("studentid").innerHTML);

    xhr.onload = function() {
        data = JSON.parse(this.response);
        res = "";
        height = 0
        schedule = {
            "M": [],
            "T": [],
            "W": [],
            "R": [],
            "F": []
        };

        data.forEach(availability => {
            schedule[availability['day']].push(availability['start'] + "-" + availability['finish']);
            height = Math.max(height, schedule[availability['day']].length)
        });

        while (height > 0) {
            current = "<tr>"
            for (var [day, availability] of Object.entries(schedule)) {
                if (availability.length > 0) {
                    current += "<td>" + availability.shift() + "</td>";
                } else {
                    current += "<td></td>";
                }
            }
            res += current + "</tr>";
            height -= 1;
        }

        document.getElementById("availability").innerHTML = res;
    }

    xhr.send();
}