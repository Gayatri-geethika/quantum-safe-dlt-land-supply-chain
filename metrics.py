import time
from pqc_signature import PQCSigner

def benchmark_signature(iterations=10):
    signer = PQCSigner()
    message = (
        b"property_id=LAND-001|owner=Demo Owner|"
        b"location=Vizianagaram"
    )

    sign_times = []
    verify_times = []
    signature_size = 0
    successful = 0

    for _ in range(iterations):
        start = time.perf_counter()
        signature = signer.sign(message)
        sign_times.append(time.perf_counter() - start)

        signature_size = len(signature)

        start = time.perf_counter()
        ok = signer.verify(signature, message)
        verify_times.append(time.perf_counter() - start)
        successful += int(ok)

    return {
        "algorithm": signer.scheme,
        "iterations": iterations,
        "signature_size_bytes": signature_size,
        "average_sign_time_ms": round(
            sum(sign_times) / len(sign_times) * 1000, 3
        ),
        "average_verify_time_ms": round(
            sum(verify_times) / len(verify_times) * 1000, 3
        ),
        "successful_verifications": successful,
        "verification_success_rate_percent": round(
            successful / iterations * 100, 2
        )
    }
