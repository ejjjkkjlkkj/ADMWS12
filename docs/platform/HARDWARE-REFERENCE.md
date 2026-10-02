# ADMWS12 — Reference hardware

## Purpose

This document defines the first physical reference platform for ADMWS12. It records observed capabilities without making the implementation dependent on device-specific identifiers.

The software architecture is designed from a blank slate. The physical hardware is the compatibility constraint.

## Observed baseline

- CPU architecture: x86-64.
- CPU: AMD Ryzen 7 5800H with Radeon Graphics.
- CPU topology: 8 physical cores, 16 logical processors.
- Address/data width: 64 bits.
- Reported maximum CPU clock: 3201 MHz.
- L2 cache: 4 MiB.
- L3 cache: 16 MiB.
- Physical memory: 40 GiB total from two modules (8 GiB + 32 GiB), configured at 3200 MT/s.
- System storage: one NVMe SSD, approximately 1 TB, GPT, 512-byte logical sectors and 4096-byte physical sectors.
- Firmware: ASUS platform with AMI firmware, version M1603QA.308, dated 2023-05-22.
- Firmware boot model: UEFI.
- PCIe network device: MediaTek Wi-Fi 6 MT7921, PCIe endpoint.
- Hardware virtualization: firmware virtualization is reported enabled.
- Windows virtualization components currently enabled include Hyper-V and Virtual Machine Platform.

## Compatibility interpretation

These observations define the first validation target. They do not define the universal ADMWS12 platform.

ADMWS12 must:

1. detect capabilities at runtime;
2. expose hardware through stable internal abstractions;
3. avoid embedding serial numbers, GUIDs, MAC addresses, host names, or other machine identifiers in the core design;
4. tolerate optional hardware features being absent;
5. keep hardware-specific drivers and adapters outside the core model.

## Required capability classes

The first architecture must provide abstract interfaces for:

- CPU and execution;
- physical memory;
- timers;
- interrupts;
- PCI/PCIe devices;
- persistent storage;
- firmware/boot services;
- network devices;
- display/GPU capabilities;
- virtualization capabilities.

## Optional capabilities

Wi-Fi, GPU acceleration, virtualization extensions, Secure Boot, and other platform features are capabilities to detect rather than assumptions to hard-code.

## Source

The measurements come from the research/platform-inventory directory. Raw inventory remains evidence; this document is the ADMWS12 abstraction of that evidence.
