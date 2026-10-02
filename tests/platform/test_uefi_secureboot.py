import unittest

from src.platform.uefi_secureboot import EFI_CERT_X509_GUID, extract_x509_certificates


def signature_list(cert: bytes, owner: bytes = bytes(range(16))) -> bytes:
    signature_size = 16 + len(cert)
    list_size = 16 + signature_size
    header = (
        list_size.to_bytes(4, "little")
        + (0).to_bytes(4, "little")
        + signature_size.to_bytes(4, "little")
        + EFI_CERT_X509_GUID
    )
    return header + owner + cert


class UefiSecureBootTests(unittest.TestCase):
    def test_extracts_x509_der(self):
        cert = b"fake-der-certificate"
        result = extract_x509_certificates("db", signature_list(cert))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].variable, "db")
        self.assertEqual(result[0].der, cert)
        self.assertEqual(len(result[0].sha256), 64)

    def test_ignores_non_x509_signature(self):
        signature = bytes.fromhex("a5" * 16) + b"hash"
        size = 16 + len(signature)
        data = (
            size.to_bytes(4, "little")
            + (0).to_bytes(4, "little")
            + len(signature).to_bytes(4, "little")
            + bytes(16)
            + signature
        )
        self.assertEqual(extract_x509_certificates("dbx", data), ())

    def test_truncated_list_is_safe(self):
        self.assertEqual(extract_x509_certificates("db", b"\x01\x02"), ())


if __name__ == "__main__":
    unittest.main()
