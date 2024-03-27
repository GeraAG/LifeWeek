function getNote(id) {
    var container = $('#note-container');
    var compStyles = window.getComputedStyle(container[0], null);
    if(compStyles.getPropertyValue("visibility") === "hidden") {
        console.log("container is hidden")
        $.get('/note', { week_id: id })
            .done(function (response) {
                var container = $('#note-container');
                container.html(response);
                container.css("visibility", "visible");

                // Stop clickthrough
                const life_container = document.getElementById("life-container");
                const top_bar = document.getElementById("top-bar");
                life_container.classList.add("avoid-clicks");
                top_bar.classList.add("avoid-clicks");

                const bd = document.querySelector("body");
                bd.classList.add("dark-background");
            })
            .fail(function (error) {
                console.error('Error handling AJAX response:', error);
            });
    }

};

function closeNote() {
    var container = $('#note-container');
    container.css("visibility", "hidden");
    const life_container = document.getElementById("life-container");
    const top_bar = document.getElementById("top-bar");
    life_container.classList.remove("avoid-clicks");
    top_bar.classList.remove("avoid-clicks");

    const bd = document.querySelector("body");
    bd.classList.remove("dark-background");
};

function saveNote() {
    note = $('#note').text();
    week_id = $('#note-week-id').text();

    // Changes appereance of the small box if note has content
    week_box = document.getElementById(week_id);
    if(note == "" && week_box.classList.contains('has-notes')) {
        week_box.classList.remove("has-notes");
    } else if (note != "" && !week_box.classList.contains('has-notes') && !week_box.classList.contains('current')){
        week_box.classList.add("has-notes");
    }

    console.log(JSON.stringify({text: note, week_id: week_id}));

    $.ajax({
        url: "/note",
        type: "POST",
        dataType: "application/json",
        data: JSON.stringify({text: note, week_id: week_id}),
        success: function(response) {
            alert('Succes');
        }
      });

}

document.addEventListener("mousedown", function(e) {
    var container = document.getElementById('note-container');
    if (!container.contains(e.target)) {
        closeNote();
    }
});

function getAge()
{
    var container = document.getElementById('birthday');
    var dateString = container.title;
    var today = new Date();
    var birthDate = new Date(dateString);
    var age = today.getFullYear() - birthDate.getFullYear();
    var weeks = document.getElementsByClassName("current")[0].id % 52;
    //container.textContent += '${age} Years and ${weeks} weeks';
    container.textContent += age + ' years and ' + weeks + ' weeks';
    //return age;
}

const scrollIntoViewWithOffset = (selector, offset) => {
    window.scrollTo({
      behavior: 'smooth',
      top:
        document.querySelector(selector).getBoundingClientRect().top -
        document.body.getBoundingClientRect().top -
        offset,
    })
};

window.onload = function() {
    //var elem = document.getElementsByClassName("current")[0];
    //console.log(elem.id % 52)
    scrollIntoViewWithOffset(".current",200)
    getAge();

  };
