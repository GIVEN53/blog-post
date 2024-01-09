import feedparser
import os
from markdownify import markdownify


def update(feeds: list):
    for feed in feeds:
        category = feed["tags"][0]["term"]
        title = feed["title"]
        content = create_content(title, feed["summary"])

        file_name = get_file_name(category, title)
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(content)
        update_readme(category)


def create_content(title: str, summary: str) -> str:
    markdown_summary = markdownify(summary)
    return f"{title}\n=\n{markdown_summary}"


def get_file_name(category: str, title: str) -> str:
    file_path = f"{category}/{title}/".replace(" ", "_")
    os.makedirs(file_path, exist_ok=True)
    return file_path + "README.md"


def update_readme(category: str):
    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()

    if readme.find(category) == -1:
        with open("README.md", "a", encoding="utf-8") as f:
            f.write(
                f"- [{category}](https://github.com/GIVEN53/blog-post/tree/main/{category})\n"
            )


if __name__ == "__main__":
    tistory_blog_uri = "https://given-dev.tistory.com"
    feeds = feedparser.parse(tistory_blog_uri + "/rss")
    update(feeds["entries"])
