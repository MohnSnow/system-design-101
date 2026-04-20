# 📱 Apple Pay vs

> 都是手机支付，但安全实现方式完全不同

![Apple Pay vs Google Pay](./how-applegoogle-pay-works.png)

Apple Pay和Google Pay都很安全，但实现方式不同 👇

📌 **注册信用卡**

Apple Pay：
- Apple不存储任何卡信息
- 卡信息传给银行，银行返回DAN（设备账号）
- DAN存储在iPhone的安全硬件芯片中

Google Pay：
- 卡信息存储在Google服务器
- Google返回支付令牌到手机

📌 **支付流程**

Apple Pay：
- 电商服务器把DAN传给银行
- 信用卡信息不经过公网

Google Pay：
- 电商服务器把支付令牌传给Google服务器
- Google查找信用卡信息再传给银行
- 信用卡信息经过公网（虽然加密了）

💡 核心区别：Apple Pay的卡信息永远不离开安全芯片，Google Pay的卡信息存在Google服务器。两者都安全，但Apple的方案隐私性更强。

---

#ApplePay #GooglePay #移动支付 #支付 #程序员 #技术干货
