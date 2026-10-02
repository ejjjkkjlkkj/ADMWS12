# ADMWS12 — Architecture initiale

Ce document définit les frontières initiales du projet sans imposer d'implémentation existante.

## Couches

### 1. Foundation
Modèles fondamentaux, types, invariants et conventions communes.

### 2. Platform
Abstraction matérielle et description de la plateforme.

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

## Direction des dépendances

Foundation
→ Platform / Firmware / Security / Data / Accessibility
→ Tools et applications

Les couches basses ne dépendent pas d'applications particulières.

## État actuel

Cette architecture est une spécification de départ. Elle ne prétend pas que les composants sont déjà implémentés.

Chaque composant devra passer de :
SPECIFICATION → PROTOTYPE → REFERENCE → VALIDATION → PRODUCTION.
