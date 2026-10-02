# ADMWS12 — Fondation page blanche

## Règle fondamentale

ADMWS12 est conçu à partir d'une page blanche.

Aucun logiciel, protocole, algorithme, format, architecture ou implémentation existant n'est notre conception par défaut.

Les technologies existantes peuvent uniquement être utilisées comme :
- références techniques ;
- contraintes de compatibilité explicitement choisies ;
- objets de comparaison ;
- sources d'inspiration documentées.

Une référence externe ne doit jamais être présentée comme une création ADMWS12.

## Ordre de construction

1. Objectifs et limites.
2. Modèle conceptuel.
3. Architecture.
4. Spécifications.
5. Invariants et propriétés attendues.
6. Prototype minimal.
7. Implémentation de référence.
8. Tests.
9. Analyse de sécurité.
10. Optimisation.
11. Compatibilité et intégration.
12. Validation finale.

## Principe de séparation

La recherche, les prototypes, les données, les spécifications et le code de production sont séparés.

Aucun prototype expérimental ne devient automatiquement une implémentation de production.

## Cryptographie

Toute nouvelle primitive cryptographique doit disposer de sa propre spécification, de ses hypothèses de sécurité, de vecteurs de test, d'une implémentation de référence et d'une procédure de validation.

Une comparaison avec ML-DSA/Dilithium ne constitue pas une dérivation de l'algorithme ADMWS12.

## UEFI et firmware

Les spécifications existantes peuvent être étudiées pour comprendre les contraintes d'interopérabilité. Toute nouvelle couche ADMWS12 doit être spécifiée séparément avant son implémentation.

## Données

Les données d'inventaire sont traitées comme des sources d'observation. Le schéma ADMWS12 est défini indépendamment des sorties brutes des outils utilisés pour les collecter.

## Règle de qualité

Aucun composant n'est déclaré « meilleur » qu'une technologie existante sans critères mesurables, tests reproductibles et validation indépendante.
