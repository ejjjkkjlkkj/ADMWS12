# ADMWS12 Adapter Evidence Model

Evidence is the adapter-local representation of an observation. It is translated into a core capability before discovery completes.

Flow:

hardware or firmware -> adapter -> evidence -> capability translation -> DiscoveryResult -> PlatformContext

States:

- OBSERVED: observation obtained.
- ABSENT: property known to be absent.
- UNSUPPORTED: observation cannot be provided by the current adapter.
- FAILED: observation was attempted and failed.
- UNKNOWN: no reliable conclusion exists.

The adapter owns evidence interpretation. The core receives only capability states. Evidence does not control lifecycle transitions.

Current status: evidence states, an immutable evidence record, deterministic translation, and tests are implemented. No hardware-specific collector exists.
