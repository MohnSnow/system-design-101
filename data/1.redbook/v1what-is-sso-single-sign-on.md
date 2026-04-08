# 🔐 SSO单点登录是怎么工作的？一次登录到处通行

> 登录Gmail后打开YouTube不用再登录，就是SSO的功劳

![SSO工作原理](v1what-is-sso-single-sign-on.jpeg)

一次登录，多个网站通用。SSO 是怎么做到的？👇

📌 **完整流程：**

1️⃣ 用户访问Gmail，未登录 → 重定向到SSO认证服务器
2️⃣ SSO服务器发现用户未登录 → 跳转登录页
3️⃣ 用户输入凭证 → SSO验证通过，创建全局Session和Token
4️⃣ Gmail用Token向SSO验证 → 验证通过
5️⃣ SSO注册Gmail系统 → Gmail返回受保护资源
6️⃣ 用户从Gmail跳转到YouTube
7️⃣ YouTube发现未登录 → 请求SSO认证
8️⃣ SSO发现用户已登录 → 直接返回Token
9️⃣ YouTube验证Token → 返回受保护资源 ✅

💡 SSO的核心：一个中心认证服务 + 全局Session + Token传递。用户只需登录一次。

你的项目实现了SSO吗？👇

---

#SSO #单点登录 #认证 #安全 #OAuth #后端 #面试
