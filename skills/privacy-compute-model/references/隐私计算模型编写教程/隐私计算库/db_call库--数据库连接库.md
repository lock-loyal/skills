## db_call库--数据库连接库

通过require("db_call")引入，用以进行数据库连接操作。

### mysql

**getMysqlConnection方法**

- **参数**

| 字段       | 类型     | 描述   | 必要字段 | 示例          |
| -------- | ------ | ---- | ---- | ----------- |
| host     | string | 主机号  | 是    | "127.0.0.1" |
| port     | number | 端口   | 是    | 3306        |
| database | string | 数据库名 | 是    | "test_db"   |
| user     | string | 用户名  | 是    | "root"      |
| password | string | 密码   | 是    | "admin"     |

- **返回值**

```lua
mysql连接对象
包含query函数
```

- **示例**

```lua
-- 导入扩展库
dbcall = require("db_call")
-- 拿到一个mysql连接对象（会使用连接池，不存在则会创建并缓存一段时间）
-- local是本地变量的关键字，使用local关键字后会避免很多可能发生的错误，建议使用local的方式声明变量
local c = dbcall.getMysqlConnection({host = '127.0.0.1', port = 3306, database = 'test', user = 'root', password = 'admin'})
```

**mysql连接对象**~~**-**~~**query方法**

- **参数**

| 字段  | 类型     | 描述    | 必要字段 | 示例                   |
| --- | ------ | ----- | ---- | -------------------- |
| sql | string | sql语句 | 是    | "select * from test" |

- **返回值**

```lua
matrix对象
```

- **示例**

```lua
-- 导入扩展库
dbcall = require("db_call")
-- 拿到一个mysql连接对象（会使用连接池，不存在则会创建并缓存一段时间）
local c = dbcall.getMysqlConnection({host = '127.0.0.1', port = 3306, database = 'test', user = 'root', password = 'admin'})
-- 查询
local res = c:query({sql="select * from test"})
```

### postgresql

**getPostgresConnection方法**

- **参数**

| 字段       | 类型     | 描述   | 必要字段 | 示例          |
| -------- | ------ | ---- | ---- | ----------- |
| host     | string | 主机号  | 是    | "127.0.0.1" |
| port     | number | 端口   | 是    | 1521        |
| database | string | 数据库名 | 是    | "test_db"   |
| user     | string | 用户名  | 是    | "root"      |
| password | string | 密码   | 是    | "admin"     |

- **返回值**

```lua
postgres连接对象
包含query函数
```

- **示例**

```lua
-- 导入扩展库
dbcall = require("db_call")
-- 拿到一个postgres连接对象（会使用连接池，不存在则会创建并缓存一段时间）
-- local是本地变量的关键字，使用local关键字后会避免很多可能发生的错误，建议使用local的方式声明变量
local c = dbcall.getPostgresConnection({host = '127.0.0.1', port = 1521, database = 'test', user = 'root', password = 'admin'})
```

**postgres连接对象**~~**-**~~**query方法**

- **参数**

| 字段  | 类型     | 描述    | 必要字段 | 示例                   |
| --- | ------ | ----- | ---- | -------------------- |
| sql | string | sql语句 | 是    | "select * from test" |

- **返回值**

```lua
matrix对象
```

- **示例**

```lua
-- 导入扩展库
dbcall = require("db_call")
-- 拿到一个mysql连接对象（会使用连接池，不存在则会创建并缓存一段时间）
local c = dbcall.getPostgresConnection({host = '127.0.0.1', port = 1521, database = 'test', user = 'root', password = 'admin'})
-- 查询
local res = c:query({sql="select * from test"})
```

### 

### oracle

**getOracleConnection方法**

- **参数**

| 字段       | 类型     | 描述   | 必要字段 | 示例          |
| -------- | ------ | ---- | ---- | ----------- |
| host     | string | 主机号  | 是    | "127.0.0.1" |
| port     | number | 端口   | 是    | 3306        |
| database | string | 数据库名 | 是    | "test_db"   |
| user     | string | 用户名  | 是    | "root"      |
| password | string | 密码   | 是    | "admin"     |

- **返回值**

```lua
oracle连接对象
包含query函数
```

- **示例**

```lua
-- 导入扩展库
dbcall = require("db_call")
-- 拿到一个mysql连接对象（会使用连接池，不存在则会创建并缓存一段时间）
local c = dbcall.getOracleConnection({host = '127.0.0.1', port = 3306, database = 'test', user = 'root', password = 'admin'})
```

**oracle连接对象-query方法**

- **参数**

| 字段  | 类型     | 描述    | 必要字段 | 示例                   |
| --- | ------ | ----- | ---- | -------------------- |
| sql | string | sql语句 | 是    | "select * from test" |

- **返回值**

```lua
matrix对象
```

- **示例**

```lua
-- 导入扩展库
dbcall = require("db_call")
-- 拿到一个mysql连接对象（会使用连接池，不存在则会创建并缓存一段时间）
local c = dbcall.getOracleConnection({host = '127.0.0.1', port = 3306, database = 'test', user = 'root', password = 'admin'})
-- 查询
local res = c:query({sql="select * from test"})
```

### mongo

**getMongoConnection方法**

- **参数**

| 字段       | 类型     | 描述   | 必要字段 | 示例          |
| -------- | ------ | ---- | ---- | ----------- |
| host     | string | 主机号  | 是    | "127.0.0.1" |
| port     | number | 端口   | 是    | 3306        |
| database | string | 数据库名 | 是    | "test_db"   |
| user     | string | 用户名  | 是    | "root"      |
| password | string | 密码   | 是    | "admin"     |

- **返回值**

```lua
mongo连接对象
包含query函数
```

- **示例**

```lua
-- 导入扩展库
dbcall = require("db_call")
-- 拿到一个mysql连接对象（会使用连接池，不存在则会创建并缓存一段时间）
local c = dbcall.getMongoConnection({host = '127.0.0.1', port = 3306, database = 'test', user = 'root', password = 'admin'})
```

**mongo连接对象-query方法**

- **参数**

| 字段         | 类型     | 描述                   | 必要字段 | 示例                  |
| ---------- | ------ | -------------------- | ---- | ------------------- |
| collection | string | 集合                   | 是    | "test_col"          |
| query      | string | 查询语句(json格式)         | 是    | "{\"name\":\"11\"}" |
| isAll      | bool   | 是否查询全部数据，false则为分页查询 | 是    | false               |
| page       | number | 分页查询的页数              | 否    | 1                   |
| size       | number | 分页查询的页大小             | 否    | 10                  |

- **返回值**

```lua
嵌套table，和查询结果结构一致
```

- **示例**

```lua
-- 导入扩展库
dbcall = require("db_call")
-- 拿到一个mysql连接对象（会使用连接池，不存在则会创建并缓存一段时间）
local c = dbcall.getMongoConnection({host = '127.0.0.1', port = 3306, database = 'test', user = 'root', password = 'admin'})
-- 查询全部
local res = c:query({collection = 'test_coll', query = "{\"name\":\"11\"}", isAll=true})
-- 查询第一页数据
local res = c:query({collection = 'test_coll', query = "{\"name\":\"11\"}", isAll=false, page=1, size = 10})

```