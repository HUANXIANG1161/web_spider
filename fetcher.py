import logging
import time

import requests

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "CourseSpider/0.1 (course project; contact: 123@example.com)",
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "en-US,en;q=0.9",
}

RETRY_STATUS = {429, 500, 502, 503, 504}


def fetch_html(
    url: str,
    max_attempts: int = 3,
    retry_delay: float = 1.0,
) -> str:
    if max_attempts < 1:
        raise ValueError("max_attempts 必须 >= 1")

    for attempt in range(1, max_attempts + 1):
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            return response.text

        except requests.HTTPError as exc:
            status = exc.response.status_code if exc.response is not None else None

            if status not in RETRY_STATUS or attempt == max_attempts:
                logger.error(f"fetch failed ({attempt}/{max_attempts}): {url} -> {exc}")
                raise

            logger.warning(
                f"fetch failed ({attempt}/{max_attempts}): {url} -> {exc}; "
                f"retry in {retry_delay}s"
                )
            
        except requests.RequestException as exc:
            if attempt == max_attempts:
                logger.error(f"fetch failed ({attempt}/{max_attempts}): {url} -> {exc}")
                raise

            logger.warning(
                    f"fetch failed ({attempt}/{max_attempts}): {url} -> {exc}; "
                    f"retry in {retry_delay}s"
                    )

        # 还有下一次才睡；最后一次会在上面 raise，不会走到这里
        time.sleep(retry_delay)

    raise RuntimeError(f"fetch failed: {url}")