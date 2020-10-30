

//fonction qui ajoute du texte
function aff_message(txt = "", color = "white", text_on_click = null, elts_speciaux = []){
    console.log("eeeeeeeee   elts spéciaux : ", elts_speciaux,"   txt : '",txt,"'");
    var div=document.createElement("div");
    div.setAttribute("class","mes")
    //on crée l'element
    if(text_on_click!=null){
        var p = document.createElement("pre");
        p.innerHTML=txt;
        p.style.color=color;
        var s = document.createElement("span");
        s.appendChild(p);
        s.setAttribute("onclick",'text_click("'+text_on_click+'");');
        //on l'ajoute
        div.appendChild(s);
    }
    else{
        var p = document.createElement("p");
        p.innerHTML=txt;
        p.style.color=color;
        //on l'ajoute
        div.appendChild(p);
    }
    for(el of elts_speciaux){
        console.log(el);
        div.appendChild(el);
    }
    document.getElementById("mm").appendChild(div);
    document.getElementById("messages").scrollTop = document.getElementById("messages").scrollHeight;
}

function init(){
}

function text_click(text){
    document.getElementById("input").value+=" "+text;
}

function create_text(txts){
    var p = document.createElement("p");
    for(t of txts){
        var s = document.createElement("span");
        s.innerHTML = t[0];
        s.style.color = t[1];
    }
    return p;
}

function colorie_commande(txt){
    elts_s = [];
    t = txt.split(" ");
    if(t.length>0){
        switch (t[0]){
            case "inventaire":
                var nl = [];
                for(x=1; x<t.length; x++){
                    nl.push(t[x]);
                }
                var p = create_text([[t[0],"red"],[nl.join(" "),"blue"]]);
                elts_s.push(p);
                break;
    
            case "commande suivante":
                break;
    
            case "commande suivante":
                break;
    
            case "commande suivante":
                break;
    
            case "commande suivante":
                break;
    
            case "commande suivante":
                break;
    
            case "commande suivante":
                break;
    
            case "commande suivante":
                break;
    
            default:
                var p = document.createElement("p");
                p.innerHTML = txt;
                p.style.color = "blue";
                elts_s.push(p);
        }
    }
    
    return elts_s;
}

function sende(){
    var texte = document.getElementById("input").value;
    var j = {"type":"text","value":texte};
    var jt = JSON.stringify(j);
    websocket.send(jt);
    document.getElementById("input").value = "";
    elts_s = colorie_commande(texte);
    if(elts_s.length==0){
        aff_message(txt = "> "+texte, color = "white");
    }
    else{
        aff_message(txt = "> ", color = "white" , elts_speciaux = elts_s);
    }
}

function checkEnter(e) {
    if(e && e.keyCode == 13) {
        sende();
    }
}

