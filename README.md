# ADMWS12

Projet de recherche et développement IA.

## Objectifs

- modèle spécialisé programmation
- cybersécurité
- réseau
- UEFI
- Windows
- Linux
- PowerShell
- accessibilité numérique
- NVDA
- JAWS
- Narrator
- Orca
- automatisation
- benchmark matériel

Le projet est développé directement sur la machine physique
afin d'exploiter au mieux les ressources CPU, GPU, RAM et stockage.

## Architecture

- src/model
- src/training
- src/inference
- src/evaluation
- data
- tests
- scripts
- configs
- .github/workflows

## Sources UEFI

ADMWS12 référence les spécifications UEFI par métadonnées et ne copie pas les PDF
dans le dépôt. La base UEFI suivie par le projet comprend :

- UEFI Specification 2.11
- UEFI Platform Initialization Specification 1.10

Les métadonnées sont dans `data/metadata/sources/` et la cartographie de travail
dans `data/metadata/uefi_2.11_mapping.json`.

Les documents UEFI Forum restent des sources externes. Le dépôt ne doit pas
incorporer leur contenu intégral sans droits de redistribution appropriés.

## Validation

- `python scripts/validate_json.py`
- `python -m pytest -q`

La validation automatique est définie dans `.github/workflows/validate.yml`.

## Licence

À définir.
