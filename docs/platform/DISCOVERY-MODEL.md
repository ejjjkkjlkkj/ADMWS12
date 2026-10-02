# ADMWS12 Platform Discovery Model

Discovery observes capabilities without embedding hardware or firmware identity into the core.

## Contract

A source exposes `discover()` and returns explicit capability states with non-empty, unique capability names. The core does not require vendor, product, serial, MAC, PCI, firmware identifiers, or an operating-system API.

## Snapshot

A discovery pass produces an immutable tuple. A later pass may produce a different snapshot when platform state changes.

## Separation

Discovery is separated from hardware observation, capability interpretation, initialization, and runtime service use. The first hardware adapter will implement this contract later and remain outside the core capability model.

## Invariants

- Empty names are invalid.
- Duplicate names are invalid.
- Capability states remain distinct.
- Discovery does not imply initialization or usability.
- Hardware identifiers are adapter evidence, not core capability names.

## Current status

Contract and reference validation exist. No x86-64/UEFI adapter is implemented.
