---
name: tikv-performance
description: Fetch and diagnose TiKV/TiDB performance metrics from Prometheus with direct `curl` queries, using staged collection and built-in benchmark thresholds. Use when Codex needs to evaluate TiKV read performance, write performance, CPU, memory, disk health, cluster skew, or hotspot symptoms, especially for requests like "check TiKV performance", "query TiKV metrics", "use curl to get Prometheus metrics", "analyze read/write latency", or "evaluate metrics on 172.22.67.41 or another specified IP".
---

# TiKV Performance

## Overview

Use this skill to fetch TiKV metrics from Prometheus and judge them against practical SSD/NVMe OLTP benchmarks. Default to `172.22.67.41`, and allow the user to override the target IP.

## Quick Start

Run the bundled script from the skill directory:

```bash
python scripts/report_tikv_metrics.py --operation write
python scripts/report_tikv_metrics.py --operation read --ip 10.0.0.8
python scripts/report_tikv_metrics.py --operation write --time '2026-03-23T15:11:00+08:00'
python scripts/report_tikv_metrics.py --operation read --start '2026-03-23T15:10:00+08:00' --end '2026-03-23T15:13:00+08:00' --step 30s
```

## Workflow

1. Choose `--operation read`, `write`, or `system`.
2. Query only the core metrics for that operation.
3. Compare the core metrics to the built-in benchmarks.
4. If a core metric is abnormal, collect the secondary metrics for that operation.
5. Use the secondary metrics to explain whether the issue is queueing, disk pressure, cache pressure, coprocessor pressure, or per-instance skew.

## Operation Routing

- Use `write` for write latency, apply queueing, append/apply stages, raftstore pressure, and disk-write checks.
- Use `read` for point-read latency, cache hit ratio, seek latency, coprocessor pressure, and disk-read checks.
- Use `system` only when the user explicitly wants host-level CPU, memory, and general storage health.
- Do not collect every metric by default. Follow the staged diagnosis rule unless the user explicitly asks for a full dump.

## Core-First Rules

Use only these core metrics first:

- `write`
  - `Storage async write duration p99`
  - `Apply wait duration p99`
- `read`
  - `Get duration p99`
  - `Block cache hit ratio`
- `system`
  - `TiKV total CPU per instance`
  - `Memory usage per instance`

Collect secondary metrics only when a core metric is abnormal.

## Interpretation Rules

- High `apply wait` with relatively low `apply log` usually means queueing or backlog rather than expensive apply execution.
- High `append log` together with high disk-write latency usually points to log-path or storage pressure.
- High `get p99` with low block-cache hit ratio usually points to cache or storage issues.
- High `get p99` with high coprocessor metrics usually points to scan/query pressure.
- One instance much worse than its peers usually suggests hotspot or local node imbalance.

## References

- Benchmarks: [`references/benchmarks.md`](./references/benchmarks.md)
- PromQL catalog and direct-IP `curl` examples: [`references/promql-catalog.md`](./references/promql-catalog.md)

## Prompt Examples

- `Use $tikv-performance to check write performance on the default TiKV cluster.`
- `Use $tikv-performance to evaluate read latency on 10.0.0.8 at 2026-03-23 15:11 +08:00.`
- `Use $tikv-performance to diagnose why write performance is slow and collect secondary metrics only if the core write metrics are abnormal.`
- `Use $tikv-performance to compare TiKV system health on a specific IP and summarize CPU, memory, and disk pressure.`
