<!-- @AI_GENERATED -->
# 实现计划：微信公众号自动发布工具

## 概述

基于已有的小红书自动发布工具架构，在 `scripts/wechat/` 目录下构建微信公众号自动发布工具。最大化复用 `scripts/redbook/` 的数据模型、文件归档器，适配微信公众号后台的页面结构和发布流程。按模块逐步构建：项目结构 → 内容扫描与过滤 → 浏览器连接 → Token 提取与发布器 → CLI 入口。

## 任务列表

- [x] 1. 项目初始化与目录结构
  - [x] 1.1 创建 `scripts/wechat/` 项目结构
    - 创建 `scripts/wechat/__init__.py`
    - 创建 `scripts/wechat/tests/__init__.py`
    - 确认 `scripts/redbook/models.py` 中的 ContentPair、PublishResult、BatchSummary 可被正常导入
    - _需求: 9.1, 9.2, 9.3_

- [x] 2. 实现 WechatContentParser 内容扫描与过滤
  - [x] 2.1 实现 WechatContentParser 核心逻辑
    - 在 `scripts/wechat/content_parser.py` 中实现 `WechatContentParser` 类
    - 构造函数接收 `source_dir`（`data/0.redbook_published/`）和 `archive_dir`（`data/0.redbook_published/wechat_published/`）
    - 实现 `scan()` 方法：扫描源目录下所有 Markdown 文件，排除归档目录中已存在同名文件的内容，返回按文件名字母顺序排序的 ContentPair 列表
    - 实现 `_get_archived_stems()` 方法：获取归档目录中所有 Markdown 文件的 stem
    - 实现 `_find_image()` 方法：查找同名图片文件（.png/.jpg/.jpeg）
    - 实现 `_parse_markdown()` 方法：解析 Markdown 文件，返回 (标题, 正文, 标签列表)
    - 实现 `_extract_title()` 方法：提取标题，超过20字符自动截断
    - 源目录不存在时输出警告并返回空列表；Markdown 无同名图片时跳过并输出提示
    - 复用小红书 ContentParser 的 Markdown 解析逻辑（标题提取、正文提取、标签提取）
    - _需求: 1.1, 1.2, 1.3, 1.4, 1.5, 2.1, 2.2, 2.3, 2.4_

  - [ ]* 2.2 编写属性测试：内容扫描正确性
    - **Property 1: 内容扫描正确性**
    - 对任意源目录中的 Markdown 文件集合和归档目录中的已归档文件集合，扫描结果应且仅应包含有同名图片配对且文件名不在归档集合中的 Markdown 文件
    - 在 `scripts/wechat/tests/test_content_parser.py` 中使用 Hypothesis + `tmp_path` 实现
    - **验证: 需求 1.1, 1.2, 1.3**

  - [ ]* 2.3 编写属性测试：扫描结果排序不变量
    - **Property 2: 扫描结果排序不变量**
    - 对任意扫描返回的内容组列表，列表中的元素应按 Markdown 文件名的字母顺序严格排序
    - **验证: 需求 1.4**

  - [ ]* 2.4 编写属性测试：标题提取与截断不变量
    - **Property 3: 标题提取与截断不变量**
    - 对任意字符串作为标题输入，截断后长度始终 ≤ 20 且输出是原始标题的前缀
    - **验证: 需求 2.1, 2.2**

  - [ ]* 2.5 编写属性测试：Markdown 解析 round-trip
    - **Property 4: Markdown 解析 round-trip**
    - 对随机生成的标题、正文和标签列表，按约定格式组装为 Markdown 文本后，解析函数提取出的正文应与原始正文一致
    - **验证: 需求 2.3, 2.4**

  - [ ]* 2.6 编写 WechatContentParser 单元测试
    - 测试边界情况：源目录不存在返回空列表、归档目录为空时返回全部内容、Markdown 无图片跳过、标题恰好20字符
    - 在 `scripts/wechat/tests/test_content_parser.py` 中实现
    - _需求: 1.1, 1.2, 1.3, 1.4, 1.5, 2.1, 2.2_

- [x] 3. 检查点 - 确保内容扫描模块测试通过
  - 确保所有测试通过，如有问题请询问用户。

- [x] 4. 实现 BrowserConnector 浏览器连接
  - [x] 4.1 实现 BrowserConnector CDP 连接逻辑
    - 在 `scripts/wechat/browser_connector.py` 中实现 `BrowserConnector` 类
    - 实现 `connect()` 方法：通过 CDP 协议（端口 9222）连接已打开的 Chrome 浏览器，返回第一个 BrowserContext
    - 连接失败时抛出包含 Chrome 调试模式启动命令的错误信息
    - 不需要 Cookie 注入，直接复用用户已登录的浏览器会话
    - _需求: 3.1, 3.2, 3.3_

  - [ ]* 4.2 编写 BrowserConnector 单元测试
    - 测试 CDP 连接失败时的错误信息格式（包含启动命令提示）
    - 在 `scripts/wechat/tests/test_browser_connector.py` 中实现
    - _需求: 3.2_

- [x] 5. 实现 WechatPublisher 发布器
  - [x] 5.1 实现 Token 提取逻辑
    - 在 `scripts/wechat/publisher.py` 中实现 `WechatPublisher` 类
    - 实现 `extract_token()` 方法：遍历所有已打开的页面，从包含 `mp.weixin.qq.com` 的页面 URL 中提取 `token` 参数
    - 未找到微信后台页面时提示用户先打开微信公众号后台
    - 使用提取到的 token 构造编辑页面 URL
    - _需求: 4.1, 4.2, 4.3_

  - [x] 5.2 实现单篇发布流程
    - 实现 `publish_one()` 方法：打开新编辑页面 → 上传封面图 → 填写标题 → 填写正文 → 保存为草稿
    - 实现 `_upload_cover()` 方法：在编辑页面上传封面图
    - 实现 `_fill_title()` 方法：在标题输入框（placeholder 为"请在这里输入标题"）中填写标题
    - 实现 `_fill_body()` 方法：在正文编辑区域填写正文内容
    - 实现 `_save_draft()` 方法：点击"保存为草稿"按钮
    - 每步操作添加适当的等待和超时处理
    - 发布异常时捕获并返回包含错误信息的 PublishResult，不中断后续发布
    - _需求: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7_

  - [x] 5.3 实现批量发布逻辑
    - 实现 `publish_batch()` 方法：按顺序逐篇执行发布流程，每篇之间等待适当间隔
    - 每篇发布前输出进度信息（"正在发布第 X/Y 篇：标题名"）
    - 每篇发布后输出结果（成功/失败/跳过）
    - 单篇失败不影响后续内容的发布
    - _需求: 6.1, 6.2, 6.3_

  - [ ]* 5.4 编写属性测试：Token 提取与 URL 构造 round-trip
    - **Property 5: Token 提取与 URL 构造 round-trip**
    - 对随机生成的数字字符串作为 token，使用该 token 构造编辑页面 URL 后，从该 URL 中提取 token 应返回原始 token 值
    - 在 `scripts/wechat/tests/test_token.py` 中使用 Hypothesis 实现
    - **验证: 需求 4.1, 4.3**

  - [ ]* 5.5 编写 WechatPublisher 单元测试
    - 测试未找到微信后台页面时的错误提示
    - 测试发布异常时 PublishResult 包含错误信息
    - 在 `scripts/wechat/tests/test_token.py` 中实现
    - _需求: 4.2, 5.7_

- [x] 6. 检查点 - 确保发布器模块测试通过
  - 确保所有测试通过，如有问题请询问用户。

- [x] 7. 实现 CLI 入口与流程串联
  - [x] 7.1 实现 CLI 入口 main.py
    - 在 `scripts/wechat/main.py` 中实现 `main()` 异步函数和 `parse_args()` 函数
    - 支持 `--batch-size` 参数控制每次发布篇数，默认值为 5
    - 实现完整流程串联：内容扫描 → 浏览器连接 → Token 获取 → 批量发布 → 文件归档 → 输出摘要
    - 复用 `scripts/redbook/file_archiver.py` 的 `FileArchiver` 类进行文件归档，传入 `source_dir=data/0.redbook_published`、`archive_dir=data/0.redbook_published/wechat_published`
    - 复用 `scripts/redbook/models.py` 的 `BatchSummary.from_results()` 生成摘要
    - 浏览器连接失败或 Token 获取失败时输出错误信息并以非零退出码退出
    - 发布完成后输出批量发布摘要（总数、成功数、失败数、跳过数）
    - _需求: 6.1, 6.4, 7.1, 7.2, 7.3, 7.4, 8.1, 8.2, 8.3, 8.4_

  - [ ]* 7.2 编写 CLI 入口单元测试
    - 测试 `--batch-size` 参数解析：默认值为 5、自定义值
    - 测试初始化失败时以非零退出码退出
    - 在 `scripts/wechat/tests/test_main.py` 中实现
    - _需求: 8.2, 8.4_

- [x] 8. 最终检查点 - 确保所有测试通过
  - 确保所有测试通过，如有问题请询问用户。

## 备注

- 标记 `*` 的子任务为可选测试任务，可跳过以加速 MVP 开发
- 每个任务引用了对应的需求编号，确保需求可追溯
- 检查点任务用于增量验证，确保每个阶段的代码质量
- 属性测试验证通用正确性属性，单元测试验证具体示例和边界情况
- Playwright 相关的浏览器自动化操作建议在开发阶段使用 `headed` 模式调试
- 直接复用 `scripts/redbook/models.py`（ContentPair, PublishResult, BatchSummary）和 `scripts/redbook/file_archiver.py`（FileArchiver），通过导入方式使用，不复制代码

<!-- @AI_GENERATED: end -->
