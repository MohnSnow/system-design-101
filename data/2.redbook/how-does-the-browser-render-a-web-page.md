# 🖥️ 浏览器是怎么渲染网页的？6步完成

> 从HTML到像素，浏览器做了这些事

![浏览器渲染](./how-does-the-browser-render-a-web-page.png)

浏览器渲染网页的6个步骤 👇

1️⃣ **解析HTML → DOM树** — 收到HTML数据后立即解析转换

2️⃣ **解析CSS → CSSOM树** — 加载并解析样式文件

3️⃣ **DOM + CSSOM → 渲染树** — 合并两棵树，排除不可见元素（如head、display:none）

4️⃣ **布局（Layout）** — 计算每个元素的几何信息（位置、大小）

5️⃣ **绘制（Painting）** — 渲染树转换为屏幕上的实际内容，获取绝对像素

6️⃣ **显示（Display）** — 发送像素到GPU显示

💡 理解渲染流程有助于优化前端性能：减少重排（Layout）和重绘（Painting）是关键。

---

#浏览器 #前端 #渲染 #Web开发 #程序员 #技术干货
