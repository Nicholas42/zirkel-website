function get_toggled() {
    if (typeof (Storage) !== "undefined") {
        let tmp = localStorage.getItem("toggled");
        if (tmp === null) {
            return "false";
        }
        return tmp;
    } else {
        return document.getElementById("togglestate").value;
    }
}

function set_toggled(state) {
    if (typeof (Storage) !== "undefined") {
        localStorage.setItem("toggled", state);
    }
    document.getElementById("togglestate").value = state;
}

function toggle_navbar() {
    let new_state = get_toggled() === "false";
    set_toggled(new_state ? "true" : "false");

    set_navbar(new_state)
}

function load_navbar() {
    let state = get_toggled() !== "false";
    set_navbar(state)
}

function set_navbar(new_state) {

    let navbar = document.getElementsByClassName("nav-toggle");
    for (var i = 0; i < navbar.length; ++i) {
        navbar[i].style.display = new_state ? "none" : "initial";
    }

    let glyphs = document.getElementById("navbar-toggler").classList;
    if (new_state) {
        glyphs.remove("glyphicon-chevron-down");
        glyphs.add("glyphicon-chevron-up");
    } else {
        glyphs.add("glyphicon-chevron-down");
        glyphs.remove("glyphicon-chevron-up");
    }
}