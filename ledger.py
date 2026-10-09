import hashlib
import json
from datetime import datetime, timezone
from pqc_signature import PQCSigner

class QuantumSafeLedger:
    """Small educational DLT-style ledger for the hackathon prototype."""

    def __init__(self):
        self.signer = PQCSigner()
        self.records = []

    def _canonical_bytes(self, record):
        return json.dumps(record, sort_keys=True, separators=(",", ":")).encode()

    def add_record(self, record_type, payload):
        previous_hash = (
            self.records[-1]["record_hash"] if self.records else "GENESIS"
        )

        record = {
            "index": len(self.records),
            "type": record_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": payload,
            "previous_hash": previous_hash,
        }

        record_bytes = self._canonical_bytes(record)
        record_hash = hashlib.sha256(record_bytes).hexdigest()
        signature = self.signer.sign(record_bytes)

        record["record_hash"] = record_hash
        record["signature"] = signature.hex()
        record["signature_scheme"] = "ML-DSA-65"

        self.records.append(record)
        return record

    def verify_chain(self):
        results = []

        for i, record in enumerate(self.records):
            unsigned = {
                "index": record["index"],
                "type": record["type"],
                "timestamp": record["timestamp"],
                "payload": record["payload"],
                "previous_hash": record["previous_hash"],
            }

            raw = self._canonical_bytes(unsigned)
            expected_hash = hashlib.sha256(raw).hexdigest()

            hash_ok = expected_hash == record["record_hash"]
            signature_ok = self.signer.verify(
                bytes.fromhex(record["signature"]), raw
            )

            link_ok = (
                i == 0
                and record["previous_hash"] == "GENESIS"
            ) or (
                i > 0
                and record["previous_hash"] == self.records[i - 1]["record_hash"]
            )

            results.append({
                "index": i,
                "hash_valid": hash_ok,
                "signature_valid": signature_ok,
                "previous_hash_link_valid": link_ok,
                "valid": hash_ok and signature_ok and link_ok
            })

        return {
            "records_checked": len(self.records),
            "ledger_valid": all(x["valid"] for x in results),
            "details": results
        }
