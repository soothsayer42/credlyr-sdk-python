# Credlyr Python SDK

Official Python SDK for the Credlyr API - verifiable credentials infrastructure for identity verification.

## Installation

```bash
pip install credlyr
```

## Quick Start

```python
from credlyr import CredlyrClient

client = CredlyrClient(api_key="sk_live_xxx")

# Create a verification session
verification = client.verifications.create(
    policy_id="pol_abc123",
    return_url="https://yourapp.com/callback",
)

print("Verification URL:", verification["hosted_url"])
```

## Configuration

```python
client = CredlyrClient(
    api_key="your-api-key",           # Required
    base_url="https://api.credlyr.com",  # Optional, defaults to production
    timeout=30.0,                      # Optional, request timeout in seconds
    max_retries=2,                     # Optional, retry failed requests
)
```

## Resources

### Verifications

```python
# Create a verification session
verification = client.verifications.create(
    policy_id="pol_abc123",
    return_url="https://yourapp.com/callback",
    metadata={"user_id": "user_123"},
)

# Get verification details
details = client.verifications.retrieve("ver_xyz789")

# List all verifications
result = client.verifications.list(status="completed")
```

### Issuance

```python
# Create an issuance session
session = client.issuance.create_session(
    credential_type="EmploymentCredential",
    claims={
        "employer": "Acme Corp",
        "position": "Software Engineer",
        "start_date": "2024-01-15",
    },
)
```

### Policies

```python
# Create a policy
policy = client.policies.create(
    name="Age Verification",
    rules={"required_claims": ["birthDate"]},
)

# List policies
result = client.policies.list()
```

### Team Management

```python
# List team members
result = client.team.list()

# Invite a new member
member = client.team.invite(
    email="developer@company.com",
    role="developer",
)
```

### Billing

```python
# Get current usage
usage = client.billing.get_usage()

# Open billing portal
portal = client.billing.create_portal_session()
```

## Webhook Verification

```python
from credlyr import verify_webhook_signature

# In your webhook handler
def handle_webhook(request):
    payload = request.body.decode()
    signature = request.headers["X-Credlyr-Signature"]

    try:
        event = verify_webhook_signature(
            payload,
            signature,
            "your_webhook_secret",
        )

        if event["type"] == "verification.completed":
            # Handle completed verification
            pass

    except ValueError as e:
        return {"error": "Invalid signature"}, 400
```

## Error Handling

```python
from credlyr import (
    CredlyrError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
    NotFoundError,
)

try:
    verification = client.verifications.create(policy_id="invalid")
except AuthenticationError:
    print("Invalid API key")
except RateLimitError as e:
    print(f"Rate limited, retry after {e.retry_after}s")
except ValidationError as e:
    print(f"Validation error: {e.message}")
except NotFoundError:
    print("Resource not found")
except CredlyrError as e:
    print(f"API error: {e.code} - {e.message}")
```

## Context Manager

```python
with CredlyrClient(api_key="sk_live_xxx") as client:
    verification = client.verifications.create(...)
# Client is automatically closed
```

## Requirements

- Python 3.8+
- httpx

## License

MIT
