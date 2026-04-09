# 🏗️ Amazon的构建系统Brazil

> Amazon内部用的构建系统，值得学习

![Amazon Brazil构建系统](./how-does-amazon-build-system-work.png)

Amazon的所有权模型要求每个团队管理自己的仓库，Brazil构建系统应运而生 👇

📌 **核心概念**
- 开发者只需写代码和简单的构建配置文件
- 构建系统负责重复一致地处理输出制品
- 配置包含：语言、版本、依赖、冲突解决策略

📌 **本地构建**
Brazil将配置解释为DAG（有向无环图），从私有空间（VersionSet）获取包，生成语言特定的构建配置

📌 **远程构建**
包构建服务支持Amazon Linux（x86/x64/ARM），可手动触发或master分支提交时自动触发，保证构建一致性和可重现性

💡 Brazil的设计理念：让开发者专注于代码，构建系统处理一切复杂性。

---

#Amazon #构建系统 #DevOps #程序员 #大厂案例 #技术干货
