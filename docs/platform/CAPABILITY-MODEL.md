# ADMWS12 Platform Capability Model

## Purpose

This document defines the ADMWS12 capability model from a blank slate. It is an internal contract between hardware discovery, the HAL, the core, and higher services.

## Principles

- A capability is an observable platform property, not a device name.
- Discovery precedes use.
- Optional capabilities have an explicit absent state.
- Core interfaces must not depend on vendor or model identifiers.
- Capability values must come from runtime evidence or a validated platform profile.
- Unsupported, unavailable, and failed are distinct states.

## Capability classes

### Execution
- architecture
- execution width
- processor topology
- supported execution modes

### Memory
- physical capacity
- usable capacity
- allocation granularity
- memory protection capabilities

### Time
- monotonic time source
- timer resolution
- timer availability

### Events
- interrupt/event delivery
- event routing
- synchronization primitives exposed by the platform layer

### Fabric
- PCI/PCIe discovery
- bus topology
- device capability discovery

### Storage
- persistent storage discovery
- block size
- capacity
- read/write capability
- durability state

### Firmware and boot
- firmware mode
- boot services availability
- boot target information
- secure-boot state when detectable

### Network
- interface discovery
- link capabilities
- packet transport capability

### Display and GPU
- display discovery
- graphics acceleration
- framebuffer or equivalent output capability

### Virtualization
- hardware virtualization support
- virtualization acceleration state
- host/guest capability context

## Capability state

Each capability has one explicit state: unknown, available, unavailable, unsupported, or failed.

- unknown: not discovered.
- available: discovered and usable.
- unavailable: known not to exist or not exposed.
- unsupported: exists conceptually but the current implementation cannot use it.
- failed: discovery or initialization was attempted and failed.

## Invariants

- No feature may silently treat unknown as available.
- No hardware identifier is an architectural capability.
- Capability discovery must be repeatable for the same platform state.
- State transitions must be observable by the platform layer.
- Higher layers consume capabilities; they do not rediscover hardware directly.

## Reference platform

The current physical machine is the first validation platform. Its observed properties are recorded separately in HARDWARE-REFERENCE.md. Those observations do not define the universal architecture.

## Next implementation step

Define the capability data structure and lifecycle state machine before implementing device-specific adapters.
