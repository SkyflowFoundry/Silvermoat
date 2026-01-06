"""Vertical detection from subdomain"""


def detect_vertical(host_header: str) -> str:
    """
    Extract vertical from Host header subdomain.

    Args:
        host_header: Host header from API Gateway event (e.g., "insurance.silvermoat.net")

    Returns:
        Vertical name: "insurance" or "retail" (defaults to "insurance")

    Examples:
        insurance.silvermoat.net -> insurance
        retail.silvermoat.net -> retail
        silvermoat.net -> insurance (default)
        localhost -> insurance (local dev)
    """
    if not host_header:
        return "insurance"

    # Extract subdomain
    parts = host_header.lower().split(".")

    # localhost or IP address -> default to insurance
    if "localhost" in host_header or host_header.replace(".", "").isdigit():
        return "insurance"

    # Check if first part is a known vertical
    subdomain = parts[0] if len(parts) > 1 else ""

    valid_verticals = ["insurance", "retail"]

    if subdomain in valid_verticals:
        return subdomain

    # Default to insurance (covers silvermoat.net, unknown subdomains, etc.)
    return "insurance"
