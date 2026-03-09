# 深度调研清单

每个项目必须完成的调研清单，确保内容专业、深入、有据可查。

## 强制搜索平台（优先级排序）

1. **官网** - 产品定位、核心功能、技术架构、定价
2. **GitHub** - Stars趋势、Contributors、Issues讨论、Release历史
3. **HuggingFace** - 如果相关，模型下载量、Spaces演示、论文链接
4. **公众号** - 中文社区讨论、测评文章、使用教程
5. **Reddit** - r/programming、r/LocalLLaMA、相关子版块讨论
6. **X (Twitter)** - 创始人、技术负责人、行业KOL的讨论

## 每个项目至少10个来源

| 平台 | 最少数量 | 说明 |
|------|----------|------|
| 官网 | 1 | 官方信息为准 |
| GitHub | 2 | README + Issues讨论 |
| HuggingFace | 1-2 | 如果适用 |
| 公众号 | 2-3 | 中文社区视角 |
| Reddit | 1-2 | 英文社区讨论 |
| X | 2-3 | 实时动态、创始人 |
| 其他补充 | 1-2 | 技术博客、评测文章 |

## 深度调研项（每项必须覆盖）

### 1. 基础信息 [必须]
- [ ] 项目名称、创始人/团队
- [ ] 创立时间、当前版本
- [ ] 开源协议（MIT/Apache/等）
- [ ] 核心定位一句话描述

**搜索指令**：
```
site:github.com [project-name]
site:official-website.com [project-name]
```

### 2. 创始人/团队背景 [建议]
- [ ] 创始人LinkedIn/GitHub主页
- [ ] 之前的工作/创业经历
- [ ] 在AI/技术领域的声誉
- [ ] 是否有黑客松/比赛获奖经历

**搜索指令**：
```
[project-name] founder OR creator
[creator-name] GitHub LinkedIn
[project-name] hackathon award
```

### 3. 核心功能与特性 [必须]
- [ ] 解决了什么核心痛点
- [ ] 3-5个核心功能亮点
- [ ] 与竞品相比的差异化
- [ ] 技术实现原理（架构、技术栈）

**搜索指令**：
```
[project-name] features OR "how it works"
[project-name] vs [competitor] comparison
```

### 4. GitHub数据分析 [必须]
- [ ] 当前Stars数、增长趋势
- [ ] Fork数、Contributor数
- [ ] 最近一次提交时间/活跃度
- [ ] 热门Issues讨论（用户关心什么）
- [ ] Releases版本历史

**搜索指令**：
```
site:github.com/stars [project-name]
[project-name] trending OR popular
```

### 5. 真实用户反馈 [必须]
- [ ] 用户的核心好评点
- [ ] 用户的核心抱怨点
- [ ] 使用场景/最佳实践
- [ ] 常见问题/踩坑经验

**搜索指令**：
```
[project-name] review OR experience OR feedback
[project-name] Reddit discussion
"[project-name]" "how to" OR "tutorial"
```

### 6. 竞品对比 [建议]
- [ ] 主要竞品有哪些
- [ ] 各自的优劣势
- [ ] 为什么选择/不选择XX
- [ ] 市场份额/采用率对比

**搜索指令**：
```
[project-name] alternatives OR vs
best [category] tools 2026
```

### 7. 最新动态与趋势 [必须]
- [ ] 最近一次更新内容
- [ ] 路线图/未来规划
- [ ] 行业趋势/所在赛道讨论
- [ ] 是否有重大争议或负面

**搜索指令**：
```
[project-name] latest OR release OR update
[project-name] roadmap OR future
[project-name] controversy OR problem
```

### 8. 中文社区讨论 [必须]
- [ ] 公众号文章评价
- [ ] 知乎/掘金等平台讨论
- [ ] 国内用户使用体验
- [ ] 是否有中文文档/教程

**搜索指令**：
```
[project-name] 公众号
[project-name] 知乎 OR 掘金
[project-name] 中文文档
```

### 9. X(Twitter)实时动态 [必须]
- [ ] 创始人/团队的最近发言
- [ ] 行业KOL的讨论/评测
- [ ] 用户真实反馈
- [ ] 相关技术趋势讨论

**搜索指令**：
```
from:[founder-twitter-handle]
[project-name] OR "#hashtag"
[project-name] review OR "my thoughts"
```

### 10. HuggingFace相关信息 [如果适用]
- [ ] 模型下载量/排名
- [ ] Spaces在线演示
- [ ] 论文/技术报告链接
- [ ] Model Card详细信息

**搜索指令**：
```
huggingface.co/[project-name]
[project-name] model download
```

## 调研注意事项

### 信息验证
- 交叉验证关键数据（多个来源确认）
- 标注数据获取时间
- 对于争议性信息，呈现多方观点

### 优先级
- 官方来源 > 社区来源
- 一手信息 > 二手转发
- 最新信息 > 过时信息

### 记录来源
- 保存所有搜索URL
- 记录关键信息对应的来源
- 选择性引用，而非全部列出

## 调研模板

```
## [Project Name] 调研记录

### 基础信息
- 项目名：
- 创始人：
- GitHub：
- 官网：
- Stars：
- 开源协议：

### 核心亮点
1.
2.
3.

### 用户评价
- 好评：
- 差评：

### 最新动态
-

### 数据来源
- [1] 官网: url
- [2] GitHub: url
- [3] Reddit: url
- [4] X: url
- ...
```
