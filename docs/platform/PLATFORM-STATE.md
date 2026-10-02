# ADMWS12 Platform State Model

## Purpose

Define the authoritative lifecycle and the capability sufficiency rules for the ADMWS12 platform layer.

## States

- EMPTY — no platform information is trusted.
- DISCOVERING — platform capabilities are being observed.
- DISCOVERED — discovery completed; no runtime ownership exists yet.
- INITIALIZING — mandatory platform resources are being validated and initialized.
- READY — all declared mandatory capabilities are available.
- DEGRADED — mandatory capabilities are available, but one or more declared optional capabilities are unavailable, unsupported, unknown, or failed.
- FAILED — a mandatory capability or lifecycle invariant failed.
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

## Initialization contract

Initialization receives two explicit sets of capability names:

- mandatory: every named capability must be AVAILABLE;
- optional: an unavailable, unsupported, unknown, or failed named capability produces DEGRADED rather than FAILED.

A capability name cannot occur in both sets. Duplicate names are rejected.

Missing mandatory capabilities cause FAILED and preserve a diagnostic reason. Degraded capability names are preserved in the platform context.

Initialization does not discover hardware. Discovery must already have reached DISCOVERED.

## Invariants

- State is owned by the platform layer.
- Higher layers cannot force an invalid transition.
- DEGRADED identifies the optional capabilities that are not usable.
- FAILED preserves a diagnostic reason for the failed invariant or mandatory capability.
- STOPPING prevents new resource acquisition.
- STOPPED is terminal for that platform instance.
- Discovery and initialization remain separate operations.

## Relationship with capabilities

Capability discovery populates the capability model. Initialization evaluates that snapshot against an explicit mandatory/optional policy. Capability state is never inferred from a device identifier.

## Current status

Lifecycle, discovery integration, and initialization policy are implemented at the core-model level. No hardware adapter or device driver is implemented.
