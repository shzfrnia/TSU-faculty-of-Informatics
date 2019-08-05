// Vue.swap = function(arr, x, y) {
//     var origin = arr[x];
//     arr[x] = arr[y];
//     Vue.set(arr, y, origin);
//   }


$(document).ready(function () {
  if ($('.memorizePanel').length != 0) {

    $('.flipCard').click(function () {
      if ($('.cardFront').is(":visible") == true) {
        $('.cardFront').hide();
        $('.cardBack').show();
      } else {
        $('.cardFront').show();
        $('.cardBack').hide();
      }
    });
  }
  // to remove the short delay on click on touch devices
  // FastClick.attach(document.body);
});

$("#fork-button").tooltip({
  placement: "bottom"
});




var notepad = new Vue({
  el: "#editNotepad",
  data: {
    notepad_id: $("#editNotepad").attr("notepad_id"), // FIXME есть ли во вью получение атрибута?
    notepad_name: "",
    notepad_description: "",
    notepad_subject: "",
    public: false,
    cards: []
  },
  created: function() {
    $.getJSON("/getnotepadjson?notepad_id=" + this.notepad_id, function(data) {
      notepad.deserialize(data);
      if (data.cards.length === 0) {
        notepad.cards.push({ first_part: "Term", last_part: "Defenition" });
      }
    });
  },
  methods: {
    deserialize: function(data) {
      this.notepad_name = data.notepad_name;
      this.notepad_description = data.notepad_description;
      this.notepad_subject = data.notepad_subject;
      this.public = data.public;
      data.cards.forEach(function(card, i, arr) {
        notepad.cards.push({
          card_id: card.card_id,
          first_part: card.fisrt_part,
          last_part: card.last_part
        });
      });
    },
    addElement: function() {
      this.cards.push({ card_id: "new_card", first_part: "", last_part: "" });
    },
    deleteFromArray: function(index) {
      if (this.cards.length === 1) {
        alert("Notepad must have 1 card!");
        return;
      }
      this.$delete(this.cards, index);
    },
    sentPost: function() {
      if (this.notepad_name === "" || this.notepad_name.length > 20 ) {
        alert("GIVE norm notepad name  ༼ つ ◕_◕ ༽つ!");
        return;
      }
      postData = {
        notepad_id: this.notepad_id,
        notepad_name: this.notepad_name,
        notepad_description: this.notepad_description,
        notepad_subject: this.notepad_subject,
        public: this.public,
        cards: this.cards
      };
      var validation = true;
      this.cards.forEach(function(card, index) {
        if (
          card.first_part === "" ||
          card.first_part === null ||
          (card.last_part === "" || card.last_part === null)
        ) {
          alert("Fill card! " + index);
          validation = false;
          return;
        }
      });
      if (!validation) {
        return;
      }
      $.ajax({
        type: "POST",
        url: "/editNotepad?notepad_id=" + this.notepad_id,
        data: JSON.stringify(postData, null, "\t"),
        contentType: "application/json;charset=UTF-8",
        success: function(result) {
          $.ajax({
            type: "POST",
            url:
              "/flashMessage?message=" +
              "Your changes have been saved.&category=success",
            success: function() {
              $(location).attr("href", "/myNotepads");
            }
          });
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
          alert("Status: " + textStatus);
          alert("Error: " + errorThrown);
        }
      });
    },
    deleteNotepad: function() {
      var conf = confirm("Are you sure?");
      if (conf === true) {
        $.ajax({
          type: "POST",
          url: "/deleteNotepad?notepad_id=" + this.notepad_id,
          success: function(result) {
            $.ajax({
              type: "POST",
              url:
                "/flashMessage?message=" +
                "Your notepad have been deleted.&category=success",
              success: function() {
                $(location).attr("href", "/myNotepads");
              }
            });
          }
        });
      } else {
        return;
      }
    }
  }
});
