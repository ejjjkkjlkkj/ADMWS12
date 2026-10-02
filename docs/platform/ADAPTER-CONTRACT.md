# ADMWS12 Platform Adapter Contract

## Purpose

Define the boundary between hardware-specific observation and the hardware-independent ADMWS12 platform model.

## Adapter responsibility

A platform adapter may:

- observe hardware and firmware through platform-specific mechanisms;
- translate observations into ADMWS12 capability states;
- return a capability snapshot through the CapabilitySource contract.

An adapter must not:

- expose vendor, product, serial, MAC, GUID, PCI address, firmware identifier, or operating-system object as a core capability name;
- make initialization decisions for the core;
- silently convert an unknown observation into AVAILABLE;
- require a higher layer to understand its hardware-specific representation.

## Data flow

Hardware observation -> adapter evidence -> capability translation -> CapabilitySource -> DiscoveryResult -> PlatformContext -> initialization policy.

The core consumes the translated capability model. Hardware-specific evidence remains at the adapter boundary.

## Lifecycle

The adapter participates in discovery only. PlatformContext owns lifecycle transitions. Initialization evaluates mandatory and optional capability policy separately.

## Failure semantics

A capability whose observation was attempted but failed is FAILED. A known absent capability is UNAVAILABLE. A capability that exists but cannot be used by the current implementation is UNSUPPORTED. An unobserved capability remains UNKNOWN.

## Reference status

No hardware-specific adapter is implemented yet. The first adapter will target the observed x86-64/UEFI platform only after this contract is validated by tests.
