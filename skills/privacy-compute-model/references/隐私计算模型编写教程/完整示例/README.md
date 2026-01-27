# 完整示例

---

## 主内容

# 完整示例

本章将以PSA为例写出一个完整的模型示例以供参考，注意，对应不同算法的情况不同，具体情况请参考隐私计算库对应部分进行相应修改。

场景描述：趣链，产链和数钮都有员工信息表，该表中有员工的收入信息，现在需要统计三家机构的员工平均收入为多少，数据详情如下

| 姓名     | 身份证号   | 电话号码   | 入职时间   | 年龄  | 收入    |
| ------ | ------ | ------ | ------ | --- | ----- |
| string | string | string | string | int | float |

1. 以共享数据为例，首先发起方获得产链与数钮共享的数据，新建对应隐私计算任务，并添加对应数据。

![](http://teambitiondoc.hyperchain.cn:8099/storage/01290c03a4d745aa74c398105b50123ae242?Signature=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJBcHBJRCI6IjU5Mzc3MGZmODM5NjMyMDAyZTAzNThmMSIsIl9hcHBJZCI6IjU5Mzc3MGZmODM5NjMyMDAyZTAzNThmMSIsIl9vcmdhbml6YXRpb25JZCI6IiIsImV4cCI6MTc2ODU2MzMzOCwiaWF0IjoxNzY3OTU4NTM4LCJyZXNvdXJjZSI6Ii9zdG9yYWdlLzAxMjkwYzAzYTRkNzQ1YWE3NGMzOTgxMDViNTAxMjNhZTI0MiJ9.z-5OXwwJGRdRQq42OreL7JULUWvoh3d4V2yvht8dv6o&download=image.png "")

1. 添加对应数据的子模型并通知审核，这里三个模型的代码都如下所示

```lua
datacall = require("data_call")

function main()
    p = {
		-- 所有的表都为DefaultTable，bxm会自动填充表名
        sql = "select sum(收入) as income, count(收入) as num from defaultTable"
    }
    data = datacall.call(p)
	-- psa算法需要输入数组，matrix的格式不符合，故需要在子模型中进行拼接
    res = {data:get(1, "income"), data:get(1, "num")}
    return res
end

```

1. 添加主模型代码

```lua
fccall = require("fc_call")
function main()
	-- 添加趣链数据
	p1 = {}
	p1.modelName = "submodel-003"
	p1.method = "main"
	p1.args = {}

	-- 添加产链参数
	p2 = {}
	p2.modelName = "submodel-001"
	p2.method = "main"
	p2.args = {}
    p2.op = "+"

	-- 添加数钮参数
	p3 = {}
	p3.modelName = "submodel-002"
	p3.method = "main"
	p3.args = {}
    p3.op = "+"

    -- 使用psa获得收入总和与员工总和
    -- 目前avg的功能还未覆盖此场景，我们会尽快接入
	invokeData = {p2,p3}
	res = fccall.psaInvoke(invokeData)

    -- 获得本地数据结果
    localRes = fccall.normalInvoke(p1)

    -- 收入总和
    incomeSum = localRes[1] + res[1]
    -- 人数总和
    numSUm = localRes[2] + res[2]
    avg = incomeSum/numSUm
	return avg
end

```

1. 部署模型并运行

![](http://teambitiondoc.hyperchain.cn:8099/storage/0129adbf4456c10894233ab7044ac2cfcf06?Signature=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJBcHBJRCI6IjU5Mzc3MGZmODM5NjMyMDAyZTAzNThmMSIsIl9hcHBJZCI6IjU5Mzc3MGZmODM5NjMyMDAyZTAzNThmMSIsIl9vcmdhbml6YXRpb25JZCI6IiIsImV4cCI6MTc2ODU2MzMzOCwiaWF0IjoxNzY3OTU4NTM4LCJyZXNvdXJjZSI6Ii9zdG9yYWdlLzAxMjlhZGJmNDQ1NmMxMDg5NDIzM2FiNzA0NGFjMmNmY2YwNiJ9.A3OWymfIqB-1oO2_guiO-HuBFGcEVuv-YcBolQryiIc&download=image.png "")
