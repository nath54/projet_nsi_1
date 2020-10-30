
var ip = sessionStorage.getItem("ip");
var port = sessionStorage.getItem("port");

if(!(ip!=undefined && port!=undefined)){
    alert("Probleme de connection ! (ip et port manquant)");
    window.href.location="index.html";
}

websocket = new WebSocket("ws://"+ip+":"+port+"/");

console.log(typeof websocket);
console.log(websocket);

if(websocket==undefined){
    alert("Erreur, vous n'êtes pas connecté")
    window.SharedWorker.location="index.html";
}

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
