"""UEFI Secure Boot certificate collection for ADMWS12."""
from __future__ import annotations

import base64
import hashlib
import shutil
import subprocess
from dataclasses import dataclass
from typing import Iterable

EFI_CERT_X509_GUID = bytes.fromhex("c1c41626504c4092aca941f936934328")
SECURE_BOOT_VARIABLES = ("PK", "KEK", "db", "dbx")


@dataclass(frozen=True)
class SecureBootCertificate:
    variable: str
    der: bytes
    sha256: str
    owner_guid: bytes


@dataclass(frozen=True)
class SecureBootVariable:
    name: str
    raw: bytes
    sha256: str
    certificates: tuple[SecureBootCertificate, ...]


class SecureBootCollectionError(RuntimeError):
    """Raised when a firmware variable cannot be collected."""


def _powershell() -> str:
    for candidate in ("pwsh", "powershell.exe", "powershell"):
        path = shutil.which(candidate)
        if path:
            return path
    raise SecureBootCollectionError("PowerShell was not found")


def read_secure_boot_variable(name: str) -> bytes:
    """Read one UEFI Secure Boot variable through Windows PowerShell."""
    if name not in SECURE_BOOT_VARIABLES:
        raise ValueError(f"unsupported Secure Boot variable: {name}")

    command = (
        "$v = Get-SecureBootUEFI -Name "
        + name
        + " -ErrorAction Stop; "
        "[Convert]::ToBase64String([byte[]]$v.Bytes)"
    )
    result = subprocess.run(
        [_powershell(), "-NoProfile", "-NonInteractive", "-Command", command],
        capture_output=True, text=True, check=False
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        raise SecureBootCollectionError(
            f"Get-SecureBootUEFI {name} failed: {detail or 'unknown error'}"
        )
    try:
        return base64.b64decode(result.stdout.strip(), validate=True)
    except (ValueError, base64.binascii.Error) as exc:
        raise SecureBootCollectionError(
            f"Get-SecureBootUEFI {name} returned invalid base64"
        ) from exc


def extract_x509_certificates(
    variable: str, data: bytes
) -> tuple[SecureBootCertificate, ...]:
    """Extract X.509 DER certificates from EFI_SIGNATURE_LIST data."""
    found: list[SecureBootCertificate] = []
    offset = 0
    total = len(data)

    while offset + 28 <= total:
        signature_type = data[offset:offset + 16]
        list_size = int.from_bytes(data[offset + 16:offset + 20], "little")
        header_size = int.from_bytes(data[offset + 20:offset + 24], "little")
        signature_size = int.from_bytes(data[offset + 24:offset + 28], "little")

        if list_size < 28 or signature_size < 16:
            break

        end = offset + list_size
        signatures_start = offset + 28 + header_size
        if end > total or signatures_start > end:
            break

        if signature_type == EFI_CERT_X509_GUID:
            cursor = signatures_start
            while cursor + signature_size <= end:
                signature = data[cursor:cursor + signature_size]
                owner_guid = signature[:16]
                der = signature[16:]
                if der:
                    found.append(
                        SecureBootCertificate(
                            variable=variable,
                            der=der,
                            sha256=hashlib.sha256(der).hexdigest(),
                            owner_guid=owner_guid,
                        )
                    )
                cursor += signature_size

        offset = end

    return tuple(found)


def collect_secure_boot_variables(
    names: Iterable[str] = SECURE_BOOT_VARIABLES,
) -> tuple[SecureBootVariable, ...]:
    """Collect available Secure Boot variables without inventing absent data."""
    result: list[SecureBootVariable] = []
    for name in names:
        raw = read_secure_boot_variable(name)
        result.append(
            SecureBootVariable(
                name=name,
                raw=raw,
                sha256=hashlib.sha256(raw).hexdigest(),
                certificates=extract_x509_certificates(name, raw),
            )
        )
    return tuple(result)
