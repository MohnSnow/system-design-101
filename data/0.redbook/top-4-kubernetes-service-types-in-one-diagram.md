# 🌐 K8s四种Service类型一图搞懂

> ClusterIP、NodePort、LoadBalancer、ExternalName

![K8s Service类型](top-4-kubernetes-service-types-in-one-diagram.png)

K8s 中 Service 是暴露网络应用的方式，4种类型 👇

📌 **ClusterIP（默认）**
分配集群内部IP，只能在集群内访问。最常用

📌 **NodePort**
在 ClusterIP 基础上加一个集群级端口，可以通过 NodeIP:NodePort 从外部访问

📌 **LoadBalancer**
使用云厂商的负载均衡器对外暴露服务

📌 **ExternalName**
把 Service 映射到一个域名，常用于在K8s内部表示外部数据库

💡 简单记：集群内用 ClusterIP，开发测试用 NodePort，生产环境用 LoadBalancer。

你最常用哪种 Service 类型？👇

---

#Kubernetes #K8s #Service #云原生 #DevOps #运维 #面试
