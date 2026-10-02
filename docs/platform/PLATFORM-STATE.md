# ADMWS12 Platform State Model

## Purpose

Define the authoritative state machine for the ADMWS12 platform layer.

## States

- EMPTY — no platform information is trusted.
- DISCOVERING — hardware and firmware capabilities are being discovered.
- DISCOVERED — discovery completed; no runtime ownership exists yet.
- INITIALIZING — mandatory platform resources are being initialized.
- READY — the platform contract is valid and runtime services may start.
- DEGRADED — runtime remains possible with one or more optional capabilities unavailable.
- FAILED — a mandatory invariant or initialization operation failed.
- STOPPING — runtime ownership is being released.
- STOPPED — platform resources are released.

## Allowed transitions

EMPTY -> DISCOVERING
DISCOVERING -> DISCOVERED
DISCOVERING -> FAILED
DISCOVERED -> INITIALIZING
INITIALIZING -> READY
INITIALIZING -> DEGRADED
INITIALIZING -> FAILED
READY -> DEGRADED
READY -> STOPPING
DEGRADED -> READY
DEGRADED -> STOPPING
STOPPING -> STOPPED

## Invariants

- State is owned by the platform layer.
- Higher layers cannot force an invalid transition.
- DEGRADED must identify which optional capabilities are unavailable or failed.
- FAILED must preserve enough diagnostic state to identify the failed invariant or operation.
- STOPPING must prevent new resource acquisition.
- STOPPED is terminal for that platform instance.

## Relationship with capabilities

Capability discovery populates the capability model. Platform state determines whether those capabilities are sufficient for the next lifecycle phase. A capability being unavailable is not itself a platform failure when it is optional.

## Implementation rule

Implement the state machine only after the capability representation and transition invariants have been specified and tested.
