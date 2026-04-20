# 🔗 LinkedIn如何使用GraphQ

> "迁移到GraphQL改变了数千名工程师的开发工作流"

![LinkedIn GraphQL](./how-does-graphql-work-in-the-real-world.png)

LinkedIn采用GraphQL后的工作流分3部分 👇

📌 **Part 1：编辑和测试查询**
客户端开发者编写查询并与后端服务测试

📌 **Part 2：注册查询**
提交查询并发布到查询注册中心

📌 **Part 3：生产使用**
- 查询随客户端代码一起发布
- 路由元数据包含在每个注册查询中
- 注册查询在服务运行时缓存
- 查询先到身份服务获取成员信息，再到组织服务获取公司信息

📌 **LinkedIn不用GraphQL网关的原因**
1. 避免额外的网络跳转
2. 避免单点故障

💡 LinkedIn的方案说明：GraphQL不一定需要网关，根据实际需求选择架构。

---

#GraphQL #LinkedIn #API #后端开发 #程序员 #大厂案例 #技术干货
