import feedparser
import os
from markdownify import markdownify
from pygments.lexers import guess_lexer


def post(feeds: list):
    for feed in feeds:
        category = feed["tags"][0]["term"]
        title = feed["title"]
        content = create_content(title, feed["summary"])

        file_name = get_file_name(category, title)
        f = open(file_name, mode="w", encoding="utf-8")
        f.write(content)
        f.close()


def create_content(title: str, summary: str) -> str:
    markdown_summary = markdownify(summary)
    return attach_language_name(f"{title}\n=\n{markdown_summary}")


def attach_language_name(content: str) -> str:
    code_block = "```"
    blocks = content.split(code_block)

    for i in range(1, len(blocks), 2):
        code = blocks[i]
        lexer = guess_lexer(code)
        blocks[i] = code_block + " " + lexer.name + code + code_block + "\n"
    return "".join(blocks)


def get_file_name(category: str, title: str) -> str:
    file_path = f"{category}/{title}/".replace(" ", "_")
    os.makedirs(file_path, exist_ok=True)
    return file_path + "README.md"


if __name__ == "__main__":
    tistory_blog_uri = "https://given-dev.tistory.com"
    feeds = feedparser.parse(tistory_blog_uri + "/rss")
    post(feeds["entries"])
