# @AI_GENERATED
"""微信公众号自动发布工具 - 发布器

驱动 Playwright 完成单篇发布到草稿箱的全流程。

微信公众号后台编辑页面结构：
- 封面图上传：input[type=file] 或点击上传区域
- 标题输入框：placeholder 为"请在这里输入标题"
- 正文编辑区域：contenteditable div 或 iframe
- 保存按钮：文本为"保存为草稿"
"""

from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from dotenv import dotenv_values
from playwright.async_api import BrowserContext, Page

from scripts.redbook.models import ContentPair, PublishResult
from scripts.redbook.utils import markdown_to_plain


EDIT_PAGE_URL_TEMPLATE = (
    "https://mp.weixin.qq.com/cgi-bin/appmsg"
    "?t=media/appmsg_edit_v2&action=edit&isNew=1"
    "&type=77&createType=8&token={token}&lang=zh_CN"
)

DEFAULT_TIMEOUT = 30_000
UPLOAD_TIMEOUT = 60_000


def load_wechat_token() -> str:
    """从环境变量或 .env 文件读取 WECHAT_TOKEN。"""
    token = os.environ.get("WECHAT_TOKEN", "").strip()
    if token:
        return token
    env_path = Path.cwd() / ".env"
    if env_path.exists():
        env_values = dotenv_values(env_path)
        token = env_values.get("WECHAT_TOKEN", "").strip()
        if token:
            return token
    raise RuntimeError(
        "未找到微信公众号 Token。请在 .env 文件中配置 WECHAT_TOKEN=你的token"
    )


class WechatPublisher:
    """微信公众号发布器"""

    def __init__(self, context: BrowserContext, token: str):
        self.context = context
        self.token = token

    # ------------------------------------------------------------------
    # Task 5.2: 单篇发布
    # ------------------------------------------------------------------

    async def publish_one(self, content: ContentPair) -> PublishResult:
        """执行单篇发布到草稿箱的完整流程。

        流程：打开编辑页面 → 上传封面图 → 填写标题 → 填写正文 → 保存为草稿。
        任何步骤异常均捕获并返回失败结果，不中断后续发布。
        """
        page: Page | None = None
        try:
            edit_url = EDIT_PAGE_URL_TEMPLATE.format(token=self.token)
            page = await self.context.new_page()

            await page.goto(
                edit_url,
                wait_until="domcontentloaded",
                timeout=DEFAULT_TIMEOUT,
            )
            await page.wait_for_timeout(3000)

            # 步骤 1：上传封面图
            await self._upload_cover(page, content.image_path)

            # 步骤 2：填写标题
            await self._fill_title(page, content.title)

            # 步骤 3：填写正文（含话题标签）
            await self._fill_body(page, content.body, content.tags)

            # 步骤 4：保存为草稿
            await self._save_draft(page)

            return PublishResult(content=content, success=True)

        except Exception as e:
            error_msg = f"{type(e).__name__}: {e}"
            print(f"❌ 发布失败 [{content.title}]: {error_msg}")
            return PublishResult(content=content, success=False, error=error_msg)

    async def _upload_cover(self, page: Page, image_path: Path) -> None:
        """上传封面图。

        微信封面图使用 webuploader 组件，file input 是 display:none 的。
        通过 JS 让 file input 可见，然后用 set_input_files 设置文件，
        最后触发 webuploader 的 change 事件。
        """
        abs_path = str(Path(image_path).resolve())

        try:
            # 用 JS 找到封面图区域的 file input 并让它可见
            await page.evaluate("""() => {
                const container = document.querySelector('.js_upload_btn_container');
                if (container) {
                    const input = container.querySelector('input[type="file"]');
                    if (input) {
                        input.style.display = 'block';
                        input.style.visibility = 'visible';
                        input.style.opacity = '1';
                        input.style.position = 'relative';
                        input.style.width = '100px';
                        input.style.height = '30px';
                    }
                }
            }""")
            await page.wait_for_timeout(500)

            # 现在 file input 可见了，用 set_input_files 设置文件
            cover_input = page.locator("div.js_upload_btn_container input[type='file']").first
            await cover_input.set_input_files(abs_path)
            await page.wait_for_timeout(5000)
            print(f"🖼️ 封面图已上传: {image_path.name}")
        except Exception as e:
            print(f"⚠️ 封面图上传失败: {e}，请手动上传")

    async def _fill_title(self, page: Page, title: str) -> None:
        """填写标题。微信标题是 div.title-editor__input（contenteditable div）。"""
        title_editor = page.locator("div.title-editor__input").first
        await title_editor.wait_for(state="visible", timeout=DEFAULT_TIMEOUT)
        await title_editor.click()
        await page.keyboard.type(title, delay=20)
        await page.wait_for_timeout(500)
        print(f"📌 标题已填写: {title}")

    async def _fill_body(self, page: Page, body: str, tags: list[str] | None = None) -> None:
        """填写正文。先转纯文本，再追加话题标签。"""
        plain_body = markdown_to_plain(body)

        # 追加话题标签（换行后直接加 #标签）
        if tags:
            tag_line = " ".join(f"#{t}" for t in tags)
            plain_body = plain_body + "\n\n" + tag_line

        editors = page.locator("div.ProseMirror")
        count = await editors.count()
        editor = editors.nth(1) if count > 1 else editors.first
        await editor.wait_for(state="visible", timeout=DEFAULT_TIMEOUT)
        await editor.click()
        await page.keyboard.type(plain_body, delay=10)
        await page.wait_for_timeout(500)
        print("📝 正文已填写")

    async def _save_draft(self, page: Page) -> None:
        """点击"保存为草稿"按钮。等待10秒让封面图等内容处理完毕。"""
        # 等待10秒，确保封面图上传和内容都处理完毕
        print("⏳ 等待10秒让内容处理完毕...")
        await page.wait_for_timeout(10000)
        clicked = await page.evaluate("""() => {
            const buttons = document.querySelectorAll('button, a, div[role="button"]');
            for (const btn of buttons) {
                const text = btn.textContent.trim();
                if (text.includes('保存为草稿')) {
                    btn.click();
                    return true;
                }
            }
            return false;
        }""")

        if not clicked:
            draft_btn = page.locator("text=保存为草稿").first
            await draft_btn.click(timeout=DEFAULT_TIMEOUT)

        await page.wait_for_timeout(5000)

        # 检测是否有错误提示
        error_text = await page.evaluate("""() => {
            // 查找常见的错误提示元素
            const tips = document.querySelectorAll('.weui-desktop-tooltip, .tips_global, .global_error, [class*="error"], [class*="toast"]');
            for (const tip of tips) {
                const text = tip.textContent.trim();
                if (text && (text.includes('失败') || text.includes('错误') || text.includes('error'))) {
                    return text;
                }
            }
            return null;
        }""")

        if error_text:
            raise Exception(f"保存草稿失败: {error_text}")

        print("💾 已保存为草稿")

    # ------------------------------------------------------------------
    # Task 5.3: 批量发布
    # ------------------------------------------------------------------

    async def publish_batch(
        self, contents: list[ContentPair], batch_size: int = 5
    ) -> list[PublishResult]:
        """批量发布多组内容。

        按顺序逐篇执行发布流程，输出进度信息。
        单篇失败不影响后续内容的发布。

        Args:
            contents: 待发布的内容组列表。
            batch_size: 每次最多发布篇数。

        Returns:
            各篇发布结果列表。
        """
        batch = contents[:batch_size]
        total = len(batch)
        results: list[PublishResult] = []

        for idx, content in enumerate(batch, start=1):
            print(f"正在发布第 {idx}/{total} 篇：{content.title}")
            result = await self.publish_one(content)
            results.append(result)

            if result.success:
                print(f"✅ 第 {idx}/{total} 篇发布成功：{content.title}")
            elif result.error is not None:
                print(f"❌ 第 {idx}/{total} 篇发布失败：{content.title}")
            else:
                print(f"⏭️ 第 {idx}/{total} 篇已跳过：{content.title}")

        return results


# ------------------------------------------------------------------
# 纯函数工具：Token 提取与 URL 构造（便于单元测试）
# ------------------------------------------------------------------


def extract_token_from_url(url: str) -> str | None:
    """从 URL 的 query string 中提取 token 参数值。

    Args:
        url: 包含 token 参数的 URL。

    Returns:
        token 字符串，未找到时返回 None。
    """
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    tokens = params.get("token")
    if tokens:
        return tokens[0]
    return None


def build_edit_url(token: str) -> str:
    """使用 token 构造微信公众号编辑页面 URL。

    Args:
        token: 微信公众号后台 token。

    Returns:
        完整的编辑页面 URL。
    """
    return EDIT_PAGE_URL_TEMPLATE.format(token=token)
# @AI_GENERATED: end
