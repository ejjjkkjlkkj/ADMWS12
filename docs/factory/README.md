# ADMWS12 — Construction aval

Ce dossier décrit une couche de production située après les primitives. Il ne
constitue pas la fondation du projet.

## Architecture de construction

Néant -> atome -> composants -> outils -> chaînes -> sous-systèmes -> système -> modèle.

Le modèle de langage, les outils, le firmware, les systèmes de données et les
moteurs d'exécution seront construits progressivement à partir de composants
ADMWS12 vérifiés.

Les sources externes peuvent apporter de la matière à étudier ou à transformer,
mais elles ne deviennent jamais automatiquement une fondation copiée dans le
projet.

## Production aval

- données : acquisition autorisée, normalisation, validation et provenance ;
- entraînement : préparation, apprentissage et reprise déterministe ;
- évaluation : jeux indépendants, mesures et régressions ;
- outils : exécutables construits sur les primitives internes ;
- firmware : composants et mécanismes étudiés puis implémentés séparément ;
- modèle de langage : architecture, tokenizer, entraînement et runtime construits
  comme sous-systèmes distincts.

Les données brutes restent intactes. Toute transformation doit être traçable et
déterministe autant que possible.
