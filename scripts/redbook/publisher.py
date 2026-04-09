# @AI_GENERATED
"""小红书自动发布工具 - 发布器

驱动 Playwright 完成单篇发布到草稿箱的全流程。

小红书创作者平台页面结构（基于实际 DOM 探测）：
- 初始页面默认是"上传视频"tab
- 需要点击 div.creator-tab > span.title 文本为"上传图文"来切换
- 切换后进入编辑模式：
  - input[type=file] accept=.jpg,.jpeg,.png,.webp（图片上传）
  - div.tiptap.ProseMirror（正文 contenteditable 编辑器）
  - button.topic-btn（话题按钮）
  - button.save-btn 文本"暂存离开"（保存草稿）
  - button.bg-red 文本"发布"（直接发布）
- 标题没有独立输入框，在正文编辑器中输入
"""

from __future__ import annotations

from pathlib import Path

from playwright.async_api import BrowserContext, Page

from .models import ContentPair, PublishResult


CREATOR_PUBLISH_URL = "https://creator.xiaohongshu.com/publish/publish?source=official"

# 各步骤默认超时时间（毫秒）
DEFAULT_TIMEOUT = 30000
UPLOAD_TIMEOUT = 60000
TAG_SEARCH_TIMEOUT = 5000


class Publisher:
    """小红书发布器"""

    def __init__(self, context: BrowserContext):
        self.context = context

    # @AI_GENERATED
    async def publish_batch(
        self, contents: list[ContentPair], batch_size: int = 5
    ) -> list[PublishResult]:
        """批量发布多组内容。"""
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
    # @AI_GENERATED: end

    async def publish_one(self, content: ContentPair) -> PublishResult:
        """执行单篇发布到草稿箱的完整流程。"""
        page: Page | None = None
        try:
            page = await self.context.new_page()

            # 打开创作者平台发布页面
            await page.goto(
                CREATOR_PUBLISH_URL,
                wait_until="domcontentloaded",
                timeout=DEFAULT_TIMEOUT,
            )
            await page.wait_for_timeout(2000)

            # 步骤 0：切换到"上传图文"tab
            await self._switch_to_image_tab(page)

            # 步骤 1：上传图片
            await self._upload_image(page, content.image_path)

            # 步骤 2：填写标题
            await self._fill_title(page, content.title)

            # 步骤 3：填写正文
            await self._fill_body(page, content.body)

            # 步骤 4：添加话题标签（点击推荐标签）
            unmatched_tags: list[str] = []
            if content.tags:
                unmatched_tags = await self._add_tags(page, content.tags)
                for tag in unmatched_tags:
                    print(f"⚠️ 话题标签未匹配: #{tag}，请手动添加")

            # 步骤 5：加入 System-Design 合集
            await self._join_collection(page, "System-Design")

            # 步骤 6：发布
            await self._save_draft(page)

            return PublishResult(content=content, success=True)

        except Exception as e:
            error_msg = f"{type(e).__name__}: {e}"
            print(f"❌ 发布失败 [{content.title}]: {error_msg}")
            return PublishResult(content=content, success=False, error=error_msg)
        finally:
            if page:
                await page.close()

    async def _switch_to_image_tab(self, page: Page) -> None:
        """切换到"上传图文"tab。

        小红书创作者平台默认是"上传视频"tab。
        由于 tab 元素可能在视口外导致 click 失败，
        使用 JavaScript 直接触发点击来切换。
        """
        # 用 JS 找到文本为"上传图文"且没有 active class 的 tab 并点击
        clicked = await page.evaluate("""() => {
            const tabs = document.querySelectorAll('div.creator-tab');
            for (const tab of tabs) {
                const text = tab.textContent.trim();
                if (text === '上传图文' && !tab.classList.contains('active')) {
                    tab.click();
                    return true;
                }
            }
            // 检查是否已经在上传图文 tab
            for (const tab of tabs) {
                const text = tab.textContent.trim();
                if (text === '上传图文' && tab.classList.contains('active')) {
                    return true;
                }
            }
            return false;
        }""")

        if not clicked:
            raise Exception("未找到上传图文 tab")

        await page.wait_for_timeout(2000)
        print("📑 已切换到上传图文 tab")

    async def _upload_image(self, page: Page, image_path: Path) -> None:
        """上传图片。

        切换到上传图文 tab 后，页面有 input[type=file] accept=.jpg,.jpeg,.png,.webp，
        直接通过 set_input_files 上传。
        """
        file_inputs = page.locator('input[type="file"]')
        count = await file_inputs.count()

        uploaded = False
        for i in range(count):
            fi = file_inputs.nth(i)
            accept = await fi.get_attribute("accept") or ""
            if any(ext in accept for ext in [".jpg", ".jpeg", ".png"]):
                await fi.set_input_files(str(image_path))
                uploaded = True
                break

        if not uploaded:
            if count > 0:
                await file_inputs.first.set_input_files(str(image_path))
            else:
                raise Exception("未找到图片上传的 file input")

        # 等待图片上传和页面编辑区域出现
        await page.wait_for_timeout(5000)
        print(f"🖼️ 图片已上传: {image_path.name}")

    async def _fill_title(self, page: Page, title: str) -> None:
        """填写标题。

        上传图片后出现标题输入框：
        input[placeholder='填写标题会有更多赞哦'] class=d-text
        """
        title_input = page.locator("input[placeholder='填写标题会有更多赞哦']").first
        await title_input.wait_for(state="visible", timeout=DEFAULT_TIMEOUT)
        await title_input.click()
        await title_input.fill(title)
        await page.wait_for_timeout(500)
        print(f"📌 标题已填写: {title}")

    async def _fill_body(self, page: Page, body: str) -> None:
        """填写正文。先将 Markdown 转为纯文本，再输入到编辑器。"""
        from .utils import markdown_to_plain

        plain_body = markdown_to_plain(body)
        editor = page.locator("div.tiptap.ProseMirror").first
        await editor.wait_for(state="visible", timeout=DEFAULT_TIMEOUT)
        await editor.click()
        await page.keyboard.type(plain_body, delay=10)
        await page.wait_for_timeout(500)
        print("📝 正文已填写")

    async def _add_tags(self, page: Page, tags: list[str]) -> list[str]:
        """添加话题标签。

        先在正文编辑器中按两次 Enter 换行（和正文隔开），
        然后点击推荐话题标签。
        """
        unmatched: list[str] = []

        # 先在编辑器中按两次 Enter，让话题和正文之间有空行
        editor = page.locator("div.tiptap.ProseMirror").first
        await editor.click()
        await page.keyboard.press("Enter")
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(300)

        for tag in tags:
            try:
                # 尝试点击推荐标签区域中匹配的标签
                # 推荐标签格式：span.tag 文本为 "#技术干货" 等
                recommended = page.locator(
                    f"div.recommend-topic-wrapper span.tag:has-text('#{tag}')"
                )
                if await recommended.count() > 0:
                    await recommended.first.click(timeout=3000)
                    await page.wait_for_timeout(500)
                    print(f"🏷️ 已添加推荐话题: #{tag}")
                else:
                    unmatched.append(tag)
            except Exception:
                unmatched.append(tag)

        return unmatched

    async def _join_collection(self, page: Page, collection_name: str) -> None:
        """加入指定合集。

        在发布页面下方"内容设置"区域，点击"选择合集"，
        然后从下拉列表中选择指定的合集名称。
        """
        try:
            # 向下滚动让"内容设置"区域可见
            await page.evaluate("window.scrollBy(0, 500)")
            await page.wait_for_timeout(1000)

            # 点击"选择合集"链接
            select_btn = page.locator("text=选择合集").first
            await select_btn.click(timeout=5000)
            await page.wait_for_timeout(1000)

            # 从下拉列表中选择合集
            collection_option = page.locator(f"text={collection_name}").first
            await collection_option.click(timeout=5000)
            await page.wait_for_timeout(500)

            print(f"📂 已加入合集: {collection_name}")
        except Exception as e:
            print(f"⚠️ 加入合集失败: {e}，请手动添加")

    async def _save_draft(self, page: Page) -> None:
        """点击"发布"按钮直接发布笔记。

        小红书草稿箱是浏览器本地存储，关掉浏览器就没了，
        所以直接点击"发布"按钮发布到小红书。
        """
        clicked = await page.evaluate("""() => {
            const buttons = document.querySelectorAll('button');
            for (const btn of buttons) {
                const text = btn.textContent.trim();
                if (text === '发布') {
                    btn.click();
                    return true;
                }
            }
            return false;
        }""")

        if not clicked:
            raise Exception("未找到发布按钮")

        await page.wait_for_timeout(5000)
        print("🚀 已发布")
# @AI_GENERATED: end