---
name: ccf-submission
description: Help researchers make informed CCF paper submission decisions by providing comprehensive venue information including CCF class (A/B/C), acceptance rates, review cycles, and field matching. Use when user asks about paper submission recommendations, CCF venue selection, acceptance rate queries, journal/conference comparison, submission deadlines, or review timeline questions. Trigger phrases include "where to submit", "CCF推荐", "投稿建议", "acceptance rate", "review cycle", "会议推荐", "期刊投稿", "Compare venues", "A类会议", "B类期刊".
---

# CCF Submission Advisor

This skill helps researchers make informed decisions about where to submit their research papers by combining the official CCF (China Computer Federation) Recommendation Catalog (7th Edition) with dynamic research on venue statistics, acceptance rates, and submission timelines.

## Supported Query Types

| Query Type | Detection Pattern | Example |
|------------|-------------------|---------|
| Venue Lookup | Specific venue name | "What's the acceptance rate of NeurIPS?" |
| Field-based Recommendation | Research field mentioned | "Where to submit ML paper?" |
| Comparison | Multiple venues or "vs" | "Compare CVPR and ICCV" |
| CCF Class Query | "A类", "B类", "CCF-A" | "List CCF-A AI conferences" |
| Submission Planning | Deadline/timeline focus | "Upcoming CV deadlines" |

## Workflow

### Step 1: Parse Query Intent

Analyze the user's query to identify:
- **Research field**: AI, CV, NLP, systems, security, etc.
- **Venue names**: Specific conferences/journals mentioned
- **CCF class filter**: A, B, or C (if specified)
- **Information needs**: acceptance rate, review cycle, comparison, recommendation

### Step 2: Search CCF Catalog

Use the reference files in `references/ccf_catalog/`:
- `all_entries.json` - All 682 CCF venues
- `all_conferences.json` - 387 conferences
- `all_journals.json` - 295 journals
- `by_field/*.md` - Field-specific listings

Search by:
- Venue abbreviation (e.g., "NeurIPS", "CVPR")
- Full name (partial matching)
- Field category
- CCF class (A/B/C)
- Type (journal/conference)

### Step 3: Research Dynamic Information

For each relevant venue, gather up-to-date information using a three-layer research approach:

#### Layer 1: Bing Chinese Search
Use `mcp__bing-search__bing_search` for:
- Chinese researchers' submission experiences
- Acceptance rate discussions on CSDN, Zhihu
- Review cycle timelines shared by authors

**Query Patterns:**
- `[venue] 投稿经验 录取率`
- `[venue] 审稿周期 多久`
- `[venue] 接受率 2024`
- `CCF [class] [field] 会议推荐`

#### Layer 2: Firecrawl Global Search
For comprehensive research on:
- Official acceptance rate statistics
- CSRankings conference metrics
- OpenReview/SoftConf data
- Recent CFP (Call for Papers) information

#### Layer 3: Direct Web Crawling
Use `mcp__bing-search__crawl_webpage` or Firecrawl extract for:
- Official conference/journal websites
- CFP pages with deadlines
- OpenReview statistics pages
- CSRankings venue details

**Research Priorities per Venue:**
1. **Acceptance Rate**: Historical statistics from official sources or CSRankings
2. **Review Cycle**: Submission deadlines, review timeline, notification dates
3. **Venue Characteristics**: Scope, audience, emerging topics
4. **Impact Metrics**: For journals - impact factor; for conferences - h5-index

### Step 4: Integrate and Present

Combine static CCF data with dynamic research and present in a structured format.

## Output Format

### For Single Venue Queries

```
## [Venue Name] ([Abbreviation])

**CCF Classification**
- Class: [A/B/C]
- Type: [Conference/Journal]
- Field: [Field name]

**Key Statistics**
- Acceptance Rate: [X%] (source: [official/CSRankings/estimate])
- Review Cycle: [timeline]
- Next Deadline: [date] (if applicable)

**Venue Profile**
- Scope: [brief description]
- Publisher: [publisher name]
- DBLP: [url]

**Submission Tips**
[Actionable advice based on research]
```

### For Field-Based Recommendations

```
## Recommended Venues for [Field]

### Top Recommendation: [Venue Name] ([CCF Class])
- **Type**: Conference/Journal
- **CCF Class**: A/B/C
- **Acceptance Rate**: X% (source)
- **Review Cycle**: [timeline]
- **Next Deadline**: [date] (if applicable)
- **Match Score**: Why this fits the user's paper

### Alternatives
[List other options with key metrics in table format]

| Venue | Class | Type | Acceptance Rate | Review Cycle |
|-------|-------|------|-----------------|--------------|
| ... | ... | ... | ... | ... |

### Recommendation Summary
[Actionable advice with strategic considerations]
```

### For Venue Comparisons

```
## Comparison: [Venue A] vs [Venue B]

| Metric | [Venue A] | [Venue B] |
|--------|-----------|-----------|
| CCF Class | A/B/C | A/B/C |
| Type | Conf/Journal | Conf/Journal |
| Acceptance Rate | X% | Y% |
| Review Cycle | [timeline] | [timeline] |
| Next Deadline | [date] | [date] |
| Field Focus | [scope] | [scope] |

### Recommendation
[Which venue to choose based on user's situation]
```

## Reference Files Guide

### CCF Catalog Data (`references/ccf_catalog/`)

| File | Purpose | When to Use |
|------|---------|-------------|
| `all_entries.json` | All 682 venues | Programmatic search |
| `all_conferences.json` | 387 conferences | Conference-only queries |
| `all_journals.json` | 295 journals | Journal-only queries |
| `by_field/08_ai.md` | AI venues | AI/ML field queries |
| `by_field/07_graphics.md` | Graphics venues | CV/graphics queries |
| `by_field/03_security.md` | Security venues | Security queries |
| `by_field/06_theory.md` | Theory venues | Theory/algorithms queries |

### Venue Entry Structure

Each entry contains:
```json
{
  "field": "Field name in Chinese",
  "type": "期刊" (journal) or "会议" (conference),
  "class": "A", "B", or "C",
  "rank": 1, 2, 3... (within class),
  "abbreviation": "Venue abbreviation",
  "full_name": "Full venue name",
  "publisher": "Publisher",
  "url": "DBLP URL"
}
```

## Research Guidelines

### Acceptance Rate Sources (in priority order)

1. **Official Statistics**: Conference website statistics pages
2. **CSRankings**: csrankings.org for CS conferences
3. **OpenReview**: For venues using OpenReview
4. **Wikicfp**: Historical CFP data
5. **Author Experiences**: From Chinese tech blogs (CSDN, Zhihu)

### Review Cycle Patterns

**Conferences:**
- Submission: Usually 6-9 months before conference
- Review: 1-2 months
- Notification: 2-3 months after submission
- Camera-ready: 1 month after notification

**Journals:**
- First decision: 1-3 months (fast) to 6+ months (slow)
- Revision cycles: 1-3 rounds typical
- Total time: 6 months to 2 years

### CCF Class Interpretation

- **CCF-A**: Top-tier venues, highly competitive
- **CCF-B**: Established venues, good reputation
- **CCF-C**: Specialized venues, emerging areas

Note: CCF classification is China-specific but internationally recognized.

## Common Field Mappings

| User Query | CCF Field File |
|------------|----------------|
| "machine learning", "deep learning", "AI" | `by_field/08_ai.md` |
| "computer vision", "image processing" | `by_field/07_graphics.md` |
| "NLP", "natural language processing" | `by_field/08_ai.md` |
| "security", "privacy", "cryptography" | `by_field/03_security.md` |
| "systems", "distributed systems", "cloud" | `by_field/01_architecture.md` |
| "networks", "networking", "communication" | `by_field/02_network.md` |
| "database", "data mining", "information retrieval" | `by_field/05_database.md` |
| "software engineering", "programming languages" | `by_field/04_software.md` |
| "algorithms", "theory", "complexity" | `by_field/06_theory.md` |
| "HCI", "human-computer interaction" | `by_field/09_hci.md` |
| "interdisciplinary", "bioinformatics", "quantum" | `by_field/10_interdisciplinary.md` |

## Tips for First-Time Submitters

1. **Start with B/C venues** if new to the field
2. **Check recent proceedings** to understand scope
3. **Consider workshop submissions** for early feedback
4. **Review recent acceptance rates** - some A venues may have higher rates than B
5. **Factor in timeline** - conferences have fixed deadlines, journals are more flexible

## Tool Usage Priority

1. **Search CCF catalog first** - Use `scripts/search_venue.py` or read JSON files
2. **Bing Chinese Search** - For Chinese researcher experiences and recent data
3. **Firecrawl Global Search** - For official statistics and comprehensive venue research
4. **Web Crawling** - For specific official pages and CFP details
