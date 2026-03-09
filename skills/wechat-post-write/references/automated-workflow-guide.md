# 自动化工作流指南

本文档提供微信文章写作技能的自动化热点发现工作流的详细指导。

## 工作流概述

自动化工作流实现端到端的选题、研究和文章生成流程，无需用户提供具体主题或项目。

### 工作流触发条件

当用户请求以下任一内容时，启动自动化工作流：

| 触发短语 | 说明 |
|---------|------|
| "发现今天的热点" | 发现今日热点 |
| "生成今日AI热点文章" | 生成今日AI热点文章 |
| "自动选题并写文章" | 自动选题并写文章 |
| "GitHub trending + AI热点" | GitHub trending + AI热点 |
| "今天有什么值得写的" | 今天有什么值得写的 |

## 工作流步骤

### 步骤1：GitHub Trending 抓取

#### 工具选择

**推荐工具：** `mcp__firecrawl__firecrawl_scrape` (JSON 格式 + Schema)

Firecrawl 支持 JavaScript 渲染和结构化数据提取，无需浏览器自动化工具。

#### 操作步骤

1. **抓取每日 Trending**
   ```json
   {
     "url": "https://github.com/trending",
     "formats": [{
       "type": "json",
       "prompt": "提取所有 trending 仓库：作者/项目名、描述、今日星标数、编程语言",
       "schema": {
         "type": "object",
         "properties": {
           "repositories": {
             "type": "array",
             "items": {
               "type": "object",
               "properties": {
                 "name": {"type": "string"},
                 "url": {"type": "string"},
                 "description": {"type": "string"},
                 "stars_today": {"type": "string"},
                 "language": {"type": "string"}
               }
             }
           }
         }
       }
     }],
     "waitFor": 8000
   }
   ```

2. **抓取周度 Trending**
   - URL: `https://github.com/trending?since=weekly`
   - 使用相同的 JSON schema

3. **保存数据**
   - 每日数据：`YYYY-MM-DD/01_github-trending-daily.json`
   - 周度数据：`YYYY-MM-DD/02_github-trending-weekly.json`

#### 数据结构

```json
{
  "timestamp": "2026-02-18T12:00:00Z",
  "source": "github.com/trending",
  "repositories": [
    {
      "name": "owner/repo",
      "url": "https://github.com/owner/repo",
      "stars_today": "666 today",
      "language": "Python",
      "description": "A brief description..."
    }
  ]
}
```

### 步骤2：三层递进式调研

#### 概述

三层递进式调研策略确保全面覆盖 AI 科技热点：

```
Layer 1: Bing 中文搜索（快速，24小时国内热点）
   ↓ 搜索: "AI热点 国内 2026", "AI科技 最新发布 24小时"
Layer 2: Firecrawl 全局搜索（英文，全球范围）
   ↓ 搜索: "AI breakthrough 2026", "new AI model release"
Layer 3: Firecrawl Agent（深度自主研究）
   ↓ 提示词: 综合前两层，深度研究 AI 科技热点
```

每一层的结果都会累积到最终的调研报告中。

#### Layer 1: Bing 中文调研

**工具：** `mcp__bing-search__bing_search` + `mcp__bing-search__crawl_webpage`

**搜索词：**
- `AI热点 国内 2026`
- `AI科技 最新发布 24小时`
- `人工智能 新模型 上线`
- `AI 产品 发布 今天`

**操作步骤：**

1. 执行搜索，每个搜索词 count=10
   ```json
   {
     "query": "AI热点 国内 2026",
     "count": 10
   }
   ```

2. 使用 `crawl_webpage` 批量抓取搜索结果
   ```json
   {
     "uuids": ["uuid1", "uuid2", ...],
     "urlMap": {"uuid1": "https://...", "uuid2": "https://..."}
   }
   ```

3. 整合发现，输出报告
   - 文件：`YYYY-MM-DD/03_research-layer1-bing.md`

**报告格式：**
```markdown
# Layer 1: Bing 中文调研报告

## 国内 AI 热点 (24小时)

### 主题 1: [标题]
- 来源: [URL]
- 摘要: [摘要]
- 时间: [时间戳]

### 主题 2: [标题]
...
```

#### Layer 2: Firecrawl 全局搜索

**工具：** `mcp__firecrawl__firecrawl_search`

**搜索词：**
- `AI breakthrough 2026`
- `new AI model release`
- `machine learning breakthrough today`
- `AI product launch 2026`

**参数：**
- `limit`: 10
- `tbs`: `qdr:d`（过去24小时）
- `sources`: [{"type": "web"}]

**操作步骤：**

1. 执行带时间过滤的搜索
   ```json
   {
     "query": "AI breakthrough 2026",
     "limit": 10,
     "tbs": "qdr:d",
     "sources": [{"type": "web"}]
   }
   ```

2. 对相关结果执行深度抓取
   ```json
   {
     "url": "https://...",
     "formats": ["markdown"],
     "onlyMainContent": true
   }
   ```

3. 整合发现，输出报告
   - 文件：`YYYY-MM-DD/04_research-layer2-firecrawl-search.md`

**报告格式：**
```markdown
# Layer 2: Firecrawl 全局搜索报告

## 全球 AI 热点 (24小时)

### [主题名称]
- 来源: [URL]
- 摘要: [英文摘要]
- 中文翻译: [中文摘要]
```

#### Layer 3: Firecrawl Agent 深度研究

**工具：** `mcp__firecrawl__firecrawl_agent` + 轮询

**提示词：**
```
综合前两层研究结果，深度研究当前AI科技领域的热点事件：
1. 新模型发布（大语言模型、多模态模型）
2. AI应用产品上线
3. 开源项目突破
4. 技术框架/工具发布

重点关注：
- 过去24小时内的最新动态
- 全球和国内两个维度
- 数据来源：GitHub, X(Twitter), Reddit, HuggingFace, arxiv, 技术博客

输出结构化报告，包含每个热点的详细信息、来源链接、影响力评估。
```

**轮询策略：**
- 轮询间隔：30秒
- 最大时长：20分钟
- 最大轮询次数：40次

**操作步骤：**

1. 启动 Agent
   ```json
   {
     "prompt": "综合前两层研究结果..."
   }
   ```
   获取 `jobId`

2. 轮询状态检查
   ```python
   for i in range(40):
       status = firecrawl_agent_status(id=jobId)
       if status["status"] in ["completed", "failed"]:
           break
       sleep(30)
   ```

3. 提取结果并保存
   - 文件：`YYYY-MM-DD/05_research-layer3-agent.md`

**报告格式：**
```markdown
# Layer 3: Firecrawl Agent 深度研究报告

## 综合研究发现

### 热点 1: [主题名称]
- 详细信息: [完整描述]
- 来源链接: [多个来源]
- 影响力评估: [高/中/低]

### 热点 2: [主题名称]
...
```

### 步骤3：选题决策

#### 优先级规则

| 优先级 | 类型 | 说明 |
|--------|------|------|
| 1 | **AI技术新闻** | 新模型、产品发布、框架发布 |
| 2 | 优质开源项目 | >10K stars、新颖技术、活跃社区 |

#### 评分公式

```
总分 = (影响力 × 3) + (新颖性 × 2) + (数据可用性 × 2) + (时效性 × 3)
```

| 因素 | 权重 | 评分标准 (1-10) |
|------|------|----------------|
| 影响力 | ×3 | 微信读者会感兴趣吗？ |
| 新颖性 | ×2 | 是否足够新/不同？ |
| 数据可用性 | ×2 | 能否充分研究？ |
| 时效性 | ×3 | 是否在24-48小时内？ |

#### 选题流程

1. **合并数据源**：
   - GitHub trending (daily + weekly)
   - Layer 1: Bing 中文调研
   - Layer 2: Firecrawl 全局搜索
   - Layer 3: Firecrawl Agent 深度研究

2. **评分候选**：对每个候选主题评分

3. **筛选候选**：选择前 3-5 个高分候选

4. **生成候选列表**：创建带描述和分数的候选列表

5. **等待用户选择**：让用户从候选列表中选择

#### 候选列表格式

```markdown
# Topic Candidates - YYYY-MM-DD

Based on GitHub trending and three-layer AI hotspots research:

## 1. [Topic Name]
**Score:** 9.2/10
**Sources:** GitHub trending + Layer 2 (Firecrawl Search) + Layer 3 (Agent)
**Brief:** [2-3 sentence description]
**Why it's hot:** [Reason for selection]

## 2. [Topic Name]
**Score:** 8.7/10
**Sources:** Layer 1 (Bing Chinese)
**Brief:** [Description]
**Why it's hot:** [Reason]

## 3. [Topic Name]
**Score:** 8.3/10
...

Please select a topic (1/2/3) or specify your own:
```

#### 保存数据

- 选题记录：`YYYY-MM-DD/06_topic-selection.md`

### 步骤4：深度研究

**参考：** `references/research-checklist.md`（勿重复）

使用现有的深度调研清单进行调研。

#### 研究平台（10+来源）

| 平台 | 工具 | 数量 |
|------|------|------|
| 官网 | firecrawl_scrape | 1 |
| GitHub | firecrawl_scrape | 2 |
| HuggingFace | firecrawl_scrape | 1-2 |
| 微信公众号 | bing_search + crawl_webpage | 2-3 |
| Reddit | bing_search + crawl_webpage | 1-2 |
| X (Twitter) | bing_search | 2-3 |
| 其他补充 | firecrawl_search | 1-2 |

#### 保存数据

- 研究笔记：`YYYY-MM-DD/07_research-notes.md`

### 步骤5：文章生成

**参考：**
- `references/writing-guide.md` - 写作风格
- `references/samples/` - 研究样本文章
- `references/samples.md` - 样本使用指南

#### 写作流程

1. **研究样本文章**（5篇）
2. **应用写作风格指南**
3. **生成文章内容**
4. **确保所有链接为纯文本**（微信兼容）

#### 保存数据

- 最终文章：`YYYY-MM-DD/08_[article-title].md`

## 文件组织结构

```
[working-directory]/
  YYYY-MM-DD/
    01_github-trending-daily.json           - GitHub trending 每日数据
    02_github-trending-weekly.json          - GitHub trending 周度数据
    03_research-layer1-bing.md              - Layer 1: Bing 中文调研
    04_research-layer2-firecrawl-search.md  - Layer 2: Firecrawl 全局搜索
    05_research-layer3-agent.md             - Layer 3: Firecrawl Agent 深度研究
    06_topic-selection.md                   - 选题记录与候选列表
    07_research-notes.md                    - 研究笔记
    08_[article-title].md                  - 最终文章
```

## 工具使用模式

### Firecrawl 模式

| 操作 | 工具 | 用途 |
|------|------|------|
| 抓取页面（JSON） | firecrawl_scrape | 结构化数据提取 |
| 抓取页面（Markdown） | firecrawl_scrape | 获取完整内容 |
| 网站地图 | firecrawl_map | 发现页面 URL |
| 搜索 | firecrawl_search | Web 搜索 |
| Agent 研究 | firecrawl_agent | 深度自主研究 |

### Bing 搜索模式

| 操作 | 工具 | 用途 |
|------|------|------|
| 搜索 | bing_search | 发现来源（中文优化） |
| 批量抓取 | crawl_webpage | 批量获取搜索结果 |

### Web Reader 模式

| 操作 | 工具 | 用途 |
|------|------|------|
| 快速提取 | webReader | 简单页面内容提取 |

## 常见问题

### Q: Firecrawl Agent 轮询多久合适？
A: 建议 30 秒间隔，总时长 20 分钟（40 次轮询）。

### Q: 如何处理 JavaScript 渲染的页面？
A: 使用 `firecrawl_scrape` 时设置 `waitFor` 参数（推荐 8000ms）。

### Q: 三层调研是否必须全部执行？
A: 是的，每一层都会累积信息到最终报告中，确保覆盖全面。

### Q: 如何提高 GitHub Trending 抓取成功率？
A: 使用 JSON 格式 + schema，设置 `waitFor: 8000` 确保渲染完成。

## 完整工作流示例

```python
# 1. 创建工作目录
date_dir = create_date_directory()

# 2. 抓取 GitHub Trending
daily_trending = firecrawl_scrape(
    url="https://github.com/trending",
    formats=[json_schema],
    waitFor=8000
)
save_json(date_dir + '/01_github-trending-daily.json', daily_trending)

weekly_trending = firecrawl_scrape(
    url="https://github.com/trending?since=weekly",
    formats=[json_schema],
    waitFor=8000
)
save_json(date_dir + '/02_github-trending-weekly.json', weekly_trending)

# 3. 三层调研
# Layer 1: Bing 中文搜索
layer1_results = bing_search(query="AI热点 国内 2026", count=10)
layer1_content = crawl_webpage(uuids=..., urlMap=...)
save_md(date_dir + '/03_research-layer1-bing.md', layer1_content)

# Layer 2: Firecrawl 全局搜索
layer2_results = firecrawl_search(
    query="AI breakthrough 2026",
    tbs="qdr:d",
    limit=10
)
layer2_content = aggregate_results(layer2_results)
save_md(date_dir + '/04_research-layer2-firecrawl-search.md', layer2_content)

# Layer 3: Firecrawl Agent
agent_job = firecrawl_agent(prompt="综合前两层研究结果...")
for i in range(40):
    status = firecrawl_agent_status(id=agent_job["id"])
    if status["status"] in ["completed", "failed"]:
        break
    sleep(30)
save_md(date_dir + '/05_research-layer3-agent.md', status["result"])

# 4. 选题
candidates = generate_candidates(
    daily_trending, weekly_trending,
    layer1_content, layer2_content, layer3_content
)
save_md(date_dir + '/06_topic-selection.md', candidates)

# 5. 等待用户选择
selected_topic = wait_for_user_selection(candidates)

# 6. 深度研究
research_notes = deep_research(selected_topic)
save_md(date_dir + '/07_research-notes.md', research_notes)

# 7. 生成文章
article = generate_article(selected_topic, research_notes)
save_md(date_dir + '/08_' + article_title + '.md', article)
```

## 参考

- **三层调研详解：** `references/three-layer-research-guide.md`
- **写作风格指南：** `references/writing-guide.md`
- **调研清单：** `references/research-checklist.md`
- **样本文章：** `references/samples/`
