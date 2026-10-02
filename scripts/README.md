# Scripts ADMWS12

## Pipeline d'inventaire

1. Les sources restent dans `research/platform-inventory/`.
2. `clean_inventory.py` nettoie et normalise les fichiers TXT.
3. La sortie est écrite dans `data/normalized/` au format JSONL.
4. `validate_inventory.py` contrôle JSON, enregistrements vides, doublons et identifiants sensibles.
5. Les sources brutes ne sont jamais supprimées automatiquement.

### Exécution

Depuis la racine du dépôt :

    python scripts/clean_inventory.py

Puis :

    python scripts/validate_inventory.py

### Principe de conservation

Conserver ce qui décrit réellement la plateforme : matériel, firmware, stockage, réseau matériel, sécurité, virtualisation, système et topologie.

Écarter par défaut les identifiants propres à une machine : GUID, UUID, numéro de série, identifiant PnP, MAC, DeviceID et identifiants CIM internes.

Toute suppression définitive des données brutes doit être faite après validation du jeu normalisé.
