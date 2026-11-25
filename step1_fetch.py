import os

from fetcher import fetch_html


def main():
    url = "https://arxiv.org/abs/1706.03762"
    html = fetch_html(url=url)

    os.makedirs("data", exist_ok=True)
    with open("data/sample_arxiv.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("saved to data/sample_arxiv.html")


if __name__ == "__main__":
    main()