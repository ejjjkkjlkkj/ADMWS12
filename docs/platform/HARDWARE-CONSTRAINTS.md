# ADMWS12 — Hardware constraints

## Principle

ADMWS12 is software designed from a blank slate, but it must execute on real hardware. Hardware compatibility is therefore a constraint, not an implementation template.

## Constraint levels

### H0 — Fundamental

The platform must provide:

- a 64-bit execution environment;
- addressable physical memory;
- a monotonic time source;
- interrupt or equivalent event delivery;
- persistent storage for a complete installation;
- a firmware boot path.

### H1 — Current reference platform

The first validation target provides:

- AMD x86-64 CPU;
- 8 cores / 16 logical processors;
- approximately 40 GiB RAM;
- NVMe storage;
- UEFI firmware;
- PCIe devices;
- MediaTek MT7921 Wi-Fi;
- hardware virtualization support enabled in firmware.

### H2 — Optional acceleration

The architecture may use, but must not require:

- GPU acceleration;
- virtualization acceleration;
- Wi-Fi;
- additional PCIe devices;
- Secure Boot.

## Design rules

1. Hardware detection precedes feature activation.
2. No core component may depend on a specific vendor model.
3. A device driver may depend on a specific hardware model.
4. Device-specific code must terminate at the hardware abstraction boundary.
5. Missing optional hardware must produce a defined capability state, not an undefined failure.
6. Performance optimizations must be selected from detected capabilities.
7. Hardware identifiers are inventory data, not architecture primitives.

## Validation

Every hardware-dependent feature must have:

- a capability definition;
- a detection method;
- a minimal implementation;
- a negative/absence case;
- a validation test on the reference platform.

## Non-goals

This document does not define a new CPU architecture, motherboard, SSD, Wi-Fi chipset, or firmware. Those are external physical constraints.
