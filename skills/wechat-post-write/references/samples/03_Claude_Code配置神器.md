---
title: 堪称外挂的 Claude Code 配置神器，在 GitHub 上杀疯了。
author: 逛逛GitHub
url: https://mp.weixin.qq.com/s/K7nVgjV8uiieK9ZdP10FuA
date: 2026-02-08
---

# 堪称外挂的 Claude Code 配置神器，在 GitHub 上杀疯了。

这个叫 **everything-claude-code** 的开源项目太顶了。

开源没几天就 **3.5 万的 Star** 了。。。

先看它的简介，上面写的是：**完整的 Claude Code 配置合集——Agent、Skill、Hook、快捷命令、规则、MCPs**。来自 Anthropic 黑客马拉松获胜者的经过实战检验的配置。

重点是：**来自 Anthropic 黑客马拉松获胜者的经过实战检验。**

这个开源项目的作者是 **Affaan Mustafa**，是一位超级资深的 AI 开发者。

这个开源项目是它长达 **10 个月的高强度使用 Claude Code 经验**总结而来的。而且它用这套配置赢得了 **Anthropic x Forum Ventures 黑客松 Hackathon 的冠军**。

在黑客松比赛中，时间很紧迫，通常只有一天。

他们在短短 **8 小时**内，完全依靠 Claude Code 这一工具从零开发了一个 AI 驱动的客户发现平台：**zenith.chat**。

并成功进行了现场演示，最后获得了冠军儿🏆。

## 01 开源项目简介

**everything-claude-code** 是一个为 Claude Code 打造的完整配置工具箱，包括：可以直接用的 **agents、skills、 hooks、快捷命令、 规则、MCP 配置**。

它不是提示词合集，而是一个把 Claude Code 从 ChatBot 变成资深工程师的、实战检验过的完整开发工作流与配置套件。

说白了，就是能把你的 Claude Code **武装到牙齿**。

```
开源地址：github.com/affaan-m/everything-claude-code
```

看它这套开源项目架构，对于黑客松比赛有针对性的战术：

### ① 合理使用 Agents

他们没有把 Claude 仅仅当作一个 ChatBot，而是利用项目中的 Agents 配置，把 Claude 分裂成不同的角色：

- **Planner Agent**：负责在写代码前由 AI 自动生成架构图和实施计划，避免了盲目编码导致的返工，在黑客松中这个很重要。
- **Code Reviewer Agent**：在代码提交前自动审查，确保演示时不会因为低级错误，比如语法错误、未捕获的异常啥的，导致 Demo 失败。

### ②克服上下文腐烂

在长达 8 小时的连续 Coding 中，普通 AI 往往会忘记之前的设定。

Affaan 利用这套配置中的 Skills 和 Rules，强制 AI 始终遵循特定的 **TDD测试驱动开发模式**，保持了代码逻辑的一致性，直到比赛结束。

### ③ MCP的使用

他们通过配置 MCP 工具，比如 **GitHub MCP, Supabase MCP**等。

让 Claude 直接操作数据库和代码仓库。这意味着他们几乎不需要手动去数据库建表或在 IDE 之间来回切换，极大缩短了开发周期。

## 学习指南

当然只看这个开源项目学不到精髓，作者写了两篇文章，一定要去看看：

```
指南一：https://x.com/affaanmustafa/status/2012378465664745795
```

```
指南二：https://x.com/affaanmustafa/status/2012378465664745795
```

## 02 如何使用

在 Claude Code 中添加此仓库为插件市场：

```
/plugin marketplace add affaan-m/everything-claude-code
```

安装插件：

```
/plugin install everything-claude-code@everything-claude-code
```

安装完成后，立即获得仓库中定义的所有 commands / agents / skills / hooks，开箱即用。

### 在新项目启动阶段

可以先用 /plan 命令调用 planner/architect 等 agents，帮助梳理目标功能、选择技术栈并划分模块边界。

同时启用 **coding-style.md、security.md、testing.md** 等规则文件，把团队统一的编码规范、安全要求和测试标准固化下来，让后续所有对话和生成代码都在同一工程轨道上运行。

### 在具体开发过程中

采用 **TDD + 验证循环**的方式：通过 /tdd 命令让 Claude 按 RED → GREEN → REFACTOR → VERIFY 的流程推进开发。

用 /verify 执行实现验证、对比和边界分析，在关键里程碑使用 /checkpoint 记录思路快照和当前状态，既方便回滚，也方便日后回顾设计决策。

### 在质量与长期维护方面

日常多用 /code-review 命令，请专门的 review/safety agent 进行代码与安全审查，再配合 hooks 自动执行如清理 console.log、生成会话总结等后台任务。

对于中长期项目，则结合 **continuous-learning/** 和 **strategic-compact/** 相关 skills 与 hooks，让 Claude 持续积累项目记忆，并在上下文接近上限前做有策略的压缩，保证长期协作的连贯性与效率。

你可以把这个开源项目作为一个**生产级起步模板**，高效用 Claude Code 搭建严肃的软件工程工作流，在极短时间内产出可 demo 的产品。

**不需要自己从 0 写 agents / skills / hooks。**
