# ADMWS12 — Architecture initiale

Ce document définit les frontières initiales du projet sans imposer d'implémentation existante.

## Couches

### 1. Foundation
Modèles fondamentaux, types, invariants et conventions communes.

### 2. Platform
Abstraction matérielle et description de la plateforme. Le modèle de capacités, le modèle de démarrage et l'état de plateforme sont définis dans `docs/platform/`.

### 3. Firmware
Interfaces de démarrage, firmware et sécurité de plateforme.

### 4. Security
Modèle de confiance, politiques, isolation et vérification.

### 5. Cryptography
Primitives et protocoles cryptographiques conçus et spécifiés dans ADMWS12.

### 6. Data
Collecte, normalisation, validation et représentation des données.

### 7. Accessibility
Interfaces et représentation accessibles, notamment pour les lecteurs d'écran.

### 8. Tools
Outils de génération, analyse, validation et expérimentation.

## Contrats Platform

- `CAPABILITY-MODEL.md` définit les capacités observables et leurs états.
- `BOOT-MODEL.md` définit les phases de démarrage et le contrat de handoff.
- `PLATFORM-STATE.md` définit la machine d'état du cycle de vie de la plateforme.
- `HAL.md` définit la frontière entre matériel, adaptateurs et cœur ADMWS12.

Ces documents sont complémentaires : les capacités décrivent ce qui est disponible, le boot décrit comment le contrôle arrive au cœur, et l'état décrit le cycle de vie de la plateforme.

## Direction des dépendances

Foundation
→ Platform / Firmware / Security / Data / Accessibility
→ Tools et applications

Les couches basses ne dépendent pas d'applications particulières.

## État actuel

Cette architecture est une spécification de départ. Elle ne prétend pas que les composants sont déjà implémentés.

Chaque composant devra passer de :
SPECIFICATION → PROTOTYPE → REFERENCE → VALIDATION → PRODUCTION.
