# ADMWS12 — Domaines à construire

Le projet ne commence pas avec un modèle existant. Chaque domaine reçoit ses
propres primitives, contrats, tests et outils.

## Langage

Alphabet, texte canonique, segmentation, tokenizer, vocabulaire, représentations
et opérations linguistiques.

## Modèle de langage

Représentation, embeddings, attention ou mécanismes équivalents, blocs,
paramètres, initialisation, propagation, fonction de perte, optimisation,
checkpoint, inférence et runtime.

## Outils

CLI, inspection, conversion, validation, stockage, indexation, orchestration,
benchmark, journalisation et outils d'administration.

## Données

Atomes de données, provenance, formats canoniques, nettoyage, déduplication,
partitionnement, génération contrôlée et validation.

## Firmware

Représentation des structures firmware, volumes, fichiers, variables, interfaces,
boot flow, pilotes et outils de diagnostic. Les spécifications externes servent
de références techniques ; leurs implémentations ne sont pas copiées.

## Système

Mémoire, stockage, processus, IPC, réseau, sécurité, pilotes, accès matériel,
observabilité et gestion des erreurs.

## Hardware

Inventaire, capacités, mesure, benchmarks et interfaces nécessaires au système.
Le projet distingue ce que le logiciel contrôle de ce qui appartient réellement
au matériel.

## Accessibilité

Texte explicite, navigation clavier, sorties lisibles par lecteur d'écran,
messages déterministes et tests NVDA/JAWS/Narrator/Orca.

## Règle commune

Aucun domaine ne peut sauter directement au produit final. Il doit passer par
les niveaux atome -> composant -> outil -> chaîne -> sous-système.
