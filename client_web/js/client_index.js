window.ip_ = null;
window.port_ = null;
window.websocket = null;

function main_client(txt){
    var ip=document.getElementById("inpip").value;
    var port=document.getElementById("inport").value;

    sessionStorage.setItem("ip",ip);
    sessionStorage.setItem("port",port);

    if(window.websocket == null || window.ip_ != ip  || window.port_ != port){
        var websocket = new WebSocket("ws://"+ip+":"+port+"/");
        window.websocket = websocket;
    }
    else{
        websocket = window.websocket;
    }
    window.ip_ = ip;
    window.port_ = port;
    
    websocket.onerror=cantconnect;
    
    var change = false;

    // Connection opened
    websocket.addEventListener('open', (event) => {
        websocket.send(txt);
    });

    websocket.onclose = function(){
        if(change){
            window.location.href="game.html";
        }
    }

    websocket.onmessage = function (event) {
        try {
            console.log("recu : ",event.data);
            data = JSON.parse(event.data);
            if(typeof data == "string"){
                data = JSON.parse(data);   
            }
        } catch (error) {
            return;
        }
        switch (data.type) {
            case "autorisation changement page":
                change=true;
                break;
            case "connection failed":
                alert("Connection failed : \n"+data.value);
                document.getElementById("alert_wait").style.display="none";
                break;
            case "connection successed":
                document.getElementById("alert_wait").style.display="none";
                websocket.send(JSON.stringify({"type":"veut changer de page"}))
                break;
            case "inscription failed":
                alert("Inscription failed : \n"+data.value);
                document.getElementById("alert_wait").style.display="none";
                break;
            case "inscription successed":
                document.getElementById("alert_wait").style.display="none";
                websocket.send(JSON.stringify({"type":"veut changer de page"}))
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
