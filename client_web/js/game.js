

//fonction qui ajoute du texte 
function aff_message(txt,color="white"){
    //on crée l'element
    var p = document.createElement("pre");
    p.innerHTML=txt;
    p.setAttribute("class","mes")
    p.style.color=color;
    //on l'ajoute 
    document.getElementById("mm").appendChild(p);
    document.getElementById("messages").scrollTop = document.getElementById("messages").scrollHeight;
}



function init(){
}











