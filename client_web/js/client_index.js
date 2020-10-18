var websocket = new WebSocket("ws://127.0.0.1:9876/");
websocket.onerror=cantconnect;
console.log(websocket);

function randchoice(liste){ return liste[parseInt(Math.random()*liste.length)]; }

websocket.onmessage = function (event) {
    data = JSON.parse(event.data);
    switch (data.type) {
        case 'connection failed':
            alert("Connection failed : \n"+data.error);
            break;
        case 'connection successed':
            window.location.href="game.html?"+data.id+"&"+data.key;
            break;
        case 'inscription failed':
            alert("Inscription failed : \n"+data.error);
            break;
        case 'inscription successed':
                window.location.href="game.html?"+data.id+"&"+data.key;
                break;
        case "info account":
            alert("get infos account");
            actualise_infos(account);
            break;
        default:
            console.error("unsupported event", data);
    }
};

function cantconnect(){
    alert("Error : can't connect to the server");
    window.location.href="index.html";
}

function youarenotconnected(){
    alert("Error : You are not connected !");
    window.location.href="index.html";
}

function disconnected(){

}








