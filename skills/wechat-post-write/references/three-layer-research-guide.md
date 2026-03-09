# 三层递进式调研指南

本文档详细说明三层递进式调研策略，该策略用于全面覆盖 AI 科技热点，确保不遗漏重要信息。

## 概述

三层递进式调研策略通过三个层次的搜索和研究，确保全面、深入地获取 AI 科技热点信息：

```
Layer 1: Bing 中文搜索（快速，24小时国内热点）
   ↓ 搜索: "AI热点 国内 2026", "AI科技 最新发布 24小时"
Layer 2: Firecrawl 全局搜索（英文，全球范围）
   ↓ 搜索: "AI breakthrough 2026", "new AI model release"
Layer 3: Firecrawl Agent（深度自主研究）
   ↓ 提示词: 综合前两层，深度研究 AI 科技热点
```

**核心设计理念：**
- 每一层的结果都会累积到最终的调研报告中
- 从中文快速搜索开始，逐步扩展到全球深度研究
- 层与层之间信息互补，确保覆盖全面

## Layer 1: Bing 中文搜索

### 目标

快速获取国内 AI 科技热点，重点关注中文资讯源。

### 工具

- **搜索：** `mcp__bing-search__bing_search`
- **抓取：** `mcp__bing-search__crawl_webpage`

### 搜索词设计

| 搜索词 | 用途 | 预期结果 |
|--------|------|----------|
| `AI热点 国内 2026` | 国内 AI 综合热点 | 科技新闻、资讯 |
| `AI科技 最新发布 24小时` | 最新发布内容 | 产品发布、模型上线 |
| `人工智能 新模型 上线` | 新模型发布 | 模型相关新闻 |
| `AI 产品 发布 今天` | 今日产品发布 | 应用产品资讯 |

### 操作步骤

1. **执行搜索**
   ```json
   {
     "query": "AI热点 国内 2026",
     "count": 10
   }
   ```

2. **批量抓取结果**
   ```json
   {
     "uuids": ["uuid1", "uuid2", "uuid3", ...],
     "urlMap": {
       "uuid1": "https://example.com/article1",
       "uuid2": "https://example.com/article2"
     }
   }
   ```

3. **整合发现**

### 输出格式

```markdown
# Layer 1: Bing 中文调研报告

## 国内 AI 热点 (24小时)

### 主题 1: [标题]
- **来源:** [URL]
- **摘要:** [摘要]
- **时间:** [时间戳]
- **关键词:** [AI模型, 发布]

### 主题 2: [标题]
...

## 数据来源平台
- 科技媒体: [列举发现的主要媒体]
- 微信公众号: [相关公众号名称]
- 论坛社区: [相关讨论]
```

### 优势

- 快速获取中文内容
- 覆盖国内资讯源
- 支持批量抓取

### 注意事项

- 自动过滤黑名单网站（知乎、小红书等）
- 优先抓取权威媒体
- 关注时间戳，确保24小时内

## Layer 2: Firecrawl 全局搜索

### 目标

获取全球 AI 科技热点，重点关注英文资讯源和技术社区。

### 工具

- **搜索：** `mcp__firecrawl__firecrawl_search`
- **抓取：** `mcp__firecrawl__firecrawl_scrape`

### 搜索词设计

| 搜索词 | 用途 | 预期结果 |
|--------|------|----------|
| `AI breakthrough 2026` | AI 技术突破 | 研究论文、技术博客 |
| `new AI model release` | 新模型发布 | HuggingFace、GitHub |
| `machine learning breakthrough today` | 今日 ML 突破 | arxiv、技术社区 |
| `AI product launch 2026` | AI 产品发布 | 官方公告、新闻 |

### 时间过滤

使用 `tbs: qdr:d` 参数过滤过去 24 小时的内容：
- `qdr:d` - 过去 24 小时
- `qdr:w` - 过去一周
- `qdr:m` - 过去一个月

### 操作步骤

1. **执行带时间过滤的搜索**
   ```json
   {
     "query": "AI breakthrough 2026",
     "limit": 10,
     "tbs": "qdr:d",
     "sources": [{"type": "web"}]
   }
   ```

2. **深度抓取相关结果**
   ```json
   {
     "url": "https://...",
     "formats": ["markdown"],
     "onlyMainContent": true,
     "waitFor": 5000
   }
   ```

3. **整合发现**

### 输出格式

```markdown
# Layer 2: Firecrawl 全局搜索报告

## 全球 AI 热点 (24小时)

### [Topic Name]
- **来源:** [URL]
- **英文摘要:** [English summary]
- **中文翻译:** [中文摘要]
- **发布时间:** [Timestamp]
- **相关链接:** [Additional sources]

### [Topic Name]
...

## 覆盖平台
- GitHub: [发现的热门项目]
- HuggingFace: [新模型发布]
- X (Twitter): [官方公告]
- Reddit: [社区讨论]
- Tech Blogs: [技术博客]
```

### 优势

- 覆盖全球技术社区
- 支持时间过滤
- 强大的搜索语法

### 搜索运算符

| 运算符 | 功能 | 示例 |
|--------|------|------|
| `site:` | 指定网站 | `site:huggingface.co new model` |
| `inurl:` | URL 包含 | `inurl:release AI` |
| `intitle:` | 标题包含 | `intitle:breakthrough AI` |
| `-` | 排除关键词 | `AI -crypto` |

## Layer 3: Firecrawl Agent 深度研究

### 目标

综合前两层结果，进行深度自主研究，挖掘隐藏的热点和详细信息。

### 工具

- **Agent：** `mcp__firecrawl__firecrawl_agent`
- **状态检查：** `mcp__firecrawl__firecrawl_agent_status`

### 提示词设计

**综合研究提示词：**
```
综合前两层研究结果，深度研究当前AI科技领域的热点事件：

重点方向：
1. 新模型发布（大语言模型、多模态模型、语音模型等）
2. AI应用产品上线（生产力工具、创意应用等）
3. 开源项目突破（GitHub 热门项目、框架发布）
4. 技术框架/工具发布（开发工具、部署平台等）

重点关注：
- 过去24小时内的最新动态
- 全球和国内两个维度
- 数据来源优先级：GitHub > X(Twitter) > Reddit > HuggingFace > arxiv > 技术博客

输出结构化报告，包含：
- 每个热点的详细信息（名称、发布方、主要特点）
- 来源链接（多个来源交叉验证）
- 影响力评估（高/中/低，基于 Star 数、讨论热度等）
```

### 轮询策略

| 参数 | 值 | 说明 |
|------|-----|------|
| 轮询间隔 | 30 秒 | 平衡响应时间和资源消耗 |
| 最大时长 | 20 分钟 | 大多数研究可在此时长内完成 |
| 最大轮询次数 | 40 次 | 20 分钟 / 30 秒 = 40 |

### 操作步骤

1. **启动 Agent**
   ```json
   {
     "prompt": "综合前两层研究结果，深度研究当前AI科技领域的热点事件..."
   }
   ```
   响应示例：
   ```json
   {
     "id": "550e8400-e29b-41d4-a716-446655440000",
     "status": "processing"
   }
   ```

2. **轮询状态检查**
   ```python
   for i in range(40):
       status = firecrawl_agent_status(id=jobId)

       if status["status"] == "completed":
           # 提取结果
           research_data = status.get("result")
           break
       elif status["status"] == "failed":
           # 处理失败
           break
       else:
           # 继续等待
           sleep(30)
   ```

3. **提取结果**

### Agent 状态说明

| 状态 | 说明 | 操作 |
|------|------|------|
| `processing` | 正在研究中 | 继续轮询 |
| `completed` | 研究完成 | 提取结果 |
| `failed` | 研究失败 | 记录错误，使用前两层结果 |

### 输出格式

```markdown
# Layer 3: Firecrawl Agent 深度研究报告

## 综合研究发现

### 热点 1: [主题名称]
- **详细信息:** [完整描述]
- **发布方:** [公司/组织]
- **主要特点:** [特点列表]
- **来源链接:**
  - [来源 1](URL)
  - [来源 2](URL)
- **影响力评估:** 高/中/低
- **GitHub Star 数:** [如有]
- **社区讨论热度:** [描述]

### 热点 2: [主题名称]
...

## 补充发现（前两层未覆盖）

### [热点名称]
- **发现来源:** [Agent 自主发现]
- **详细信息:** [描述]

## 交叉验证结果
- [验证每个热点的多个来源]
```

### 优势

- 自主浏览多个来源
- 深度挖掘信息
- 交叉验证数据

### 注意事项

- 轮询需要耐心，通常 2-5 分钟
- 复杂研究可能需要更长时间
- 失败时使用前两层结果作为降级策略

## 三层整合策略

### 数据整合流程

```
Layer 1 结果
    ↓
Layer 2 结果 (补充 Layer 1 未覆盖内容)
    ↓
Layer 3 结果 (深度挖掘 + 交叉验证)
    ↓
综合报告 (去重、合并、排序)
```

### 去重策略

1. **URL 去重**：相同 URL 的内容只保留一份
2. **主题去重**：相同主题的内容合并到一起
3. **来源优先级**：官网 > GitHub > 媒体 > 社交媒体

### 优先级排序

| 优先级 | 类型 | 示例 |
|--------|------|------|
| 1 | 新模型发布 | GPT-5、Claude 4 |
| 2 | 重大产品发布 | 新 AI 应用上线 |
| 3 | 热门开源项目 | GitHub 日榜第一 |
| 4 | 技术突破 | 新架构、新算法 |
| 5 | 社区热点 | 热门讨论话题 |

### 最终报告格式

```markdown
# AI 科技热点综合报告 (YYYY-MM-DD)

## 报告摘要
- 研究时间范围: [过去 24 小时]
- 数据来源: 3 层调研
- 发现热点数量: N 个
- 覆盖平台: [平台列表]

## Top 热点 (按影响力排序)

### 1. [热点名称]
**数据来源:** Layer 2 + Layer 3
**影响力:** 高
**详细信息:**
- ...

### 2. [热点名称]
**数据来源:** Layer 1 + Layer 3
**影响力:** 中
**详细信息:**
- ...

## 分地区热点

### 国内
- [列表]

### 全球
- [列表]

## 数据来源统计
- GitHub: N 个项目
- HuggingFace: N 个模型
- X (Twitter): N 条动态
- Reddit: N 个讨论
- 其他: N 个
```

## 工具选择参考

| 场景 | 推荐工具 | 原因 |
|------|----------|------|
| 快速中文搜索 | bing_search | 中文优化 |
| 全球技术搜索 | firecrawl_search | 高级运算符 |
| 结构化数据提取 | firecrawl_scrape | JSON schema |
| 深度自主研究 | firecrawl_agent | 自主浏览 |
| 批量内容抓取 | crawl_webpage | 自动过滤 |

## 常见问题

### Q: 三层调研的顺序可以调整吗？
A: 不建议。当前顺序（中文快速 → 全局搜索 → 深度研究）经过优化，从快速获取到深度挖掘，效率最高。

### Q: 某一层失败怎么办？
A: 继续执行其他层，最终报告中标注数据来源层级。完整的三层调研最理想，但两层也能产生有价值的结果。

### Q: Agent 轮询超时怎么办？
A: 使用前两层的结果作为最终报告，记录 Agent 超时情况。前两层已经覆盖大部分热点。

### Q: 如何评估热点的影响力？
A: 综合多个指标：
- GitHub: Star 数增长速度
- X (Twitter): 转发、评论数
- Reddit: upvote 数、评论数
- HuggingFace: 下载量
- 媒体报道: 报道数量和质量

## 最佳实践

1. **记录每一层的元数据**
   - 搜索时间、搜索词
   - 发现的 URL 数量
   - 成功抓取的数量

2. **保存原始数据**
   - 每一层的原始结果单独保存
   - 便于后续追溯和调试

3. **交叉验证重要信息**
   - 重要热点至少 2 个来源
   - 优先采用官方来源

4. **关注时效性**
   - 优先报道 24 小时内的内容
   - 标注每个热点的发布时间

5. **中英文平衡**
   - Layer 1 覆盖中文内容
   - Layer 2 覆盖英文内容
   - 最终报告提供双语摘要

## 完整示例

```python
# 三层递进式调研完整流程

# Layer 1: Bing 中文搜索
layer1_search = bing_search(query="AI热点 国内 2026", count=10)
layer1_content = crawl_webpage(
    uuids=[item["uuid"] for item in layer1_search["results"]],
    urlMap={item["uuid"]: item["url"] for item in layer1_search["results"]}
)
save_layer1(layer1_content)

# Layer 2: Firecrawl 全局搜索
layer2_search = firecrawl_search(
    query="AI breakthrough 2026",
    limit=10,
    tbs="qdr:d"
)
layer2_content = []
for result in layer2_search:
    content = firecrawl_scrape(
        url=result["url"],
        formats=["markdown"],
        onlyMainContent=True
    )
    layer2_content.append(content)
save_layer2(layer2_content)

# Layer 3: Firecrawl Agent
agent_prompt = f"""
综合前两层研究结果，深度研究当前AI科技领域的热点事件：

Layer 1 发现：{summary(layer1_content)}
Layer 2 发现：{summary(layer2_content)}

请进行深度研究，输出结构化报告。
"""

agent_job = firecrawl_agent(prompt=agent_prompt)
job_id = agent_job["id"]

# 轮询等待
for i in range(40):
    status = firecrawl_agent_status(id=job_id)

    if status["status"] == "completed":
        layer3_content = status["result"]
        save_layer3(layer3_content)
        break
    elif status["status"] == "failed":
        print("Agent research failed, using layers 1-2 only")
        break
    else:
        print(f"Waiting... ({i+1}/40)")
        sleep(30)

# 整合三层结果
final_report = integrate_layers(
    layer1=layer1_content,
    layer2=layer2_content,
    layer3=layer3_content if status["status"] == "completed" else None
)
save_final_report(final_report)
```
