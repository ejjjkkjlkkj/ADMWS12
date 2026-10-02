# ADMWS12 — Tool layer

The tool layer is the first executable-capability contract above atoms and
components.

## Construction rule

Néant -> atome -> composant -> outil.

A tool is not a wrapper around an existing framework. It is a project-owned
capability whose contract records:

- its name and version;
- the component identities it uses;
- its input contract;
- its output contract;
- its execution policy;
- its provenance.

The tool identity is derived deterministically from those fields.

## Engineering targets

The layer is designed to make hidden dependencies difficult to introduce:

- no copied external implementation;
- no copied binary as a foundation;
- explicit dependencies;
- deterministic identity;
- explicit input/output contracts;
- provenance;
- tamper detection.

Actual executable behavior will be added only after the contract layer is
validated. External standards may describe interfaces that ADMWS12 implements,
but their implementations are not imported as the project's foundation.

## Next step

The next layer is chain: deterministic composition of verified tools into a
larger operation.
