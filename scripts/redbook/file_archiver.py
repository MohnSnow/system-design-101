# @AI_GENERATED
"""小红书自动发布工具 - 文件归档器

将已成功发布的内容组文件从待发布目录移动到已发布目录。
"""

from __future__ import annotations

import shutil
from pathlib import Path

from .models import ContentPair


class FileArchiver:
    """文件归档器：将已发布内容的文件移动到已发布目录。"""

    def __init__(self, pending_dir: Path, published_dir: Path):
        self.pending_dir = pending_dir
        self.published_dir = published_dir

    def archive(self, content: ContentPair) -> bool:
        """将内容组的 Markdown 和图片文件移动到已发布目录。

        已发布目录不存在时自动创建。
        文件移动失败时记录错误，保留原文件不删除。

        Returns:
            True 表示所有文件归档成功，False 表示至少有一个文件归档失败。
        """
        # 确保已发布目录存在
        try:
            self.published_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            print(f"❌ 无法创建已发布目录 {self.published_dir}: {e}")
            return False

        files_to_move = [content.md_path, content.image_path]
        all_success = True

        for src in files_to_move:
            dst = self.published_dir / src.name
            try:
                shutil.move(str(src), str(dst))
                print(f"📦 已归档: {src.name} → {self.published_dir.name}/")
            except (OSError, shutil.Error) as e:
                print(f"❌ 归档失败 {src.name}: {e}")
                all_success = False

        return all_success


# @AI_GENERATED: end
