---
name: wechat-post
description: Generate high-quality Chinese articles about open source projects for WeChat posting. Supports multiple input methods - GitHub URL (auto-fetch README), project name (auto-search and fetch), or direct paste of README/content. Each project section is under 800 Chinese characters combined. Output includes eye-catching title, background, motivation, purpose, features (3-5 points), deployment, project source URL, and latest hot topic integration per project. Articles are saved as markdown files. Articles can cover single or multiple projects with smooth transitions. Tone is serious but humorous. Use when user wants to write WeChat articles about projects, create project roundups, or summarize multiple projects in Chinese. Trigger phrases include '公众号文章', '介绍项目', '推荐开源项目', '写文章介绍', 'project roundup', '项目推荐'.
---

# WeChat Article Generator for Open Source Projects

## Overview

Generate polished Chinese articles about open source projects suitable for WeChat public accounts. The skill handles project information gathering via three input methods, integrates latest hot topics, and saves articles as markdown files with all links in plain text format.

## Workflow

### Step 1: Identify Input Method

Determine how the user provides project information:

| Input Type | Detection | Action |
|------------|-----------|--------|
| GitHub URL | Contains `github.com` | Fetch README directly |
| Project name | Plain text, repo name, or project title | Search then fetch |
| Direct content | Full README, markdown content, or detailed description | Use as-is |

### Step 2: Gather Project Information

**For GitHub URL:**
- Convert to raw README URL: `github.com/user/repo` → `raw.githubusercontent.com/user/repo/main/README.md`
- Try `main` branch first, fallback to `master`
- Use `mcp__Fetch__fetch` to retrieve content
- Save original GitHub URL for later inclusion

**For project name:**
- Use `mcp__bing-search__bing_search` to find the project
- Search term: `[project name] github`
- Identify correct GitHub repo from results
- Save the GitHub URL
- Fetch README using the GitHub URL method above

**For direct content:**
- Parse the provided markdown/text directly
- Extract: project name, description, features, installation info
- Ask user for GitHub URL if not provided

**Extract from README:**
- Project name and tagline
- Background/motivation (often in "About", "Why", or intro sections)
- Key features (bullet points or "Features" section)
- Installation/deployment instructions (README, Getting Started, Quick Start)

### Step 3: Search for Latest Hot Topics

For each project, search for recent relevant information:

**Search approach:**
- Use `mcp__bing-search__bing_search` with current year in query: `[project name] 2026`
- Alternative search terms: `[project name] news`, `[project name] release`, `[project name] update`
- Look for: recent releases, version updates, trending discussions, community highlights

**Integrate hot topics into article:**
- Mention latest version if recently released
- Reference new features or breaking changes
- Note community discussions or controversies (if relevant and appropriate)
- Keep hot topic integration brief (1-2 sentences) to maintain character limits

### Step 4: Generate Article Content

**Per project structure:**

1. **Title** - Eye-catching, possibly with wordplay or tech puns
   - Use active language: "Build", "Create", "Transform"
   - Include project name and core benefit
   - Example: "告别手动部署：用这个工具一键搞定一切"

2. **Background (背景)** - What is this project?
   - 1-2 sentences explaining what the project is
   - Technical but accessible language

3. **Motivation (动机)** - Why was it created?
   - Problem statement or pain point addressed
   - Brief context about the creation story

4. **Purpose (目的)** - What problem does it solve?
   - Clear benefit statement
   - Who is this for?

5. **Features (3-5 points)** - Key capabilities
   - List format for readability
   - Focus on most impactful features
   - Each point: benefit + technical detail

6. **Deployment (部署)** - How to install/use
   - Quick setup instructions
   - Keep practical and concise

7. **Hot Topic (热点)** - Latest relevant information
   - Recent updates, releases, or community discussions
   - 1-2 sentences maximum

8. **Source URL (项目地址)** - Original project link in plain text
   - Format: `项目地址：github.com/user/repo` (plain text, not markdown link)
   - Always include at the end of each project section

**Character limit:** Entire project section (all 8 parts combined) under 800 Chinese characters.

### Step 5: Apply Tone (Serious but Humorous)

**Serious elements:**
- Accurate technical information
- Professional terminology
- Respectful treatment of the project and authors

**Humorous elements:**
- Light wordplay or puns (tech-related)
- Relatable analogies (comparing tech to everyday experiences)
- Self-aware commentary about developer challenges
- Subtle wit without being distracting

**Avoid:**
- Inappropriate jokes
- Mockery of projects or developers
- Excessive slang or meme culture
- Humor that obscures technical meaning

### Step 6: Multi-Project Articles

When covering multiple projects:

1. **Identify connections** between projects:
   - Shared technology stack (e.g., both use Rust)
   - Related problems solved
   - Complementary use cases
   - Same author or organization

2. **Write transitions:**
   - Connect logically: "Speaking of [project A's feature], [project B] takes it further by..."
   - Contrast deliberately: "While [project A] focuses on X, [project B] approaches from the Y angle"
   - Build narrative: Start with foundation, layer with advanced tools

3. **Maintain consistency:**
   - Similar article structure per project
   - Balanced coverage (not over-emphasizing some projects)
   - Coherent narrative flow

**No preset limit on project count** - let article scope and reader attention guide the number.

### Step 7: Save Article as Markdown

After generating the article content:

1. **Generate filename:**
   - Filename must exactly match the article title
   - Format: `[article-title].md`
   - Example: If article title is "Rust开发必备工具", filename must be `Rust开发必备工具.md`
   - For English titles, use `.md` extension
   - For Chinese titles, use `.md` extension (Chinese filenames are supported)

2. **Write to file:**
   - Use the Write tool to save the article
   - Save in current working directory or specify output path
   - Confirm file location with user

3. **Format requirements:**
   - All URLs in plain text format (not markdown hyperlinks)
   - Example: `github.com/user/repo` instead of `[link](github.com/user/repo)`
   - This ensures WeChat compatibility

## Output Template

```
# [Thematic Title for article]

## [Project 1 Name]

### [Eye-catching Project Title]

**背景：** [1-2 sentences]

**动机：** [Why created]

**目的：** [What problem solved]

**核心特性：**
- [Feature 1]
- [Feature 2]
- [Feature 3]

**部署方式：** [Quick setup]

**最新动态：** [Hot topic info]

**项目地址：** github.com/user/repo (plain text)

---

## [Project 2 Name]

### [Eye-catching Project Title]

[Repeat structure above]

**项目地址：** github.com/user2/repo2 (plain text)
```

## Link Format Rules

**ALL links must be plain text, not markdown hyperlinks:**

Correct:
```
项目地址：github.com/user/repo
文档：raw.githubusercontent.com/user/repo/main/README.md
```

Incorrect:
```
项目地址：[github.com/user/repo](https://github.com/user/repo)
文档：[README](https://raw.githubusercontent.com/user/repo/main/README.md)
```

This format ensures compatibility with WeChat and other platforms that may not render markdown links correctly.

## MCP Tools Reference

When implementing this skill, use these available tools:

- `mcp__Fetch__fetch` - Fetch GitHub README content
- `mcp__bing-search__bing_search` - Search for projects by name and hot topics
- `mcp__bing-search__crawl_webpage` - Crawl search results if needed
- `Write` - Save article as markdown file
