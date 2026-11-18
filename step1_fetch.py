import os
import requests

def fetch_html(url: str) -> str:
    headers = {
    "User-Agent": "CourseSpider/0.1 (course project; contact: 123@example.com)",
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "en-US,en;q=0.9",
    }
    response=requests.get(url,headers=headers,timeout=10)

    response.raise_for_status()
    
    return response.text

def main():
    url="https://arxiv.org/abs/1706.03762"
    html=fetch_html(url=url)
    os.makedirs("data", exist_ok=True)
    with open("data/sample_arxiv.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("saved to data/sample_arxiv.html")


if __name__ == "__main__":
    main()