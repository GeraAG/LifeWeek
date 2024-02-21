function getNote(id) {
    $.get('/note', { week_id: id })
        .done(function (response) {
            var container = $('#note-container');
            container.html(response);
            container.css("visibility", "visible")
        })
        .fail(function (error) {
            console.error('Error handling AJAX response:', error);
        });
};

function closeNote() {
    var container = $('#note-container');
    container.css("visibility", "hidden")
};

function saveNote() {
    note = $('#note').text();
    console.log(note)
    week_id = $('#note-week-id').text();

    /*$.post("/note", {data: note, dataType: application/json});*/
    var jsonSTR = JSON.stringify({text: note})
    console.log(jsonSTR)
    console.log(JSON.stringify({text: note, week_id: week_id}))
    console.log(typeof jsonSTR === 'object');

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

window.onload = function() {
    var elem = document.getElementsByClassName("current")[0];
    elem.scrollIntoView();
  };
