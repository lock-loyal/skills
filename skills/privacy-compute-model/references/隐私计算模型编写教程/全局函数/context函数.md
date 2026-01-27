## context函数

内置函数，直接调用

获取当前调用的上下文信息，是一个table

```lua
context()
```

总模型中调用的结果

```lua
{
	-- 任务id
	taskID = "TQmWzeaq17i6TEyfiqCszUVzEm4ebEHRSV2r8G4wRkKSVeb",
	-- 当前执行的模型名称（主模型名称）
	modelName = "chief_model",
	-- 子模型信息列表，table数组
	subModelInfos = [
		{
			-- 子模型对应的数据id
			dataID = "CQmTHXiWHwyjK8pxfwCVwczJg2rUGhn8v9keXUGoAdCjFmG",
			-- 子模型名称
			name = "submodel-001",
			-- 子模型对应的数据是否是发起方本地的数据
			isLocalData = false
		},
		{
			-- 子模型对应的数据id
			dataID = "CQmZVhZ5iL8fxeTnwdGMsFV4K9CRshTFiEXTQAkxqmJFCou",
			-- 子模型名称
			name = "submodel-002",
			-- 子模型对应的数据是否是发起方本地的数据
			isLocalData = true	
		}
	]
}
```

子模型中调用的返回值

```lua
{
	-- 任务id
	taskID = "TQmWzeaq17i6TEyfiqCszUVzEm4ebEHRSV2r8G4wRkKSVeb",
	-- 子模型对应的数据id
	dataID = "CQmZVhZ5iL8fxeTnwdGMsFV4K9CRshTFiEXTQAkxqmJFCou",
	-- 当前执行的模型名称（子模型名称）
	modelName = "chief_model",
	-- 被调用的类型
	-- "NORMAL",
	-- "PSA",
	-- "PSI",
	-- "UPSI",
	-- "DUPSI",
	-- "CMP",
	-- "PSU",
	-- "AVG",
	-- "MEDIAN",
	-- "VAR",
	-- "PSD",
	-- "MAX",
	-- "PIR",
	-- "INNERPRODUCT",
	-- "MIN",
	-- "AVG_VECTOR",
	fcType = "PSI"
}
```