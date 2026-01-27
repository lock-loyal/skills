## data_call库--子模型数据导入库

该库只能在联邦计算**子模型**中导入

库导入方式

```lua
datacall = require("data_call")
```

调用函数都是相同的，只是参数会根据子模型对应的数据类型进行自动重载

```lua
data = datacall.call(p)
```

目前对应着三个大类的数据类型：`共享数据`，`邀请数据`和`本地数据`。

1. 共享数据是指在市场中获取或购买的数据，使用Appkey形式关联。

1. 邀请数据是在隐私计算过程中发起方邀请参与方添加某种格式的数据

1. 本地数据为机构自己上传的数据

目前邀请数据和导入数据仅支持导入数据，更具体的，为csv文件，未来将会支持Mysql等数据源直接连接的方式。

### 访问共享数据为Mysql数据源数据

表名必须为defaultTable，BitXMesh会动态替换成真实表名，字段为真实字段

- **参数**

```lua
p = {
	sql = "select employeeInfo from defaultTable"
}
```

- **返回值**

```lua
matrix对象
```

- **调用示例**

```lua
datacall = require("data_call")

p = {
	sql = "select employeeInfo from defaultTable"
}
-- 或者可以写为
-- p = {}
-- p.sql = "select employeeInfo from defaultTable"
data = datacall.call(p)
-- 因为返回值是一个matrix对象，故如果需要对应行的数据，则需要取出该部分数据
res = data:getColumn("employeeInfo")
```

### 访问共享数据为Oracle数据源数据

- **参数**

```lua
p = {
	sql = "select * from defaultTable"
}
```

- **返回值**

```lua
matrix对象
```

- **调用示例**

```lua
datacall = require("data_call")

p = {
	sql = "select ID from defaultTable"
}
data = datacall.call(p)
-- 因为返回值是一个matrix对象，故如果需要对应行的数据，则需要取出该部分数据
res = data:getColumn("ID")
```

### 访问共享数据为Mongo数据源数据

- **参数**

```lua
p = {
	query = "{\"name\":\"11\"}",
	isAll=false, 
	page=1,
	size = 10
}
```

- **返回值**

```lua
嵌套table，和查询结果结构一致
```

- **调用示例**

```lua
datacall = require("data_call")

p = {
	query = "{\"name\":\"11\"}",
	isAll=false, 
	page=1,
	size = 10
}
data = datacall.call(p)
```

### 访问共享数据为模型数据

- **参数**

```lua
p = {
	--模型方法
	method = "main",
	-- 模型调用参数
	args = {1, 2}
}
```

- **返回值**

```lua
嵌套table，和模型的返回值结构一致
```

- **调用示例**

```lua


require("data_call")

p = {
	method = "main",
	args = {1, 2}
}
data = datacall.call(p)
```

### 访问共享数据为Restful接口数据

- **参数**

```lua
p = {
	--url上面的参数，字符串数组
	query = {"1", "2"},
	--请求头，字符串到字符串的map
	header = {header1="value1"},
	--请求体，json字符串
	body = "{\"key\":1}"
}
```

- **返回值**

```lua
嵌套table，和接口的返回值结构一致
```

- **调用示例**

```lua
datacall = require("data_call")

p = {
	--url上面的参数，字符串数组
	query = {"1", "2"},
	--请求头，字符串到字符串的map
	header = {"header1":"value1"},
	--请求体，json字符串
	body = "{\"key\":1}"
}
data = datacall.call(p)
```

### 访问邀请数据为导入数据

表名必须为defaultTable，BitXMesh会动态替换成真实表名，字段为发起方映射所用的字段

- **参数**

```lua
p = {
	sql = "select id from defaultTable"
}
```

- **返回值**

```lua
matrix对象
```

- **调用示例**

```lua
datacall = require("data_call")

p = {
	sql = "select id from defaultTable"
}
data = datacall.call(p)
```

### 访问本地数据为导入数据

表名必须为defaultTable，BitXMesh会动态替换成真实表名，字段为真实字段

- **参数**

```lua
p = {
	sql = "select id from defaultTable"
}
```

- **返回值**

```lua
matrix对象
```

- **调用示例**

```lua
datacall = require("data_call")

p = {
	sql = "select id1,id2 from defaultTable"
}
data = datacall.call(p)
```