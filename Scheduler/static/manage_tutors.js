function createTutor() {
    var name = document.getElementById("name").value;
    var nickname = document.getElementById("nickname").value;
    var primary_phone = document.getElementById("primary_phone").value;
    var personal_email = document.getElementById("personal_email").value;
    var work_email = document.getElementById("work_email").value;
    var hire_date = document.getElementById("hire_date").value;
    var dob = document.getElementById("dob").value;
    var avail_calendar = document.getElementById("avail_calendar").value;
    var sched_calendar = document.getElementById("sched_calendar").value;
    var comment = document.getElementById("comment").value;

    var tutor = {
      "name": name,
      "nickname": nickname,
      "primary_phone": primary_phone,
      "personal_email": personal_email,
      "work_email": work_email,
      "hire_date": hire_date,
      "dob": dob,
      "avail_calendar": avail_calendar,
      "sched_calendar": sched_calendar,
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
        document.getElementById("avail_calendar").value = "";
        document.getElementById("sched_calendar").value = "";
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
        header = ['name', 'nickname', 'primary_phone', 'personal_email', 'work_email', 'hire_date', 'dob', 'avail_calendar', 'sched_calendar', 'comment'];

        data.forEach(tutor => {
            res += "<tr>";
            res += "<td><button onclick=\"deleteTutor(" + tutor['id'] + ")\">Delete</button></td>";
            res += "<td><a href=\"tutorinfo/" + tutor['id'] + "\">" + tutor['id'] + "</a></td>";
            header.forEach(att => {
                if (att === "avail_calendar" || att === "sched_calendar") {
                    if (tutor[att] != "") {
                        console.log("<td><button onclick=\"copyLink(\"" + tutor[att] + "\")\">Calendar Link</button></td>");
                        res += "<td><button onclick=\"copyLink(\'" + tutor[att] + "\')\">Calendar Link</button></td>";
                    } else {
                        res += "<td></td>"
                    }
                } else {
                    res += "<td>" + tutor[att] + "</td>";
                }
            });
            res += "</tr>";
        });
        

        document.getElementById("tutors_table").innerHTML = res;
    }

    xhr.send();
}

function copyLink(link) {
    navigator.clipboard.writeText(link);
    alert("Copied calendar ID to clipboard");
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
    attributes = ['name', 'nickname', 'primary_phone', 'personal_email', 'work_email', 'hire_date', 'dob', 'avail_calendar', 'sched_calendar', 'comment'];
    attributes.forEach(att => {
        data[att] = document.getElementById(att).value;
    });

    xhr.onload = function() {
        if (this.status === 201)
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

function showAvailability() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/tutoravailability/" + document.getElementById("tutorid").innerHTML);

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

function fetchAvailability() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/fetchtutoravailability/" + document.getElementById("tutorid").innerHTML);

    xhr.onload = function () {
        if (this.status != 200)
            alert(this.response)
        showAvailability();
        document.getElementById("fetchSuccess").innerHTML = "";
    }

    document.getElementById("fetchSuccess").innerHTML = "Fetching...";

    xhr.send();
}

function pushAvailability() {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/pushtutoravailability/" + document.getElementById("tutorid").innerHTML);

    xhr.onload = function () {
        if (this.status == 201)
            alert("Created events");
        else
            alert(this.response);

        document.getElementById("pushSuccess").innerHTML = "";
    }

    document.getElementById("pushSuccess").innerHTML = "Pushing...";

    xhr.send();
}