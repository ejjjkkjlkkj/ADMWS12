# ADMWS12 Factory

ADMWS12 est construit comme une chaîne de fabrication reproductible.

## Principe

Source externe -> référence -> acquisition autorisée -> normalisation -> validation -> déduplication -> SFT -> séparation des jeux -> entraînement -> évaluation -> benchmark.

Chaque étape doit produire un artefact identifiable et un journal. Les données brutes ne sont jamais modifiées en place.

## Zones

- `data/raw/` : données brutes autorisées, immuables.
- `data/processed/` : données normalisées et nettoyées.
- `data/sft/` : exemples prêts pour le fine-tuning.
- `data/metadata/` : provenance, versions, schémas et manifests.
- `src/` : code de transformation, entraînement, inférence et évaluation.
- `tests/` : contrôles automatiques.
- `scripts/` : outils reproductibles.
- `configs/` : paramètres versionnés.

## Règles de production

1. Une source possède un identifiant stable.
2. Toute transformation doit être déterministe autant que possible.
3. Les données brutes restent intactes.
4. Un exemple SFT doit avoir sa provenance.
5. Les doublons doivent être détectés avant séparation train/validation/test.
6. Aucun secret ne doit entrer dans le dataset ou le dépôt.
7. Une modification du pipeline doit être testée.
8. Un modèle ne devient une référence qu'après benchmark avant/après.

## UEFI

Pour UEFI 2.11 et PI 1.10, ADMWS12 conserve actuellement les métadonnées et des exemples rédigés indépendamment. Les spécifications intégrales ne sont pas recopiées dans le dépôt.
