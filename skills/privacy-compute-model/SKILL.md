---
name: privacy-computing-model
description: Generate privacy computing models (chief_model.lua and submodels) for multi-party secure computation. Use when user needs to create Lua models for: (1) Privacy-preserving data intersection (PSI), union (PSU), or difference (PSD), (2) Statistical computations like average, variance, median, max, min, (3) Homomorphic operations (addition, multiplication), (4) Private information retrieval (PIR), (5) Aggregation operations with PSA, (6) Inner product or comparison operations. User will provide: data metadata (field names, types), computation requirements (e.g., intersection, mean), and business requirements (e.g., private query vs normal query).
---

# Privacy Computing Model Generator

Generate privacy computing models for multi-party secure computation based on user requirements.

## Quick Start

To generate privacy computing models, collect these inputs from user:

1. **Data metadata**: Field names and types for each participant's data
2. **Computation requirements**: Algorithm type (PSI, AVG, PSA, etc.)
3. **Business requirements**: Query type (private query vs normal query)

Then generate `chief_model.lua` and `submodel-00{i}.lua` files following the workflow below.

## Computation Types

Select appropriate algorithm based on user requirements:

| Type | Function | Description | Participants | Data Format |
|------|----------|-------------|--------------|-------------|
| NORMAL | normalInvoke | Plaintext remote call | >=1 | Any |
| PSA | psaInvoke | Aggregation (+, -, *, /) | >=2 | number[] |
| ADD | addInvoke | Homomorphic addition | >=2 | number[] |
| MUL | mulInvoke | Homomorphic multiplication | >=2 | number[] |
| AVG | avgInvoke | Average | >=2 | number[] |
| VAR | varInvoke | Variance | >=2 | number[] |
| INNERPRODUCT | innerproductInvoke | Inner product | 1 | number[] |
| CMP | cmpInvoke | Comparison | 1 | number[] |
| MEDIAN | medianInvoke | Median | >=2 | number[] |
| MAX | maxInvoke | Maximum | >=2 | number[] |
| MIN | minInvoke | Minimum | >=2 | number[] |
| PSI | psiInvoke | Intersection | >=1 | string[] |
| PSD | psdInvoke | Difference | 1 | string[] |
| PSU | psuInvoke | Union | >=2 | string[] |
| PIR | pirInvoke | Private query | 1 | keys: string[], values: string[] |
| PIR_PREPROCESS | pirInvokeWithPreprocess | Private query with preprocess | 1 | Multi-field key-value |

## Code Generation Workflow

### Step 1: Gather Requirements

Ask user for:
- Number of participants (default: 2)
- Data source types for each participant (MYSQL, ORACLE, MONGO, CSV, MODEL, RESTFUL)
- **Data source to organization mapping** - If user mentions multiple data sources but doesn't specify which organization/institution uses which data, you MUST explicitly ask for clarification
- Computation algorithm (from table above)
- Field names and types for each data source
- Any specific business requirements (e.g., private query)

### Step 2: Generate Sub-models

For each participant, generate `submodel-00{i}.lua`:

**Sub-model structure:**
```lua
datacall = require("data_call")

function main()
    -- Access data based on source type
    local p = {
        -- For SQL sources (MYSQL, ORACLE, CSV):
        sql = "select field1, field2 from defaultTable"

        -- For Mongo:
        query = "{\"name\":\"value\"}", isAll=false, page=1, size=10

        -- For Model:
        method = "main", args = {}

        -- For RESTful:
        query = {}, header = {}, body = "{}"
    }

    local data = datacall.call(p)

    -- Process and return data
    -- For statistical ops: return number array
    -- For set ops: return string array
    -- For PIR: return {keys={}, values={}}
    return processResult(data)
end
```

**Important patterns:**
- SQL: Use `defaultTable` as table name (auto-replaced by system)
- Return format MUST match algorithm requirement
- For PSA/ADD/MUL: return `number[]` with equal length across participants
- For PSI/PSU: return `string[]`
- For PIR: return `{keys={}, values={}}`

### Step 3: Generate Chief Model

Generate `chief_model.lua` based on computation type.

**Important:** The `main()` function MUST return the final computation result. If post-processing is needed on the invoke result, perform it before returning.

**NormalInvoke pattern:**
```lua
fccall = require("fc_call")

function main()
    p = {}
    p.modelName = "submodel-001"
    p.method = "main"
    p.args = {}

    return fccall.normalInvoke(p)
end
```

**PSA pattern (aggregation with ops):**
```lua
function main()
    p1 = {}
    p1.modelName = "submodel_1"
    p1.method = "main"
    p1.args = {}
    p1.op = "+"  -- or "-", "*", "/"

    p2 = {}
    p2.modelName = "submodel-002"
    p2.method = "main"
    p2.args = {}
    p2.op = "+"

    return fccall.psaInvoke({p1, p2})
end
```

**AVG/VAR pattern (with initiator data):**
```lua
function main()
    initiatorData = {1, 2, 3}  -- or query object

    p2 = {}
    p2.modelName = "submodel-002"
    p2.method = "main"
    p2.args = {}

    return fccall.avgInvoke(initiatorData, {p2})
end
```

**PSI pattern (intersection):**
```lua
function main()
    initiatorData = {"id1", "id2"}  -- nil if no local data

    p = {}
    p.modelName = "submodel-001"
    p.method = "main"
    p.args = {}

    return fccall.psiInvoke(initiatorData, p)
end
```

**PIR pattern (private query):**
```lua
function main()
    initiatorData = {"key1", "key2"}

    p = {}
    p.modelName = "submodel-001"
    p.method = "main"
    p.args = {}

    return fccall.pirInvoke(initiatorData, p)
end
```

### Step 4: Validate Generated Code

Ensure:
- All Lua syntax is valid
- Library imports are correct (`fc_call` for chief, `data_call` for sub)
- Return types match algorithm requirements
- Table construction follows Lua conventions
- Model names match between chief and sub-models

## Common Patterns

### Statistical Computation (Average)

```lua
-- Submodel
function main()
    p = {sql = "select income from defaultTable"}
    data = datacall.call(p)
    return {data:get(1, "income"), data:get(1, "count")}
end

-- Chief model
function main()
    localData = {10000, 100}
    p = {modelName="submodel-001", method="main", args={}}
    result = fccall.avgInvoke(localData, {p})
    return result
end
```

### Intersection (PSI)

```lua
-- Submodel
function main()
    p = {sql = "select user_id from defaultTable"}
    data = datacall.call(p)
    return data:getColumn("user_id")
end

-- Chief model
function main()
    localIds = {"id1", "id2"}
    p = {modelName="submodel-001", method="main", args={}}
    result = fccall.psiInvoke(localIds, p)
    return result
end
```

### Private Query (PIR)

```lua
-- Submodel
function main()
    return {
        keys = {"user1", "user2"},
        values = {"data1", "data2"}
    }
end

-- Chief model
function main()
    queryKeys = {"user1"}
    p = {modelName="submodel-001", method="main", args={}}
    result = fccall.pirInvoke(queryKeys, p)
    return result
end
```

## Data Source Handling

| Source Type | Configuration | Return Type |
|-------------|---------------|-------------|
| MySQL/Oracle | `sql = "select ... from defaultTable"` | matrix |
| MongoDB | `query = "{}", isAll, page, size` | nested table |
| CSV | `sql = "select ... from defaultTable"` | matrix |
| Model | `method = "main", args = {}` | varies |
| RESTful | `query = {}, header = {}, body = "{}"` | varies |

## Multi-party Call Standards

All invocations follow this structure:
```lua
param = {
    modelName = "submodel-00{i}",  -- Must match actual submodel name (e.g., submodel-001, submodel-002)
    method = "main",               -- Method to call
    args = {}                      -- Arguments to pass
    -- Optional for PSA:
    -- op = "+" or "-" or "*" or "/"
}
```

## References

For detailed API documentation, see:
- [fc_call library](references/隐私计算库/fc_call库--主模型隐私计算算法库.md) - All privacy computing algorithms
- [data_call library](references/隐私计算库/data_call库--子模型数据导入库.md) - Data access patterns
- [Complete example](references/完整示例/README.md) - Full working example
- [Concepts](references/概念/README.md) - Architecture overview
