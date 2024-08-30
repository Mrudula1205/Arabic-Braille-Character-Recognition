const canvas = document.getElementById("canvas");
canvas.width = 300;
canvas.height = 300;

let start_background_color = "white";
let context = canvas.getContext("2d");
context.fillStyle = start_background_color;
context.fillRect(0,0, canvas.width, canvas.height);


let draw_color = "black";
let draw_width = "2";
let is_drawing = false;


canvas.addEventListener("touchstart", start, false);
canvas.addEventListener("touchmove", draw, false);
canvas.addEventListener("mousedown", start, false);
canvas.addEventListener("mousemove", draw, false);

canvas.addEventListener("touched", stop, false);
canvas.addEventListener("mouseup", stop, false);
canvas.addEventListener("mouseout", stop, false);

function start(event){
    is_drawing = true;
    context.beginPath();
    context.moveTo(event.clientX - canvas.offsetLeft,
        event.clientY - canvas.offsetTop);
    event.preventDefault();
}

function draw(event){
    if(is_drawing){
        context.lineTo(event.clientX - canvas.offsetLeft,
                       event.clientY - canvas.offsetTop);
        context.strokeStyle = draw_color;
        context.lineWidth = draw_width;
        context.lineCap = "round";
        context.lineJoin = "round";
        context.stroke();
    }
    event.preventDefault();
}

function stop(event){
    if(is_drawing){
        context.stroke();
        context.closePath();
        is_drawing = false;
    }
    event.preventDefault();
}

function clearcanvas(){
    context.fillstyle = start_background_color;
    context.clearRect(0, 0, canvas.width, canvas.height);
    context.fillRect(0, 0, canvas.width, canvas.height);
}

function loadNextQuestion(){
    clearcanvas();
    window.location.href = "/game";
}

function submitanswer(){
    
    const image_data = canvas.toDataURL('image/png');
    const correct_tag = document.getElementById('correctTag').value;

    fetch('/evaluate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({image_data: image_data, correct_tag: correct_tag})
    }).then(response => response.json())
    .then(data => {
        if(data.result === 'correct'){
            alert('Correct!');
            loadNextQuestion();
        }
        else{
            alert('Incorrect!');
        }
    })
    .catch(error => console.error('Error:', error));

}
