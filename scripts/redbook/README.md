<!-- @AI_GENERATED -->
# 小红书自动发布工具

基于 Python + Playwright 的浏览器自动化脚本，将本地 Markdown + 图片文件自动发布到小红书创作者平台草稿箱。

## 项目结构

```
scripts/redbook/
├── main.py             # CLI 入口
├── models.py           # 数据模型（ContentPair, PublishResult, BatchSummary）
├── content_parser.py   # 内容解析器（扫描目录、解析 md、配对图片）
├── browser_auth.py     # Cookie 认证（加载、注入、验证）
├── publisher.py        # 发布器（Playwright 驱动发布到草稿箱）
├── file_archiver.py    # 文件归档（发布后移动文件）
├── requirements.txt    # Python 依赖
└── .venv/              # 虚拟环境
```

## 安装

```bash
# 创建虚拟环境（如果还没有）
python3 -m venv scripts/redbook/.venv

# 安装依赖
scripts/redbook/.venv/bin/pip install -r scripts/redbook/requirements.txt

# 安装 Chromium 浏览器
scripts/redbook/.venv/bin/playwright install chromium
```

## 配置 Cookie

在项目根目录创建 `.env` 文件：

```env
XHS_COOKIE=你的小红书cookie字符串
```

### 获取 Cookie 方法

1. 用 Chrome 打开 https://creator.xiaohongshu.com 并登录
2. 按 F12 打开开发者工具 → Application → Cookies
3. 复制所有 cookie 键值对，格式为 `key1=value1; key2=value2; ...`
4. 或者在 Network 面板中复制任意请求的 `Cookie` 请求头

也可以通过环境变量设置（优先级更高）：

```bash
export XHS_COOKIE="你的cookie字符串"
```

## 使用方式

所有命令在项目根目录下执行：

```bash
# 单篇模式 — 发布第一组有效内容到草稿箱
scripts/redbook/.venv/bin/python -m scripts.redbook.main

# 批量模式 — 发布前 5 组到草稿箱
scripts/redbook/.venv/bin/python -m scripts.redbook.main --batch

# 自定义批量数量
scripts/redbook/.venv/bin/python -m scripts.redbook.main --batch --batch-size 3
```

## 内容格式

每组内容由一个 `.md` 文件和同名图片文件组成，存放在 `data/1.redbook/` 目录：

```
data/1.redbook/
├── fixing-bugs-automatically-at-meta-scale.md
├── fixing-bugs-automatically-at-meta-scale.png
├── git-commands-cheat-sheet.md
├── git-commands-cheat-sheet.png
└── ...
```

Markdown 文件格式：

```markdown
# 标题（不超过20字，超出自动截断）

> 引用/副标题（可选）

![图片描述](同名图片文件)

正文内容...

---

#标签1 #标签2 #标签3
```

图片支持 `.png`、`.jpg`、`.jpeg` 格式。没有同名图片的 md 文件会被跳过。

## 发布流程

1. 扫描 `data/1.redbook/` 目录，按文件名排序，配对 md + 图片
2. 加载 Cookie 并验证认证状态
3. 打开小红书创作者平台发布页面
4. 上传图片 → 填写标题 → 填写正文 → 添加话题标签 → 点击"存草稿"
5. 发布成功后，自动将文件移动到 `data/0.redbook_published/`
6. 输出发布摘要（成功/失败/跳过数量）

## 注意事项

- 浏览器默认以 **有头模式**（headed）运行，方便观察和调试
- 话题标签会尝试自动搜索匹配，无法匹配的会提示手动添加
- Cookie 过期后需要重新获取并更新 `.env` 文件
- 单篇发布失败不会中断批量流程
- Playwright 选择器基于小红书创作者平台当前页面结构，如果平台改版可能需要更新选择器
- 首次运行建议用单篇模式测试，确认流程正常后再批量发布

## 故障排查

| 问题 | 解决方案 |
|------|----------|
| `AuthenticationError: 未找到小红书 Cookie` | 检查 `.env` 文件或环境变量 `XHS_COOKIE` |
| `Cookie 无效或已过期` | 重新登录小红书创作者平台获取新 Cookie |
| `TimeoutError` 页面加载超时 | 检查网络连接，或增加超时时间 |
| 选择器定位失败 | 小红书页面可能改版，需要更新 `publisher.py` 中的选择器 |
| 图片上传失败 | 确认图片文件存在且格式正确（png/jpg/jpeg） |
<!-- @AI_GENERATED: end -->
