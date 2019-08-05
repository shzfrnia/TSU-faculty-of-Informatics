function set_text(input_id, text) {
    var input = $(`#${input_id}`);
    input.val(text);
}

function change_value_in_input(el, input_id) {
    set_text(input_id, $(el).text());
}