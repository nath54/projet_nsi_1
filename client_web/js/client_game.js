
var ip = sessionStorage.getItem("ip");
var port = sessionStorage.getItem("port");

if(!(ip!=undefined && port!=undefined)){
    alert("Probleme de connection ! (ip et port manquant)");
    window.href.location="index.html";
}

websocket = new WebSocket("ws://"+ip+":"+port+"/");

if(websocket==undefined){
    alert("Erreur, vous n'êtes pas connecté")
    window.SharedWorker.location="index.html";
}

websocket.onmessage = function (event) {
    data = JSON.parse(event.data);
    if(typeof data == "string"){
        data = JSON.parse(data);
    }
    console.log(data, typeof data, "creation perso", data.type=="creation perso");
    switch (data["type"]) {
        case "message":
            aff_message(txt = data.value, color = "rgb(200,200,200)");
            break;
        case "genres":
            genres = JSON.parse(data.genres);
            break;
        case "creation perso":
            perso_creator();
            break;
        default:
            console.error("unsupported event", data);
    }
};

function cantconnect(){
    alert("Error : can't connect to the server");
    window.location.href="index.html";
}
