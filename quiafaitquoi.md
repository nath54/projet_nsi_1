# Voici ce que chacun a fait

## Qui a fait quoi ?

### Nathan :

A initialisé le projet, a créé l'organisation du projet, les différentes classes principales,
A beaucoup travaillé sur l'interaction client-serveur, sur le client, sur la base de donnée,
sur le moteur du jeu.

### Hugo :

A travaillé sur la DB, ainsi que certaines commandes à entrer en jeu.
A aussi corrigé les textes, que ce soit docstring ou .json
Nettoyage de code pour essayer de les adapter aux normes Python. (un maximum)

### Alexis :

A imaginé et créé la fonction cheat_code, et a créé quasiment tous les lieux de la map

### Léa :

A fait la fonction python creation_perso dans le client principal python, et a créé beaucoup d'objets

## Auteurs des fonctions python

Nathan:
  - ./client_python/main_client.py -  test_email
  - ./client_python/main_client.py -  test_pseudo
  - ./client_python/main_client.py -  test_password
  - ./client_python/main_client.py -  is_json
  - ./client_python/main_client.py -  __init__
  - ./client_python/main_client.py -  debut
  - ./client_python/main_client.py -  attente_serv
  - ./client_python/main_client.py -  connexion
  - ./client_python/main_client.py -  inscription
  - ./client_python/main_client.py -  send
  - ./client_python/main_client.py -  start
  - ./client_python/main_client.py -  handle
  - ./client_python/main_client.py -  on_message
  - ./client_python/main_client.py -  on_close
  - ./client_python/main_client.py -  interface
  - ./client_python/main_client.py -  main
  - ./init_projet.py -  demande_install
  - ./init_projet.py -  main
  - ./server_python/client_db.py -  __init__
  - ./server_python/client_db.py -  test_version
  - ./server_python/client_db.py -  is_first_time
  - ./server_python/client_db.py -  create_table_comptes
  - ./server_python/client_db.py -  create_table_persos
  - ./server_python/client_db.py -  create_table_objets
  - ./server_python/client_db.py -  create_table_pnjs
  - ./server_python/client_db.py -  create_table_ennemis
  - ./server_python/client_db.py -  create_table_lieux
  - ./server_python/client_db.py -  create_table_genre
  - ./server_python/client_db.py -  create_table_version
  - ./server_python/client_db.py -  update
  - ./server_python/client_db.py -  test_connexion
  - ./server_python/client_db.py -  set_perso
  - ./server_python/client_db.py -  save_player
  - ./server_python/client_db.py -  get_perso
  - ./server_python/client_db.py -  get_lieux
  - ./server_python/client_db.py -  get_data_Lieu_DB
  - ./server_python/client_db.py -  get_data_Pnj_DB
  - ./server_python/Game/Etres/Combattant.py -  full_vie
  - ./server_python/Game/Etres/Combattant.py -  full_energie
  - ./server_python/Game/Etres/Combattant.py -  sum_lsts
  - ./server_python/Game/Etres/Combattant.py -  sous_lsts
  - ./server_python/Game/Etres/Combattant.py -  sum_lst_nb
  - ./server_python/Game/Etres/Combattant.py -  moy_lst
  - ./server_python/Game/Etres/Combattant.py -  get_attaque
  - ./server_python/Game/Etres/Combattant.py -  attaque_cible
  - ./server_python/Game/Etres/Ennemis/Ennemi.py -  __init__
  - ./server_python/Game/Etres/Ennemis/Ennemi.py -  tour
  - ./server_python/Game/Etres/Ennemis/Ennemi.py -  __repr__
  - ./server_python/Game/Etres/Perso.py -  test_dialogue
  - ./server_python/Game/Etres/Perso.py -  quete_finie
  - ./server_python/Game/Etres/Pnjs/Pnj.py -  load
  - ./server_python/Game/Game.py -  __init__
  - ./server_python/Game/Game.py -  start
  - ./server_python/Game/Map/Lieux/Lieu.py -  aff
  - ./server_python/Game/Map/Map.py -  load_from_bdd
  - ./server_python/Game/Map/Map.py -  load_from_json
  - ./server_python/Game/Map/Map.py -  create_lieu
  - ./server_python/libs.py -  jload
  - ./server_python/libs.py -  traiter_txt
  - ./server_python/libs.py -  is_one_of
  - ./server_python/main_server.py -  __init__
  - ./server_python/main_server.py -  start
  - ./server_python/main_server.py -  handle
  - ./server_python/main_server.py -  send_all_except_c
  - ./server_python/main_server.py -  send_all
  - ./server_python/main_server.py -  send
  - ./server_python/main_server.py -  on_accept
  - ./server_python/main_server.py -  on_message
  - ./server_python/main_server.py -  on_close
  - ./server_python/main_server.py -  fin_dialogue
  - ./server_python/main_server.py -  main
  - ./server_python/Player.py -  load_perso

Léa:
  - ./client_python/main_client.py -  test_nom
  - ./client_python/main_client.py -  creation_perso

Alexis:
  - ./server_python/cheat_code.py -  cheat_code

Hugo:
  - ./server_python/client_db.py -  create_table_quete
  - ./server_python/client_db.py -  inscription
  - ./server_python/client_db.py -  save_map
  - ./server_python/client_db.py -  get_data_quetes_DB
  - ./server_python/Game/Etres/Combattant.py -  soigne_PV
  - ./server_python/Game/Etres/Combattant.py -  soigne_EN
  - ./server_python/Game/Etres/Perso.py -  format_invent
  - ./server_python/Game/Etres/Perso.py -  format_equip
  - ./server_python/Game/Etres/Perso.py -  search_invent
  - ./server_python/Game/Etres/Perso.py -  consomme_item
  - ./server_python/Game/Etres/Perso.py -  add_to_invent
  - ./server_python/Game/Etres/Pnjs/Pnj.py -  __init__
  - ./server_python/Game/Objets/Objet.py -  __repr__
  - ./server_python/Game/Objets/Objet.py -  format_contenu
  - ./server_python/libs.py -  are_texts_equals
  - ./server_python/main_server.py -  invent_multi_args

Nathan, Hugo:
  - ./server_python/client_db.py -  init_database
  - ./server_python/client_db.py -  transfert_json_to_bdd
  - ./server_python/client_db.py -  get_data_Ennemi_DB
  - ./server_python/Game/Etres/Combattant.py -  __init__
  - ./server_python/Game/Etres/Combattant.py -  test_mort
  - ./server_python/Game/Etres/Combattant.py -  test_mort_cible
  - ./server_python/main_server.py -  commandes

Hugo, Nathan:
  - ./server_python/client_db.py -  test_compte_inscrit
  - ./server_python/client_db.py -  save_lieu
  - ./server_python/client_db.py -  get_data_obj_DB
  - ./server_python/client_db.py -  perso_death
  - ./server_python/Game/Etres/Perso.py -  __init__
  - ./server_python/Game/Etres/Perso.py -  format_stats
  - ./server_python/Game/Etres/Perso.py -  desequiper
  - ./server_python/Game/Etres/Perso.py -  equiper
  - ./server_python/Game/Etres/Perso.py -  on_death
  - ./server_python/Game/Objets/Objet.py -  __init__

Internet:
  - ./init_projet.py -  install

