let main_url = "http://raspberrypi.local:8000";
var canvas, ctx;

window.addEventListener('load', () => {

    canvas = document.getElementById('canvas');
    ctx = canvas.getContext('2d');
    resize();

    document.addEventListener('mousedown', startDrawing);
    document.addEventListener('mouseup', stopDrawing);
    document.addEventListener('mousemove', Draw);

    document.addEventListener('touchstart', startDrawing);
    document.addEventListener('touchend', stopDrawing);
    document.addEventListener('touchcancel', stopDrawing);
    document.addEventListener('touchmove', Draw);
    window.addEventListener('resize', resize);

    document.getElementById("x_coordinate").innerText = 0;
    document.getElementById("y_coordinate").innerText = 0;
    document.getElementById("angle").innerText = 0;

    document.addEventListener('touchstart', (event) => {
        event.preventDefault();
        startDrawing(event);
    });

    document.addEventListener('touchmove', (event) => {
        event.preventDefault();
        Draw(event);
    });

    document.addEventListener('touchend', (event) => {
        event.preventDefault();
        stopDrawing(event);
    });

});

var width, height, radius, x_orig, y_orig;
function resize() {
    width = window.innerWidth;
    radius = 100;
    height = radius * 6.5;
    ctx.canvas.width = width;
    ctx.canvas.height = height;
    background();
    joystick(width / 2, height / 3);
}

function background() {
    x_orig = width / 2;
    y_orig = height / 3;

    ctx.beginPath();
    ctx.arc(x_orig, y_orig, radius + 20, 0, 2 * Math.PI * 2, true);
    ctx.fillStyle = "#ECE5E5";
    ctx.fill();
}

function joystick(width, height) {
    ctx.beginPath();
    ctx.arc(width, height, radius, 0, 2 * Math.PI, true);
    ctx.fillStyle = "gray";
    ctx.fill();
}

let coord = { x: 0, y: 0 };
let paint = false;

function getPosition(event) {
    var mouse_x = event.clientX || event.touches[0].clientX;
    var mouse_y = event.clientY || event.touches[0].clientY;

    coord.x = mouse_x - canvas.offsetLeft;
    coord.y = mouse_y - canvas.offsetTop;
}

function in_circle() {
    var current_radius = Math.sqrt(Math.pow(coord.x - x_orig, 2) + Math.pow(coord.y - y_orig, 2));

    if (radius >= current_radius) return true;
    else return false;
}

function startDrawing(event) {
    paint = true;
    getPosition(event)

    if (in_circle()) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        background();
        joystick(coord.x, coord.y);
        Draw(event);
    }
}

function stopDrawing() {
    paint = false;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    background();
    joystick(width / 2, height / 3);
    document.getElementById("x_coordinate").innerText = 0;
    document.getElementById("y_coordinate").innerText = 0;
    document.getElementById("angle").innerText = 0;

    call_api(0, 0, 0)

}

function Draw(event) {
    if (paint) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        background()
        var angle = Math.atan2(coord.y - y_orig, coord.x - x_orig);
        if (Math.sign(angle) == -1) {
            angle_degree = Math.round(Math.abs(angle) * (180 / Math.PI));
        }
        else {
            angle_degree = 360 - Math.round(angle * (180 / Math.PI));
        }

        if (in_circle()) {
            joystick(coord.x, coord.y);
            x = coord.x;
            y = coord.y;
        } else {
            x = radius * Math.cos(angle) + x_orig;
            y = radius * Math.sin(angle) + y_orig;
            joystick(x, y);
        }

        getPosition(event);

        var x_rel = Math.round(x - x_orig);
        var y_rel = Math.round(y_orig - y);

        document.getElementById("x_coordinate").innerText = x_rel;
        document.getElementById("y_coordinate").innerText = y_rel;
        document.getElementById("angle").innerText = angle_degree;

        call_api(x_rel, y_rel, angle)
    }
}

function call_api(x, y, angle) {
    var url = `${main_url}/move/${x}/${y}/${angle}`;
    $.ajax({
        url: url,
        method: 'GET',
        success: function (response) {
            console.log("API Response:", response);
        },
        error: function (xhr, status, error) {
            console.error("API Error:", status, error);
        }
    });
}


