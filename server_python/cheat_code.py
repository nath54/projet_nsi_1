
import random

def cheat_code(server, client, commande):
    """Fonction pour rajouter quelques petits checkcodes dans le jeu :)

    retourne True si une action a été faite, sinon retourne False

    Author : Alexis
    """
    action_faite = False
    perso = server.clients[client]["player"].perso
    if commande == "sonto":
        # game.pnj (le pére noel donne un cadeau)
        pass
    if commande == "docteur":
        # game.objets (du soin)
        pass
    if commande == "666":
        print ("vous avez passer un pacte avec le diable")
        pass
        # game.objets
    if commande == "Excalibur":
        pass
        # game.objets (une épée)
    if commande == "Merlin":
        pass
        # game.objets (une baguette)
    if commande == "Trump":
        possibilites = ["chance", "neutre", "malchance"]
        choix = random.choice(possibilites)
        if choix == "chance":
            server.send(client, json.dumps({"type": "message", "value": "Trump est arrivé avec son jetpack privé et vous a donné un petit million de pièces d'or et repart avec son jet privé en vous faisant coucou de la main :)"}))
            perso.argent += 10000000
        elif choix == "neutre":
            server.send(client, json.dumps({"type": "message", "value": "Trump vous envoie un tweet en vous disant que vous êtes une fake news, vous perdez un point de vie a cause de votre égo surdimensioné qui a été sérieusement touché :|"}))
            perso.vie -= 1
        elif choix == "malchance":
            server.send(client, json.dumps({"type": "message", "value": "Trump a gagné les élections et met en place une loi pour vous foutre une amende de 1000000 de pieces d'or, vous perdez donc 1000000 de pieces d'or"}))
            perso.argent -= 10000000
        action_faite = True
    if commande == "brevis":
        server.send(client, json.dumps({"type": "message", "value": "Une brevis volante apparaît du ciel et vous annonce une très mauvaise nouvelle : `Je suis désolée, mais je vous enlève un point à la note de votre projet, vous n'aurez pas 21/20, mais 20/20, c'est vraiment dommage !`"}))
        action_faite = True
    # ...
    else:
        print("non mais ca va pas, ce n'est pas bien de tricher")
    
    return action_faite