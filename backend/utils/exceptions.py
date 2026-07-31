class ScraperError(Exception):
    def __init__(self, market, url, reason, status_code=None):
        self.market = market
        self.url = url
        self.reason = reason
        self.status_code = status_code
        super().__init__(f"[{market}] {reason} (url: {url})")
