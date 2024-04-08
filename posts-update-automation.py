import feedparser
import os
import re
from markdownify import markdownify
import html

BLOG_URI = "https://given-dev.tistory.com/"
GITHUB_URI = "https://github.com/GIVEN53/blog-post/tree/main/"


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
    summary = html.unescape(summary)
    contents = summary.split("<pre>")

    for i in range(len(contents)):
        code_block = re.search(r'<code\s+class="([^"]+)"', contents[i])
        if code_block:
            language = code_block.group(1)
            if "language-" in language:
                language = language.replace("language-", "")
            contents[i] = attach_language(language, "<pre>" + contents[i])
        else:
            contents[i] = markdownify(contents[i])
    return f"{title}\n=\n" + "".join(contents)


def attach_language(language: str, content: str) -> str:
    content = markdownify(content).split("```")
    return "\n```" + language + content[1] + "```\n" + "".join(content[2:])


def get_file_name(category: str, title: str) -> str:
    file_path = f"{category}/{title}/".replace(" ", "_")
    os.makedirs(file_path, exist_ok=True)
    return file_path + "README.md"


def update_readme(category: str):
    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()

    if readme.find(category) == -1:
        with open("README.md", "a", encoding="utf-8") as f:
            f.write(f"\n- [{category}]({GITHUB_URI + category})")

    sort_toc()


def sort_toc():
    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()

    start = readme.find("## 목차")
    toc = readme[start:].strip()
    toc_lines = sorted(toc.split("\n")[1:])
    sort_toc = "\n".join(["## 목차"] + toc_lines)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme.replace(toc, sort_toc))


if __name__ == "__main__":
    feeds = feedparser.parse(BLOG_URI + "rss")
    update(feeds["entries"])
