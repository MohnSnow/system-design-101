# @AI_GENERATED
"""小红书自动发布工具 - 内容解析器

扫描待发布目录，配对 Markdown 和图片文件，解析 Markdown 内容。
"""

from __future__ import annotations

import re
from pathlib import Path

from .models import ContentPair

# 支持的图片扩展名
IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg")

# 标题最大长度
MAX_TITLE_LENGTH = 20


class ContentParser:
    """内容解析器：扫描目录、配对文件、解析 Markdown"""

    def __init__(self, pending_dir: Path):
        self.pending_dir = pending_dir

    def scan(self) -> list[ContentPair]:
        """扫描待发布目录，返回按文件名排序的有效内容组列表。

        无图片配对的 Markdown 文件会被跳过并输出控制台提示。
        """
        if not self.pending_dir.exists():
            print(f"⚠️ 待发布目录不存在: {self.pending_dir}")
            return []

        md_files = sorted(self.pending_dir.glob("*.md"))
        if not md_files:
            print("📭 待发布目录中没有 Markdown 文件")
            return []

        results: list[ContentPair] = []
        for md_path in md_files:
            image_path = self._find_image(md_path)
            if image_path is None:
                print(f"⚠️ 跳过 {md_path.name}：未找到同名图片文件，请手动处理")
                continue

            title, body, tags = self._parse_markdown(md_path)
            results.append(
                ContentPair(
                    md_path=md_path,
                    image_path=image_path,
                    title=title,
                    body=body,
                    tags=tags,
                )
            )

        return results

    def _find_image(self, md_path: Path) -> Path | None:
        """查找同名图片文件（.png/.jpg/.jpeg）。

        按 .png → .jpg → .jpeg 顺序查找，返回第一个存在的文件。
        """
        stem = md_path.stem
        for ext in IMAGE_EXTENSIONS:
            image_path = md_path.parent / f"{stem}{ext}"
            if image_path.exists():
                return image_path
        return None

    def _parse_markdown(self, md_path: Path) -> tuple[str, str, list[str]]:
        """解析 Markdown 文件，返回 (标题, 正文, 标签列表)。

        - 标题：第一个 `# ` 开头的行，去除前缀后截断至20字符
        - 正文：标题行之后的所有内容（不含标签区域的 --- 分隔线及之后内容）
        - 标签：`---` 分隔线之后的 `#标签名` 格式文本
        """
        content = md_path.read_text(encoding="utf-8")
        lines = content.split("\n")

        # 找到标题行
        title_line_idx = -1
        raw_title = ""
        for i, line in enumerate(lines):
            if line.startswith("# "):
                raw_title = line[2:].strip()
                title_line_idx = i
                break

        title = self._extract_title(raw_title)
        tags = self._extract_tags(content)

        # 正文：标题行之后的所有内容，去除末尾标签区域
        if title_line_idx >= 0:
            body_lines = lines[title_line_idx + 1 :]
        else:
            body_lines = lines

        # 从末尾向前查找 --- 分隔线，移除标签区域
        separator_idx = -1
        for i in range(len(body_lines) - 1, -1, -1):
            if body_lines[i].strip() == "---":
                separator_idx = i
                break

        if separator_idx >= 0:
            body_lines = body_lines[:separator_idx]

        body = "\n".join(body_lines)
        # 去除正文开头的空行
        body = body.lstrip("\n")
        # 去除正文末尾的空白
        body = body.rstrip()

        return title, body, tags

    def _extract_title(self, first_heading: str) -> str:
        """提取标题，超过20字符自动截断。"""
        if len(first_heading) <= MAX_TITLE_LENGTH:
            return first_heading
        return first_heading[:MAX_TITLE_LENGTH]

    def _extract_tags(self, content: str) -> list[str]:
        """从文件末尾 `---` 分隔线之后提取 `#标签名` 格式的话题标签。

        返回不含 # 前缀的标签名列表。
        """
        lines = content.split("\n")

        # 从末尾向前查找 --- 分隔线
        separator_idx = -1
        for i in range(len(lines) - 1, -1, -1):
            if lines[i].strip() == "---":
                separator_idx = i
                break

        if separator_idx < 0:
            return []

        # 取分隔线之后的内容
        tag_section = "\n".join(lines[separator_idx + 1 :])

        # 提取 #标签名 格式的标签（不含 # 前缀）
        tags = re.findall(r"#(\S+)", tag_section)
        return tags


# @AI_GENERATED: end
