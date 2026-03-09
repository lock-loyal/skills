---
name: wechat-post-write
description: Generate high-quality Chinese articles about open source projects for WeChat posting. Supports two workflows: (1) Manual workflow - GitHub URL (auto-fetch README), any URL (blogs/docs), local documents (PDF/Word/txt), project name (auto-search), fuzzy requests ("recommend a good Python crawler"), or direct content paste. (2) Automated workflow - Discover hot topics by crawling GitHub trending, researching 24-hour AI tech hotspots via three-layer research strategy (Bing Chinese search, Firecrawl global search, Firecrawl Agent deep research), selecting attractive topics, performing deep research, and generating professional articles. Both workflows perform deep research from 6 priority platforms (official sites, GitHub, HuggingFace, WeChat accounts, Reddit, X), with 10+ sources per project covering founder backgrounds, real-world usage, community discussions. Uses reference samples for professional but engaging tone. Output includes engaging article structure with catchy titles, pain point solutions, core highlights with specific values, best use scenarios, quick start, latest updates, and project source URL. Multi-project articles with smooth transitions. Serious but humorous tone. Use when user wants to write WeChat articles about projects, create project roundups, summarize multiple projects in Chinese, or discover and write about hot topics. Trigger phrases for manual workflow include '公众号文章', '介绍项目', '推荐开源项目', '写文章介绍', 'project roundup', '项目推荐'. Trigger phrases for automated workflow include '发现今天的热点', '生成今日AI热点文章', '自动选题并写文章', 'GitHub trending + AI热点'.
---

# WeChat Article Generator for Open Source Projects

## Overview

Generate polished Chinese articles about open source projects suitable for WeChat public accounts. The skill supports **two workflows**:

1. **Manual Workflow:** User provides explicit topics/projects, skill performs deep research and generates articles
2. **Automated Workflow:** Skill discovers hot topics automatically (GitHub trending + AI hotspots), performs research, and generates articles

Both workflows perform comprehensive three-dimensional information gathering (core + extended + community sources) and save articles with engaging structure and plain text links.

## Workflow Selection

### Decision Tree

```
User Request
    │
    ├─ Contains explicit topic/project URL?
    │   └─ YES → Manual Workflow
    │
    ├─ Wants hot topic discovery?
    │   └─ YES → Automated Workflow
    │
    └─ Fuzzy request?
        └─ Manual Workflow (project discovery)
```

### Trigger Phrase Detection

#### Manual Workflow Triggers

| Trigger Phrase | Example |
|----------------|---------|
| "写一篇关于[project]的文章" | 写一篇关于 React 的文章 |
| "介绍这个项目: [URL]" | 介绍这个项目: https://github.com/... |
| "推荐几个好用的Python爬虫库" | 推荐几个好用的Python爬虫库 |
| "公众号文章" | 写一篇公众号文章 |
| "介绍项目" | 介绍这个项目 |
| "推荐开源项目" | 推荐几个开源项目 |
| "写文章介绍" | 写文章介绍这个框架 |
| "project roundup" | Create a project roundup |
| "项目推荐" | 推荐一些项目 |

#### Automated Workflow Triggers

| Trigger Phrase | Example |
|----------------|---------|
| "发现今天的热点" | 发现今天的热点 |
| "生成今日AI热点文章" | 生成今日AI热点文章 |
| "自动选题并写文章" | 自动选题并写文章 |
| "GitHub trending + AI热点" | 用 GitHub trending + AI热点来写文章 |
| "今天有什么值得写的" | 今天有什么值得写的 |

## Workflow

### Step 1: Identify Input Type

Determine how the user provides project information:

| Input Type | Detection Rule | Example | Action |
|------------|----------------|---------|--------|
| GitHub URL | Contains `github.com` with username/repo path | `github.com/user/repo` | Fetch README directly |
| Other URL | Contains `http://` or `https://` but NOT GitHub | `blog.example.com/article` | Use crawl4ai or webReader |
| Local document | Contains file extension (`.pdf`, `.docx`, `.txt`) | `/path/to/file.pdf` | Read local file |
| Direct content | Long text (>200 chars) with markdown | README content paste | Parse directly |
| Project name | Short text (<100 chars) | `react`, `vue-router` | Search then fetch |
| Fuzzy request | Contains "推荐", "好用的", etc. | "推荐一个好用的Python爬虫库" | Execute Steps 2-3 |
| Multi-project | Contains separators or "和", "以及" | "react和vue" | Process each project |

### Step 2: Extract Keywords and Analyze Intent (Fuzzy Requests Only)

For fuzzy requests, perform keyword and intent analysis:

**Extract core keywords:**
- Technology stack: Python, JavaScript, Rust, Go, etc.
- Functional category: crawler, web framework, database, CLI, etc.
- Domain: frontend, backend, DevOps, AI/ML, etc.

**Understand user intent:**
- Recommendation: "推荐", "有什么好的", "最好的"
- Comparison: "对比", "区别", "哪个好"
- Learning: "学习", "入门", "教程"
- Production: "生产环境", "企业级", "稳定"

**Generate search strategy:**
- Construct multi-term search queries
- Identify relevant tech communities
- Determine project quality indicators (stars, activity, etc.)

### Step 3: Project Discovery and List Generation (Fuzzy Requests Only)

Execute three-round search strategy to find relevant projects:

**Round 1: Aggregation article search**
- Query: `[关键词] 推荐 最佳 2026`
- Tool: `mcp__bing-search__bing_search`
- Goal: Find curated lists and comparison articles

**Round 2: GitHub hot search**
- Query: `[关键词] github stars:>1000`
- Tool: `mcp__bing-search__bing_search`
- Goal: Find popular GitHub repositories

**Round 3: Community discussion**
- Query: `[关键词] site:reddit.com OR site:news.ycombinator.com`
- Tool: `mcp__bing-search__bing_search`
- Goal: Find community discussions and recommendations

**Filter and sort:**
1. Deduplicate by GitHub URL
2. Score each project: stars + recommendation count + discussion热度
3. Select top 3-5 diverse projects (avoid too similar)
4. Output sorted list for user confirmation

### Step 4: Deep Research from Priority Platforms

**CRITICAL: You MUST search these 6 platforms first, then supplement with others:**

| Priority | Platform | Search For | Min Sources |
|----------|----------|------------|-------------|
| 1 | **Official Site** | Product positioning, core features, tech architecture, pricing | 1 |
| 2 | **GitHub** | Stars trends, Contributors, Issues, Release history, README | 2 |
| 3 | **HuggingFace** | If applicable: model downloads, Spaces demos, papers | 1-2 |
| 4 | **WeChat Accounts** | Chinese community discussions, reviews, tutorials | 2-3 |
| 5 | **Reddit** | r/programming, r/LocalLLaMA, related sub-communities | 1-2 |
| 6 | **X (Twitter)** | Founder posts, tech KOL discussions, user feedback | 2-3 |

**Minimum: 10 sources per project.**

**For each project, research these items (see references/research-checklist.md for full list):**

- [ ] Project basics: name, founder, license, version
- [ ] Founder/team background (LinkedIn, GitHub, hackathon achievements)
- [ ] Core features and differentiation from competitors
- [ ] GitHub stats: stars, forks, contributors, recent activity
- [ ] User feedback: pros, cons, use cases, pitfalls
- [ ] Competitor comparison
- [ ] Latest updates, roadmap, industry trends
- [ ] Chinese community discussions
- [ ] X(Twitter) real-time dynamics
- [ ] HuggingFace metrics (if applicable)

**Reference:** See `references/research-checklist.md` for detailed search commands and research template.

### Step 5: Information Integration and Structuring

Process collected information from multiple sources:

**Deduplicate and verify:**
- Cross-check facts across sources
- Remove redundant information
- Verify latest version numbers and dates

**Categorize information:**
- **Basics**: What is this project, who made it, license
- **Technical**: Tech stack, architecture, dependencies
- **Features**: Key capabilities, unique selling points
- **Usage**: Installation, configuration, common patterns
- **Evaluation**: Community feedback, adoption, limitations
- **Latest**: Recent updates, roadmap, hot topics

**Extract key insights:**
- Pain points solved (what problems does it address?)
- Advantages (why choose this over alternatives?)
- Use cases (when is this the right choice?)
- Limitations (what are the trade-offs?)
- Trends (what's the community excited about?)

### Step 6: Generate Article Content

**Before writing, review reference materials:**

1. Read `references/samples/` - study the 5 sample articles for tone and structure
2. Reference `references/writing-guide.md` - for detailed tone and style guidance
3. Reference `references/research-checklist.md` - to ensure all research items are covered

**Writing principles:**

- **Professional but not serious**: Accurate tech descriptions with engaging rhythm
- **Data-driven titles**: Use specific numbers (3.5万Star, 80.9%, 8小时)
- **Compelling openings**: Hook readers in first 200 characters with data, scenarios, or suspense
- **Flexible structure**: Not rigid template - adapt based on content type
- **Selective citations**: Only cite sources for key information (controversies, specific data, founder quotes)
- **Rhythmic paragraphs**: Mix short and long sentences, keep paragraphs under 100 chars

**Title style options (from writing-guide.md):**

| Type | Format | Example |
|------|--------|---------|
| Data-driven | [数字] + [效果] | 3.5万Star、8小时夺冠 |
| Suspense | [强情感词] + [亮点] | 史诗级泄露、太顶了 |
| Question | [提问] + [方向] | 为什么它能夺冠？ |
| Contrast | [A] + [对比词] + [B] | 开源平替、正面硬刚 |
| Action | [动词] + [动作] | 冲了、赶紧用起来 |

**Article structure (adapt as needed, not rigid template):**

```markdown
### [Catchy Title with Data/Suspense]

[Engaging opening - 2-3 sentences with rhythm]

**核心亮点**
- [Feature 1]：[Specific value with data]
- [Feature 2]：[Specific value]
- [Feature 3]：[Specific value]

**最佳使用场景**
[Specific use cases]

**如何上手**
[Quick installation - 1-2 lines]

**最新动态**
[Recent updates - 1-2 sentences]

**项目地址**
github.com/user/repo (plain text)
```

**Reference:** See `references/writing-guide.md` for detailed tone examples, paragraph rhythm, and transition techniques.

**Character limit:** Entire project section under 800 Chinese characters.

### Step 7: Multi-Project Transitions and Integration

When covering multiple projects:

**Identify connections:**
- Shared technology stack (e.g., both use Rust)
- Related problems solved
- Complementary use cases
- Same author or organization
- Evolutionary relationship (successor/fork)

**Write smooth transitions:**
- Logical connection: "Speaking of [project A's feature], [project B] takes it further by..."
- Deliberate contrast: "While [project A] focuses on X, [project B] approaches from the Y angle"
- Narrative build: "Start with foundation tools like [A], then layer with advanced options like [B]"
- Progressive depth: "[A] handles basic cases well, but for complex scenarios, consider [B]"

**Maintain consistency:**
- Similar article structure per project
- Balanced coverage (not over-emphasizing some projects)
- Coherent narrative flow from start to finish

### Step 8: Apply Tone (Professional but Engaging)

**Reference:** See `references/writing-guide.md` for detailed tone guidance and examples.

**Tone principles:**

**Professional**:
- Accurate technical descriptions
- Data-backed claims (specific numbers, benchmarks)
- Proper terminology usage
- Respect for projects and authors

**Engaging (not serious)**:
- Data-driven titles: "3.5万Star"、"80.9%碾压"
- Compelling openings with rhythm
- Selective use of strong words: "太顶了"、"杀疯了"、"冲了"
- Conversational flow over rigid structure

**Avoid**:
- Overly formal or stiff language
- Forced templates and repetitive structure
- Excessive slang or forced memes
- Humor that obscures technical meaning

**Tone contrast:**

| Too Serious | Professional but Engaging |
|-------------|--------------------------|
| "本项目是一个优秀的开源工具" | "这个项目太顶了" |
| "该项目获得了大量关注" | "开源没几天就3.5万Star了" |
| "使用该工具可以提高效率" | "8小时就能从零开发一个完整项目" |

**Paragraph rhythm:**
- Mix short and long sentences
- Keep paragraphs under 100 characters
- Use impactful short sentences for emphasis

## Automated Workflow (Hot Topic Discovery)

This workflow automatically discovers hot topics, performs research, and generates articles without requiring user input on specific topics.

### Overview

```
[Automated Workflow Steps]

1. Crawl GitHub Trending (daily + weekly)
   ↓
2. Three-Layer Research Strategy:
   - Layer 1: Bing Chinese Search (24h AI hotspots)
   - Layer 2: Firecrawl Global Search (AI breakthrough)
   - Layer 3: Firecrawl Agent (deep research supplement)
   ↓
3. Topic Selection (score + present to user)
   ↓ [User selects]
4. Deep Research (following research-checklist.md)
   ↓
5. Article Generation (following writing-guide.md)
   ↓
6. Save to YYYY-MM-DD/ directory
```

### Step A1: Crawl GitHub Trending

**Tool:** `mcp__firecrawl__firecrawl_scrape` (JSON format with schema)

**Procedure:**

1. Scrape `https://github.com/trending` (daily)
2. Scrape `https://github.com/trending?since=weekly` (weekly)
3. Use JSON format with structured schema for precise extraction
4. Set `waitFor: 8000` to ensure JavaScript rendering completes

**Tool Call Example:**
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

5. Save to files:
   - `YYYY-MM-DD/01_github-trending-daily.json`
   - `YYYY-MM-DD/02_github-trending-weekly.json`

**Data Structure:**
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

### Step A2: Three-Layer Research Strategy

**Overview:** Three progressive research layers ensure comprehensive coverage of AI tech hotspots. Each layer's results accumulate to the final research report.

```
Layer 1: Bing Chinese Search (Fast, 24h domestic focus)
   ↓ Search: "AI热点 国内 2026", "AI科技 最新发布 24小时"
Layer 2: Firecrawl Global Search (English, worldwide)
   ↓ Search: "AI breakthrough 2026", "new AI model release"
Layer 3: Firecrawl Agent (Deep autonomous research)
   ↓ Prompt: Comprehensive AI tech hotspots research
```

#### Layer 1: Bing Chinese Research

**Tools:** `mcp__bing-search__bing_search` + `mcp__bing-search__crawl_webpage`

**Search Queries:**
- `AI热点 国内 2026`
- `AI科技 最新发布 24小时`
- `人工智能 新模型 上线`
- `AI 产品 发布 今天`

**Procedure:**
1. Execute searches with count=10 for each query
2. Use `crawl_webpage` to fetch full content from relevant results
3. Aggregate findings into structured report
4. Output: `YYYY-MM-DD/03_research-layer1-bing.md`

**Report Format:**
```markdown
# Layer 1: Bing Chinese Research Report

## 国内 AI 热点 (24小时)

### 主题 1: [Title]
- 来源: [URL]
- 摘要: [Summary]
- 时间: [Timestamp]

### 主题 2: [Title]
...
```

#### Layer 2: Firecrawl Global Search

**Tool:** `mcp__firecrawl__firecrawl_search`

**Search Queries:**
- `AI breakthrough 2026`
- `new AI model release`
- `machine learning breakthrough today`
- `AI product launch 2026`

**Parameters:**
- `limit`: 10
- `tbs`: `qdr:d` (past 24 hours)
- `sources`: [{"type": "web"}]

**Procedure:**
1. Execute searches with time filter (past 24h)
2. Scrape top results for full content
3. Aggregate findings
4. Output: `YYYY-MM-DD/04_research-layer2-firecrawl-search.md`

**Report Format:**
```markdown
# Layer 2: Firecrawl Global Search Report

## Global AI Hotspots (24 Hours)

### [Topic Name]
- Source: [URL]
- Summary: [English summary]
- Chinese Translation: [中文摘要]
```

#### Layer 3: Firecrawl Agent Deep Research

**Tool:** `mcp__firecrawl__firecrawl_agent` with polling

**Prompt:**
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

**Polling Strategy:**
- Poll interval: 30 seconds
- Max duration: 20 minutes
- Max attempts: 40

**Procedure:**
1. Call `firecrawl_agent` with prompt → get `jobId`
2. Poll `firecrawl_agent_status` every 30 seconds
3. Check for status: "completed" or "failed"
4. Extract results when complete
5. Output: `YYYY-MM-DD/05_research-layer3-agent.md`

**Polling Code Pattern:**
```python
# 1. Start agent
result = firecrawl_agent(prompt=...)

# 2. Poll for completion
for i in range(40):
    status = firecrawl_agent_status(id=result["id"])
    if status["status"] in ["completed", "failed"]:
        break
    sleep(30)  # Wait 30 seconds

# 3. Extract results
if status["status"] == "completed":
    research_data = status["result"]
```

### Step A3: Topic Selection

**Priority:**
1. Major AI Tech News (new models, product launches, framework releases)
2. Excellent Open Source Projects (>10K stars, novel tech, strong community)

**Selection Criteria:**
- Impact (×3): Will this interest WeChat readers?
- Novelty (×2): Is this new/different enough?
- Data Available (×2): Can we research this thoroughly?
- Timeliness (×3): Within 24-48 hours?

**Process:**

1. Combine data from all sources:
   - GitHub trending (daily + weekly)
   - Layer 1: Bing Chinese research
   - Layer 2: Firecrawl global search
   - Layer 3: Firecrawl agent deep research

2. Score candidates: `(Impact×3) + (Novelty×2) + (Data×2) + (Timeliness×3)`

3. Generate candidate list (top 3-5 topics) with brief descriptions and scores

4. **Present candidates to user for selection** - wait for user's choice

5. Save user's selection to `YYYY-MM-DD/06_topic-selection.md`

**Candidate List Format:**
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

### Step A4: Deep Research

**Reference:** Use existing `references/research-checklist.md` - DO NOT duplicate

**Platforms (10+ sources minimum):**
- Official site, GitHub, HuggingFace, WeChat, Reddit, X, plus supplements

**Tools:**
- `mcp__bing-search__bing_search` for discovery
- `mcp__firecrawl__firecrawl_scrape` for specific pages
- `mcp__web_reader__webReader` for quick content extraction

**Output:** `YYYY-MM-DD/07_research-notes.md`

### Step A5: Article Generation

**References to Use (preserve, don't duplicate):**
- `references/writing-guide.md` - Tone and style
- `references/samples/` - Study 5 sample articles
- `references/samples.md` - Sample guide

**Output:** `YYYY-MM-DD/08_[article-title].md`

**Link Format:** All URLs must be plain text (WeChat compatibility)

### File Organization (Automated Workflow)

**Save Location:** Use current working directory (where skill is executed) to create daily directories.

```
[working-directory]/
  YYYY-MM-DD/
    01_github-trending-daily.json           - GitHub trending daily data
    02_github-trending-weekly.json          - GitHub trending weekly data
    03_research-layer1-bing.md              - Layer 1: Bing Chinese research
    04_research-layer2-firecrawl-search.md  - Layer 2: Firecrawl global search
    05_research-layer3-agent.md             - Layer 3: Firecrawl agent deep research
    06_topic-selection.md                   - Topic selection with candidate list
    07_research-notes.md                    - Deep research notes
    08_[article-title].md                  - Final article
```

### Reference: Three-Layer Research Guide

See `references/three-layer-research-guide.md` for detailed guidance on the progressive research strategy.

### Step 9: Save Article as Markdown

After generating the article content:

**Generate filename:**
- Filename must exactly match the article title
- Format: `[article-title].md`
- Example: If article title is "Rust开发必备工具", filename must be `Rust开发必备工具.md`
- For English titles, use `.md` extension
- For Chinese titles, use `.md` extension (Chinese filenames are supported)

**Write to file:**
- Use the Write tool to save the article
- Save in current working directory or specify output path
- Confirm file location with user

**Format requirements:**
- All URLs in plain text format (not markdown hyperlinks)
- Example: `github.com/user/repo` instead of `[link](github.com/user/repo)`
- This ensures WeChat compatibility

## Output Template

```
# [Thematic Title for article]

## [Project 1 Name]

### [Catchy Project Title]

[Engaging opening hook]

**它解决了什么痛点**
[Problem and solution description]

**核心亮点**
- [Feature 1]：[Specific value and outcome]
- [Feature 2]：[Specific value and outcome]
- [Feature 3]：[Specific value and outcome]

**最佳使用场景**
[Specific use cases and when to choose this project]

**如何上手**
[Quick installation steps]

**最新动态**
[Recent updates or community buzz]

**项目地址**
github.com/user/repo (plain text)

---

## [Project 2 Name]

### [Catchy Project Title with Transition]

[Transition from previous project, then engaging opening]

**它解决了什么痛点**
[Problem and solution]

**核心亮点**
- [Feature 1]：[Specific value]
- [Feature 2]：[Specific value]
- [Feature 3]：[Specific value]

**最佳使用场景**
[Use cases]

**如何上手**
[Quick start]

**最新动态**
[Latest info]

**项目地址**
github.com/user2/repo2 (plain text)
```

## Link Format Rules

**ALL links must be plain text, not markdown hyperlinks:**

Correct:
```
项目地址：github.com/user/repo
官网：example.com
文档：docs.example.com
```

Incorrect:
```
项目地址：[github.com/user/repo](https://github.com/user/repo)
官网：[example.com](https://example.com)
文档：[文档](https://docs.example.com)
```

This format ensures compatibility with WeChat and other platforms that may not render markdown links correctly.

## Skills and Tools Reference

### Search and Discovery

**mcp__bing-search__bing_search** - Chinese-optimized search for projects and hot topics
- Use for project discovery by name
- Find aggregation and comparison articles
- Search community discussions (Reddit, HN)
- Include current year (2026) for latest results
- Best for: Chinese content discovery

**mcp__firecrawl__firecrawl_search** - Powerful global web search
- Advanced search operators supported (site:, inurl:, intitle:)
- Filter by time range (tbs: qdr:d for 24h)
- Sources: web, images, news
- Best for: English content, global AI news

### Content Extraction

**mcp__firecrawl__firecrawl_scrape** - Most powerful scraping tool
- JSON format with schema for structured data extraction
- Markdown format for full page content
- Supports JavaScript rendering (waitFor parameter)
- Best for: GitHub Trending, documentation sites, blogs

**mcp__web_reader__webReader** - Quick web content extraction
- Fast extraction from web pages
- Returns markdown or text content
- Use for: simple pages, quick extraction

**mcp__bing-search__crawl_webpage** - Batch crawl search results
- Use with UUIDs from bing_search results
- Automatically filters blacklisted sites (Zhihu, Xiaohongshu)
- Use for: community discussion threads

**mcp__firecrawl__firecrawl_agent** - Autonomous web research agent
- Deep research across multiple sources
- Self-directed browsing and data gathering
- Polling required for completion (async)
- Best for: Complex research tasks, multi-source analysis

### Tool Selection Guide

| Scenario | Recommended Tool | Notes |
|----------|-----------------|-------|
| GitHub README | `webReader` or `firecrawl_scrape` | Direct URL access |
| GitHub Trending | `firecrawl_scrape` (JSON + schema) | Set waitFor: 8000 |
| Structured data extraction | `firecrawl_scrape` (JSON) | Define schema for output |
| Complex/JS-heavy page | `firecrawl_scrape` | Use waitFor parameter |
| Simple web page | `webReader` | Quick extraction |
| Project discovery (Chinese) | `bing_search` | Chinese-optimized |
| Project discovery (Global) | `firecrawl_search` | Advanced operators |
| Deep research task | `firecrawl_agent` | Poll for completion |
| Community discussions | `bing_search` + `crawl_webpage` | Search then batch crawl |
| Local document | Read tool | Direct file access |

### Tool Selection Examples

**Fetching GitHub README:**
```python
# Use webReader for direct access
webReader(url="https://github.com/user/repo")
```

**Scraping GitHub Trending:**
```python
# Use firecrawl_scrape with JSON schema
firecrawl_scrape({
  "url": "https://github.com/trending",
  "formats": [{"type": "json", "prompt": "...", "schema": {...}}],
  "waitFor": 8000
})
```

**Deep research with Firecrawl Agent:**
```python
# 1. Start agent research
result = firecrawl_agent(prompt="Research AI breakthroughs 2026")

# 2. Poll for completion
while True:
    status = firecrawl_agent_status(id=result["id"])
    if status["status"] in ["completed", "failed"]:
        break
    sleep(30)

# 3. Extract results
research_data = status["result"]
```

**Project search flow:**
```python
# 1. Search for project
bing_search(query="react alternatives 2026")
# OR
firecrawl_search(query="best react alternatives 2026")

# 2. Crawl top results for details
crawl_webpage(uuids=[...], urlMap={...})
# OR
firecrawl_scrape(url="...", formats=["markdown"])
```

## Reference Files

This skill includes reference files for detailed guidance:

| File | Description | When to Read |
|------|-------------|--------------|
| `references/samples/` | 5优秀公众号文章样本 | Before writing any article |
| `references/samples.md` | 样本使用说明和亮点分析 | Understand sample characteristics |
| `references/writing-guide.md` | 写作风格指南（标题、开头、段落节奏） | During writing for tone guidance |
| `references/research-checklist.md` | 深度调研清单（10项调研要求） | During research phase |
| `references/automated-workflow-guide.md` | 自动化工作流完整指南 | During automated workflow execution |
| `references/three-layer-research-guide.md` | 三层递进式调研策略详解 | During three-layer research |

**Quick reference:**
- Writing style: `references/writing-guide.md`
- Research requirements: `references/research-checklist.md`
- Sample articles: `references/samples/`
- Automated workflow: `references/automated-workflow-guide.md`
- Three-layer research: `references/three-layer-research-guide.md`
