
//variables globales utilisées dans ce programme
var password_view=false;
var inp_pass=[];

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
