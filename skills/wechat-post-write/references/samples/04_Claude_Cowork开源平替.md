---
title: 挖到了 GitHub 上 3 个 Claude Cowork 的开源平替。
author: 逛逛GitHub
url: https://mp.weixin.qq.com/s/xPDK-KcP7gbKTM_ymmfAvw
date: 2026-02-08
---

# 挖到了 GitHub 上 3 个 Claude Cowork 的开源平替。

**Claude Cowork** 是 Anthropic 推的一个**新功能**，它让 Claude 变成一个能操作你电脑文件的 AI Agent 。

Cowork 不仅仅是陪你聊天，而是可以直接在你授权的电脑文件夹中做一些文件处理。

**用它能做文件整理、数据提取与转换、批量文档处理、代码/脚本辅助啥的。**

**而且与普通的一问一答不同，当你给 Cowork 下达一个复杂指令的时候，它会先制定一个计划，然后一步步执行，并在关键步骤向你确认或汇报进度。**

**它不需要你一直盯着，可以并行处理任务。**

一般有什么新东西出来，GitHub 上一定会开源平替的。

逛逛就找到最近很火的 3 个 Claude Cowork 开源平替。

## 01 桌面级多智能体平台：Eigent

**目前这个叫 eigent 的开源项目已经登上了 GitHub 的热榜。**

**现在已经获得 7800+ 的星星了，还是比较火的。**

这个开源项目的团队是**多智能体（Multi-Agent）协作**，用它你能组建一支 AI 员工团队，自动协作完成复杂的任务。

它能把复杂的任务拆解，分发给不同的 AI 员工并行处理。用它你可以读取本地 excel 生成数据分析报告、整理本地文件，比如批量重命名、删除重复文件等等。

系统预定义了多种角色的 Agent，还内置了大量的 MCP 工具，能够让 AI 直接操作外部工具和服务。

```
开源地址：https://github.com/eigent-ai/eigent
```

## 02 桌面级 AI Agent 办公：openwork

**OpenWork 开源项目的目标是打造一个开源版的 Claude Cowork，让复杂的 Agent 任务变成像使用普通软件一样简单。**

**它由 OpenCode 驱动，让智能体工作感觉像是在使用一个成熟的产品，而不是在操作冰冷的终端。**

**用 OpenWork 你不需要学习复杂的 CLI 指令，也不用担心配置满天飞。**

**它将 AI 的思考和执行过程变成了清晰的时间线和待办事项，你可以实时看到 AI 打算干什么，干到了哪一步。**

**它有两种运行模式：**

**Host Mode**：直接在本地启动 OpenCode 服务，选择一个文件夹作为工作区，AI 就在你眼皮底下帮你干活。

**Client Mode**：如果你有一个远程的 OpenCode 服务器，OpenWork 也可以通过 URL 连接上去，实现远程办公。

**OpenWork 内置了 Skill 管理器**。你可以像给浏览器装插件一样，给你的 AI Agent 安装各种 Skills。

**对于那些重复性的工作流，你可以将它们保存为模板。下次再遇到同样的一套任务，一键载入 AI 自动执行，极大提升效率。**

```
开源地址：https://github.com/different-ai/openwork
```

## 03 Claude-Cowork

**这个开源项目把 Claude Code 强大的 Agent 能力封装进了一个可视化操作界面里。**

**如果 Claude Code 能在你的终端里运行，那么它就能在 Claude-Cowork 里运行。**

**Claude Code 原生只有黑乎乎的命令行，把它封装成 Claude Cowork 有一些好处：**

**Claude Cowork 提供了流式输出和 Markdown 渲染，你可以清晰地看到 Claude 的思考路径、代码高亮以及具体的工具调用状态。**

**Claude-Cowork 内置了基于 SQLite 的会话管理系统。你可以创建不同的会话，针对不同的项目或任务设定独立的工作目录，并且随时保存或恢复之前的对话历史。**

**还有就是 AI 想要执行敏感操作，比如删除文件、运行脚本时，你可以通过交互式界面进行允许或拒绝，更加安心和直观。**

**下面是一个整理本地文件的视频：**

```
开源地址：https://github.com/DevAgentForge/Claude-Cowork
```
