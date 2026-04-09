# @AI_GENERATED
"""公共工具函数"""

import re


def markdown_to_plain(text: str) -> str:
    """将 Markdown 格式文本转为纯文本。

    去除：**粗体**、*斜体*、![图片](url)、> 引用前缀、--- 分隔线
    """
    text = re.sub(r"!\[.*?\]\(.*?\)", "", text)
    text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"__(.*?)__", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = re.sub(r"^>\s?", "", text, flags=re.MULTILINE)
    text = re.sub(r"^-{3,}\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()
# @AI_GENERATED: end