# ADMWS12 — Hardware Abstraction Layer

## Objective

The ADMWS12 Hardware Abstraction Layer (HAL) is an original software boundary between the ADMWS12 core and physical hardware.

The HAL is not a copy of an existing operating-system HAL. Its interfaces are specified independently.

## Boundary

The dependency direction is:

Hardware
→ device-specific implementation
→ ADMWS12 HAL
→ ADMWS12 core
→ higher-level services

The core must never call a vendor driver directly.

## Initial capability domains

### CPU

Responsibilities:

- identify execution capabilities;
- select execution units;
- expose architecture-neutral CPU operations;
- provide safe synchronization primitives.

### Memory

Responsibilities:

- discover physical memory;
- describe address ranges;
- manage allocation domains;
- enforce ownership and lifetime rules.

### Time

Responsibilities:

- provide monotonic time;
- provide timers;
- expose clock characteristics;
- avoid dependence on wall-clock changes.

### Interrupts and events

Responsibilities:

- register handlers;
- route hardware events;
- acknowledge and mask events;
- provide a defined concurrency model.

### PCI and PCIe

Responsibilities:

- enumerate devices;
- identify class and capabilities;
- expose configuration access;
- bind devices to drivers.

### Storage

Responsibilities:

- discover persistent media;
- expose block-oriented operations;
- report geometry and capabilities;
- isolate device protocol details from the core.

### Firmware

Responsibilities:

- discover the boot environment;
- obtain firmware-provided platform information;
- define the transition from boot environment to ADMWS12 runtime.

### Network

Responsibilities:

- enumerate network interfaces;
- expose link state and capabilities;
- provide packet transport primitives;
- isolate chipset-specific operations.

### Display and GPU

Responsibilities:

- detect display/graphics capabilities;
- expose a minimal display abstraction;
- permit optional acceleration without making it a core dependency.

### Virtualization

Responsibilities:

- detect virtualization capabilities;
- expose only explicitly supported operations;
- keep virtualization optional unless a future specification promotes it to a baseline requirement.

## HAL invariants

1. The core cannot depend on a device model.
2. A HAL operation has a defined success, failure, and unsupported state.
3. Resource ownership is explicit.
4. Hardware state is never assumed to remain unchanged.
5. Initialization order is deterministic.
6. Capability discovery is separated from capability use.
7. Device identifiers do not become API contracts.

## Development order

1. Define capability models.
2. Define invariants.
3. Define lifecycle/state machines.
4. Define minimal interfaces.
5. Implement a reference platform adapter.
6. Validate on the current hardware.
7. Add other hardware only after the abstraction survives the reference implementation.

## Current platform mapping

The first adapter targets the observed x86-64/UEFI/NVMe/PCIe platform recorded in the research/platform-inventory directory.

No driver implementation is committed by this specification alone.
