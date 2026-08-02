import ipaddress
import socket
import requests
from urllib.parse import urlparse


def _is_blocked_ip(ip_str):
    """Return True if the given IP address is loopback, private, link-local,
    reserved, or otherwise unroutable — i.e. not a legitimate public target."""
    try:
        ip = ipaddress.ip_address(ip_str)
    except ValueError:
        return True  # Can't parse it -> treat as unsafe

    return (
        ip.is_loopback
        or ip.is_private
        or ip.is_link_local
        or ip.is_reserved
        or ip.is_multicast
        or ip.is_unspecified
    )


def _is_safe_host(hostname):
    """Resolve hostname to all its IPs and make sure none of them point at
    internal infrastructure. Prevents SSRF via DNS rebinding / internal
    hostnames such as 'localhost', '169.254.169.254', '10.0.0.5', etc."""
    if not hostname:
        return False

    try:
        # getaddrinfo resolves both IPv4 and IPv6 addresses for the host
        addr_info = socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        return False

    resolved_ips = {info[4][0] for info in addr_info}
    if not resolved_ips:
        return False

    return all(not _is_blocked_ip(ip) for ip in resolved_ips)


DEFAULT_PATH_KEYWORDS = {
    'crypto': ['api', 'coins', 'markets', 'tickers', 'paprika'],
    'ecommerce': ['e-commerce', 'allinone', 'computers', 'tablets'],
}


def validate_scrape_url(url, scraper_type, path_keywords=None):
    """
    Validate that `url` is safe and plausible to scrape.

    `path_keywords`, when provided (e.g. from a website registered via
    POST /api/websites), overrides the hardcoded per-scraper-type keyword
    list below. This lets newly-registered sites pass validation without
    editing this function every time a team adds a target.
    """
    if not url:
        return False, "URL is empty"
    parsed = urlparse(url)
    if parsed.scheme not in ('http', 'https'):
        return False, "Invalid scheme"
    if not parsed.netloc:
        return False, "Invalid netloc"

    # SSRF guard: block loopback / private / link-local / reserved targets
    hostname = parsed.hostname
    if not _is_safe_host(hostname):
        return False, "URL resolves to a disallowed or internal address"

    path = parsed.path.lower()
    keywords = path_keywords if path_keywords else DEFAULT_PATH_KEYWORDS.get(scraper_type)
    if keywords and not any(word.lower() in path for word in keywords):
        return False, f"Invalid {scraper_type} path"

    return True, None

def health_check(url, scraper_type):
    # SSRF guard: re-validate the host is safe right before making the
    # request, in case this is ever called independently of validate_scrape_url.
    parsed = urlparse(url)
    if parsed.scheme not in ('http', 'https') or not _is_safe_host(parsed.hostname):
        return False

    try:
        if scraper_type == 'crypto':
            res = requests.get(url, timeout=3, allow_redirects=False)
            if res.status_code == 200:
                try:
                    data = res.json()
                    return isinstance(data, list)
                except ValueError:
                    return False
            return False
        elif scraper_type == 'ecommerce':
            # E-commerce health check: HEAD request (or lightweight GET)
            res = requests.head(url, timeout=3, allow_redirects=False)
            if res.status_code == 405: # Method Not Allowed, fallback to GET
                res = requests.get(url, timeout=3, stream=True, allow_redirects=False)
                res.close()
            return 200 <= res.status_code < 400
    except requests.RequestException:
        return False
    return False
