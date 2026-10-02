# ADMWS12 Platform Boot Model

## Purpose

Define the boot lifecycle as an ADMWS12 contract without copying an existing operating-system boot architecture.

## Boot phases

1. RESET — execution begins in the firmware-controlled initial state.
2. DISCOVERY — firmware mode and boot-visible platform capabilities are identified.
3. PLATFORM_INIT — the minimal platform state required by the core is established.
4. CORE_HANDOFF — control is transferred to the ADMWS12 core through a defined handoff contract.
5. RUNTIME — normal platform services operate through the HAL.
6. SHUTDOWN — runtime resources are quiesced and control leaves the runtime environment.

## Handoff requirements

The handoff must explicitly identify:
- execution architecture;
- memory regions available to the core;
- firmware mode;
- boot source information;
- discovered mandatory capabilities;
- discovered optional capabilities;
- ownership of platform resources;
- error state, if initialization is incomplete.

## Invariants

- A missing optional capability does not invalidate boot.
- A missing mandatory capability stops the transition to runtime.
- Boot discovery does not expose device-specific identifiers as core contracts.
- Resource ownership changes are explicit.
- Every boot phase has a defined success and failure transition.

## Current validation target

The first validation target is the existing ASUS/AMI UEFI x86-64 platform documented in HARDWARE-REFERENCE.md. Compatibility with that platform is a validation requirement, not the definition of the architecture.
