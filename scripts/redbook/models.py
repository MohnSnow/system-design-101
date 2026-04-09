# @AI_GENERATED
"""小红书自动发布工具 - 数据模型定义"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ContentPair:
    """一组待发布内容：Markdown 文件与同名图片文件的配对"""

    md_path: Path  # Markdown 文件路径
    image_path: Path  # 图片文件路径
    title: str  # 解析后的标题（已截断至20字符）
    body: str  # 正文内容（不含标题行）
    tags: list[str] = field(default_factory=list)  # 话题标签列表，不含 # 前缀


@dataclass
class PublishResult:
    """单篇发布结果"""

    content: ContentPair  # 对应的内容组
    success: bool  # 是否发布成功
    error: str | None = None  # 失败时的错误信息


@dataclass
class BatchSummary:
    """批量发布摘要"""

    total: int  # 总处理数量
    success_count: int  # 成功数量
    fail_count: int  # 失败数量
    skip_count: int  # 跳过数量（无图片配对等）
    results: list[PublishResult] = field(default_factory=list)  # 各篇发布结果详情

    @classmethod
    def from_results(cls, results: list[PublishResult]) -> BatchSummary:
        """从 PublishResult 列表生成批量发布摘要"""
        total = len(results)
        success_count = sum(1 for r in results if r.success)
        fail_count = sum(1 for r in results if not r.success and r.error is not None)
        skip_count = total - success_count - fail_count
        return cls(
            total=total,
            success_count=success_count,
            fail_count=fail_count,
            skip_count=skip_count,
            results=results,
        )


# @AI_GENERATED: end
