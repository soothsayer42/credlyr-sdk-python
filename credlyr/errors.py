class CredlyrError(Exception):
    """Base exception for Credlyr API errors."""

    def __init__(self, code: str, message: str, status_code: int = 500, request_id: str = None):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.request_id = request_id
        super().__init__(message)


class AuthenticationError(CredlyrError):
    """Raised when API authentication fails."""

    def __init__(self, message: str = "Invalid API key", request_id: str = None):
        super().__init__("authentication_error", message, 401, request_id)


class RateLimitError(CredlyrError):
    """Raised when rate limit is exceeded."""

    def __init__(self, retry_after: int = 60, request_id: str = None):
        self.retry_after = retry_after
        super().__init__("rate_limit_exceeded", "Too many requests", 429, request_id)


class NotFoundError(CredlyrError):
    """Raised when a resource is not found."""

    def __init__(self, resource: str, id: str, request_id: str = None):
        super().__init__("not_found", f"{resource} '{id}' not found", 404, request_id)


class ValidationError(CredlyrError):
    """Raised when request validation fails."""

    def __init__(self, message: str, param: str = None, request_id: str = None):
        self.param = param
        super().__init__("validation_error", message, 400, request_id)


class ServerError(CredlyrError):
    """Raised when a server error occurs."""

    def __init__(self, message: str = "Internal server error", request_id: str = None):
        super().__init__("server_error", message, 500, request_id)
