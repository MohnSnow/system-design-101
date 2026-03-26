# 🔔 推送通知是怎么到达你手机的？FCM原理解析

> 从App服务器到你的手机，推送通知经历了什么？

![推送通知原理](./how-are-notifications-pushed-to-our-phones-or-pcs.png)

Firebase Cloud Messaging（FCM）是跨平台消息推送方案 👇

📌 **注册流程（步骤1-3）**
1-2. App首次启动时，向FCM发送凭证（Sender ID、API Key、App ID）
FCM为该App实例生成注册令牌
3. App把令牌发给App服务器缓存（建议定期清理过期令牌）

📌 **发送流程（步骤4-7）**
4. 两种发送方式：控制台GUI直接发送 或 App服务器通过SDK/HTTP发送
5. FCM接收消息，设备离线时存入队列
6. FCM转发到平台级传输层（处理平台特定配置）
7. 消息路由到目标设备，按配置显示通知

💡 FCM提供了统一的API，屏蔽了iOS和Android的推送差异，是移动开发的标配方案。

---

#推送通知 #Firebase #移动开发 #程序员 #后端开发 #技术干货
