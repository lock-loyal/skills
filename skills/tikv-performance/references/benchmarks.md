# TiKV Performance Benchmarks

Assumption: these benchmarks are practical thresholds for a TiKV/TiDB OLTP-style cluster on SSD/NVMe, and diagnosis should rely mostly on `p95` and `p99`, not only averages.

## Full Table

| Category | Metric | Unit | Good | Acceptable | Warning | Bad | How to read it |
|---|---|---:|---:|---:|---:|---:|---|
| Write | Storage async write duration `p99` | ms | `< 2` | `2 - 10` | `10 - 30` | `> 30` | Core end-to-end write-path latency inside TiKV |
| Write | Storage async write duration `avg` | ms | `< 0.5` | `0.5 - 3` | `3 - 10` | `> 10` | If avg is high, the whole write path is slow, not just tail latency |
| Write | Append log duration `p99` | ms | `< 3` | `3 - 10` | `10 - 20` | `> 20` | High values usually point to Raft log / fsync / storage pressure |
| Write | Apply wait duration `p99` | ms | `< 5` | `5 - 50` | `50 - 200` | `> 200` | Queueing before apply; large values mean backlog |
| Write | Apply log duration `p99` | ms | `< 1` | `1 - 5` | `5 - 20` | `> 20` | Real apply execution time; if low but wait is high, the problem is queueing |
| Write | RocksDB-KV write duration `p99` | ms | `< 1` | `1 - 5` | `5 - 20` | `> 20` | Storage-engine-side KV write cost |
| Read | Get duration `p99` | us | `< 200` | `200 - 1000` | `1000 - 5000` | `> 5000` | Key read latency benchmark |
| Read | Get duration `avg` | us | `< 50` | `50 - 200` | `200 - 1000` | `> 1000` | Good for seeing general read health |
| Read | Seek duration `p99` | us | `< 500` | `500 - 3000` | `3000 - 10000` | `> 10000` | Range-like / iterator read cost |
| Read | Block cache hit ratio | % | `> 95` | `85 - 95` | `70 - 85` | `< 70` | Low hit ratio often explains slow reads |
| Read | Coprocessor handle duration `p99` | ms | `< 10` | `10 - 50` | `50 - 200` | `> 200` | Important for scan/aggregation-heavy SQL |
| Throughput | Read ops / Write ops | ops/s | No absolute benchmark | No absolute benchmark | Judge with latency | Judge with latency | Throughput alone is not “good” or “bad”; rising ops with stable latency is good |
| CPU | TiKV total CPU per instance | % of host | `< 60%` | `60 - 75%` | `75 - 90%` | `> 90%` | Sustained high CPU usually creates tail latency |
| CPU | Raftstore / Apply / Coprocessor CPU | cores or % | Balanced, no single node >2x peers | Slightly uneven | One node clearly high | Sustained hotspot | Compare instances; imbalance is often more important than the absolute value |
| Memory | TiKV memory usage | % of RAM | `< 70%` | `70 - 80%` | `80 - 90%` | `> 90%` | High memory pressure can hurt cache and cause stalls |
| Memory | Block cache usage | % of configured size | `70 - 90%` | `50 - 70%` or `90 - 95%` | Very low or nearly full all the time | Thrashing / OOM risk | Too low means wasted cache, too high with low hit ratio means poor cache effectiveness |
| Disk | Disk latency (write) | ms | `< 1` | `1 - 3` | `3 - 10` | `> 10` | Strong storage bottleneck signal |
| Disk | Disk latency (read) | ms | `< 1` | `1 - 3` | `3 - 10` | `> 10` | Important when read p99 rises |
| Disk | Disk load / queue depth | value | `< 1` | `1 - 2` | `2 - 5` | `> 5` | Sustained high load usually means disk saturation |
| Disk | Disk bandwidth / IOPS | MB/s / IOPS | No absolute benchmark | Device-dependent | Judge with latency/load | Judge with latency/load | High bandwidth is fine if latency stays low |
| Cluster balance | Per-instance skew | ratio | `< 1.5x` | `1.5x - 2x` | `2x - 3x` | `> 3x` | If one TiKV is much worse than peers, suspect hotspot or local issue |
| Reliability | Retry / conflict / lock resolve | rate | Near zero | Low | Noticeable and rising | Sustained high | Important for hotspot and write-conflict diagnosis |

## Short Rule Of Thumb

| Scenario | Healthy benchmark |
|---|---|
| Online writes | `async write p99 < 10 ms`, `apply wait p99 < 50 ms`, `append log p99 < 10 ms` |
| Online reads | `get p99 < 1 ms`, `block cache hit > 85%`, no single node much worse than peers |
| Disk health | `disk latency < 3 ms`, `disk load < 2` most of the time |
| Cluster balance | Any key metric should stay within about `2x` across TiKV instances |

## Staged Collection Rule

Default to core metrics first:

- `write`
  - `Storage async write duration p99`
  - `Apply wait duration p99`
- `read`
  - `Get duration p99`
  - `Block cache hit ratio`
- `system`
  - `TiKV total CPU per instance`
  - `Memory usage per instance`

Collect the wider metric set only when a core metric is abnormal or the user explicitly asks for deeper diagnosis.
