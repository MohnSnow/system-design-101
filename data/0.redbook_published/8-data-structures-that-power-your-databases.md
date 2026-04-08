# 🗃️ 驱动数据库的8种数据结构！底层原理揭秘

> 数据库为什么快？秘密藏在这些数据结构里

![数据库数据结构](./8-data-structures-that-power-your-databases.png)

不同的数据库选择不同的索引结构，取决于读写比例、数据类型等因素 👇

📌 **Skiplist（跳表）** — 常见的内存索引，Redis在用

📌 **Hash Index（哈希索引）** — Map数据结构的经典实现，O(1)查找

📌 **SSTable** — 不可变的磁盘Map实现

📌 **LSM Tree** — Skiplist + SSTable，写入吞吐量极高

📌 **B-Tree（B树）** — 磁盘方案，读写性能均衡稳定，MySQL InnoDB在用

📌 **Inverted Index（倒排索引）** — 文档索引，Elasticsearch/Lucene的核心

📌 **Suffix Tree（后缀树）** — 字符串模式匹配

📌 **R-Tree** — 多维搜索，如查找最近的餐厅

💡 简单记忆：写多用LSM Tree，读写均衡用B-Tree，搜索用倒排索引，地理位置用R-Tree。

---

#数据库 #数据结构 #Redis #MySQL #Elasticsearch #程序员 #技术干货
