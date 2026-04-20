# 📋 HTTP Headers

> 请求头和响应头到底在传递什么信息？

![HTTP Headers详解](important-things-about-http-headers-you-may-not-know.png)

HTTP请求就像给服务器写信，响应就是服务器的回信。而 **Header** 就是信封上的附加信息 👇

📌 **请求头（Request Headers）**
你在发请求时附带的额外信息：
- 我发的是什么类型的数据？
- 我是谁？
- 我能接受什么格式的响应？

📌 **响应头（Response Headers）**
服务器回复时附带的信息：
- 返回的数据是什么类型？
- 有没有特殊指令？
- 缓存策略是什么？

📌 **为什么要懂 Headers？**
做 RESTful API 开发时，正确设置 Header 是基本功：
- **Content-Type** — 告诉对方数据格式
- **Authorization** — 身份认证信息
- **Cache-Control** — 缓存策略
- **CORS 相关头** — 跨域访问控制

💡 很多接口调试的坑，其实都是 Header 没设对。下次遇到问题先检查 Headers。

你踩过哪些 Header 相关的坑？👇

---

#HTTP #Headers #API #Web开发 #后端 #RESTful #程序员
