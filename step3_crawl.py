from collections import deque
import time
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests

from step2_parse import parse_paper


def fetch_html(url: str) -> str:
    headers = {
    "User-Agent": "CourseSpider/0.1 (course project; contact: 123@example.com)",
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "en-US,en;q=0.9",
    }
    response=requests.get(url,headers=headers,timeout=10)

    response.raise_for_status()
    
    return response.text


def extract_links(html: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, "lxml")
    links = []
    for a in soup.select("a[href]"):
        href = a.get("href")
        full = urljoin(base_url, href)
        if full.startswith("https://arxiv.org/abs/"):
            links.append(full)
    return links


def crawl(seed: str, max_pages: int = 4, delay: float = 15.0) -> list[dict]:
    queue = deque([seed])
    seen = {seed}
    papers = []
    fetched = 0

    while queue and fetched < max_pages:
        url = queue.popleft()
        if fetched > 0:
            time.sleep(delay)

        html = fetch_html(url)
        fetched += 1
        print(f"[{fetched}/{max_pages}] {url}")

        # TODO 2：如果 url 是论文摘要页（URL 里有 "/abs/"），
        #         用 parse_paper(html, url) 解析，加入 papers，并打印标题
        if "/abs/" in url:
            paper=parse_paper(html,url)
            papers.append(paper)
            print("  标题:", paper["title"])
        # TODO 3：对 extract_links(html, url) 的每个链接：
        #         如果不在 seen 里，加入 seen，再 append 到 queue
        for link in extract_links(html, url):
            if link not in seen:
                seen.add(link)
                queue.append(link)

    return papers


def main():
    seed = "https://arxiv.org/list/cs.CL/2017-06"
    papers = crawl(seed, max_pages=4, delay=15)
    print(f"共抓到 {len(papers)} 篇论文")


if __name__ == "__main__":
    main()