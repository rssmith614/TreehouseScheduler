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
        header = ['id', 'name', 'nickname', 'primary_phone', 'personal_email', 'work_email', 'hire_date', 'dob', 'comment'];

        data.forEach(tutor => {
            res += "<tr>";
            res += "<td><button onclick=\"deleteTutor(" + tutor['id'] + ")\">Delete</button></td>";
            header.forEach(att => {
                res += "<td>" + tutor[att] + "</td>";
            });
            res += "</td>";
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