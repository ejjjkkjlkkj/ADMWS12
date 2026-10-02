# ADMWS12 — Construction depuis zéro

Le dépôt est traité comme un terrain de construction. Nous ne prenons pas un
framework, un dataset, un moteur d'entraînement ou un outil externe comme
fondation du système.

## Ordre

0. Néant : aucun composant projet considéré comme acquis.
1. Atome : unité immuable, déterministe et adressée par son contenu.
2. Composants : assemblages d'atomes avec leurs propres invariants.
3. Outils : programmes ADMWS12 construits à partir des composants internes.
4. Chaînes : orchestration déterministe des outils.
5. Sous-systèmes : groupes de chaînes avec un contrat commun.
6. Système : intégration des sous-systèmes.
7. Modèle : apprentissage et inférence alimentés par le système.

Les sources externes pourront fournir de la matière à traiter plus tard. Elles
ne constituent pas le noyau et leur contenu n'est pas copié dans le noyau.

## Première primitive

src/zero/atom.py définit notre premier objet : l'atome. Il utilise uniquement
la bibliothèque standard Python et impose une représentation JSON canonique,
une identité SHA-256 calculée sur le contenu canonique, une provenance
obligatoire, une version et un type explicites, puis une vérification de
l'identité avant utilisation.

Cette couche ne dépend ni de l'UEFI, ni de PyTorch, ni de Transformers, ni
d'un outil de dataset externe. L'UEFI devient une matière d'entrée lorsque les
primitives de base sont suffisamment solides.
