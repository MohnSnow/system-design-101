# 💬 设计聊天应用！WhatsApp/微信的架构是怎样的？

> 系统设计面试经典题，一对一聊天的完整架构

![聊天应用设计](./how-do-we-design-a-chat-application-like-whatsapp-facebook-messenger-or-discord.png)

简化版一对一聊天应用的设计 👇

📌 **用户登录流程**
1. Alice登录，建立WebSocket连接
2-4. 在线状态服务更新Alice的状态，通知好友

📌 **消息流程**
1-2. Alice发消息给Bob，路由到聊天服务A
3-4. 消息发送到序列服务生成唯一ID，持久化到消息存储
5. 消息发送到同步队列
6. 消息同步服务检查Bob的在线状态：
   - 在线 → 发送到聊天服务B
   - 离线 → 发送到推送服务器
7-8. Bob在线时通过WebSocket接收消息

💡 核心组件：WebSocket（实时通信）、消息存储（持久化）、在线状态服务、推送服务。

---

#聊天应用 #系统设计 #WebSocket #面试 #程序员 #技术干货
