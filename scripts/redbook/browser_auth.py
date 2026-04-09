# @AI_GENERATED
"""小红书自动发布工具 - Cookie 认证模块

支持两种浏览器模式：
1. 连接已有 Chrome（通过 CDP 调试端口）— 推荐，复用已登录的浏览器
2. 启动新的持久化浏览器 — 备选方案
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import dotenv_values
from playwright.async_api import BrowserContext, Playwright


CREATOR_PLATFORM_URL = "https://creator.xiaohongshu.com"
COOKIE_DOMAIN = ".xiaohongshu.com"
BROWSER_DATA_DIR = Path(__file__).parent / ".browser_data"

# Chrome CDP 调试端口
CDP_PORT = 9222
CDP_URL = f"http://localhost:{CDP_PORT}"


class AuthenticationError(Exception):
    """Cookie 认证失败时抛出的异常"""
    pass


class BrowserAuth:
    """Cookie 认证管理器"""

    def __init__(self, cookie_string: str):
        self.cookie_string = cookie_string

    @staticmethod
    def load_cookie() -> str:
        """从环境变量或 .env 文件中读取 Cookie 字符串。"""
        cookie = os.environ.get("XHS_COOKIE", "").strip()
        if cookie:
            return cookie

        env_path = Path.cwd() / ".env"
        if env_path.exists():
            env_values = dotenv_values(env_path)
            cookie = env_values.get("XHS_COOKIE", "").strip()
            if cookie:
                return cookie

        raise AuthenticationError(
            "未找到小红书 Cookie 配置。请设置环境变量 XHS_COOKIE 或在 .env 文件中配置 XHS_COOKIE=..."
        )

    async def connect_existing_browser(self, pw: Playwright) -> BrowserContext:
        """连接到已打开的 Chrome 浏览器（通过 CDP 调试端口）。

        需要先用以下命令启动 Chrome：
        macOS:
          /Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --remote-debugging-port=9222

        连接后注入 Cookie 到已有的浏览器上下文。
        """
        try:
            browser = await pw.chromium.connect_over_cdp(CDP_URL)
            # 使用已有的 context（第一个）
            if browser.contexts:
                context = browser.contexts[0]
            else:
                context = await browser.new_context()

            # 注入 Cookie
            await self._inject_cookies(context)
            return context
        except Exception as e:
            raise AuthenticationError(
                f"无法连接到已有的 Chrome 浏览器（端口 {CDP_PORT}）。\n"
                f"请先启动 Chrome 调试模式：\n"
                f'  /Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --remote-debugging-port={CDP_PORT}\n'
                f"错误: {e}"
            ) from e

    async def create_persistent_context(self, pw: Playwright) -> BrowserContext:
        """创建持久化浏览器上下文（备选方案）。"""
        BROWSER_DATA_DIR.mkdir(parents=True, exist_ok=True)
        context = await pw.chromium.launch_persistent_context(
            user_data_dir=str(BROWSER_DATA_DIR),
            headless=False,
            locale="zh-CN",
        )
        await self._inject_cookies(context)
        return context

    async def _inject_cookies(self, context: BrowserContext) -> None:
        """将 Cookie 注入到浏览器上下文。"""
        cookies = []
        for pair in self.cookie_string.split(";"):
            pair = pair.strip()
            if not pair or "=" not in pair:
                continue
            name, value = pair.split("=", 1)
            name = name.strip()
            value = value.strip()
            if name:
                cookies.append({
                    "name": name,
                    "value": value,
                    "domain": COOKIE_DOMAIN,
                    "path": "/",
                })
        if cookies:
            await context.add_cookies(cookies)

    async def verify_auth(self, context: BrowserContext) -> bool:
        """验证认证是否有效。"""
        page = await context.new_page()
        try:
            response = await page.goto(
                CREATOR_PLATFORM_URL, wait_until="domcontentloaded", timeout=30000
            )
            if "login" in page.url.lower():
                raise AuthenticationError("Cookie 无效或已过期，请更新 Cookie。")
            if response and response.status >= 400:
                raise AuthenticationError(f"访问失败，HTTP {response.status}。")
            return True
        except AuthenticationError:
            raise
        except Exception as e:
            raise AuthenticationError(f"认证验证错误：{e}") from e
        finally:
            await page.close()
# @AI_GENERATED: end