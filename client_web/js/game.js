
debug = true; 

//fonction qui ajoute du texte
function aff_message(txt , color, text_on_click, elts_speciaux){
    var div=document.createElement("div");
    div.setAttribute("class","mes")
    //on crée l'element
    var p = document.createElement("pre");
    p.innerHTML=txt;
    p.style.color=color;
    //on l'ajoute
    div.appendChild(p);
    if(elts_speciaux!=null){
        for(el of elts_speciaux){
            div.appendChild(el);
        }
    }
    if(text_on_click!=null){
        div.setAttribute("onclick",'text_click("'+text_on_click+'");');
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
    var p = document.createElement("span");
    p.setAttribute("class","txt_commande")
    for(t of txts){
        var s = document.createElement("pre");
        s.innerHTML = t[0];
        s.style.color = t[1];
        p.appendChild(s);
    }
    return p;
}

function colorie_commande(txt){
    elts_s = [];
    t = txt.split(" ");
    if(t.length>0){
        switch (t[0]){
            //commandes à 0 arguments
            case "inventaire":
            case "equipement":
            case "attendre":
            case "voir":
                var nl = [];
                for(x=1; x<t.length; x++){
                    nl.push(t[x]);
                }
                var p = create_text([[t[0],"red"],[" "+nl.join(" "),"blue"]]);
                elts_s.push(p);
                break;
            
            //commandes à 1 arguments sur
            case "desequiper":
            case "equiper":
            case "examiner":
            case "fouiller":
            case "prendre":
            case "jeter":
            case "consommer":
            case "ouvrir":
            case "fermer":
            case "aller":
            case "parler":
            case "attaquer":
                if(t.length>=2){
                    var nl = [];
                    for(x=2; x<t.length; x++){
                        nl.push(t[x]);
                    }
                    var p = create_text([[t[0],"red"],[" "+t[1],"yellow"],[" "+nl.join(" "),"blue"]]);
                    elts_s.push(p);
                    break;
                }
            
            //commandes à 2 arguments sur
            case "mettre":
            case "sortilege":
                if(t.length>=3){
                    var nl = [];
                    for(x=3; x<t.length; x++){
                        nl.push(t[x]);
                    }
                    var p = create_text([[t[0],"red"],[" "+t[1],"yellow"],[" "+t[2],"yellow"],[" "+nl.join(" "),"blue"]]);
                    elts_s.push(p);
                    break;
                }

            //commandes à 3 arguments sur
            case "commande à 3 arguments":
                if(t.length>=4){
                    var nl = [];
                    for(x=4; x<t.length; x++){
                        nl.push(t[x]);
                    }
                    var p = create_text([[t[0],"red"],[" "+t[1],"yellow"],[" "+t[2],"yellow"],[" "+t[3],"yellow"],[" "+nl.join(" "),"blue"]]);
                    elts_s.push(p);
                    break;
                }

            //commandes à n arguments sur
            case "commande avec tout comme arguments":
                var nl = [];
                for(x=1; x<t.length; x++){
                    nl.push(t[x]);
                }
                var p = create_text([[t[0],"red"],[" "+nl.join(" "),"yellow"]]);
                elts_s.push(p);
                break;
            
            //Des commandes à nombre d'arguments multiples ici :
            
            //quand il y a rien
            default:
                var p = document.createElement("pre");
                p.innerHTML = txt;
                p.style.color = "blue";
                elts_s.push(p);
        }
    }
    
    return elts_s;
}

function commandes_client(txt){
    t = txt.split(" ");
    if(t.length>0){
        switch (t[0]){
            case "clear":
                var mm=document.getElementById("mm");
                for(child of mm.children){
                    mm.removeChild(child)
                }
                mm.children = [];
                mm.innerHTML = "";
                return false;
            case "perso_creator":
                perso_creator();
            default:
                break;
        }
    }
    return true;
}

function sende(){
    var texte = document.getElementById("input").value;
    var ts = texte.split(" ")
    var j = {"type": "none"};
    if(ts.length >= 1){
        var com = ts[0];
        var args = "";
        for(x=1; x<ts.length; x++){
            args += ts[x];
            if(x < ts.length-1){
                args += " ";
            }
        }
        j = {"type":"commande","commande":com, "arguments": args};
    }
    else{
        j = {"type":"text","value":texte};
    }
    var jt = JSON.stringify(j);
    websocket.send(jt);
    if(commandes_client(texte)){
        elts_s = colorie_commande(texte);
        if(elts_s.length==0){
            aff_message("> "+texte, "white", texte, null);
        }
        else{
            aff_message("> ", "white" , texte , elts_s);
        }
    }
    document.getElementById("input").value = "";
}

function checkEnter(e) {
    if(e && e.keyCode == 13) {
        sende();
    }
}

