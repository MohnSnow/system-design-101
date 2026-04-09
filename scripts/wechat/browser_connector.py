# @AI_GENERATED
"""微信公众号自动发布工具 - 浏览器连接模块

支持两种模式：
1. CDP 连接已有 Chrome（优先）
2. 启动 persistent context 浏览器（fallback）
"""

from __future__ import annotations

from pathlib import Path

from playwright.async_api import BrowserContext, Playwright


CDP_PORT = 9222
CDP_URL = f"http://127.0.0.1:{CDP_PORT}"
BROWSER_DATA_DIR = Path(__file__).parent / ".browser_data"


class BrowserConnector:
    """浏览器连接器，优先 CDP，fallback 到 persistent context。"""

    async def connect(self, pw: Playwright) -> tuple[BrowserContext, bool]:
        """连接浏览器，返回 (context, is_cdp)。

        优先尝试 CDP 连接已有 Chrome，失败则启动 persistent context。
        is_cdp=True 表示连接的是已有浏览器，脚本结束后不应关闭。
        """
        # 尝试 CDP
        try:
            browser = await pw.chromium.connect_over_cdp(CDP_URL)
            if browser.contexts:
                return browser.contexts[0], True
            return await browser.new_context(), True
        except Exception:
            pass

        # Fallback: persistent context
        print("⚠️ 未检测到 Chrome 调试端口，启动新浏览器...")
        print("  提示：用以下命令启动 Chrome 可复用已登录会话：")
        print(f"  /Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --remote-debugging-port={CDP_PORT}")
        BROWSER_DATA_DIR.mkdir(parents=True, exist_ok=True)
        context = await pw.chromium.launch_persistent_context(
            user_data_dir=str(BROWSER_DATA_DIR),
            headless=False,
            locale="zh-CN",
        )
        return context, False
# @AI_GENERATED: end