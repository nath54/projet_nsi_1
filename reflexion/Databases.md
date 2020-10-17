Ce ne sont que des pistes qu'on pourra creuser évidemment, juste pour un peu mettre en forme

# Différentes tables :
- Lieux(id INT, name TEXT, lieux TEXT, objets TEXT, ennemis TEXT, pnj TEXT, joueur TEXT)
`lieux`, `objets`, `ennemis`, `pnj` et `joueur` seront composé de l'id du premier élément, d'un séparateur, id du 2ème, etc... Histoire de permettre le split en python
- Objets(id INT, name TEXT, description TEXT)
Possiblement créer de quoi stocker l'effet de l'objet
- Ennemis(id INT, name TEXT, description TEXT, atk INT, def INT, loot TEXT)
Stocker toutes les caractéristiques. `loot` de la forme "id1|\$|id2". On peut imaginer rajouter "|$|id3:50" Pour dire que la probabilité d'obtenir l'objet d'ID id3 est de 50%
- PNJ(id INT, name TEXT, description TEXT, dialogue TEXT)
`dialogue` permettra de stocker le dialogue qu'on peut avoir avec ce PNJ
- Joueur(id INT, name TEXT, toutes les caracs...)
