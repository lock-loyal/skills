-- Privacy Computing Sub-model
-- Data access model that runs on participant's side

datacall = require("data_call")

function main()
    -- Configure data access based on data source type
    -- Supported types: MYSQL, ORACLE, MONGO, CSV, MODEL, RESTFUL

    local dataSourceType = "{{DATA_SOURCE_TYPE}}"

    if dataSourceType == "MYSQL" or dataSourceType == "ORACLE" or dataSourceType == "CSV" then
        -- SQL-based data source
        local p = {
            sql = "{{SQL_QUERY}}"
        }
        local data = datacall.call(p)
        {{RESULT_PROCESSING}}

    elseif dataSourceType == "MONGO" then
        -- MongoDB data source
        local p = {
            query = "{{MONGO_QUERY}}",
            isAll = {{IS_ALL}},
            page = {{PAGE}},
            size = {{SIZE}}
        }
        local data = datacall.call(p)
        return data

    elseif dataSourceType == "MODEL" then
        -- Model data source
        local p = {
            method = "{{METHOD_NAME}}",
            args = {{METHOD_ARGS}}
        }
        local data = datacall.call(p)
        return data

    elseif dataSourceType == "RESTFUL" then
        -- RESTful API data source
        local p = {
            query = {{QUERY_PARAMS}},
            header = {{HEADERS}},
            body = "{{BODY}}"
        }
        local data = datacall.call(p)
        return data

    else
        error("Unsupported data source type: " .. tostring(dataSourceType))
    end
end
