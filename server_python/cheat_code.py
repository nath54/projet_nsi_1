import random
import json


def cheat_code(server, client, commande):
    """Rajoute quelques petits cheat-codes dans le jeu :)
    Pour faire un cheat code, il faut taper "\cheat nom du cheat"

    Returns:
        bool: True --> Une action a été faite
              False --> Aucune action effectuée

    Auteur: Alexis

    """
    action_faite = False
    perso = server.clients[client]["player"].perso
    if perso is None:
        return
    if commande == "sonto":
        # game.pnj (le père noel donne un cadeau)
        pass
    elif commande == "docteur":
        # game.objets (du soin)
        pass
    elif commande == "666":
        server.send(client, json.dumps({"type": "message", "value": "Vous avez passé un pacte avec le Diable. Cependant, la flemme des développeurs fait que cela ne change rien à votre vie. Soyez heureux !"}))
        pass
        # game.objets
    elif commande == "Excalibur":
        pass
        # game.objets (une épée)
    elif commande == "Merlin":
        pass
        # game.objets (une baguette)
    elif commande == "Trump":
        possibilites = ["chance", "neutre", "malchance"]
        choix = random.choice(possibilites)
        if choix == "chance":
            server.send(client, json.dumps({"type": "message", "value": "Trump est arrivé avec son jetpack privé et vous a donné un petit million de pièces d'or et repart avec son jetpack privé en vous faisant coucou de la main :)"}))
            perso.argent += 10000000
        elif choix == "neutre":
            server.send(client, json.dumps({"type": "message", "value": "Trump vous envoie un tweet en vous disant que vous êtes une fake news, vous perdez un point de vie a cause de votre égo surdimensioné qui a été sérieusement touché :|"}))
            perso.vie -= 1
        elif choix == "malchance":
            server.send(client, json.dumps({"type": "message", "value": "Trump a gagné les élections et met en place une loi pour vous foutre une amende de 1000000 de pieces d'or, vous perdez donc 1000000 de pieces d'or"}))
            perso.argent -= 10000000
        action_faite = True
    elif commande == "brevis":
        server.send(client, json.dumps({"type": "message", "value": "Une brevis volante apparaît du ciel et vous annonce une très mauvaise nouvelle : `Je suis désolée, mais je vous enlève un point à la note de votre projet, vous n'aurez pas 21/20, mais 20/20, c'est vraiment dommage !`"}))
        action_faite = True
    elif commande == "tuto":
        perso.lieu = 50
        server.send(client, {"type": "message", "value": f"{server.game.map_.lieux[perso.lieu].aff(perso)}"})
    elif commande == "game":
        perso.lieu = 0
        server.send(client, {"type": "message", "value": f"{server.game.map_.lieux[perso.lieu].aff(perso)}"})
    elif commande == "suicide":
        perso.vie = 0
        server.send(client, {"type": "message", "value": "Vous avez pris le premier gun qui arrivait et bam, dans la tête, one shot, etc..."}, True)
        perso.on_death()
    # ...
    else:
        server.send(client, json.dumps({"type": "message", "value": "non mais ca va pas, ce n'est pas bien de tricher"}))
    return action_faite
