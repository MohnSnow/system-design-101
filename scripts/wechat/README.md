<!-- @AI_GENERATED -->
# 微信公众号自动发布工具

基于 Python + Playwright 的浏览器自动化脚本，将已发布到小红书的内容（Markdown + 图片）批量保存为微信公众号草稿。

## 项目结构

```
scripts/wechat/
├── main.py              # CLI 入口
├── content_parser.py    # 内容扫描与过滤（排除已发微信的）
├── browser_connector.py # CDP 连接已有 Chrome
├── publisher.py         # Token 提取 + 编辑页面交互 + 保存草稿
└── tests/

scripts/redbook/         # 复用的模块
├── models.py            # ContentPair, PublishResult, BatchSummary
└── file_archiver.py     # 文件归档
```

## 前置条件

- 小红书自动发布工具的虚拟环境已安装（`scripts/redbook/.venv/`）
- Chrome 浏览器已安装

## 使用方式

### 1. 启动 Chrome 调试模式

先关掉所有 Chrome，然后用调试端口启动：

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
```

### 2. 登录微信公众号后台

在 Chrome 中打开 https://mp.weixin.qq.com 并登录。保持页面打开。

### 3. 运行脚本

```bash
# 默认批量发布 1 篇
scripts/redbook/.venv/bin/python3 -m scripts.wechat.main

# 自定义批量数量
scripts/redbook/.venv/bin/python3 -m scripts.wechat.main --batch-size 5
```

## 工作流程

1. 扫描 `data/0.redbook_published/` 目录，排除 `wechat_published/` 中已发布的
2. 通过 CDP 连接已打开的 Chrome 浏览器
3. 从已打开的微信公众号后台页面 URL 中自动提取 Token
4. 逐篇打开编辑页面：上传封面图 → 填写标题 → 填写正文 → 保存为草稿
5. 成功后将文件从 `data/0.redbook_published/` 移动到 `data/0.redbook_published/wechat_published/`
6. 输出发布摘要

## 内容来源

内容来自 `data/0.redbook_published/`（已发布到小红书的内容），格式和小红书一样：

```
data/0.redbook_published/
├── some-article.md
├── some-article.png
├── wechat_published/     # 已发布到微信的（自动排除）
│   ├── old-article.md
│   └── old-article.png
```

## 故障排查

| 问题 | 解决方案 |
|------|----------|
| `无法连接到 Chrome 浏览器` | 确认 Chrome 以 `--remote-debugging-port=9222` 启动 |
| `未找到微信公众号后台页面` | 在 Chrome 中打开 https://mp.weixin.qq.com 并保持登录 |
| `Token 获取失败` | 刷新微信公众号后台页面后重试 |
| 封面图上传失败 | 确认图片文件存在且格式正确 |
| 选择器定位失败 | 微信后台页面可能改版，需更新 `publisher.py` 中的选择器 |
<!-- @AI_GENERATED: end -->
