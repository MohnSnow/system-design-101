# 📧 设计Gmail！一封邮件的完整旅程

> 从Alice发邮件到Bob收到，中间经历了什么？

![设计Gmail](./design-gmail.png)

Alice给Bob发一封邮件，背后发生了什么？👇

📌 **发送流程**
1. Alice在Outlook客户端写好邮件，点击发送
2. 邮件通过SMTP协议发送到Outlook邮件服务器
3. Outlook服务器查DNS找到Gmail的SMTP服务器地址
4. 通过SMTP协议将邮件传输到Gmail服务器

📌 **接收流程**
5. Gmail服务器存储邮件
6. Bob登录Gmail时，客户端通过IMAP/POP协议从服务器获取新邮件

🔑 **关键协议**
- SMTP — 发送邮件（客户端→服务器，服务器→服务器）
- IMAP/POP — 接收邮件（服务器→客户端）

💡 邮件系统看似简单，但涉及DNS解析、多协议交互、存储等多个环节。这也是系统设计面试的经典题目。

---

#邮件系统 #系统设计 #SMTP #程序员 #技术干货 #面试
