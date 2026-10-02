# ADMWS12 Platform Discovery Model

## Lifecycle integration

The platform context owns the lifecycle boundary for discovery.

1. EMPTY contains no trusted platform snapshot.
2. begin_discovery() moves the context to DISCOVERING.
3. complete_discovery(source) validates one discovery result, stores its immutable capability snapshot, and moves the context to DISCOVERED.
4. Initialization remains a separate transition and is not implied by discovery.

## Contract

A discovery source exposes discover() and returns explicit capability states with non-empty, unique capability names.

The core does not require vendor, product, serial, MAC, PCI, firmware identifiers, or an operating-system API.

## Separation

The reference StaticCapabilitySource exists only for tests and prototypes. It does not represent hardware access.

Hardware-specific observation remains outside the core. The future x86-64/UEFI adapter must implement the same discovery contract without changing the capability model.

## Invariants

- Discovery cannot start from an invalid lifecycle state.
- Invalid discovery data is rejected before the context reaches DISCOVERED.
- Discovery does not imply initialization or capability usability.
- Hardware identifiers are adapter evidence, not core capability names.

## Current status

The discovery contract, context integration, and reference tests exist. No hardware adapter is implemented.
