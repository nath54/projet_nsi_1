
function main_client(txt){
    var ip=document.getElementById("inpip").value;
    var port=document.getElementById("inport").value;

    var websocket = new WebSocket("ws://"+ip+":"+port+"/");
    websocket.onerror=cantconnect;
    console.log(websocket);

    // Connection opened
    websocket.addEventListener('open', (event) => {
        websocket.send(txt);
    });

    websocket.onmessage = function (event) {
        data = JSON.parse(event.data);
        switch (data.type) {
            case 'connection failed':
                alert("Connection failed : \n"+data.error);
                document.getElementById("alert_wait").style.display="none";
                break;
            case 'connection successed':
                document.getElementById("alert_wait").style.display="none";
                sessionStorage.setItem("websocket",websocket)
                window.location.href="game.html";
                break;
            case 'inscription failed':
                alert("Inscription failed : \n"+data.error);
                document.getElementById("alert_wait").style.display="none";
                break;
            case 'inscription successed':
                    document.getElementById("alert_wait").style.display="none";
                    sessionStorage.setItem("websocket",websocket)
                    window.location.href="game.html";
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
    }

    function youarenotconnected(){
        alert("Error : You are not connected !");
    }

}
