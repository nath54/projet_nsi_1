

//fonction qui ajoute du texte
function aff_message(txt,color="white",text_on_click=null){
    //on crée l'element
    if(text_on_click!=null){
        var p = document.createElement("pre");
        p.innerHTML=txt;
        p.setAttribute("class","mes")
        p.style.color=color;
        var s = document.createElement("span");
        s.appendChild(p);
        s.setAttribute("onclick",'text_click("'+text_on_click+'");');
        //on l'ajoute
        document.getElementById("mm").appendChild(s);
    }
    else{
        var p = document.createElement("pre");
        p.innerHTML=txt;
        p.setAttribute("class","mes")
        p.style.color=color;
        //on l'ajoute
        document.getElementById("mm").appendChild(p);
    }
    document.getElementById("messages").scrollTop = document.getElementById("messages").scrollHeight;
}

function init(){
    aff_message("click",color="blue",text_on_click="This is blue !")
    aff_message("click",color="white",text_on_click="This is white !")
    aff_message("click",color="red",text_on_click="This is red !")
}

function text_click(text){
    document.getElementById("input").value+=" "+text;
}

function sende(){
    var texte=document.getElementById("input").value;
    var j={"type":"text","value":texte};
    var jt=JSON.stringify(j);
    websocket.send(jt);
}

