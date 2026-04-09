<!-- @AI_GENERATED -->
# 实现计划：小红书自动发布工具

## 概述

基于 Python + Playwright 实现小红书自动发布工具，按模块逐步构建：数据模型 → 内容解析 → Cookie 认证 → 发布器 → 文件归档 → CLI 入口 → 批量模式。每个模块实现后紧跟测试，确保增量验证。

## 任务列表

- [x] 1. 项目初始化与数据模型定义
  - [x] 1.1 创建项目结构和依赖配置
    - 创建 `scripts/redbook/` 目录作为项目根目录
    - 创建 `pyproject.toml` 或 `requirements.txt`，声明依赖：`playwright`, `python-dotenv`, `hypothesis`, `pytest`, `pytest-asyncio`, `pytest-playwright`
    - 创建 `scripts/redbook/__init__.py`
    - 创建 `scripts/redbook/tests/` 目录和 `__init__.py`
    - _需求: 全局_

  - [x] 1.2 定义 ContentPair 和 PublishResult 数据模型
    - 在 `scripts/redbook/models.py` 中定义 `ContentPair` dataclass（md_path, image_path, title, body, tags）
    - 定义 `PublishResult` dataclass（content, success, error）
    - 定义 `BatchSummary` dataclass（total, success_count, fail_count, skip_count, results）
    - 实现 `BatchSummary.from_results(results)` 类方法，从 PublishResult 列表生成摘要
    - _需求: 1.1, 1.2, 5.4_

- [x] 2. 实现 ContentParser 内容解析器
  - [x] 2.1 实现 ContentParser 核心解析逻辑
    - 在 `scripts/redbook/content_parser.py` 中实现 `ContentParser` 类
    - 实现 `scan()` 方法：扫描待发布目录，返回按文件名排序的有效内容组列表
    - 实现 `_find_image()` 方法：查找同名图片文件（.png/.jpg/.jpeg）
    - 实现 `_parse_markdown()` 方法：解析 Markdown 文件，返回 (标题, 正文, 标签列表)
    - 实现 `_extract_title()` 方法：提取标题，超过20字符自动截断
    - 实现 `_extract_tags()` 方法：从文件末尾 `---` 分隔线之后提取 `#标签名` 格式的话题标签
    - 无图片配对的 Markdown 文件应跳过并输出控制台提示
    - _需求: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7_

  - [ ]* 2.2 编写属性测试：Markdown 解析 round-trip
    - **Property 1: Markdown 解析 round-trip**
    - 对任意包含 `# 标题` 行和正文内容的有效 Markdown 文本，解析出的标题（截断前）与正文拼接后应能重构出原始内容
    - 在 `scripts/redbook/tests/test_content_parser.py` 中使用 Hypothesis 实现
    - **验证: 需求 1.4, 1.6**

  - [ ]* 2.3 编写属性测试：标题长度不变量
    - **Property 2: 标题长度不变量**
    - 对任意长度的字符串作为标题输入，截断后长度始终 ≤ 20 且输出是原始标题的前缀
    - **验证: 需求 1.5**

  - [ ]* 2.4 编写属性测试：标签提取 round-trip
    - **Property 3: 标签提取 round-trip**
    - 对随机生成的标签名列表，格式化为 `#标签1 #标签2 ...` 后，提取函数应返回与原始列表一致的结果
    - **验证: 需求 1.7**

  - [ ]* 2.5 编写属性测试：文件配对正确性
    - **Property 4: 文件配对正确性**
    - 对给定的 Markdown 文件名和目录中的文件列表，配对函数应且仅应返回同名且扩展名为 .png/.jpg/.jpeg 的图片文件
    - 使用临时目录模拟文件系统
    - **验证: 需求 1.2, 1.3**

  - [ ]* 2.6 编写 ContentParser 单元测试
    - 测试边界情况：空目录、标题恰好20字符、无标签的 Markdown 文件、多种图片格式
    - 使用真实的 `data/1.redbook/` 目录中的样例文件验证解析结果
    - _需求: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7_

- [x] 3. 检查点 - 确保内容解析模块测试通过
  - 确保所有测试通过，如有问题请询问用户。

- [x] 4. 实现 BrowserAuth Cookie 认证
  - [x] 4.1 实现 BrowserAuth 认证逻辑
    - 在 `scripts/redbook/browser_auth.py` 中实现 `BrowserAuth` 类
    - 实现 `load_cookie()` 静态方法：按优先级从环境变量 `XHS_COOKIE` 或 `.env` 文件读取 Cookie
    - 实现 `create_context()` 方法：解析 Cookie 字符串并注入到 Playwright BrowserContext
    - 实现 `verify_auth()` 方法：访问创作者平台验证认证是否有效，失败时抛出明确异常
    - _需求: 2.1, 2.2, 2.3_

  - [ ]* 4.2 编写 BrowserAuth 单元测试
    - 在 `scripts/redbook/tests/test_browser_auth.py` 中编写测试
    - 测试 Cookie 从环境变量读取（mock os.environ）
    - 测试 Cookie 从 .env 文件读取（mock 文件系统）
    - 测试 Cookie 为空时的错误处理
    - _需求: 2.1, 2.3_

- [x] 5. 实现 Publisher 发布器
  - [x] 5.1 实现 Publisher 单篇发布逻辑
    - 在 `scripts/redbook/publisher.py` 中实现 `Publisher` 类
    - 实现 `publish_one()` 方法：执行单篇发布到草稿箱的完整流程
    - 实现 `_upload_image()` 方法：通过 file chooser 上传图片
    - 实现 `_fill_title()` 方法：填写标题字段
    - 实现 `_fill_body()` 方法：填写正文字段
    - 实现 `_add_tags()` 方法：搜索并选择话题标签，返回未匹配的标签列表
    - 实现 `_save_draft()` 方法：点击"存草稿"按钮
    - 每步操作添加适当的等待和超时处理
    - _需求: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8_

  - [x] 5.2 实现 Publisher 批量发布逻辑
    - 实现 `publish_batch()` 方法：依次发布多组内容，单篇失败不影响后续
    - 每篇发布前输出进度信息（"正在发布第 X/Y 篇：标题名"）
    - 每篇发布后输出结果（成功/失败/跳过）
    - _需求: 5.1, 5.2, 5.3, 6.1, 6.2_

  - [ ]* 5.3 编写属性测试：批量选取排序与截取
    - **Property 5: 批量选取排序与截取**
    - 对随机生成的内容组列表，批量选取结果应满足：按文件名字典序排序、数量为 min(列表长度, batch_size)、是完整排序列表的前缀
    - 在 `scripts/redbook/tests/test_batch_logic.py` 中实现
    - **验证: 需求 1.1, 5.1, 5.5**

  - [ ]* 5.4 编写属性测试：摘要统计一致性
    - **Property 7: 摘要统计一致性**
    - 对随机生成的 PublishResult 列表，摘要中 success_count + fail_count + skip_count == total，且各计数与实际数量一致
    - **验证: 需求 5.4**

- [x] 6. 实现 FileArchiver 文件归档器
  - [x] 6.1 实现 FileArchiver 归档逻辑
    - 在 `scripts/redbook/file_archiver.py` 中实现 `FileArchiver` 类
    - 实现 `archive()` 方法：将内容组的 Markdown 和图片文件移动到已发布目录
    - 已发布目录不存在时自动创建
    - 文件移动失败时记录错误，保留原文件不删除
    - _需求: 4.1, 4.2, 4.3_

  - [ ]* 6.2 编写属性测试：文件归档正确性
    - **Property 6: 文件归档正确性**
    - 对随机文件名的内容组，归档后文件应存在于已发布目录且不再存在于待发布目录
    - 使用 `tmp_path` 临时目录模拟文件系统
    - 在 `scripts/redbook/tests/test_file_archiver.py` 中实现
    - **验证: 需求 4.1**

  - [ ]* 6.3 编写 FileArchiver 单元测试
    - 测试目录自动创建、文件移动失败的容错处理、已存在同名文件的处理
    - _需求: 4.1, 4.2, 4.3_

- [x] 7. 检查点 - 确保所有模块测试通过
  - 确保所有测试通过，如有问题请询问用户。

- [x] 8. 实现 CLI 入口与日志输出
  - [x] 8.1 实现 CLI 入口 main.py
    - 在 `scripts/redbook/main.py` 中实现 `main()` 异步函数
    - 支持 `--batch` 参数切换批量模式（默认单篇模式）
    - 支持 `--batch-size` 参数自定义批量大小（默认5）
    - 实现完整流程串联：解析 → 认证 → 发布 → 归档
    - 单篇模式：发布第一组有效内容
    - 批量模式：按 batch_size 选取并依次发布
    - 发布完成后输出 BatchSummary 摘要信息
    - _需求: 5.1, 5.2, 5.4, 5.5, 6.1, 6.2, 6.3_

  - [x] 8.2 实现日志输出
    - 在各模块中添加控制台日志输出
    - 扫描阶段：输出发现的内容组数量、跳过的文件
    - 认证阶段：输出认证状态
    - 发布阶段：输出进度（"正在发布第 X/Y 篇：标题名"）和每篇结果
    - 归档阶段：输出归档结果
    - 异常时输出包含错误类型和上下文信息的日志
    - _需求: 6.1, 6.2, 6.3_

- [x] 9. 集成与端到端验证
  - [x] 9.1 串联所有模块，确保完整流程可运行
    - 验证 CLI 入口能正确调用各模块
    - 确保单篇模式和批量模式的参数传递正确
    - 确保错误处理链路完整（Cookie 失败终止、单篇失败继续）
    - _需求: 全局_

  - [ ]* 9.2 编写集成测试
    - 在 `scripts/redbook/tests/test_publisher_integration.py` 中编写
    - 使用 mock 测试批量发布容错（注入失败场景）
    - 测试完整流程的日志输出格式
    - _需求: 3.8, 5.3, 6.3_

- [x] 10. 最终检查点 - 确保所有测试通过
  - 确保所有测试通过，如有问题请询问用户。

## 备注

- 标记 `*` 的子任务为可选测试任务，可跳过以加速 MVP 开发
- 每个任务引用了对应的需求编号，确保需求可追溯
- 检查点任务用于增量验证，确保每个阶段的代码质量
- 属性测试验证通用正确性属性，单元测试验证具体示例和边界情况
- Playwright 相关的浏览器自动化操作建议在开发阶段使用 `headed` 模式调试

<!-- @AI_GENERATED: end -->
