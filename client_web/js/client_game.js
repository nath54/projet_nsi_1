var websocket = new WebSocket("ws://127.0.0.1:9876/");
websocket.onerror=cantconnect;
console.log(websocket);

function randchoice(liste){ return liste[parseInt(Math.random()*liste.length)]; }

websocket.onmessage = function (event) {
    data = JSON.parse(event.data);
    switch (data.type) {
        case "message":
            console.log(data.value);
            break;
        default:
            console.error("unsupported event", data);
    }
};

function cantconnect(){
    alert("Error : can't connect to the server");
    window.location.href="index.html";
}
