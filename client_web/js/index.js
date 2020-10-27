
//variables globales utilisées dans ce programme
var password_view=false;
var inp_pass=[];
const chars=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z",
             "A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z",
            "1","2","3","4","5","6","7","8","9","0",
            "-","_","@","."];

//fonction appellée lorsque la page a fini de charger
function init(){
    //ici, on affiche la bonne div lors de l'arrivée de l'utilisateur sur la page d'acceuil
    there_are_cookies=false;
    if(there_are_cookies){
        //s'il y a des cookies, on suppose que l'utilisateur s'est déjà inscrit, on lui montre donc la page de connection
        document.getElementById("div_inscription").style.display="none";
    }
    else{
        //s'il n'y en a pas, on suppose que l'utilisateur est nouveau, on lui montre donc la page d'inscription
        document.getElementById("div_connection").style.display="none";
    }
    //ici, on récupère les inputs password
    inp_pass=[
        document.getElementById("c_password"),
        document.getElementById("i_password"),
        document.getElementById("i_confirm_password"),
    ];
    //
}


//fonction qui montre et qui cache les mots de passes
function toggle_password(){
    for(pi of inp_pass){
        if(password_view){
            pi.type="password";
        }else{
            pi.type="text";
        }
    }
    password_view=!password_view;
}

//fonction qui montre la page de connection
function show_connection(){
    document.getElementById("div_connection").style.display="initial";
    document.getElementById("div_inscription").style.display="none";
}


//fonction qui montre la page d'inscription'
function show_inscription(){
    document.getElementById("div_connection").style.display="none";
    document.getElementById("div_inscription").style.display="initial";
}

//function qui test si un pseudo est bon
function test_pseudo(txt="",ind=""){
    //
    console.log("psuedo changed");
    //
    var elt=null;
    var erreur=false;
    if(txt==""){
        elt=document.getElementById(ind)
        txt=elt.value;
    }
    //on fait les tests
    //le pseudo doit avoir une taille entre 4 et 12 charactere
    if(txt.length<4){
        erreur="Le pseudo doit avoir au minimum de 4 characteres !";
    }
    else if(txt.length>12){
        erreur="Le pseudo doit avoir au maximum 12 characteres !";
    }
    //Le pseudo doit etre constitué uniquement des characteres autorisés
    for(car of txt){
        if(!chars.includes(car)){
            erreur="Charactere non autorisé dans le pseudo '"+car+"' !"
        }
    }
    //on colorie l'élément en fonction des erreurs
    if(elt!=null){
        if(erreur==false){
            elt.setAttribute("class","ac_input good_input");
        }
        else{
            elt.setAttribute("class","ac_input false_input");
        }
    }
    //on ne renvoie pas d'erreur
    return erreur;
}

//function qui test si un email est bon
function test_email(txt="",ind=""){
    //
    console.log("email changed");
    //
    var elt=null;
    var erreur=false;
    if(txt==""){
        elt=document.getElementById(ind)
        txt=elt.value;
    }
    //on fait les tests

    var s1=txt.split("@");
    if(s1.length!=2){
        erreur="L'email doit être composé de deux parties séparés d'un @ !";
    }
    if(erreur==false && s1[1].split(".").length!=2){
        erreur="La partie de l'email située après le @ doit être composé lui-même de deux parties séparées par un point !";
    }

    //L'email doit etre constitué uniquement des characteres autorisés
    for(car of txt){
        if(!chars.includes(car)){
            erreur="Charactere non autorisé dans l'email : '"+car+"' !";
        }
    }
    //on colorie l'élément en fonction des erreurs
    if(elt!=null){
        if(erreur==false){
            elt.setAttribute("class","ac_input good_input");
        }
        else{
            elt.setAttribute("class","ac_input false_input");
        }
    }
    //on ne renvoie pas d'erreur
    return erreur;
}

//function qui test si un password est bon
function test_password(txt="",ind=""){
    //
    console.log("password changed");
    //
    var elt=null;
    var erreur=false;
    if(ind!=""){
        elt=document.getElementById(ind);
        txt=elt.value;
    }
    //on fait les tests

    //le password doit avoir une taille entre 4 et 12 charactere
    if(txt.length<8){
        erreur="Le password doit avoir au minimum de 8 characteres !";
    }
    else if(txt.length>32){
        erreur="Le password doit avoir au maximum 32 characteres !";
    }
    //Le password doit etre constitué uniquement des characteres autorisés
    for(car of txt){
        if(!chars.includes(car)){
            erreur="Charactere non autorisé dans le password '"+car+"' !"
        }
    }

    //on colorie l'élément en fonction des erreurs
    if(elt!=null){
        if(erreur==false){
            elt.setAttribute("class","ac_input good_input");
        }
        else{
            elt.setAttribute("class","ac_input false_input");
        }
    }
    //on renvoie l'erreur
    return erreur;
}

//fonction qui va recuperer les infos pour connecter l'utilisateur
//et va renvoyer quelques erreurs si certains champs sont mal remplis
function connection(){
    var pseudo=document.getElementById("c_pseudo").value;
    var password=document.getElementById("c_password").value;
    //on vérifie que les pseudos et les password ont la bonne syntaxe
    //pseudo
    var erreur=test_pseudo(pseudo);
    if(erreur!=false){
        alert(erreur);
        return ;
    }
    //password
    var erreur=test_password(password);
    if(erreur!=false){
        alert(erreur);
        return ;
    }
    //on peut enfin renvoyer les bonnes informations
    send_infos(
        {
            "type":"connection",
            "pseudo":pseudo,
            "password":password,
        }
    )
}

//fonction qui va recuperer les infos pour inscrire et connecter l'utilisateur
//et va renvoyer quelques erreurs si certains champs sont mal remplis
function inscription(){
    var pseudo=document.getElementById("i_pseudo").value;
    var email=document.getElementById("i_email").value;
    var password=document.getElementById("i_password").value;
    var password_confirm=document.getElementById("i_confirm_password").value;
    //on vérifie que les pseudos et les password ont la bonne syntaxe
    //pseudo
    var erreur=test_pseudo(pseudo);
    if(erreur!=false){
        alert(erreur);
        return ;
    }
    //passwords
    var erreur=test_password(password);
    if(erreur!=false){
        alert(erreur);
        return ;
    }
    //on vérifie que les mots de passes ne soient pas différents
    if(password!=password_confirm){
        alert("Les mots de passes sont différents !")
        return ;
    }
    //on peut enfin renvoyer les bonnes informations
    send_infos(
        {
            "type":"inscription",
            "pseudo":pseudo,
            "email":email,
            "password":password,
        }
    )
}

//fonction qui va envoyer toutes les infos au serveur
//après, d'autres infos seront renvoyées par le serveur,
//et ce sera le websocket qui s'en chargera

function send_infos(dicte){
    txt=JSON.stringify(dicte);
    main_client(txt);
}


