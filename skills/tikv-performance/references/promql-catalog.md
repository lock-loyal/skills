# PromQL Catalog

Use Prometheus directly through `curl`. Default IP is `172.22.67.41`, but replace it freely.

## Base Pattern

```bash
IP="${1:-172.22.67.41}"
curl -sG "http://${IP}:9090/api/v1/query" \
  --data-urlencode 'query=up'
```

Point-in-time query:

```bash
IP="${1:-172.22.67.41}"
TS='2026-03-23T15:11:00+08:00'
curl -sG "http://${IP}:9090/api/v1/query" \
  --data-urlencode "time=${TS}" \
  --data-urlencode 'query=up'
```

Range query:

```bash
IP="${1:-172.22.67.41}"
curl -sG "http://${IP}:9090/api/v1/query_range" \
  --data-urlencode 'start=2026-03-23T15:10:00+08:00' \
  --data-urlencode 'end=2026-03-23T15:13:00+08:00' \
  --data-urlencode 'step=30s' \
  --data-urlencode 'query=up'
```

## Write Operation

Core metrics:

```bash
curl -sG "http://${IP}:9090/api/v1/query" \
  --data-urlencode 'query=histogram_quantile(0.99, sum(rate(tikv_storage_engine_async_request_duration_seconds_bucket{type="write"}[5m])) by (le, instance))'

curl -sG "http://${IP}:9090/api/v1/query" \
  --data-urlencode 'query=histogram_quantile(0.99, sum(rate(tikv_raftstore_apply_wait_time_duration_secs_bucket[5m])) by (le, instance))'
```

Secondary metrics:

```bash
curl -sG "http://${IP}:9090/api/v1/query" \
  --data-urlencode 'query=histogram_quantile(0.99, sum(rate(tikv_raftstore_append_log_duration_seconds_bucket[5m])) by (le, instance))'

curl -sG "http://${IP}:9090/api/v1/query" \
  --data-urlencode 'query=histogram_quantile(0.99, sum(rate(tikv_raftstore_apply_log_duration_seconds_bucket[5m])) by (le))'

curl -sG "http://${IP}:9090/api/v1/query" \
  --data-urlencode 'query=max(tikv_engine_write_micro_seconds{db="kv",type="write_percentile99"}) by (instance)'

curl -sG "http://${IP}:9090/api/v1/query" \
  --data-urlencode 'query=sum(rate(tikv_thread_cpu_seconds_total{name=~"(raftstore|rs)_.*"}[5m])) by (instance)'

curl -sG "http://${IP}:9090/api/v1/query" \
  --data-urlencode 'query=sum(rate(tikv_thread_cpu_seconds_total{name=~"apply_[0-9]+"}[5m])) by (instance)'

curl -sG "http://${IP}:9090/api/v1/query" \
  --data-urlencode 'query=irate(node_disk_write_time_seconds_total{device=~"dm-0|dm-1|sda|vda"}[5m]) / irate(node_disk_writes_completed_total{device=~"dm-0|dm-1|sda|vda"}[5m])'

curl -sG "http://${IP}:9090/api/v1/query" \
  --data-urlencode 'query=irate(node_disk_write_time_seconds_total{device=~"dm-0|dm-1|sda|vda"}[5m])'

curl -sG "http://${IP}:9090/api/v1/query" \
  --data-urlencode 'query=histogram_quantile(0.99, sum(rate(tidb_session_retry_num_bucket[5m])) by (le))'

curl -sG "http://${IP}:9090/api/v1/query" \
  --data-urlencode 'query=sum(rate(tidb_tikvclient_lock_resolver_actions_total[5m])) by (type)'
```

## Read Operation

Core metrics:

```bash
curl -sG "http://${IP}:9090/api/v1/query" \
  --data-urlencode 'query=max(tikv_engine_get_micro_seconds{db="kv",type="get_percentile99"}) by (instance)'

curl -sG "http://${IP}:9090/api/v1/query" \
  --data-urlencode 'query=(sum(rate(tikv_engine_cache_efficiency{db="kv",type="block_cache_hit"}[5m])) by (instance)) / ((sum(rate(tikv_engine_cache_efficiency{db="kv",type="block_cache_hit"}[5m])) by (instance)) + (sum(rate(tikv_engine_cache_efficiency{db="kv",type="block_cache_miss"}[5m])) by (instance))) * 100'
```

Secondary metrics:

```bash
curl -sG "http://${IP}:9090/api/v1/query" \
  --data-urlencode 'query=max(tikv_engine_seek_micro_seconds{db="kv",type="seek_percentile99"}) by (instance)'

curl -sG "http://${IP}:9090/api/v1/query" \
  --data-urlencode 'query=max(tikv_engine_get_micro_seconds{db="kv",type="get_average"}) by (instance)'

curl -sG "http://${IP}:9090/api/v1/query" \
  --data-urlencode 'query=histogram_quantile(0.99, sum(rate(tikv_coprocessor_request_handle_seconds_bucket[5m])) by (le, req))'

curl -sG "http://${IP}:9090/api/v1/query" \
  --data-urlencode 'query=sum(rate(tikv_thread_cpu_seconds_total{name=~"cop_.*"}[5m])) by (instance)'

curl -sG "http://${IP}:9090/api/v1/query" \
  --data-urlencode 'query=irate(node_disk_read_time_seconds_total{device=~"dm-0|dm-1|sda|vda"}[5m]) / irate(node_disk_reads_completed_total{device=~"dm-0|dm-1|sda|vda"}[5m])'

curl -sG "http://${IP}:9090/api/v1/query" \
  --data-urlencode 'query=irate(node_disk_read_time_seconds_total{device=~"dm-0|dm-1|sda|vda"}[5m])'

curl -sG "http://${IP}:9090/api/v1/query" \
  --data-urlencode 'query=100 * max(tikv_engine_block_cache_size_bytes{db="kv"}) by (instance) / max(tikv_engine_block_cache_capacity_bytes{db="kv"}) by (instance)'
```

## System Operation

Core metrics:

```bash
curl -sG "http://${IP}:9090/api/v1/query" \
  --data-urlencode 'query=100 * label_replace(sum(rate(tikv_thread_cpu_seconds_total[5m])) by (instance), "host", "$1", "instance", "([^:]+):.*") / on(host) group_left count by (host) (label_replace(node_cpu_seconds_total{job="overwritten-nodes",mode="idle"}, "host", "$1", "instance", "([^:]+):.*"))'

curl -sG "http://${IP}:9090/api/v1/query" \
  --data-urlencode 'query=100 * label_replace(process_resident_memory_bytes{job="tikv"}, "host", "$1", "instance", "([^:]+):.*") / on(host) group_left max by (host) (label_replace(node_memory_MemTotal_bytes{job="overwritten-nodes"}, "host", "$1", "instance", "([^:]+):.*"))'
```

Secondary metrics:

```bash
curl -sG "http://${IP}:9090/api/v1/query" \
  --data-urlencode 'query=irate(node_disk_read_time_seconds_total{device=~"dm-0|dm-1|sda|vda"}[5m]) / irate(node_disk_reads_completed_total{device=~"dm-0|dm-1|sda|vda"}[5m])'

curl -sG "http://${IP}:9090/api/v1/query" \
  --data-urlencode 'query=irate(node_disk_write_time_seconds_total{device=~"dm-0|dm-1|sda|vda"}[5m]) / irate(node_disk_writes_completed_total{device=~"dm-0|dm-1|sda|vda"}[5m])'

curl -sG "http://${IP}:9090/api/v1/query" \
  --data-urlencode 'query=irate(node_disk_read_time_seconds_total{device=~"dm-0|dm-1|sda|vda"}[5m]) + irate(node_disk_write_time_seconds_total{device=~"dm-0|dm-1|sda|vda"}[5m])'
```

## Notes

- Prefer the script for staged collection and report formatting.
- Use direct `curl` examples when the user explicitly asks for raw queries or wants to paste commands into a shell.
- If a query returns `NaN` or no series, treat it as `No data`, not as an automatic failure.
