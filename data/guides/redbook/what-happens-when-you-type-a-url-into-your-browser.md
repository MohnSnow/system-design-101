# 🌐 浏览器输入URL后发生了什么？面试经典题

> DNS查询→TCP连接→HTTP请求→渲染页面

![URL到页面](./what-happens-when-you-type-a-url-into-your-browser.png)

面试最经典的问题之一，完整流程 👇

📌 URL由4部分组成：scheme（http://）+ domain（example.com）+ path（/product/electric）+ resource（phone）

📌 **Step 1** — 浏览器查DNS获取IP地址（浏览器缓存→OS缓存→本地网络缓存→ISP缓存→递归查询）
📌 **Step 2** — 建立TCP连接
📌 **Step 3** — 发送HTTP请求
📌 **Step 4** — 服务器处理请求，返回HTML响应
📌 **Step 5** — 浏览器渲染HTML内容

💡 这个问题可以展开到任意深度：DNS递归查询、TCP三次握手、TLS握手、HTTP/2多路复用、浏览器渲染流水线……面试时根据面试官的追问深入。

你能讲多深？👇

---

#面试 #浏览器 #DNS #HTTP #TCP #前端 #后端
