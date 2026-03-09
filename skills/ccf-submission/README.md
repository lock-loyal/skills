# CCF Submission Skill

A Claude skill to help researchers make informed CCF (China Computer Federation) paper submission decisions.

## Overview

This skill combines the official CCF Recommendation Catalog (7th Edition) with dynamic research capabilities to provide comprehensive venue information including:

- CCF classification (A/B/C)
- Acceptance rates and statistics
- Review cycles and submission deadlines
- Field-specific recommendations
- Venue comparisons

## Directory Structure

```
skills/ccf-submission/
├── SKILL.md                          # Main skill instructions
├── README.md                         # This file
├── references/
│   ├── ccf_catalog/                  # CCF 7th Edition catalog data
│   │   ├── all_entries.json          # All 682 venues
│   │   ├── all_conferences.json      # 387 conferences
│   │   ├── all_journals.json         # 295 journals
│   │   ├── by_class/                 # Organized by CCF class
│   │   └── by_field/                 # 10 field-specific files
│   └── venue_research_guide.md       # Research strategies and sources
└── scripts/
    └── search_venue.py               # CLI tool to search CCF catalog
```

## Usage

### As a Claude Skill

The skill is automatically triggered by queries like:

- "Where should I submit my machine learning paper?"
- "What's the acceptance rate of NeurIPS?"
- "Compare CVPR and ICCV for computer vision"
- "Which CCF-A AI conferences have the fastest review cycle?"
- "Is TNNLS a good journal for deep learning?"

### Command Line Tool

```bash
# Search by venue name
python scripts/search_venue.py --name "NeurIPS"

# Search by field (supports English keywords)
python scripts/search_venue.py --field ai
python scripts/search_venue.py --field "computer vision"

# Filter by CCF class and type
python scripts/search_venue.py --class A --type 会议
python scripts/search_venue.py --class B --type journal

# Combined search
python scripts/search_venue.py --field ai --class A --type 会议 --table

# Output as JSON
python scripts/search_venue.py --name "CVPR" --json
```

## Data Coverage

- **Total Venues**: 682
- **Conferences**: 387
- **Journals**: 295
- **Fields**: 10 categories
  1. Computer Architecture / Parallel & Distributed Computing / Storage
  2. Computer Networks
  3. Network & Information Security
  4. Software Engineering / System Software / Programming Languages
  5. Databases / Data Mining / Content Retrieval
  6. Computer Science Theory
  7. Computer Graphics & Multimedia
  8. Artificial Intelligence
  9. Human-Computer Interaction & Pervasive Computing
  10. Interdisciplinary / Emerging

## Research Approach

The skill uses a three-layer research strategy:

1. **Bing Chinese Search**: For Chinese researcher experiences and recent data
2. **Firecrawl Global Search**: For official statistics and comprehensive venue research
3. **Direct Web Crawling**: For official CFP pages and venue details

## Sample Queries

### Venue Lookup
- "What's the acceptance rate of NeurIPS?"
- "Tell me about TNNLS journal"
- "CVPR submission deadline"

### Field-Based Recommendations
- "Where to submit my NLP paper?"
- "Recommend CCF-A conferences for computer vision"
- "Best journals for federated learning"

### Venue Comparisons
- "Compare CVPR and ICCV"
- "NeurIPS vs ICML vs ICLR"
- "Should I submit to AAAI or IJCAI?"

### CCF Class Queries
- "List all CCF-A AI conferences"
- "CCF-B journals in security"
- "What are CCF-C venues for data mining?"

## Field Mappings

| English Keyword | CCF Field |
|-----------------|-----------|
| ai, machine learning, deep learning | 人工智能 |
| cv, computer vision, graphics | 计算机图形学与多媒体 |
| nlp, natural language | 人工智能 |
| security, cryptography | 网络与信息安全 |
| systems, architecture, distributed | 计算机体系结构/并行与分布计算/存储系统 |
| networks, networking | 计算机网络 |
| database, data mining, ir | 数据库/数据挖掘/内容检索 |
| software, se, programming languages | 软件工程/系统软件/程序设计语言 |
| theory, algorithms | 计算机科学理论 |
| hci, human-computer | 人机交互与普适计算 |

## CCF Classification Guide

- **CCF-A**: Top-tier venues, highest prestige, typically 15-25% acceptance
- **CCF-B**: Established venues, good reputation, typically 20-35% acceptance
- **CCF-C**: Specialized venues, emerging areas, typically 25-45% acceptance

Note: Acceptance rates vary significantly by venue and year.

## License

The CCF catalog data is based on the public CCF Recommendation Catalog (7th Edition).
