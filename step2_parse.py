from bs4 import BeautifulSoup

def meta_content(soup, name: str) -> str:
    tag = soup.select_one(f"meta[name='{name}']")
    if tag is None:
        return ""
    return tag.get("content", "")

def parse_paper(html: str, url: str) -> dict:
    soup= BeautifulSoup(html,"lxml")

    title=meta_content(soup,"citation_title")
    author_tags=soup.select("meta[name='citation_author']")
    authors = [tag.get("content", "") for tag in author_tags]
    abstract = meta_content(soup, "citation_abstract")
    if not abstract:
        block = soup.select_one("blockquote.abstract")
        abstract = block.get_text(" ", strip=True) if block else ""
        abstract = abstract.removeprefix("Abstract:").strip()

    subjects = soup.select_one("td.subjects")
    keywords = []
    if subjects:
        text = subjects.get_text(" ", strip=True)
        keywords = [part.strip() for part in text.split(";")]

    publish_date = meta_content(soup, "citation_date") or meta_content(soup, "citation_online_date")
    pdf_url = meta_content(soup, "citation_pdf_url")

    return {
        "title": title,
        "authors": authors,
        "abstract": abstract,
        "keywords": keywords,
        "publish_date": publish_date,
        "url": url,
        "pdf_url": pdf_url,
    }


def main():
    with open("data/sample_arxiv.html", encoding="utf-8") as f:
        html = f.read()

    paper = parse_paper(html, "https://arxiv.org/abs/1706.03762")

    print("标题:", paper["title"])
    print("作者:", "; ".join(paper["authors"]))
    print("摘要:", paper["abstract"][:100] + "...")
    print("关键词:", "; ".join(paper["keywords"]))
    print("发表时间:", paper["publish_date"])
    print("URL:", paper["url"])
    print("PDF:", paper["pdf_url"])


if __name__ == "__main__":
    main()