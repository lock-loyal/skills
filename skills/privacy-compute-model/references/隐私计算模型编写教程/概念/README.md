# 概念

---

## 主内容

# 概念

**隐私计算**：联合多方数据进行基于安全多方计算技术的分布式明密文计算。

**参与方数据**：参与方的数据可以是通过appkey的形式关联，也可以通过邀请的形式由参与方手动进行配置。

![](http://teambitiondoc.hyperchain.cn:8099/storage/0129a6fa752ab311788bcdeab52b6122d4ef?Signature=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJBcHBJRCI6IjU5Mzc3MGZmODM5NjMyMDAyZTAzNThmMSIsIl9hcHBJZCI6IjU5Mzc3MGZmODM5NjMyMDAyZTAzNThmMSIsIl9vcmdhbml6YXRpb25JZCI6IiIsImV4cCI6MTc2ODU2MzMzOCwiaWF0IjoxNzY3OTU4NTM4LCJyZXNvdXJjZSI6Ii9zdG9yYWdlLzAxMjlhNmZhNzUyYWIzMTE3ODhiY2RlYWI1MmI2MTIyZDRlZiJ9.cnaUjyqwCsDx_zSAzgEIn5ZQ2wBpdcMfooUI-Q603iA&download=image.png "")

> 其中，已获取数据是指通过appkey关联的数据（即在市场*中获取或购买的数据）*

> *邀请加入则是不在市场中的数据，发起方通过设置数据格式通知参与方*自己需要什么数据，参与方对应添加该数据

**主模型**：通过主模型编写整个计算的逻辑，可以通过安全多方计算以密文的方式使用子模型函数返回的数据，也可以直接明文获取子模型函数返回的数据。主模型由发起方编写。

**子模型**：每个子模型都会绑定到参与方的具体数据上，只有通过子模型才可以访问该数据。子模型由发起方编写，在调用时会首先分发给参与方审核，审核通过之后会分发到具体参与方执行。

**审核子模型**：若子模型绑定的数据是需要对使用它的子模型进行审核，则发起方在编写完后，不能直接使用该子模型，需要将子模型发送到参与方进行审核，审核通过后发起方才能使用。

**数据隐私级别**：若参与方数据设置为隐私的，则发起方无法通过明文直接获取数据，bm会对明文使用隐私数据进行报错反馈。
