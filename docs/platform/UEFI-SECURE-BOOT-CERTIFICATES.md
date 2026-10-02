# ADMWS12 - UEFI Secure Boot certificate evidence

The Windows platform adapter reads PK, KEK, db and dbx through Get-SecureBootUEFI. It preserves the raw variable, computes SHA-256, parses EFI signature lists, and extracts X.509 DER certificates.

Reading a certificate is not proof of trust. Certificate signature verification, trust-anchor validation, Secure Boot state, and TPM boot measurements remain separate evidence stages.

The AMD Ryzen 7 5800H with ASUS/AMI UEFI is the first validation platform. The implementation remains vendor-neutral.

Physical firmware collection is required before hardware evidence can be marked observed.
