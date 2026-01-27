## util库--工具扩展库

util库中封装了一些工具函数

### matrix

通用的用于存储行列数据的结构，是一个带列标签的二维数组，作为关系型数据库的返回格式

**通过require("util")引入**

```lua
通过导入工具库new一个空的matrix,暂不支持手动设置数据
util = require("util")
util.newMatrix()
```

**结构**

结构类似python dataframe，相比于dataframe简单很多，具体如下：

```lua
本质是一个二维数组，有一个标签数组对应着列数
labels:    id     tel
row1  :    11     "17888888888"
row2  :    22     "17888888889"
```

**方法**

```lua
matrix:get(1,"id")   #返回第1条记录的标签为id的元素（从1开始）
matrix:getColumn("id")   #返回标签为id列的元素列表（table作为数组）
matrix:getRow(1)   #返回第1行的元素列表（table作为数组）
matrix:add(m2)   #参数为另一个矩阵（两个矩阵的标签列表的内容和顺序必须是一致的）
					将参数中矩阵的元素添加到接收矩阵中，无返回值
matrix:rowsNum()  #返回行数(number)-对应数据库的一条记录
matrix:labels()  #返回列对应的标签table-对应查出来的字段名列表
matrix:convertToTable() #将矩阵中元素转换为table类型
```

**示例**

```lua
sql查询返回结果使用示例1:  获取id列
queryRes:=c:query("select id from test")
local ids = queryRes:getColumn("id")

sql查询返回结果使用示例2: 转为map
queryRes:=c:query("select id,name from test")
local data = queryRes:convertToTable()
```

### http

目前的http扩展库支持get/post/put/delete/header五种常见的http请求方法，支持http请求中常见的组成部分，包括header、query、body和cookies，自定义的参数支持timeout设置。

header、query、body和cookies四个组件都是map类型的table，支持自由组合。

调用接口的返回值为json字符串，包含header和body两个组成部分。

```lua
-- 导入http扩展库
http = require("http")

function main()
	-- 设置请求头（可选）
	header ={}
	header["Authorization"]="xxx"
	-- 设置请求路径参数（可选）
	query ={}
	query["task_id"]="xxx"
    query["data_id"]="xxx"
	-- 设置请求体（可选）
	body = {}
    body["model"]="xxx"
	-- 设置cookies（可选）
	cookies = {}
    cookies["cookie_key1"]="xxx"
    cookies["cookie_key2"]="xxx"
	-- 请求方法（必须）
	method = 'post'
	-- 请求路径（必须）
	url = 'http://localhost:8180/api/v2/fc/initiator/task/sub-model/update'
	-- request方法的第一个参数为请求方法，第二个参数为url，第三个参数是一个table
	-- 第三个参数用于表示组成http请求的各个部分，以及可选参数
	res, err = http.request(method, url, {
		query=query,
		header=header,
		body=body,
		cookies=cookies,
		timeout="10s" -- 支持以s,ms,us,ns为单位
	})
	if err~=nil then
		return err
	end
return res
end
	
-- 调用结果示例（json字符串）
res = "{\"header\":{\"Content-Type\":[\"application/json\"],\"Date\":[\"Mon, 01 Feb 2021 12:28:58 GMT\"]},\"body\":{\"code\":12001,\"message\":\"can not found this task\"}}"
 

```

### sleep

传入一个number参数（表明睡眠的ms数）

无返回值

示例

```lua
util = require("util")
util.sleep(100)  // 睡眠100ms
```

### currentTime

无参数

返回当前时间戳（纳秒)

示例

```lua
util = require("util")
util.currentTime()  // 当前时间戳（纳秒)
```