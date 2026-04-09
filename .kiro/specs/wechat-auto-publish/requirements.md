<!-- @AI_GENERATED -->
# 需求文档：微信公众号自动发布工具

## 简介

基于已有的小红书自动发布工具（`scripts/redbook/`），构建微信公众号自动发布工具。该工具使用 Playwright 浏览器自动化技术，通过微信公众号后台网页版将已发布到小红书的内容（Markdown + 图片）批量保存为微信公众号草稿。工具复用小红书项目的基础架构（数据模型、浏览器连接、文件归档、内容解析），适配微信公众号后台的页面结构和发布流程。

## 术语表

- **Wechat_Publisher**：微信公众号自动发布工具的核心发布模块，负责驱动 Playwright 在微信公众号后台完成内容填写和草稿保存
- **Content_Parser**：内容解析器，扫描 `data/0.redbook_published/` 目录，配对 Markdown 和图片文件，排除已发布到微信的内容
- **File_Archiver**：文件归档器，将成功保存为草稿的内容文件移动到 `data/0.redbook_published/wechat_published/` 目录
- **Browser_Connector**：浏览器连接模块，通过 CDP 协议连接用户已登录微信公众号后台的 Chrome 浏览器
- **Content_Pair**：一组待发布内容，包含一个 Markdown 文件和一个同名图片文件的配对
- **MP_Token**：微信公众号后台的会话令牌，包含在后台页面 URL 中，每次登录后会变化
- **编辑页面**：微信公众号后台的图文编辑页面，URL 格式为 `https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=77&createType=8&token=TOKEN&lang=zh_CN`
- **Source_Dir**：内容来源目录，即 `data/0.redbook_published/`，存放已发布到小红书的内容
- **Archive_Dir**：归档目录，即 `data/0.redbook_published/wechat_published/`，存放已保存为微信草稿的内容

## 需求

### 需求 1：内容扫描与过滤

**用户故事：** 作为内容运营者，我希望工具自动扫描已发布到小红书的内容并排除已发布到微信的内容，以便只处理尚未发布到微信公众号的内容。

#### 验收标准

1. WHEN 工具启动时，THE Content_Parser SHALL 扫描 Source_Dir 目录下的所有 Markdown 文件及其同名图片文件（.png/.jpg/.jpeg）
2. THE Content_Parser SHALL 排除 Archive_Dir 目录中已存在同名文件的内容对
3. WHEN 某个 Markdown 文件在 Source_Dir 中没有同名图片文件时，THE Content_Parser SHALL 跳过该文件并在控制台输出提示信息
4. THE Content_Parser SHALL 按文件名字母顺序返回有效的 Content_Pair 列表
5. WHEN Source_Dir 目录不存在时，THE Content_Parser SHALL 输出警告信息并返回空列表

### 需求 2：Markdown 内容解析

**用户故事：** 作为内容运营者，我希望工具能正确解析 Markdown 文件中的标题和正文，以便自动填充到微信公众号编辑页面。

#### 验收标准

1. THE Content_Parser SHALL 从 Markdown 文件的第一个 `# ` 开头的行中提取标题，去除 `# ` 前缀
2. WHEN 标题长度超过 20 个字符时，THE Content_Parser SHALL 将标题截断至 20 个字符
3. THE Content_Parser SHALL 提取标题行之后、`---` 分隔线之前的所有内容作为正文
4. THE Content_Parser SHALL 去除正文开头的空行和末尾的空白字符

### 需求 3：浏览器连接与认证

**用户故事：** 作为内容运营者，我希望工具能连接到我已登录微信公众号后台的 Chrome 浏览器，以便无需重复登录即可操作。

#### 验收标准

1. THE Browser_Connector SHALL 通过 CDP 协议（端口 9222）连接到用户已打开的 Chrome 浏览器
2. IF 无法连接到 Chrome 浏览器，THEN THE Browser_Connector SHALL 抛出包含启动 Chrome 调试模式命令的错误信息
3. THE Browser_Connector SHALL 复用已有浏览器上下文中的第一个 context，保留用户已登录的微信公众号会话

### 需求 4：MP_Token 获取

**用户故事：** 作为内容运营者，我希望工具能自动获取微信公众号后台的 token，以便正确构造编辑页面 URL。

#### 验收标准

1. WHEN 连接到浏览器后，THE Wechat_Publisher SHALL 从已打开的微信公众号后台页面 URL 中提取 token 参数
2. IF 未找到包含 `mp.weixin.qq.com` 的已打开页面，THEN THE Wechat_Publisher SHALL 提示用户先在浏览器中打开微信公众号后台页面
3. THE Wechat_Publisher SHALL 使用提取到的 token 构造编辑页面 URL，格式为 `https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=77&createType=8&token=TOKEN&lang=zh_CN`

### 需求 5：单篇内容发布流程

**用户故事：** 作为内容运营者，我希望工具能自动在微信公众号编辑页面完成封面图上传、标题填写、正文填写并保存为草稿，以便减少手动操作。

#### 验收标准

1. WHEN 发布单篇内容时，THE Wechat_Publisher SHALL 打开一个新的编辑页面标签
2. THE Wechat_Publisher SHALL 在编辑页面的封面图上传区域上传 Content_Pair 中的图片文件
3. THE Wechat_Publisher SHALL 在标题输入框（placeholder 为"请在这里输入标题"）中填写 Content_Pair 的标题
4. THE Wechat_Publisher SHALL 在正文编辑区域填写 Content_Pair 的正文内容
5. THE Wechat_Publisher SHALL 点击"保存为草稿"按钮完成草稿保存
6. WHEN 草稿保存成功后，THE Wechat_Publisher SHALL 返回成功的 PublishResult
7. IF 发布过程中发生异常，THEN THE Wechat_Publisher SHALL 捕获异常并返回包含错误信息的 PublishResult，不中断后续内容的发布

### 需求 6：批量发布模式

**用户故事：** 作为内容运营者，我希望工具支持批量发布模式，每次运行自动处理多篇内容，以便提高发布效率。

#### 验收标准

1. THE Wechat_Publisher SHALL 支持通过 `--batch-size` 命令行参数指定每次批量发布的篇数，默认值为 5
2. WHEN 批量发布时，THE Wechat_Publisher SHALL 按顺序逐篇执行发布流程，每篇之间等待适当间隔
3. THE Wechat_Publisher SHALL 在每篇发布完成后输出当前进度（第 N/M 篇）和发布结果（成功/失败/跳过）
4. WHEN 所有内容发布完成后，THE Wechat_Publisher SHALL 输出批量发布摘要，包含总数、成功数、失败数和跳过数

### 需求 7：文件归档

**用户故事：** 作为内容运营者，我希望成功保存为草稿的内容文件被自动移动到归档目录，以便下次运行时不会重复处理。

#### 验收标准

1. WHEN 单篇内容成功保存为草稿后，THE File_Archiver SHALL 将对应的 Markdown 文件和图片文件从 Source_Dir 移动到 Archive_Dir
2. IF Archive_Dir 不存在，THEN THE File_Archiver SHALL 自动创建该目录
3. IF 文件移动失败，THEN THE File_Archiver SHALL 在控制台输出错误信息并保留原文件不删除
4. THE File_Archiver SHALL 对每个成功归档的文件输出归档确认信息

### 需求 8：CLI 入口与参数

**用户故事：** 作为内容运营者，我希望通过命令行启动工具并控制发布行为，以便灵活使用。

#### 验收标准

1. THE 微信公众号自动发布工具 SHALL 提供 `python -m scripts.wechat.main` 命令行入口
2. THE 微信公众号自动发布工具 SHALL 支持 `--batch-size` 参数控制每次发布篇数，默认值为 5
3. WHEN 工具启动时，THE 微信公众号自动发布工具 SHALL 按顺序执行：内容扫描 → 浏览器连接 → Token 获取 → 批量发布 → 文件归档 → 输出摘要
4. IF 任何初始化步骤失败（浏览器连接失败、Token 获取失败），THEN THE 微信公众号自动发布工具 SHALL 输出错误信息并以非零退出码退出

### 需求 9：代码复用与项目结构

**用户故事：** 作为开发者，我希望微信公众号工具复用小红书项目的基础架构，以便减少重复代码并保持一致性。

#### 验收标准

1. THE 微信公众号自动发布工具 SHALL 复用 `scripts/redbook/models.py` 中的 ContentPair、PublishResult、BatchSummary 数据模型
2. THE 微信公众号自动发布工具 SHALL 将代码组织在 `scripts/wechat/` 目录下，结构与 `scripts/redbook/` 保持一致
3. THE 微信公众号自动发布工具 SHALL 通过导入方式复用小红书项目的数据模型，而非复制代码

<!-- @AI_GENERATED: end -->
