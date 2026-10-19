from urllib.parse import urlsplit


def normalize_domain(value: str) -> str:
    candidate = value.strip().lower().rstrip(".")
    parsed = urlsplit(candidate if "://" in candidate else f"//{candidate}")
    hostname = parsed.hostname
    if hostname is None:
        raise ValueError("A valid domain or website URL is required.")
    if hostname.startswith("www."):
        hostname = hostname[4:]
    try:
        normalized = hostname.encode("idna").decode("ascii")
    except UnicodeError as exception:
        raise ValueError("A valid domain or website URL is required.") from exception
    if "." not in normalized or len(normalized) > 253:
        raise ValueError("A valid domain or website URL is required.")
    return normalized
