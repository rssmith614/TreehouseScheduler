function createTutor() {
    var name = document.getElementById("name").value;
    var nickname = document.getElementById("nickname").value;
    var primary_phone = document.getElementById("primary_phone").value;
    var personal_email = document.getElementById("personal_email").value;
    var work_email = document.getElementById("work_email").value;
    var hire_date = document.getElementById("hire_date").value;
    var dob = document.getElementById("dob").value;
    var comment = document.getElementById("comment").value;

    var tutor = {
      "name": name,
      "nickname": nickname,
      "primary_phone": primary_phone,
      "personal_email": personal_email,
      "work_email": work_email,
      "hire_date": hire_date,
      "dob": dob,
      "comment": comment
    };

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/createtutor", true);

    xhr.onload = function() {
        document.getElementById("name").value = "";
        document.getElementById("nickname").value = "";
        document.getElementById("primary_phone").value = "";
        document.getElementById("personal_email").value = "";
        document.getElementById("work_email").value = "";
        document.getElementById("hire_date").value = "";
        document.getElementById("dob").value = "";
        document.getElementById("comment").value = "";
    }

    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify(tutor));
  }

function searchTutorsByName() {
    var xhr = new XMLHttpRequest();
    var name = document.getElementById("search_name").value;
    xhr.open("GET", "/searchtutors?name=" + encodeURIComponent(name), false);

    xhr.onload = function() {
        data = JSON.parse(this.response);
        res = "";
        header = ['name', 'nickname', 'primary_phone', 'personal_email', 'work_email', 'hire_date', 'dob', 'comment'];

        data.forEach(tutor => {
            res += "<tr>";
            res += "<td><button onclick=\"deleteTutor(" + tutor['id'] + ")\">Delete</button></td>";
            res += "<td><a href=\"tutorinfo/" + tutor['id'] + "\">" + tutor['id'] + "</a></td>";
            header.forEach(att => {
                res += "<td>" + tutor[att] + "</td>";
            });
            res += "</tr>";
        });

        document.getElementById("tutors_table").innerHTML = res;
    }

    xhr.send();
}

function deleteTutor(id) {
    var xhr = new XMLHttpRequest();
    xhr.open("DELETE", "/deletetutor/" + id);

    xhr.onload = function() {
        searchTutorsByName();
    }

    xhr.send();
}

function updateTutor() {
    var xhr = new XMLHttpRequest();
    xhr.open("PUT", "/edittutor/" + document.getElementById("tutorid").innerHTML);
    data = {};
    attributes = ['name', 'nickname', 'primary_phone', 'personal_email', 'work_email', 'hire_date', 'dob', 'comment'];
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
    xhr.open("GET", "/tutorsessionhistory/" + document.getElementById("tutorid").innerHTML);

    xhr.onload = function() {
        data = JSON.parse(this.response);
        console.log(data);
        res = "";
        header = ['student_name', 'date', 'start', 'finish'];

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