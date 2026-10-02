# ADMWS12 — Chain layer

The chain layer composes verified tools into deterministic ordered operations.

Construction:

Néant -> atome -> composant -> outil -> chaîne.

A chain stores tool identities, not copied implementations. Changing the tool
sequence or the execution policy changes the chain identity.

The chain layer is deliberately small. Scheduling, storage, process execution,
networking and model operations belong to later subsystems rather than being
hidden inside the primitive.

External software is not a chain dependency. External standards can be used as
reference material when an ADMWS12 chain must implement an external interface.

The next layer is subsystem: coherent groups of chains with explicit
responsibilities and boundaries.
