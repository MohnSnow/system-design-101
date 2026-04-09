# @AI_GENERATED
"""微信公众号自动发布工具 - CLI 入口

将 data/0.redbook_published/ 中已发布到小红书的内容批量保存为微信公众号草稿。

用法：
    python3 -m scripts.wechat.main              # 批量模式（默认5篇）
    python3 -m scripts.wechat.main --batch-size 3  # 自定义批量大小
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

from playwright.async_api import async_playwright

from scripts.redbook.file_archiver import FileArchiver
from scripts.redbook.models import BatchSummary, PublishResult

from .browser_connector import BrowserConnector
from .content_parser import WechatContentParser
from .publisher import WechatPublisher, load_wechat_token


# 目录路径（相对于项目根目录）
SOURCE_DIR = Path("data/0.redbook_published")
ARCHIVE_DIR = Path("data/0.redbook_published/wechat_published")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """解析命令行参数。"""
    parser = argparse.ArgumentParser(
        description="微信公众号自动发布工具 - 将已发布到小红书的内容批量保存为微信公众号草稿"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=1,
        help="每次发布的篇数（默认 1）",
    )
    return parser.parse_args(argv)


def print_summary(summary: BatchSummary) -> None:
    """输出批量发布摘要信息。"""
    print("\n" + "=" * 40)
    print("📊 发布摘要")
    print("=" * 40)
    print(f"  总计: {summary.total} 篇")
    print(f"  ✅ 成功: {summary.success_count} 篇")
    print(f"  ❌ 失败: {summary.fail_count} 篇")
    print(f"  ⏭️ 跳过: {summary.skip_count} 篇")
    print("=" * 40)

    if summary.fail_count > 0:
        print("\n失败详情：")
        for r in summary.results:
            if not r.success and r.error is not None:
                print(f"  - {r.content.title}: {r.error}")


async def main(argv: list[str] | None = None) -> None:
    """CLI 主入口：扫描 → 连接浏览器 → 提取 Token → 批量发布 → 归档 → 输出摘要。"""
    args = parse_args(argv)
    batch_size = args.batch_size

    print(f"🚀 微信公众号自动发布工具启动 - 批量模式（每次 {batch_size} 篇）")

    # 步骤 1：内容扫描
    print("\n📂 正在扫描待发布目录...")
    parser = WechatContentParser(SOURCE_DIR, ARCHIVE_DIR)
    contents = parser.scan()

    if not contents:
        print("📭 没有找到有效的内容组，退出。")
        return

    print(f"📋 发现 {len(contents)} 组有效内容")

    # 步骤 2：加载 Token
    print("\n🔑 正在加载微信公众号 Token...")
    try:
        token = load_wechat_token()
        print(f"✅ Token 加载成功: {token}")
    except RuntimeError as e:
        print(f"❌ {e}")
        sys.exit(1)

    # 步骤 3：连接浏览器（不用 async with，避免退出时关闭浏览器）
    p = await async_playwright().start()
    print("\n🌐 正在连接浏览器...")
    connector = BrowserConnector()
    context, is_cdp = await connector.connect(p)
    if is_cdp:
        print("✅ 已连接到已有的 Chrome 浏览器")
    else:
        print("✅ 已启动新浏览器")

    # 步骤 4：批量发布
    publisher = WechatPublisher(context, token)
    print(f"\n📤 开始发布（最多 {batch_size} 篇）...")
    results: list[PublishResult] = await publisher.publish_batch(
        contents, batch_size=batch_size
    )

    # 步骤 5：归档成功发布的内容
    print("\n📦 正在归档已发布内容...")
    archiver = FileArchiver(SOURCE_DIR, ARCHIVE_DIR)
    for r in results:
        if r.success:
            archiver.archive(r.content)

    # 步骤 6：输出摘要
    summary = BatchSummary.from_results(results)
    print_summary(summary)


if __name__ == "__main__":
    asyncio.run(main())
# @AI_GENERATED: end
