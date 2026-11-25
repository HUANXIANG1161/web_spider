import logging
import requests

from fetcher import fetch_html

logging.basicConfig(level=logging.INFO)

try:
    fetch_html("https://arxiv.org/abs/0000.00000")
except requests.RequestException as exc:
    print("404 不重试:", type(exc).__name__)