# @AI_GENERATED
"""小红书自动发布工具 - CLI 入口

支持单篇模式和批量模式，串联内容解析、Cookie 认证、发布、归档全流程。

用法：
    python -m scripts.redbook.main              # 单篇模式（发布第一组有效内容）
    python -m scripts.redbook.main --batch       # 批量模式（默认5篇）
    python -m scripts.redbook.main --batch --batch-size 3  # 批量模式，自定义批量大小
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

from playwright.async_api import async_playwright

from .browser_auth import AuthenticationError, BrowserAuth
from .content_parser import ContentParser
from .file_archiver import FileArchiver
from .models import BatchSummary, PublishResult
from .publisher import Publisher


# 默认目录路径（相对于项目根目录）
PENDING_DIR = Path("data/1.redbook")
PUBLISHED_DIR = Path("data/0.redbook_published")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """解析命令行参数。"""
    parser = argparse.ArgumentParser(
        description="小红书自动发布工具 - 将本地 Markdown + 图片自动发布到小红书草稿箱"
    )
    parser.add_argument(
        "--batch",
        action="store_true",
        default=False,
        help="启用批量模式（默认为单篇模式）",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=5,
        help="批量模式下每次发布的篇数（默认 5）",
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
    """CLI 主入口：解析 → 认证 → 发布 → 归档。"""
    args = parse_args(argv)

    batch_mode = args.batch
    batch_size = args.batch_size

    mode_label = f"批量模式（每次 {batch_size} 篇）" if batch_mode else "单篇模式"
    print(f"🚀 小红书自动发布工具启动 - {mode_label}")

    # 步骤 1：内容解析
    print("\n📂 正在扫描待发布目录...")
    parser = ContentParser(PENDING_DIR)
    contents = parser.scan()

    if not contents:
        print("📭 没有找到有效的内容组，退出。")
        return

    print(f"📋 发现 {len(contents)} 组有效内容")

    # 步骤 2：Cookie 认证
    print("\n🔐 正在加载 Cookie 认证...")
    try:
        cookie_string = BrowserAuth.load_cookie()
        auth = BrowserAuth(cookie_string)
        print("✅ Cookie 加载成功")
    except AuthenticationError as e:
        print(f"❌ 认证失败: {e}")
        sys.exit(1)

    # 步骤 3：启动浏览器并发布
    # 优先连接已有 Chrome，失败则启动新的持久化浏览器
    async with async_playwright() as p:
        context = None
        is_cdp = False
        try:
            print("\n🌐 尝试连接已有的 Chrome 浏览器...")
            context = await auth.connect_existing_browser(p)
            is_cdp = True
            print("✅ 已连接到已有的 Chrome 浏览器")
        except AuthenticationError as e:
            print(f"⚠️ {e}")
            print("🌐 启动新的浏览器...")
            context = await auth.create_persistent_context(p)

        try:
            print("🔍 正在验证认证状态...")
            try:
                await auth.verify_auth(context)
                print("✅ 认证验证通过")
            except AuthenticationError as e:
                print(f"❌ 认证验证失败: {e}")
                if not is_cdp:
                    await context.close()
                sys.exit(1)

            publisher = Publisher(context)
            results: list[PublishResult]

            if batch_mode:
                print(f"\n📤 开始批量发布（最多 {batch_size} 篇）...")
                results = await publisher.publish_batch(contents, batch_size=batch_size)
            else:
                first = contents[0]
                print(f"\n📤 开始单篇发布：{first.title}")
                result = await publisher.publish_one(first)
                results = [result]

            # 步骤 4：归档成功发布的内容
            print("\n📦 正在归档已发布内容...")
            archiver = FileArchiver(PENDING_DIR, PUBLISHED_DIR)
            for r in results:
                if r.success:
                    archiver.archive(r.content)

            # 步骤 5：输出摘要
            summary = BatchSummary.from_results(results)
            print_summary(summary)

        finally:
            # 不关闭浏览器，让用户可以检查发布结果
            pass


if __name__ == "__main__":
    asyncio.run(main())
# @AI_GENERATED: end
