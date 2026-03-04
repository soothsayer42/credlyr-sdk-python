import hmac
import hashlib
import time
from typing import Dict, Any, Optional


def verify_webhook_signature(
    payload: str,
    signature: str,
    secret: str,
    tolerance: int = 300
) -> Dict[str, Any]:
    """
    Verify a webhook signature.

    Args:
        payload: The raw request body as a string
        signature: The X-Credlyr-Signature header value
        secret: Your webhook signing secret
        tolerance: Maximum age of the webhook in seconds (default: 5 minutes)

    Returns:
        The parsed payload as a dictionary

    Raises:
        ValueError: If the signature is invalid or the webhook is too old
    """
    import json

    # Parse signature header (format: "t=timestamp,v1=signature")
    parts = {}
    for part in signature.split(","):
        if "=" in part:
            key, value = part.split("=", 1)
            parts[key] = value

    timestamp = parts.get("t")
    sig = parts.get("v1")

    if not timestamp or not sig:
        raise ValueError("Invalid signature format")

    # Check timestamp tolerance
    try:
        webhook_time = int(timestamp)
        if abs(time.time() - webhook_time) > tolerance:
            raise ValueError("Webhook timestamp outside tolerance")
    except ValueError as e:
        if "tolerance" in str(e):
            raise
        raise ValueError("Invalid timestamp")

    # Compute expected signature
    signed_payload = f"{timestamp}.{payload}"
    expected_sig = hmac.new(
        secret.encode(),
        signed_payload.encode(),
        hashlib.sha256
    ).hexdigest()

    # Constant-time comparison
    if not hmac.compare_digest(sig, expected_sig):
        raise ValueError("Invalid signature")

    return json.loads(payload)


def generate_test_signature(payload: str, secret: str, timestamp: Optional[int] = None) -> str:
    """
    Generate a webhook signature for testing purposes.

    Args:
        payload: The request body as a string
        secret: Your webhook signing secret
        timestamp: Optional timestamp (defaults to current time)

    Returns:
        The signature header value
    """
    if timestamp is None:
        timestamp = int(time.time())

    signed_payload = f"{timestamp}.{payload}"
    sig = hmac.new(
        secret.encode(),
        signed_payload.encode(),
        hashlib.sha256
    ).hexdigest()

    return f"t={timestamp},v1={sig}"
