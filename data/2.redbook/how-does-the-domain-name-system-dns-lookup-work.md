# 🌐 DNS域名解析是怎么工作的

> 输入google.com后，DNS帮你找到142.251.46.238

![DNS解析](how-does-the-domain-name-system-dns-lookup-work.png)

DNS就像互联网的电话簿，把域名翻译成IP地址。三级DNS服务器 👇

📌 **根域名服务器** — 全球13个逻辑服务器，存储TLD服务器地址
📌 **TLD服务器** — 存储权威域名服务器地址（.com/.org/.cn等）
📌 **权威域名服务器** — 提供实际的DNS查询答案

📌 **查询流程（8步）**
1. 浏览器输入google.com，发送到DNS解析器
2. 解析器查询根域名服务器
3. 根服务器返回.com TLD服务器地址
4. 解析器查询.com TLD
5. TLD返回google.com的权威服务器地址
6. 解析器查询权威服务器
7. 返回google.com的IP地址
8. 解析器将IP返回给浏览器

DNS查询平均耗时20-120毫秒。

💡 DNS缓存存在于浏览器、操作系统、ISP等多个层级，大部分查询不需要走完整流程。

---

#DNS #网络 #计算机基础 #程序员 #Web开发 #技术干货
