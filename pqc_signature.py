try:
    from cryptography.hazmat.primitives.asymmetric.mldsa import MLDSA65PrivateKey
except ImportError as exc:
    raise ImportError(
        "ML-DSA support requires a recent cryptography package. "
        "Install the requirements.txt dependencies."
    ) from exc

class PQCSigner:
    """Post-quantum digital signature wrapper using standardized ML-DSA-65."""

    def __init__(self):
        self.private_key = MLDSA65PrivateKey.generate()
        self.public_key = self.private_key.public_key()

    def sign(self, message: bytes) -> bytes:
        return self.private_key.sign(message)

    def verify(self, signature: bytes, message: bytes) -> bool:
        try:
            self.public_key.verify(signature, message)
            return True
        except Exception:
            return False

    @property
    def scheme(self):
        return "ML-DSA-65"
