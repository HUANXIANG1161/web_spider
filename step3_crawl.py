from collections import deque
import time
from urllib.parse import urljoin

import logging
import os

from bs4 import BeautifulSoup
import requests
from fetcher import fetch_html

from step2_parse import parse_paper

from robots_policy import RobotsPolicy

logger = logging.getLogger(__name__)


def setup_logging() -> None:
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler("logs/crawl.log", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )



def extract_links(html: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, "lxml")
    links = []
    for a in soup.select("a[href]"):
        href = a.get("href")
        full = urljoin(base_url, href)
        if full.startswith("https://arxiv.org/abs/"):
            links.append(full)
    return links


def crawl(seed: str, max_pages: int = 4) -> list[dict]:
    attempted = 0        # 真正发起请求的页数（受 max_pages 限制）
    fetched = 0          # 下载成功的页数
    fetch_failed = 0     # 重试后仍抓取失败的页数
    parse_failed = 0     # 下载成功但解析失败的页数
    skipped = 0          # robots 拒绝的 URL 数

    queue = deque([seed])
    seen = {seed}
    papers = []
    policy = RobotsPolicy("CourseSpider")

    # 第一次会下载 robots.txt，并打印 arXiv 的 15 秒
    logger.info(f"robots delay: {policy.crawl_delay(seed)}")

    while queue and attempted < max_pages:
        url = queue.popleft()

        if not policy.can_fetch(url):
            logger.warning(f"robots disallow: {url}")
            skipped += 1
            continue

        delay = policy.crawl_delay(url)
        if attempted > 0:
            time.sleep(delay)

        attempted += 1
        logger.info(f"[{attempted}/{max_pages}] {url}")

        try:
            html = fetch_html(url, max_attempts=3, retry_delay=delay)
        except requests.RequestException as exc:
            logger.error(f"抓取失败，跳过：{url} -> {exc}")
            fetch_failed += 1
            continue

        fetched += 1

        if "/abs/" in url:
            try:
                paper = parse_paper(html, url)
            except Exception:
                logger.exception(f"解析失败，跳过：{url}")
                parse_failed += 1
                continue

            papers.append(paper)
            logger.info(f"  标题: {paper['title']}")

        for link in extract_links(html, url):
            if link not in seen:
                seen.add(link)
                queue.append(link)

    logger.info(
        f"完成：尝试 {attempted} 页，下载成功 {fetched} 页，"
        f"抓取失败 {fetch_failed} 页，解析失败 {parse_failed} 页，"
        f"robots 跳过 {skipped} 个，论文 {len(papers)} 篇"
    )

    return papers


def main():
    setup_logging()
    seed = "https://arxiv.org/list/cs.CL/2017-06"
    papers = crawl(seed, max_pages=4)
    logger.info(f"共抓到 {len(papers)} 篇论文")


if __name__ == "__main__":
    main()