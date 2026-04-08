# 💬 Discord如何存储万亿条消息！数据库三次迁移

> MongoDB → Cassandra → ScyllaDB，每次迁移都有故事

![Discord消息存储](how-discord-stores-trillions-of-messages.png)

Discord消息存储的进化之路 👇

📌 **2015：MongoDB**
单个MongoDB副本集，存了1亿条消息后内存扛不住，延迟不可预测

📌 **2017：Cassandra**
12个节点，存储数十亿条消息

📌 **2022初：Cassandra的瓶颈**
177个节点，万亿条消息，但出现问题：
- LSM树结构导致读比写贵，数百用户并发读造成热点
- 集群维护（SSTable压缩）影响性能
- GC暂停导致延迟尖峰

📌 **迁移到ScyllaDB**
C++编写的Cassandra兼容数据库，配合Rust数据服务：
- 读P99延迟：15ms（Cassandra是40-125ms）
- 写P99延迟：5ms（Cassandra是5-70ms）

💡 Discord的经验：没有永远合适的数据库，随着数据量增长要勇于迁移。

---

#Discord #数据库 #ScyllaDB #Cassandra #程序员 #大厂案例 #技术干货
