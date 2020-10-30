
const genres = [
    "homme",
    "femme",
    "agenre",
    "androgyne",
    "bigender",
    "non-binaire",
    "autre"
];

const races = {
    "guerrier":"Un guerrier sait se battre ",
    "archer":"",
    "mage blanc":"",
    "mage noir":"",
    "mage guerrier":"",
    "assassin":"",
    "voleur":"",
    "paladin":"",
    "barbare":"",
    "tank":""
};

const classes = {
    "humain":"",
    "drakonien":"",
    "elfe":"",
    "elfe noir":"",
    "orc":"",
    "nain":"",
    "demi-elfe":"",
    "fée":""
};




function perso_creator(){
    document.getElementById("div_creation_perso").style.display = "initial";
    //genres
    for(e of getComputedStyle){
        var o = document.createElement("option");
        o.innerHTML = e;
        document.getElementById("select_genre").appendChild(o)
    }
    //races
    for(e of Object.keys(races)){
        var o = document.createElement("option");
        o.innerHTML = e;
        document.getElementById("select_race").appendChild(o)
    }
    //classes
    for(e of Object.keys(classes)){
        var o = document.createElement("option");
        o.innerHTML = e;
        document.getElementById("select_classe").appendChild(o)
    }
}

function send_perso(){

}






