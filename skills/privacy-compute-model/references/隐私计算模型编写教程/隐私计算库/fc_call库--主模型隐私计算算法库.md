## fc_call库--主模型隐私计算算法库

该库只能在联邦计算主模型中导入

库导入方式

```lua
fccall = require("fc_call")
```

隐私计算的整体流程如下：

![](http://teambitiondoc.hyperchain.cn:8099/storage/0124d755c209e9f4c803e7edb7b16605fbe4?Signature=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJBcHBJRCI6IjU5Mzc3MGZmODM5NjMyMDAyZTAzNThmMSIsIl9hcHBJZCI6IjU5Mzc3MGZmODM5NjMyMDAyZTAzNThmMSIsIl9vcmdhbml6YXRpb25JZCI6IiIsImV4cCI6MTc2ODU2MzMzOCwiaWF0IjoxNzY3OTU4NTM4LCJyZXNvdXJjZSI6Ii9zdG9yYWdlLzAxMjRkNzU1YzIwOWU5ZjRjODAzZTdlZGI3YjE2NjA1ZmJlNCJ9.si7EdqhcOrm4RSjNwf8D00GTaadgXjXgDNtKro7PKWg&download=image.png "")

### 普通远程调用-normalInvoke

明文获取子模型执行的结果，**这里不涉及任何隐私。**

- **参数**

传入参数是lua的一个包含子模型信息的table map

```lua
p = {
	-- 要调用的子模型名
	modelName = "subModel1"
	-- 要调用的子模型的方法
	method = "main"
	-- 子模型方法的输入参数
	args = {1}
}
```

- **返回值**

```text
结构为子模型对应方法执行的返回
```

- **调用示例**

子模型

无返回格式限制

```lua
function main(args)
    return args
end
```

主模型

```lua
fccall = require("fc_call")

function normalInvoke()
	-- 第一种方式，先声明一个空table再为每个变量赋值
	p = {}
	p.modelName = "subModel1"
	p.method = "main"
	p.args = {{1,2}}

	-- 第二种方式，直接声明完整的table
	-- p = {
	--	 modelName = "subModel1",
	--	 method = "main",
	--	 args = {1,2}
	-- }

	data=fccall.normalInvoke(p)
	return data
end
```

**限制：**同一机构的多个数据不能同时参与一个mpc任务，同一机构的多个数据进行隐私计算是没意义的，机构内部数据都在一个BM节点上不存在隐私性。如有此类需求，可以在普通的模型(不是子模型)里面通过dbcall和http调用的方式融合多个数据，再通过这个普通模型接入到隐私计算中。

### 聚合(加减或乘除)-PSA-psaInvoke

PSA是指发起方获取两个及以上参与方数据的聚合结果（支持加减和乘除），并保护各参与方的数据安全，支持向量输入进行聚合。**具体的，如发起方需要知道参与方1的数据a与参与方数据b的求和结果，但是不能知道具体a与b的值是多少**。

> 目前，PSA算法仅支持加减或乘除，即不能进行混合运算，如a+b-c或a*b/c都是可以的，但是无法进行a+b*c。

- **参与方个数：>=2**

- **发起方输入数据：无**

- **参数**

传入参数是lua的一个不定长table数组，数组的每个数据元素是参与方的相关输入信息。

```lua
invokeData = {
	-- 节点1输入信息
	p1 = {
		-- 要调用的子模型名
		modelName = "subModel1",
		-- 要调用的子模型的方法
		method = "main",
		-- 方法的输入参数
		args = {1},
		-- 该输入的符号，为"+"和"-", 或者为"*"和"/"
		op = "+"
	},
	-- 节点2输入信息
	p2 = {
		-- 要调用的子模型名
		modelName = "subModel1",
		-- 要调用的子模型的方法
		method = "main",
		-- 方法的输入参数
		args = {1},
		-- 该输入的符号，为"+"和"-", 或者为"*"和"/"
		op = "+"
	},
	...	
}
```

- **返回值**

本算法支持batch化运算，如可以直接对向量{1,2,3}和{2,2,2}进行psa运算得到结果{3,4,5}，故输出是一个number数组。

```lua
-- number数组，如下
{3,4,5}
```

- **调用示例**

子模型

函数要求返回number数组，且在一个PSA的所有子模型输入中，返回的number数组长度必须相等。

```lua
-- 这里为了方便mock实现一个返回，省略去数据库取数据的操作，直接返回结果
function main()
    return {1,2,3}
end
```

主模型

```lua
fccall = require("fc_call")

function main()
	-- 写法1
	p1 = {}
	p1.modelName = "subModel1"
	p1.method = "main"
	p1.args = {1}
	p1.op = "+"
	-- 也可以写成
	-- p1 = {
	--	 modelName = "subModel1",
	--	 method = "main",
	--	 args = {1},
	--	 op = "+"
	-- }

	p2 = {}
	p2.modelName = "subModel2"
	p2.method = "main"
	p2.args = {2}
	p2.op = "+"

	invokeData = {p1,p2}
	data=fccall.psaInvoke(invokeData)
	return data
end
```

### 同态加法-ADD-addInvoke

同态加法是指发起方获取两个及以上参与方数据的聚合结果（支持加法），并保护各参与方的数据安全，支持向量输入进行聚合。**具体的，如发起方需要知道参与方1的数据a与参与方数据b的求和结果，但是不能知道具体a与b的值是多少**。

- **参与方个数：>=2**

- **发起方输入数据：无**

- **参数**

传入参数是lua的一个不定长table数组，数组的每个数据元素是参与方的相关输入信息。

```lua
invokeData = {
	-- 节点1输入信息
	p1 = {
		-- 要调用的子模型名
		modelName = "subModel1",
		-- 要调用的子模型的方法
		method = "main",
		-- 方法的输入参数
		args = {1}
	},
	-- 节点2输入信息
	p2 = {
		-- 要调用的子模型名
		modelName = "subModel2",
		-- 要调用的子模型的方法
		method = "main",
		-- 方法的输入参数
		args = {1}
	},
	...	
}
```

- **返回值**

本算法支持batch化运算，如可以直接对向量{1,2,3}和{2,2,2}进行psa运算得到结果{3,4,5}，故输出是一个number数组。

```lua
-- number数组，如下
{3,4,5}
```

- **调用示例**

子模型

函数要求返回number数组，且在一个同态加法的所有子模型输入中，返回的number数组长度必须相等。

```lua
-- 这里为了方便mock实现一个返回，省略去数据库取数据的操作，直接返回结果
function main()
    return {1,2,3}
end
```

主模型

```lua
fccall = require("fc_call")

function main()
	-- 写法1
	p1 = {}
	p1.modelName = "subModel1"
	p1.method = "main"
	p1.args = {1}
	-- 也可以写成
	-- p1 = {
	--	 modelName = "subModel1",
	--	 method = "main",
	--	 args = {1},
	-- }

	p2 = {}
	p2.modelName = "subModel2"
	p2.method = "main"
	p2.args = {2}

	invokeData = {p1,p2}
	data=fccall.addInvoke(invokeData)
	return data
end
```

### 同态乘法-Mul-mulInvoke

同态乘法是指发起方获取两个及以上参与方数据的乘法结果，并保护各参与方的数据安全，支持向量输入进行聚合。**具体的，如发起方需要知道参与方1的数据a与参与方数据b的求积结果，但是不能知道具体a与b的值是多少**。

- **参与方个数：>=2**

- **发起方输入数据：无**

- **参数**

传入参数是lua的一个不定长table数组，数组的每个数据元素是参与方的相关输入信息。

```lua
invokeData = {
	-- 节点1输入信息
	p1 = {
		-- 要调用的子模型名
		modelName = "subModel1",
		-- 要调用的子模型的方法
		method = "main",
		-- 方法的输入参数
		args = {1}
	},
	-- 节点2输入信息
	p2 = {
		-- 要调用的子模型名
		modelName = "subModel2",
		-- 要调用的子模型的方法
		method = "main",
		-- 方法的输入参数
		args = {1}
	},
	...	
}
```

- **返回值**

本算法支持batch化运算，如可以直接对向量{1,2,3}和{2,2,2}进行同态乘法运算得到结果{2,4,6}，故输出是一个number数组。

```lua
-- number数组，如下
{2,4,6}
```

- **调用示例**

子模型

函数要求返回number数组，且在一个乘法的所有子模型输入中，返回的number数组长度必须相等。

```lua
-- 这里为了方便mock实现一个返回，省略去数据库取数据的操作，直接返回结果
function main()
    return {1,2,3}
end
```

主模型

```lua
fccall = require("fc_call")

function main()
	-- 写法1
	p1 = {}
	p1.modelName = "subModel1"
	p1.method = "main"
	p1.args = {1}
	-- 也可以写成
	-- p1 = {
	--	 modelName = "subModel1",
	--	 method = "main",
	--	 args = {1},
	-- }

	p2 = {}
	p2.modelName = "subModel2"
	p2.method = "main"
	p2.args = {2}

	invokeData = {p1,p2}
	data=fccall.mulInvoke(invokeData)
	return data
end
```

### 平均数-Avg-avgInvoke

Avg是隐私平均数算法，可以获得多个参与方的数据的平均数是多少，但是不暴露每个参与方数据集的具体数据，支持向量输入。

- **参与方个数：>=2**

- **发起方输入数据：本方数据集**

- **参数**

传入两个参数，第一个参数是本方数据集（number数组），第二个参数是参与方列表（lua的一个不定长table数组），该数组的每个数据是参与方的相关输入信息。

```lua
-- 发起方输入数据集
-- 可以直接是一个数据集，通常在不绑定子模型的情况下使用，如
initiatorData = {1,2,3}
-- 也可以是如参与方一样的query信息，通常在绑定子模型的情况下使用，如
initiatorData = {
	-- 要调用的子模型名
	modelName = "subModel1",
	-- 要调用的子模型的方法
	method = "main",
	-- 方法的输入参数
	args = {1，2}
}
-- 参与方列表
participantData = {
	-- 节点1输入信息
	{
		-- 要调用的子模型名
		modelName = "subModel1",
		-- 要调用的子模型的方法
		method = "main",
		-- 方法的输入参数
		args = {1，2}
	},
	-- 节点2输入信息
	{
		-- 要调用的子模型名
		modelName = "subModel2",
		-- 要调用的子模型的方法
		method = "main",
		-- 方法的输入参数
		args = {2.56，3.14}
	},
	...	
}
```

- **返回值**

支持向量输入，代表如果发起方有数据{1,2,3}，参与方1有数据{3,4,5}，参与方2有数据{5,6,7}，则可以求~~出~~每一行的平均数是多少，如第一行的平均数为(1+3+5)/3=3。

```lua
-- number数组
{3,4,5}
```

- **调用示例**

子模型

函数要求返回number数组。

```lua
function main()
    return {1,2,3}
end
```

主模型

```lua
fccall = require("fc_call")
function main()
	-- 添加发起方数据
	p1 = genData()
	-- 如果发起方有对应子模型，也可以写成
	-- p1 = {}
	-- p1.modelName = "GenData"
	-- p1.method = "getData"
	-- p1.args = {0,1,3}


	-- 添加参与方2参数
	p2 = {}
	p2.modelName = "GenData1"
	p2.method = "getP2Data"
	p2.args = {0,1,3}

	-- 添加参与方3参数
	p3 = {}
	p3.modelName = "GenData2"
	p3.method = "getP2Data"
	p3.args = {1,2,4}

	invokeData = {p2,p3}
	data=fccall.avgInvoke(p1, invokeData)
	return data
end

function genData()
	return {1,2,3,4}
end
```

### 方差-Var-varInvoke

Var是隐私方差算法，可以获得多个参与方的数据集归并后的方差是多少，但是不暴露每个参与方数据集的具体数据。

- **参与方个数：>=2**

- **发起方输入数据：本方数据集**

- **参数**

传入两个参数，第一个参数是本方数据集（number数组），第二个参数是参与方列表（lua的一个不定长table数组），该数组的每个数据是参与方的相关输入信息。

```lua
-- 发起方输入数据集
-- 可以直接是一个数据集，通常在不绑定子模型的情况下使用，如
initiatorData = {1,2,3}
-- 也可以是如参与方一样的query信息，通常在绑定子模型的情况下使用，如
initiatorData = {
	-- 要调用的子模型名
	modelName = "subModel1",
	-- 要调用的子模型的方法
	method = "main",
	-- 方法的输入参数
	args = {1，2}
}
-- 参与方列表
participantData = {
	-- 节点1输入信息
	{
		-- 要调用的子模型名
		modelName = "subModel1",
		-- 要调用的子模型的方法
		method = "main",
		-- 方法的输入参数
		args = {1，2}
	},
	-- 节点2输入信息
	{
		-- 要调用的子模型名
		modelName = "subModel2",
		-- 要调用的子模型的方法
		method = "main",
		-- 方法的输入参数
		args = {2.56，3.14}
	},
	...	
}
```

- **返回值**

```lua
-- number
2.2
```

- **调用示例**

子模型

函数要求返回number数组。

```lua
function main()
    return {1,2,3}
end
```

主模型

```lua
fccall = require("fc_call")
function main()
	-- 添加发起方数据
	p1 = genData()
	-- 如果发起方有对应子模型，也可以写成
	-- p1 = {}
	-- p1.modelName = "GenData"
	-- p1.method = "getData"
	-- p1.args = {1,2,3,4}

	-- 添加参与方2参数
	p2 = {}
	p2.modelName = "GenData1"
	p2.method = "getP2Data"
	p2.args = {0,1,3}

	-- 添加参与方3参数
	p3 = {}
	p3.modelName = "GenData2"
	p3.method = "getP2Data"
	p3.args = {1,2,4}

	invokeData = {p2,p3}
	data=fccall.varInvoke(p1, invokeData)
	return data
end

function genData()
	return {1,2,3,4}
end
```

### 内积-InnerProduct-innerproductInvoke

InnerProduct是隐私内积算法，可以获取本方数据集合对方数据集的内积数据，保护双方数据集的具体数据。

- **参与方个数：1**

- **发起方输入数据：本方数据集**

- **参数**

传入两个参数，第一个参数是本方数据集（number数组），第二个参数是参与方列表（lua的一个不定长table数组），该数组的每个数据是参与方的相关输入信息。

注意，首先发起方和参与方的输入向量长度必须一致（不一致无法求内积），其次，向量长度不得小于3，否则存在安全性问题。

```lua
-- 发起方数据集
-- 可以直接是一个数据集，通常在不绑定子模型的情况下使用，如
initiatorData = {1,2}
-- 也可以是如参与方一样的query信息，通常在绑定子模型的情况下使用，如
initiatorData = {
	-- 要调用的子模型名
	modelName = "subModel1",
	-- 要调用的子模型的方法
	method = "main",
	-- 方法的输入参数
	args = {1，2}
}

-- 参与方输入信息
participantData = {
	-- 要调用的子模型名
	modelName = "subModel",
	-- 要调用的子模型的方法
	method = "main",
	-- 方法的输入参数
	args = {1}
}

```

- **返回值**

```lua
-- number
2.2
```

- **调用示例**

子模型

函数要求返回number数组。且数组大小必须与发起方数据集大小一致

```lua
function main()
    return {1,2,3}
end
```

主模型

```lua
fccall = require("fc_call")
function main()
	-- 添加发起方数据
	p1 = genData()
	-- 如果发起方有对应子模型，也可以写成
	-- p1 = {}
	-- p1.modelName = "GenData"
	-- p1.method = "getData"
	-- p1.args = {1,2,3}


	-- 添加参与方参数
	p2 = {}
	p2.modelName = "GenData1"
	p2.method = "getP2Data"
	p2.args = {0,1,3}

	data=fccall.innerproductInvoke(p1, p2)
	return data
end

function genData()
	return {1,2,3}
end
```

### 比较-Cmp-cmpInvoke

compare是隐私比较算法，可以比较发起方数据和参与方的数据大小，但是不暴露参与方数据。支持向量的比较。

- **参与方个数：1**

- **发起方输入数据：本方数据集**

- **参数**

传入两个参数，第一个参数是本节点输入数据（数组），第二个参数是参与方相关输入信息。

```lua
-- 发起方数据集
-- 可以直接是一个数据集，通常在不绑定子模型的情况下使用，如
initiatorData = {1,2,3}
-- 也可以是如参与方一样的query信息，通常在绑定子模型的情况下使用，如
initiatorData = {
	-- 要调用的子模型名
	modelName = "subModel1",
	-- 要调用的子模型的方法
	method = "main",
	-- 方法的输入参数
	args = {1，2}
}

-- 参与方输入信息
participantData = {
	-- 要调用的子模型名
	modelName = "subModel",
	-- 要调用的子模型的方法
	method = "main",
	-- 方法的输入参数
	args = {1}
}

```

- **返回值**

```lua
-- +1表示发起方数据大于参与方数据，0表示两方数据相等，-1表示发起方数据小于参与方数据
-- number数组
{ 1, 0, -1}
```

- **调用示例**

子模型

函数要求返回number数组。

```lua
function main(args)
    return args
end
```

主模型

```lua
fccall = require("fc_call")

function cmp_test()
    p1 = {1,2}
	-- 如果发起方有对应子模型，也可以写成
	-- p1 = {}
	-- p1.modelName = "GenData"
	-- p1.method = "getData"
	-- p1.args = {1,2,3}


    p2 = {}
    p2.modelName = "submodel-001"
    p2.method = "main"
    p2.args = {{-3.2, 7}}

    data = fccall.cmpInvoke(p1, p2)
    return data
end
```

### 中位数-Median-medianInvoke

Median是隐私中位数算法，可以获得多个参与方的数据集归并后的中位数是多少，但是不暴露每个参与方数据集的具体数据。不支持向量

- **参与方个数：>=2**

- **发起方输入数据：无**

- **参数**

传入参数是lua的一个不定长table数组，数组的每个数据是参与方的相关输入信息。

```lua
participantData = {
	-- 节点1输入信息
	{
		-- 要调用的子模型名
		modelName = "subModel1",
		-- 要调用的子模型的方法
		method = "main",
		-- 方法的输入参数
		args = {1，2}
	},
	-- 节点2输入信息
	{
		-- 要调用的子模型名
		modelName = "subModel2",
		-- 要调用的子模型的方法
		method = "main",
		-- 方法的输入参数
		args = {2.56，3.14}
	},
	...	
}
```

- **返回值**

```lua
-- Number
10
```

- **调用示例**

子模型

函数要求返回number数组

```lua
function main()
    return {1,2,3}
end
```

主模型

```lua
fccall = require("fc_call")
function main()
	-- 添加参与方1参数
	p1 = {}
	p1.modelName = "GenData1"
	p1.method = "getP2Data"
	p1.args = {0,1,3}

	-- 添加参与方2参数
	p2 = {}
	p2.modelName = "GenData2"
	p2.method = "getP2Data"
	p2.args = {1,2,4}

	invokeData = {p1,p2}
	data=fccall.medianInvoke(invokeData)
	return data
end
```

### 最大值-Max-maxInvoke

Max是隐私最大值算法，可以获得多个参与方的数据集对应序号的最大值是多少，但是不暴露每个参与方数据集的具体数据。支持向量（求每一行的最大值）

- **参与方个数：>=2**

- **发起方输入数据：无**

- **参数**

传入参数是lua的一个不定长table数组，数组的每个数据是参与方的相关输入信息。

```lua
participantData = {
	-- 节点1输入信息
	{
		-- 要调用的子模型名
		modelName = "subModel1",
		-- 要调用的子模型的方法
		method = "main",
		-- 方法的输入参数
		args = {1，2}
	},
	-- 节点2输入信息
	{
		-- 要调用的子模型名
		modelName = "subModel2",
		-- 要调用的子模型的方法
		method = "main",
		-- 方法的输入参数
		args = {2.56，3.14}
	},
	...	
}
```

- **返回值**

```lua
-- number数组
{10,20}
```

- **调用示例**

子模型

函数要求返回number数组，所有参与方返回的数组长度必须一致

```lua
function main()
    return {1,2}
end
```

主模型

```lua
fccall = require("fc_call")
function main()
	-- 添加参与方1参数
	p1 = {}
	p1.modelName = "GenData1"
	p1.method = "getP2Data"
	p1.args = {0,1,3}

	-- 添加参与方2参数
	p2 = {}
	p2.modelName = "GenData2"
	p2.method = "getP2Data"
	p2.args = {1,2,4}

	invokeData = {p1,p2}
	data=fccall.maxInvoke(invokeData)
	return data
end
```

### 最小值-Min-minInvoke

Min是隐私最小值算法，可以获得多个参与方的数据集对应序号的最小值是多少，但是不暴露每个参与方数据集的具体数据。支持向量（求每一行的最小值）

- **参与方个数：>=2**

- **发起方输入数据：无**

- **参数**

传入参数是lua的一个不定长table数组，数组的每个数据是参与方的相关输入信息。

```lua
participantData = {
	-- 节点1输入信息
	{
		-- 要调用的子模型名
		modelName = "subModel1",
		-- 要调用的子模型的方法
		method = "main",
		-- 方法的输入参数
		args = {1，2}
	},
	-- 节点2输入信息
	{
		-- 要调用的子模型名
		modelName = "subModel2",
		-- 要调用的子模型的方法
		method = "main",
		-- 方法的输入参数
		args = {2.56，3.14}
	},
	...	
}
```

- **返回值**

```lua
-- number数组
{10,20}
```

- **调用示例**

子模型

函数要求返回number数组，所有参与方返回的数组长度必须一致

```lua
function main()
    return {1,2}
end
```

主模型

```lua
fccall = require("fc_call")
function main()
	-- 添加参与方1参数
	p1 = {}
	p1.modelName = "GenData1"
	p1.method = "getP2Data"
	p1.args = {0,1,3}

	-- 添加参与方2参数
	p2 = {}
	p2.modelName = "GenData2"
	p2.method = "getP2Data"
	p2.args = {1,2,4}

	invokeData = {p1,p2}
	data=fccall.minInvoke(invokeData)
	return data
end
```

### 交集-PSI-psiInvoke

PSI是指求多方数据集交集，并保护交集之外的数据隐私性

支持本方和其他多方的数据集交集，也支持本方没有数据集，求其他方之间的数据集交集

- **参与方个数：至少1个**

- **发起方输入数据：本方数据集或者空**

- **参数**

传入两个参数是lua的两个table数组，第一个参数是本节点输入数据集(可通过访问数据库获取，要求是字符串数组，其他类型数组会被自动转为字符串数组)，本方没有数据时则输入nil，第二个参数是参与方相关输入信息（单个或数组）。

```lua
-- 发起方数据集
-- 可以直接是一个数据集，通常在不绑定子模型的情况下使用，如
initiatorData = {"1","2"}
-- 也可以是如参与方一样的query信息，通常在绑定子模型的情况下使用，如
initiatorData = {
	-- 要调用的子模型名
	modelName = "subModel1",
	-- 要调用的子模型的方法
	method = "main",
	-- 方法的输入参数
	args = {"1"，"2"}
}

-- 参与方输入信息
单个参与方
participantData = {
	-- 要调用的子模型名
	modelName = "subModel"
	-- 要调用的子模型的方法
	method = "main"
	-- 方法的输入参数
	args = {"1"}
}
多个参与方
participantData = {
	{
		-- 要调用的子模型名
		modelName = "subModel1"
		-- 要调用的子模型的方法
		method = "main"
		-- 方法的输入参数
		args = {"1"}
	}
	{
		-- 要调用的子模型名
		modelName = "subModel2"
		-- 要调用的子模型的方法
		method = "main"
		-- 方法的输入参数
		args = {"1"}
	}
}


```

- **返回值**

```lua
-- string数组
{"id1", "id2"}
```

- **调用示例**

子模型

函数要求返回字符串数组，其他类型数组会被自动转为字符串数组。

```lua
function main()
    return {"1","2"}
end
```

主模型

```lua
fccall = require("fc_call")

-- 求本方和其他方数据集交集 
function main()
    p1 = {'1','2'}
	-- 如果发起方有对应子模型，也可以写成
	-- p1 = {}
	-- p1.modelName = "subModel1"
	-- p1.method = "main"
	-- p1.args = {"1"}
	-- 如果本方没有数据
	-- p1 = nil


    p2 = {}
    p2.modelName = "subModel"
    p2.method = "main"
    p2.args = {}

    data=fccall.psiInvoke(p1,p2)
    return data
end

-- 求本方和多方数据集交集 
function main2()
    p1 = {'1','2'}
	-- 如果发起方有对应子模型，也可以写成
	-- p1 = {}
	-- p1.modelName = "subModel1"
	-- p1.method = "main"
	-- p1.args = {"1"}
	-- 如果本方没有数据
	-- p1 = nil

    p2 = {}
    p2.modelName = "subModel1"
    p2.method = "main"
    p2.args = {}

    p3 = {}
    p3.modelName = "subModel2"
    p3.method = "main"
    p3.args = {}


    data=fccall.psiInvoke(p1,{p2,p3})

    return data
end

```

### 差集-PSD-psdInvoke

PSD是指将本方数据集和另一方数据集求差集，并保护对方交集之外的数据隐私性

- **参与方个数：1**

- **发起方输入数据：本方数据集**

- **参数**

传入两个参数是lua的两个table数组，第一个参数是本节点输入数据集(可通过访问数据库获取，要求是字符串数组，其他类型数组会被自动转为字符串数组)，第二个参数是参与方相关输入信息。

```lua
-- 发起方数据集
-- 可以直接是一个数据集，通常在不绑定子模型的情况下使用，如
initiatorData = {"1","2"}
-- 也可以是如参与方一样的query信息，通常在绑定子模型的情况下使用，如
initiatorData = {
	-- 要调用的子模型名
	modelName = "subModel1",
	-- 要调用的子模型的方法
	method = "main",
	-- 方法的输入参数
	args = {"1"，"2"}
}

-- 参与方输入信息
participantData = {
	-- 要调用的子模型名
	modelName = "subModel"
	-- 要调用的子模型的方法
	method = "main"
	-- 方法的输入参数
	args = {"1"}
}


```

- **返回值**

```lua
-- string数组
{"id1", "id2"}
```

- **调用示例**

子模型

函数要求返回字符串数组，其他类型数组会被自动转为字符串数组。

```lua
function main()
    return {"1","2"}
end
```

主模型

```lua
fccall = require("fc_call")

function main()
    p1 = {'1','2'}
	-- 如果发起方有对应子模型，也可以写成
	-- p1 = {}
	-- p1.modelName = "subModel1"
	-- p1.method = "main"
	-- p1.args = {"1"}


    p2 = {}
    p2.modelName = "subModel"
    p2.method = "main"
    p2.args = {}

    data=fccall.psdInvoke(p1,p2)
    return data
end
```

### 并集-PSU-psuInvoke

P﻿SU是指发起方获得多方数据的并集，但无法获知某个数据具体来自哪里，同时，各参与方之间无法获得对方的数据。

- **参与方个数：>=2**

- **发起方输入数据：无**

- **参数**

传入参数是lua的一个不定长table数组，数组的每个数据元素是参与方的相关输入信息。

```lua
participantData = {
	-- 节点1输入信息
	{
		-- 要调用的子模型名
		modelName = "subModel1",
		-- 要调用的子模型的方法
		method = "main",
		-- 方法的输入参数
		args = {"1"}
	},
	-- 节点2输入信息
	{
		-- 要调用的子模型名
		modelName = "subModel2",
		-- 要调用的子模型的方法
		method = "main",
		-- 方法的输入参数
		args = {"1"}
	},
	...	
}
```

- **返回值**

```lua
-- string数组
{"id1", "id2"}
```

- **调用示例**

子模型

函数要求返回字符串数组，其他类型数组会被自动转为字符串数组。

```lua
function main()
    return {"id1","id2"}
end
```

主模型

```lua
fccall = require("fc_call")
function main()
	-- 添加参与方1参数
	p1 = {}
	p1.modelName = "GenData1"
	p1.method = "getP2Data"
	p1.args = {0,1,3}

	-- 添加参与方2参数
	p2 = {}
	p2.modelName = "GenData2"
	p2.method = "getP2Data"
	p2.args = {1,2,4}

	invokeData = {p1,p2}
	data=fccall.psuInvoke(invokeData)
	return data
end
```

### 隐私查询-PIR-pirInvoke

PIR算法是隐私查询算法，可以根据key隐私查询key对应的value，整个过程发起方无法查询到其他数据，参与方也无法感知发起方查询到的数据是哪一个。

- **参与方个数：1**

**发起方输入数据：查询key集合**

- **参数**

传入两个参数，第一个参数是本节点输入数据，第二个参数是参与方相关输入信息。

```lua
-- 本节点输入查询数据集
-- 可以直接是一个数据集，通常在不绑定子模型的情况下使用，如
inititatorData = {"id1","id2", "id3"},
-- 也可以是如参与方一样的query信息，通常在绑定子模型的情况下使用，如
initiatorData = {
	-- 要调用的子模型名
	modelName = "subModel1",
	-- 要调用的子模型的方法
	method = "main",
	-- 方法的输入参数
	args = {"id1","id2", "id3"}
}

-- 参与方输入信息
{
	-- 要调用的子模型名
	modelName = "subModel"
	-- 要调用的子模型的方法
	method = "main"
	-- 方法的输入参数
	args = {1}
}

```

- **返回值**

```lua
-- 返回二维数组，一维长度是对应查询数据集的大小，元素是对应查出的数据列表
{ {},{"value"} }
```

- **调用示例**

子模型

返回值必须是keys和values的map，keys和values都是字符串数组，key的位置和value的位置一一对应，其大小必须相等

```lua
function main()
    return { keys={ "3", "4", "4" }, values={ "v-3", "v-4", "v-44" } }
end
```

主模型

```lua
fccall = require("fc_call")

function pir_test()
    p1 = {"4"}
	-- 如果发起方有对应子模型，也可以写成
	-- p1 = {}
	-- p1.modelName = "subModel1"
	-- p1.method = "main"
	-- p1.args = {"1"}


    p2 = {}
    p2.modelName = "subModel"
    p2.method = "main"
    p2.args = {}

    data=fccall.pirInvoke(p1,p2)
    return data
end

```

### 隐私查询预处理-PIR-pirInvokeWithPreprocess

PIR算法是隐私查询算法，可以根据key隐私查询key对应的value，整个过程发起方无法查询到其他数据，参与方也无法感知发起方查询到的数据是哪一个。

隐私查询预处理是指参与方被查询的数据是提前预处理过的，可极大提高pir算法查询的效率。参与方数据必须是预处理数据时，子模型是无效不会被调用，主模型中只需要指定预处理数据对应的子模型名即可，预处理数据支持多字段构成key和value。

- **参与方个数：1**

**发起方输入数据：查询key集合(每个key由多个字段组成)**

- **参数**

传入两个参数，第一个参数是本节点输入数据，第二个参数是参与方相关输入信息。

```lua
-- 本节点输入查询数据集
-- 可以直接是一个数据集，通常在不绑定子模型的情况下使用，如
inititatorData = {
	{"字段1的值1","字段2的值1"},
	{"字段1的值2","字段2的值2"},
	{"字段1的值3","字段2的值3"}
}
-- 也可以是如参与方一样的query信息，通常在绑定子模型的情况下使用，如
initiatorData = {
	-- 要调用的子模型名
	modelName = "subModel1",
	-- 要调用的子模型的方法
	method = "main",
	-- 方法的输入参数
	args = {"id1","id2", "id3"}
}

-- 参与方输入信息
{
	-- 要查询的预处理数据的的子模型名
	modelName = "subModel"
}

```

- **返回值**

```lua
-- 返回二维数组，一维长度是对应查询数据集的大小，元素是对应查出的数据列表(可能一个key查询出多个值)
-- 单个数据是由多个字段的值构成
{ {},{{"field_1":"1","field_2":"2"}} }
```

- **调用示例**

子模型

**不生效**

主模型

```lua
fccall = require("fc_call")

function pir_test()
    p1 = {{"张三","17888888888"}}
	-- 如果发起方有对应子模型，也可以写成
	-- p1 = {}
	-- p1.modelName = "subModel1"
	-- p1.method = "main"
	-- p1.args = {"1"}

    p2 = {}
    p2.modelName = "subModel"
    p2.method = "main"
    p2.args = {}

    data=fccall.pirInvokeWithPreprocess(p1,p2)
    return data
end

```