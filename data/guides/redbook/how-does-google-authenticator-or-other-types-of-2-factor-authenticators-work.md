# 🔐 Google Authenticator是怎么工作的？两步验证原理

> 每30秒生成一个6位数密码，安全又方便

![Google Authenticator](./how-does-google-authenticator-or-other-types-of-2-factor-authenticators-work.png)

Google两步验证的完整工作流程 👇

📌 **阶段一：启用两步验证**
1-2. 前端请求密钥，认证服务生成并存储
3. 返回包含密钥的URI，显示为二维码
4. 用Google Authenticator扫码，密钥存入App

📌 **阶段二：登录验证**
1-2. Authenticator每30秒用TOTP算法生成6位密码
3-4. 服务端用相同算法和密钥生成密码
5. 比较两个密码，匹配则登录成功

📌 **安全性分析**
- 密钥会被窃取吗？用HTTPS传输+加密存储
- 密码会被猜到吗？6位=100万种组合，30秒内需每秒猜30000次，不可能

💡 TOTP的巧妙之处：客户端和服务端用相同的密钥和时间独立生成密码，不需要网络通信。

---

#两步验证 #安全 #Google #程序员 #技术干货
