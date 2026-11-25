from urllib.parse import urlsplit
from urllib.robotparser import RobotFileParser


class RobotsPolicy:
    def __init__(self, user_agent: str, default_delay: float = 15.0):
        self.user_agent = user_agent
        self.default_delay = default_delay
        self._parsers: dict[str, RobotFileParser] = {}

    def _get_parser(self, url: str) -> RobotFileParser:
        parts = urlsplit(url)
        host = parts.netloc

        # 每个站点只下载一次 robots.txt
        if host not in self._parsers:
            rp = RobotFileParser()
            rp.set_url(f"{parts.scheme}://{host}/robots.txt")
            rp.read()
            self._parsers[host] = rp

        return self._parsers[host]

    def can_fetch(self, url: str) -> bool:
        return self._get_parser(url).can_fetch(self.user_agent, url)

    def crawl_delay(self, url: str) -> float:
        delay = self._get_parser(url).crawl_delay(self.user_agent)
        return float(delay) if delay is not None else self.default_delay