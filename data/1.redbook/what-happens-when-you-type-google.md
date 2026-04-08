# 🔍 输入google.com后发生了什么？8步完整流程

> 从输入到页面显示的完整旅程

![输入google.com](what-happens-when-you-type-google.png)

经典面试题的详细版本 👇

1️⃣ 在地址栏输入网址
2️⃣ 浏览器先查缓存，缓存未命中则需要查IP
3️⃣ DNS查询开始：根DNS→TLD DNS→权威DNS，最终获取IP
4️⃣ 浏览器发起TCP连接（三次握手：SYN→SYN-ACK→ACK）
5️⃣ 握手成功后发送HTTP请求，服务器返回HTML/CSS/JS
6️⃣ 浏览器解析HTML，构建DOM树和CSSOM树
7️⃣ 执行JavaScript，经过tokenizer→parser→render tree→layout→painting
8️⃣ 页面显示在屏幕上 ✅

💡 每一步都可以深入展开，这是考察网络、浏览器、前端知识的综合题。

你能把每一步都讲清楚吗？👇

---

#面试 #DNS #TCP #浏览器 #HTTP #前端 #后端
