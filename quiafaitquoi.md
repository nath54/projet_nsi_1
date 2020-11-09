

":
  - ./recense_auteurs.py -  examine

Nathan:
  - ./client_python/main_client.py -  __init__
  - ./client_python/main_client.py -  send
  - ./client_python/main_client.py -  start
  - ./client_python/main_client.py -  handle
  - ./client_python/main_client.py -  on_message
  - ./client_python/main_client.py -  on_close
  - ./client_python/main_client.py -  interface
  - ./client_python/main_client.py -  main
  - ./init_projet.py -  demande_install
  - ./init_projet.py -  main
  - ./server_python/Player.py -  load_perso
  - ./server_python/Game/Etres/Ennemis/Ennemi.py -  __init__
  - ./server_python/Game/Etres/Ennemis/Ennemi.py -  tour
  - ./server_python/Game/Etres/Ennemis/Ennemi.py -  __repr__
  - ./server_python/Game/Etres/Combattant.py -  full_vie
  - ./server_python/Game/Etres/Combattant.py -  full_energie
  - ./server_python/Game/Etres/Combattant.py -  sum_lsts
  - ./server_python/Game/Etres/Combattant.py -  sous_lsts
  - ./server_python/Game/Etres/Combattant.py -  sum_lst_nb
  - ./server_python/Game/Etres/Combattant.py -  moy_lst
  - ./server_python/Game/Etres/Pnjs/Pnj.py -  load
  - ./server_python/Game/Game.py -  __init__
  - ./server_python/Game/Game.py -  start
  - ./server_python/Game/Map/Lieux/Lieu.py -  aff
  - ./server_python/Game/Map/Map.py -  load_from_bdd
  - ./server_python/Game/Map/Map.py -  load_from_json
  - ./server_python/Game/Map/Map.py -  create_lieu
  - ./server_python/libs.py -  jload
  - ./server_python/libs.py -  traiter_txt
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
  - ./server_python/client_db.py -  update
  - ./server_python/client_db.py -  test_connexion
  - ./server_python/client_db.py -  set_perso
  - ./server_python/client_db.py -  get_perso
  - ./server_python/client_db.py -  get_lieux
  - ./server_python/client_db.py -  get_data_Lieu_DB
  - ./server_python/client_db.py -  get_data_Pnj_DB
  - ./server_python/main_server.py -  __init__
  - ./server_python/main_server.py -  start
  - ./server_python/main_server.py -  handle
  - ./server_python/main_server.py -  send_all_except_c
  - ./server_python/main_server.py -  send_all
  - ./server_python/main_server.py -  send
  - ./server_python/main_server.py -  on_accept
  - ./server_python/main_server.py -  on_message
  - ./server_python/main_server.py -  on_close
  - ./server_python/main_server.py -  main

Internet:
  - ./init_projet.py -  install

TODO:
  - ./server_python/Game/Quetes/Quete.py -  affichage
  - ./server_python/Game/Etres/Combattant.py -  debut_tour

Hugo, Nathan:
  - ./server_python/Game/Etres/Perso.py -  __init__
  - ./server_python/Game/Etres/Perso.py -  desequiper
  - ./server_python/Game/Etres/Perso.py -  equiper
  - ./server_python/Game/Objets/Objet.py -  __init__
  - ./server_python/client_db.py -  test_compte_inscrit
  - ./server_python/client_db.py -  get_data_obj_DB

Hugo:
  - ./server_python/Game/Etres/Perso.py -  format_invent
  - ./server_python/Game/Etres/Perso.py -  format_equip
  - ./server_python/Game/Etres/Perso.py -  format_stats
  - ./server_python/Game/Etres/Perso.py -  search_invent
  - ./server_python/Game/Etres/Perso.py -  consomme_item
  - ./server_python/Game/Etres/Perso.py -  add_to_invent
  - ./server_python/Game/Etres/Combattant.py -  soigne_PV
  - ./server_python/Game/Etres/Combattant.py -  soigne_EN
  - ./server_python/Game/Etres/Pnjs/Pnj.py -  __init__
  - ./server_python/Game/Map/Lieux/Lieu2.py -  __repr__
  - ./server_python/Game/Objets/Objet.py -  __repr__
  - ./server_python/Game/Objets/Objet.py -  format_contenu
  - ./server_python/libs.py -  are_texts_equals
  - ./server_python/client_db.py -  inscription
  - ./server_python/client_db.py -  save_map
  - ./server_python/client_db.py -  save_lieu
  - ./server_python/main_server.py -  invent_multi_args

Nathan, Hugo:
  - ./server_python/Game/Etres/Combattant.py -  __init__
  - ./server_python/client_db.py -  init_database
  - ./server_python/client_db.py -  transfert_json_to_bdd
  - ./server_python/client_db.py -  get_data_Ennemi_DB
  - ./server_python/main_server.py -  commandes

Alexis:
  - ./server_python/cheat_code.py -  cheat_code