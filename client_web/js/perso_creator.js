
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
    "guerrier":"Un guerrier sait se battre au corps à corps, il est fort et il porte facilement tout type d'armure",
    "archer":"Un archer sait se battre à distance, et est plutôt agile",
    "prêtre":"Un prêtre excelle dans les sorts de soutiens, mais n'est pas très bon en attaque",
    "mage noir":"Un mage noir excelle dans la sorcellerie maudite, il peut invoquer des créatures ou controller des cadavres",
    "mage guerrier":"Un mage guerrier est équilibré dans les combats aux corps à corps et la maitrise des sorts de combats",
    "assassin":"Un assassin est habile et précis, il rate peu et esquive beaucoup, mais n'est pas très fort physiquement",
    "voleur":"Un voleur est habile et esquive beaucoup, il peut voler des pnjs et des ennemis",
    "paladin":"Un paladin est un guerrier qui connait des sorts de soutiens, il peut à la fois se battre et soigner ses alliés",
    "barbare":"Un barbare est un guerrier qui a vécu loin de la société civilisé, il se bat avec son instinct animal, et peut même devenir un berseker",
    "tank":"Un tank est un guerrier spécialisé dans la défense, il défend ses alliés et encaisse les gros dégats à leurs place, mais en contrepartie il ne fait pas beaucoup de dégats en attaque"
};

const classes = {
    "humain":"Les humains sont la race la plus présente sur la planete, ils sont équilibrés",
    "drakonien":"Les drakoniens sont des créatures mi-homme mi-dragon, ils ont une peau solide, et ont des facilités pour lancer des sorts de feu. Ils ont une apparence humaine en tant normal (même s'ils ont un bien meilleur physique que les humains ordinaires), mais ont une forme plus draconienne lors des combats",
    "elfe":"Les elfes sont les habitants de la forêt, ils ressemblent aux humains, mais ont des oreilles pointues, une peau plus verte pâle, et ont une bien meilleure longévité que les humains, ils ont des faiblesses contre le feu, mais sont plutôt habiles",
    "elfe noir":"Les elfes noirs sont des elfes qui sont tombés du côté obscur, ils ont une connaissance des sortileges maudits, n'ont pas de faiblesses contre le feu, mais contre des sortileges bénits",
    "demi-elfe":"Les demi-elfes sont des enfants d'homme et d'elfe",
    "orc":"Les orcs ne sont pas très intelligents et habiles, mais ils sont forts et résistants",
    "nain":"Les nains sont forts et résistants, peu habiles, mais ont des grands avantages dans les grottes et les montagnes",
    "fée":"Les fées sont des créatures magiques plutôt faibles physiquement, mais qui ont de gros bonus dans la magie"
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

function on_change_race(){
    document.getElementById("description_race").innerHTML=races[document.getElementById("select_race").value];
}

function on_change_classe(){
    document.getElementById("description_classe").innerHTML=classes[document.getElementById("select_classe").value];
}

function send_perso(){
    var nom = document.getElementById("i_nom").value;
    var genre = document.getElementById("select_genre").value;
    var race = document.getElementById("select_race").value;
    var classe = document.getElementById("select_classe").value;
    //
    var jt = JSON.stringify({"type":"data_creation_perso","nom":nom,"genre":genre,"race":race,"classe":classe})
    websocket.send(jt);
    //
    document.getElementById("div_creation_perso").style.display = "none";
}

