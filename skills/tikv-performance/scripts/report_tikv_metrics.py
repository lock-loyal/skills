#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from dataclasses import dataclass, field
from typing import Any

DEFAULT_IP = "172.22.67.41"
DEFAULT_STEP = "30s"
DEVICE_FILTER = 'device=~"dm-0|dm-1|sda|vda"'


@dataclass(frozen=True)
class QueryContext:
    time: str | None = None
    start: str | None = None
    end: str | None = None
    step: str = DEFAULT_STEP

    @property
    def is_range(self) -> bool:
        return self.start is not None

    def describe(self) -> str:
        if self.time:
            return self.time
        if self.start and self.end:
            return f"{self.start} -> {self.end} (step {self.step})"
        return "now"


@dataclass(frozen=True)
class BenchmarkSpec:
    key: str
    mode: str
    benchmark_text: str
    abnormal_trigger: float | None = None
    ranges: tuple[tuple[str, float | None, float | None], ...] = ()


@dataclass(frozen=True)
class MetricSpec:
    id: str
    label: str
    query: str | None
    unit: str
    benchmark_key: str | None
    interpretation: str
    summary_mode: str = "max"
    scale: float = 1.0
    abnormal_note: str = ""


@dataclass
class SeriesSummary:
    label: str
    current: float
    worst: float
    minimum: float
    maximum: float


@dataclass
class MetricResult:
    spec: MetricSpec
    value: float | None
    current_value: float | None
    status: str
    benchmark_text: str
    interpretation: str
    detail_lines: list[str]
    series_summaries: list[SeriesSummary]
    abnormal: bool
    value_text: str


@dataclass
class Anomaly:
    metric_id: str
    title: str


@dataclass
class Report:
    operation: str
    target_ip: str
    query_context: QueryContext
    core: list[MetricResult]
    anomalies: list[Anomaly] = field(default_factory=list)
    secondary: list[MetricResult] = field(default_factory=list)
    findings: list[str] = field(default_factory=list)


BENCHMARKS: dict[str, BenchmarkSpec] = {
    "write.async_write_p99_ms": BenchmarkSpec(
        key="write.async_write_p99_ms",
        mode="high",
        benchmark_text="good < 2 ms; acceptable 2-10 ms; warning 10-30 ms; bad > 30 ms",
        abnormal_trigger=10.0,
        ranges=(
            ("good", None, 2.0),
            ("acceptable", 2.0, 10.0),
            ("warning", 10.0, 30.0),
            ("bad", 30.0, None),
        ),
    ),
    "write.apply_wait_p99_ms": BenchmarkSpec(
        key="write.apply_wait_p99_ms",
        mode="high",
        benchmark_text="good < 5 ms; acceptable 5-50 ms; warning 50-200 ms; bad > 200 ms",
        abnormal_trigger=50.0,
        ranges=(
            ("good", None, 5.0),
            ("acceptable", 5.0, 50.0),
            ("warning", 50.0, 200.0),
            ("bad", 200.0, None),
        ),
    ),
    "write.append_log_p99_ms": BenchmarkSpec(
        key="write.append_log_p99_ms",
        mode="high",
        benchmark_text="good < 3 ms; acceptable 3-10 ms; warning 10-20 ms; bad > 20 ms",
        abnormal_trigger=10.0,
        ranges=(
            ("good", None, 3.0),
            ("acceptable", 3.0, 10.0),
            ("warning", 10.0, 20.0),
            ("bad", 20.0, None),
        ),
    ),
    "write.apply_log_p99_ms": BenchmarkSpec(
        key="write.apply_log_p99_ms",
        mode="high",
        benchmark_text="good < 1 ms; acceptable 1-5 ms; warning 5-20 ms; bad > 20 ms",
        abnormal_trigger=5.0,
        ranges=(
            ("good", None, 1.0),
            ("acceptable", 1.0, 5.0),
            ("warning", 5.0, 20.0),
            ("bad", 20.0, None),
        ),
    ),
    "write.rocksdb_kv_write_p99_ms": BenchmarkSpec(
        key="write.rocksdb_kv_write_p99_ms",
        mode="high",
        benchmark_text="good < 1 ms; acceptable 1-5 ms; warning 5-20 ms; bad > 20 ms",
        abnormal_trigger=5.0,
        ranges=(
            ("good", None, 1.0),
            ("acceptable", 1.0, 5.0),
            ("warning", 5.0, 20.0),
            ("bad", 20.0, None),
        ),
    ),
    "read.get_p99_us": BenchmarkSpec(
        key="read.get_p99_us",
        mode="high",
        benchmark_text="good < 200 us; acceptable 200-1000 us; warning 1000-5000 us; bad > 5000 us",
        abnormal_trigger=1000.0,
        ranges=(
            ("good", None, 200.0),
            ("acceptable", 200.0, 1000.0),
            ("warning", 1000.0, 5000.0),
            ("bad", 5000.0, None),
        ),
    ),
    "read.get_avg_us": BenchmarkSpec(
        key="read.get_avg_us",
        mode="high",
        benchmark_text="good < 50 us; acceptable 50-200 us; warning 200-1000 us; bad > 1000 us",
        abnormal_trigger=200.0,
        ranges=(
            ("good", None, 50.0),
            ("acceptable", 50.0, 200.0),
            ("warning", 200.0, 1000.0),
            ("bad", 1000.0, None),
        ),
    ),
    "read.seek_p99_us": BenchmarkSpec(
        key="read.seek_p99_us",
        mode="high",
        benchmark_text="good < 500 us; acceptable 500-3000 us; warning 3000-10000 us; bad > 10000 us",
        abnormal_trigger=3000.0,
        ranges=(
            ("good", None, 500.0),
            ("acceptable", 500.0, 3000.0),
            ("warning", 3000.0, 10000.0),
            ("bad", 10000.0, None),
        ),
    ),
    "read.block_cache_hit_ratio_pct": BenchmarkSpec(
        key="read.block_cache_hit_ratio_pct",
        mode="low",
        benchmark_text="good > 95%; acceptable 85-95%; warning 70-85%; bad < 70%",
        abnormal_trigger=85.0,
        ranges=(
            ("bad", None, 70.0),
            ("warning", 70.0, 85.0),
            ("acceptable", 85.0, 95.0),
            ("good", 95.0, None),
        ),
    ),
    "read.cop_handle_p99_ms": BenchmarkSpec(
        key="read.cop_handle_p99_ms",
        mode="high",
        benchmark_text="good < 10 ms; acceptable 10-50 ms; warning 50-200 ms; bad > 200 ms",
        abnormal_trigger=50.0,
        ranges=(
            ("good", None, 10.0),
            ("acceptable", 10.0, 50.0),
            ("warning", 50.0, 200.0),
            ("bad", 200.0, None),
        ),
    ),
    "system.cpu_pct": BenchmarkSpec(
        key="system.cpu_pct",
        mode="high",
        benchmark_text="good < 60%; acceptable 60-75%; warning 75-90%; bad > 90%",
        abnormal_trigger=75.0,
        ranges=(
            ("good", None, 60.0),
            ("acceptable", 60.0, 75.0),
            ("warning", 75.0, 90.0),
            ("bad", 90.0, None),
        ),
    ),
    "system.memory_pct": BenchmarkSpec(
        key="system.memory_pct",
        mode="high",
        benchmark_text="good < 70%; acceptable 70-80%; warning 80-90%; bad > 90%",
        abnormal_trigger=80.0,
        ranges=(
            ("good", None, 70.0),
            ("acceptable", 70.0, 80.0),
            ("warning", 80.0, 90.0),
            ("bad", 90.0, None),
        ),
    ),
    "disk.write_latency_ms": BenchmarkSpec(
        key="disk.write_latency_ms",
        mode="high",
        benchmark_text="good < 1 ms; acceptable 1-3 ms; warning 3-10 ms; bad > 10 ms",
        abnormal_trigger=3.0,
        ranges=(
            ("good", None, 1.0),
            ("acceptable", 1.0, 3.0),
            ("warning", 3.0, 10.0),
            ("bad", 10.0, None),
        ),
    ),
    "disk.read_latency_ms": BenchmarkSpec(
        key="disk.read_latency_ms",
        mode="high",
        benchmark_text="good < 1 ms; acceptable 1-3 ms; warning 3-10 ms; bad > 10 ms",
        abnormal_trigger=3.0,
        ranges=(
            ("good", None, 1.0),
            ("acceptable", 1.0, 3.0),
            ("warning", 3.0, 10.0),
            ("bad", 10.0, None),
        ),
    ),
    "disk.load": BenchmarkSpec(
        key="disk.load",
        mode="high",
        benchmark_text="good < 1; acceptable 1-2; warning 2-5; bad > 5",
        abnormal_trigger=2.0,
        ranges=(
            ("good", None, 1.0),
            ("acceptable", 1.0, 2.0),
            ("warning", 2.0, 5.0),
            ("bad", 5.0, None),
        ),
    ),
    "cluster.per_instance_skew_ratio": BenchmarkSpec(
        key="cluster.per_instance_skew_ratio",
        mode="high",
        benchmark_text="good < 1.5x; acceptable 1.5x-2x; warning 2x-3x; bad > 3x",
        abnormal_trigger=2.0,
        ranges=(
            ("good", None, 1.5),
            ("acceptable", 1.5, 2.0),
            ("warning", 2.0, 3.0),
            ("bad", 3.0, None),
        ),
    ),
    "reliability.retry_p99": BenchmarkSpec(
        key="reliability.retry_p99",
        mode="high",
        benchmark_text="good near zero; acceptable low; warning noticeable; bad sustained high",
        abnormal_trigger=1.0,
        ranges=(
            ("good", None, 0.1),
            ("acceptable", 0.1, 1.0),
            ("warning", 1.0, 3.0),
            ("bad", 3.0, None),
        ),
    ),
}


WRITE_CORE = [
    MetricSpec(
        id="write.async_write_p99_ms",
        label="Storage async write duration p99",
        query='histogram_quantile(0.99, sum(rate(tikv_storage_engine_async_request_duration_seconds_bucket{type="write"}[5m])) by (le, instance))',
        unit="ms",
        benchmark_key="write.async_write_p99_ms",
        interpretation="Core end-to-end write-path latency inside TiKV.",
        scale=1000.0,
        abnormal_note="Write path latency is abnormal.",
    ),
    MetricSpec(
        id="write.apply_wait_p99_ms",
        label="Apply wait duration p99",
        query='histogram_quantile(0.99, sum(rate(tikv_raftstore_apply_wait_time_duration_secs_bucket[5m])) by (le, instance))',
        unit="ms",
        benchmark_key="write.apply_wait_p99_ms",
        interpretation="Queueing before apply; high values mean backlog.",
        scale=1000.0,
        abnormal_note="Apply-stage queueing is abnormal.",
    ),
]

WRITE_SECONDARY = [
    MetricSpec(
        id="write.append_log_p99_ms",
        label="Append log duration p99",
        query='histogram_quantile(0.99, sum(rate(tikv_raftstore_append_log_duration_seconds_bucket[5m])) by (le, instance))',
        unit="ms",
        benchmark_key="write.append_log_p99_ms",
        interpretation="High values usually point to Raft log or storage pressure.",
        scale=1000.0,
    ),
    MetricSpec(
        id="write.apply_log_p99_ms",
        label="Apply log duration p99",
        query='histogram_quantile(0.99, sum(rate(tikv_raftstore_apply_log_duration_seconds_bucket[5m])) by (le))',
        unit="ms",
        benchmark_key="write.apply_log_p99_ms",
        interpretation="Real apply execution time; compare it to apply wait.",
        scale=1000.0,
    ),
    MetricSpec(
        id="write.rocksdb_kv_write_p99_ms",
        label="RocksDB-KV write duration p99",
        query='max(tikv_engine_write_micro_seconds{db="kv",type="write_percentile99"}) by (instance)',
        unit="ms",
        benchmark_key="write.rocksdb_kv_write_p99_ms",
        interpretation="Storage-engine-side KV write cost.",
        scale=0.001,
    ),
    MetricSpec(
        id="write.raftstore_cpu_cores",
        label="Raftstore CPU",
        query='sum(rate(tikv_thread_cpu_seconds_total{name=~"(raftstore|rs)_.*"}[5m])) by (instance)',
        unit="cores",
        benchmark_key=None,
        interpretation="Compare peers; one instance much higher than others suggests hotspot or local pressure.",
    ),
    MetricSpec(
        id="write.async_apply_cpu_cores",
        label="Async apply CPU",
        query='sum(rate(tikv_thread_cpu_seconds_total{name=~"apply_[0-9]+"}[5m])) by (instance)',
        unit="cores",
        benchmark_key=None,
        interpretation="Low CPU with high apply wait usually means queueing rather than CPU saturation.",
    ),
    MetricSpec(
        id="disk.write_latency_ms",
        label="Disk write latency",
        query=f'irate(node_disk_write_time_seconds_total{{{DEVICE_FILTER}}}[5m]) / irate(node_disk_writes_completed_total{{{DEVICE_FILTER}}}[5m])',
        unit="ms",
        benchmark_key="disk.write_latency_ms",
        interpretation="Strong storage bottleneck signal.",
        scale=1000.0,
    ),
    MetricSpec(
        id="disk.load",
        label="Disk load",
        query=f'irate(node_disk_write_time_seconds_total{{{DEVICE_FILTER}}}[5m])',
        unit="load",
        benchmark_key="disk.load",
        interpretation="Sustained high load usually means disk saturation.",
    ),
    MetricSpec(
        id="reliability.retry_p99",
        label="Transaction retry p99",
        query='histogram_quantile(0.99, sum(rate(tidb_session_retry_num_bucket[5m])) by (le))',
        unit="retries",
        benchmark_key="reliability.retry_p99",
        interpretation="Noticeable retries suggest conflict or hotspot pressure.",
    ),
    MetricSpec(
        id="reliability.lock_resolve_ops",
        label="Lock resolve ops",
        query='sum(rate(tidb_tikvclient_lock_resolver_actions_total[5m])) by (type)',
        unit="ops/s",
        benchmark_key=None,
        interpretation="Rising lock resolution can indicate write conflicts or stalled cleanup.",
        summary_mode="max",
    ),
]

READ_CORE = [
    MetricSpec(
        id="read.get_p99_us",
        label="Get duration p99",
        query='max(tikv_engine_get_micro_seconds{db="kv",type="get_percentile99"}) by (instance)',
        unit="us",
        benchmark_key="read.get_p99_us",
        interpretation="Key read latency benchmark.",
        abnormal_note="Read latency is abnormal.",
    ),
    MetricSpec(
        id="read.block_cache_hit_ratio_pct",
        label="Block cache hit ratio",
        query='(sum(rate(tikv_engine_cache_efficiency{db="kv",type="block_cache_hit"}[5m])) by (instance)) / ((sum(rate(tikv_engine_cache_efficiency{db="kv",type="block_cache_hit"}[5m])) by (instance)) + (sum(rate(tikv_engine_cache_efficiency{db="kv",type="block_cache_miss"}[5m])) by (instance))) * 100',
        unit="%",
        benchmark_key="read.block_cache_hit_ratio_pct",
        interpretation="Low hit ratio often explains slow reads.",
        summary_mode="min",
        abnormal_note="Block cache hit ratio is abnormal.",
    ),
]

READ_SECONDARY = [
    MetricSpec(
        id="read.seek_p99_us",
        label="Seek duration p99",
        query='max(tikv_engine_seek_micro_seconds{db="kv",type="seek_percentile99"}) by (instance)',
        unit="us",
        benchmark_key="read.seek_p99_us",
        interpretation="Range-like or iterator read cost.",
    ),
    MetricSpec(
        id="read.get_avg_us",
        label="Get duration avg",
        query='max(tikv_engine_get_micro_seconds{db="kv",type="get_average"}) by (instance)',
        unit="us",
        benchmark_key="read.get_avg_us",
        interpretation="Average point-read latency helps separate broad slowness from tail latency.",
    ),
    MetricSpec(
        id="read.cop_handle_p99_ms",
        label="Coprocessor handle duration p99",
        query='histogram_quantile(0.99, sum(rate(tikv_coprocessor_request_handle_seconds_bucket[5m])) by (le, req))',
        unit="ms",
        benchmark_key="read.cop_handle_p99_ms",
        interpretation="High values suggest scan or query-side pressure.",
        scale=1000.0,
    ),
    MetricSpec(
        id="read.cop_cpu_cores",
        label="Coprocessor CPU",
        query='sum(rate(tikv_thread_cpu_seconds_total{name=~"cop_.*"}[5m])) by (instance)',
        unit="cores",
        benchmark_key=None,
        interpretation="High coprocessor CPU with high read latency points to scan/query pressure.",
    ),
    MetricSpec(
        id="disk.read_latency_ms",
        label="Disk read latency",
        query=f'irate(node_disk_read_time_seconds_total{{{DEVICE_FILTER}}}[5m]) / irate(node_disk_reads_completed_total{{{DEVICE_FILTER}}}[5m])',
        unit="ms",
        benchmark_key="disk.read_latency_ms",
        interpretation="Important when read p99 rises.",
        scale=1000.0,
    ),
    MetricSpec(
        id="disk.load",
        label="Disk load",
        query=f'irate(node_disk_read_time_seconds_total{{{DEVICE_FILTER}}}[5m])',
        unit="load",
        benchmark_key="disk.load",
        interpretation="Sustained read-side load points to storage saturation.",
    ),
    MetricSpec(
        id="read.block_cache_usage_pct",
        label="Block cache usage",
        query='100 * max(tikv_engine_block_cache_size_bytes{db="kv"}) by (instance) / max(tikv_engine_block_cache_capacity_bytes{db="kv"}) by (instance)',
        unit="%",
        benchmark_key=None,
        interpretation="Use together with hit ratio; near-full cache with low hit ratio suggests weak cache effectiveness.",
    ),
    MetricSpec(
        id="system.memory_pct",
        label="Memory usage per instance",
        query='100 * label_replace(process_resident_memory_bytes{job="tikv"}, "host", "$1", "instance", "([^:]+):.*") / on(host) group_left max by (host) (label_replace(node_memory_MemTotal_bytes{job="overwritten-nodes"}, "host", "$1", "instance", "([^:]+):.*"))',
        unit="%",
        benchmark_key="system.memory_pct",
        interpretation="High memory pressure can hurt cache and cause stalls.",
    ),
]

SYSTEM_CORE = [
    MetricSpec(
        id="system.cpu_pct",
        label="TiKV total CPU per instance",
        query='100 * label_replace(sum(rate(tikv_thread_cpu_seconds_total[5m])) by (instance), "host", "$1", "instance", "([^:]+):.*") / on(host) group_left count by (host) (label_replace(node_cpu_seconds_total{job="overwritten-nodes",mode="idle"}, "host", "$1", "instance", "([^:]+):.*"))',
        unit="%",
        benchmark_key="system.cpu_pct",
        interpretation="Sustained high CPU usually creates tail latency.",
        abnormal_note="TiKV CPU pressure is abnormal.",
    ),
    MetricSpec(
        id="system.memory_pct",
        label="Memory usage per instance",
        query='100 * label_replace(process_resident_memory_bytes{job="tikv"}, "host", "$1", "instance", "([^:]+):.*") / on(host) group_left max by (host) (label_replace(node_memory_MemTotal_bytes{job="overwritten-nodes"}, "host", "$1", "instance", "([^:]+):.*"))',
        unit="%",
        benchmark_key="system.memory_pct",
        interpretation="High memory pressure can hurt cache and cause stalls.",
        abnormal_note="TiKV memory pressure is abnormal.",
        summary_mode="max",
    ),
]

SYSTEM_SECONDARY = [
    MetricSpec(
        id="disk.read_latency_ms",
        label="Disk read latency",
        query=f'irate(node_disk_read_time_seconds_total{{{DEVICE_FILTER}}}[5m]) / irate(node_disk_reads_completed_total{{{DEVICE_FILTER}}}[5m])',
        unit="ms",
        benchmark_key="disk.read_latency_ms",
        interpretation="Read-side storage bottleneck signal.",
        scale=1000.0,
    ),
    MetricSpec(
        id="disk.write_latency_ms",
        label="Disk write latency",
        query=f'irate(node_disk_write_time_seconds_total{{{DEVICE_FILTER}}}[5m]) / irate(node_disk_writes_completed_total{{{DEVICE_FILTER}}}[5m])',
        unit="ms",
        benchmark_key="disk.write_latency_ms",
        interpretation="Write-side storage bottleneck signal.",
        scale=1000.0,
    ),
    MetricSpec(
        id="disk.load",
        label="Disk load",
        query=f'irate(node_disk_read_time_seconds_total{{{DEVICE_FILTER}}}[5m]) + irate(node_disk_write_time_seconds_total{{{DEVICE_FILTER}}}[5m])',
        unit="load",
        benchmark_key="disk.load",
        interpretation="High load indicates storage queueing or saturation.",
    ),
    MetricSpec(
        id="read.block_cache_usage_pct",
        label="Block cache usage",
        query='100 * max(tikv_engine_block_cache_size_bytes{db="kv"}) by (instance) / max(tikv_engine_block_cache_capacity_bytes{db="kv"}) by (instance)',
        unit="%",
        benchmark_key=None,
        interpretation="Use together with latency and hit ratio to judge cache effectiveness.",
    ),
]

OPERATIONS = {
    "write": (WRITE_CORE, WRITE_SECONDARY, "write.async_write_p99_ms"),
    "read": (READ_CORE, READ_SECONDARY, "read.get_p99_us"),
    "system": (SYSTEM_CORE, SYSTEM_SECONDARY, "system.cpu_pct"),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch TiKV metrics from Prometheus and evaluate them with staged diagnosis.",
    )
    parser.add_argument("--operation", choices=sorted(OPERATIONS), required=True)
    parser.add_argument("--ip", default=DEFAULT_IP)
    parser.add_argument("--time")
    parser.add_argument("--start")
    parser.add_argument("--end")
    parser.add_argument("--step", default=DEFAULT_STEP)
    return parser.parse_args()


def build_query_context(args: argparse.Namespace) -> QueryContext:
    if args.time and (args.start or args.end):
        raise ValueError("--time cannot be combined with --start/--end")
    if bool(args.start) ^ bool(args.end):
        raise ValueError("--start and --end must be provided together")
    return QueryContext(time=args.time, start=args.start, end=args.end, step=args.step)


def build_base_url(ip: str) -> str:
    return f"http://{ip}:9090"


def run_curl_query(base_url: str, promql: str, query_ctx: QueryContext) -> dict[str, Any]:
    endpoint = "/api/v1/query_range" if query_ctx.is_range else "/api/v1/query"
    cmd = ["curl", "--noproxy", "*", "-sS", "-G", f"{base_url}{endpoint}", "--data-urlencode", f"query={promql}"]
    if query_ctx.time:
        cmd.extend(["--data-urlencode", f"time={query_ctx.time}"])
    if query_ctx.is_range:
        cmd.extend(
            [
                "--data-urlencode",
                f"start={query_ctx.start}",
                "--data-urlencode",
                f"end={query_ctx.end}",
                "--data-urlencode",
                f"step={query_ctx.step}",
            ]
        )
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or "curl failed")
    payload = json.loads(proc.stdout)
    if payload.get("status") != "success":
        raise RuntimeError(json.dumps(payload))
    return payload.get("data", {})


def finite_float(raw_value: str) -> float | None:
    try:
        value = float(raw_value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(value):
        return None
    return value


def series_label(metric: dict[str, str]) -> str:
    if not metric:
        return "cluster"
    preferred = ("instance", "device", "type", "req", "name")
    parts = []
    for key in preferred:
        if key in metric:
            parts.append(metric[key])
    if parts:
        return " / ".join(parts)
    filtered = [f"{k}={v}" for k, v in sorted(metric.items()) if k not in {"job", "__name__"}]
    return ", ".join(filtered) if filtered else "series"


def summarize_series(spec: MetricSpec, raw_series: list[dict[str, Any]], query_ctx: QueryContext) -> list[SeriesSummary]:
    summaries: list[SeriesSummary] = []
    benchmark = BENCHMARKS.get(spec.benchmark_key or "")
    mode = benchmark.mode if benchmark else "high"
    for entry in raw_series:
        label = series_label(entry.get("metric", {}))
        if query_ctx.is_range:
            values = [
                finite_float(point[1])
                for point in entry.get("values", [])
            ]
            points = [value * spec.scale for value in values if value is not None]
        else:
            value = finite_float(entry.get("value", [None, None])[1])
            points = [value * spec.scale] if value is not None else []
        if not points:
            continue
        current = points[-1]
        minimum = min(points)
        maximum = max(points)
        worst = minimum if mode == "low" else maximum
        summaries.append(
            SeriesSummary(
                label=label,
                current=current,
                worst=worst,
                minimum=minimum,
                maximum=maximum,
            )
        )
    return summaries


def summarize_metric(spec: MetricSpec, summaries: list[SeriesSummary], query_ctx: QueryContext) -> MetricResult:
    if not summaries:
        return MetricResult(
            spec=spec,
            value=None,
            current_value=None,
            status="no-data",
            benchmark_text=BENCHMARKS.get(spec.benchmark_key or "", BenchmarkSpec("", "", "No benchmark")).benchmark_text
            if spec.benchmark_key
            else "No benchmark",
            interpretation=spec.interpretation,
            detail_lines=[],
            series_summaries=[],
            abnormal=False,
            value_text="No data",
        )

    if spec.summary_mode == "min":
        representative = min(summaries, key=lambda item: item.worst)
    else:
        representative = max(summaries, key=lambda item: item.worst)

    value = representative.worst
    current_value = representative.current
    status, abnormal = evaluate_metric(spec.benchmark_key, value)
    benchmark_text = BENCHMARKS.get(spec.benchmark_key or "", BenchmarkSpec("", "", "No benchmark")).benchmark_text if spec.benchmark_key else "No benchmark"
    value_text = format_value_text(spec, value, current_value, query_ctx.is_range)
    detail_lines = format_detail_lines(spec, summaries, query_ctx.is_range)
    return MetricResult(
        spec=spec,
        value=value,
        current_value=current_value,
        status=status,
        benchmark_text=benchmark_text,
        interpretation=spec.interpretation,
        detail_lines=detail_lines,
        series_summaries=summaries,
        abnormal=abnormal,
        value_text=value_text,
    )


def evaluate_metric(benchmark_key: str | None, value: float | None) -> tuple[str, bool]:
    if benchmark_key is None or value is None:
        return ("n/a", False)
    benchmark = BENCHMARKS[benchmark_key]
    status = "n/a"
    for label, low, high in benchmark.ranges:
        low_ok = low is None or value >= low
        high_ok = high is None or value < high
        if low_ok and high_ok:
            status = label
            break
    if status == "n/a":
        status = "bad"
    if benchmark.abnormal_trigger is None:
        return status, status in {"warning", "bad"}
    if benchmark.mode == "low":
        return status, value < benchmark.abnormal_trigger
    return status, value >= benchmark.abnormal_trigger


def format_number(value: float, unit: str) -> str:
    if unit == "%":
        return f"{value:.1f}%"
    if unit == "ms":
        return f"{value:.2f} ms"
    if unit == "us":
        return f"{value:.0f} us"
    if unit == "load":
        return f"{value:.2f}"
    if unit == "cores":
        return f"{value:.2f} cores"
    if unit == "ops/s":
        return f"{value:.2f} ops/s"
    if unit == "retries":
        return f"{value:.2f}"
    if unit == "ratio":
        return f"{value:.2f}x"
    return f"{value:.2f} {unit}"


def benchmark_mode(spec: MetricSpec) -> str:
    benchmark = BENCHMARKS.get(spec.benchmark_key or "")
    return benchmark.mode if benchmark else "high"


def format_value_text(spec: MetricSpec, worst_value: float, current_value: float | None, is_range: bool) -> str:
    if not is_range or current_value is None:
        return format_number(worst_value, spec.unit)
    qualifier = "min" if benchmark_mode(spec) == "low" else "max"
    return f"current {format_number(current_value, spec.unit)}; {qualifier} {format_number(worst_value, spec.unit)}"


def format_detail_lines(spec: MetricSpec, summaries: list[SeriesSummary], is_range: bool) -> list[str]:
    details: list[str] = []
    ordered = sorted(summaries, key=lambda item: item.label)
    for summary in ordered:
        if is_range:
            qualifier = "min" if benchmark_mode(spec) == "low" else "max"
            details.append(
                f"{summary.label}: current {format_number(summary.current, spec.unit)}, {qualifier} {format_number(summary.worst, spec.unit)}"
            )
        else:
            details.append(f"{summary.label}: {format_number(summary.current, spec.unit)}")
    return details


def fetch_metric(base_url: str, spec: MetricSpec, query_ctx: QueryContext) -> MetricResult:
    assert spec.query is not None
    raw = run_curl_query(base_url, spec.query, query_ctx)
    summaries = summarize_series(spec, raw.get("result", []), query_ctx)
    return summarize_metric(spec, summaries, query_ctx)


def collect_core_metrics(operation: str, ip: str, query_ctx: QueryContext) -> list[MetricResult]:
    base_url = build_base_url(ip)
    core_specs = OPERATIONS[operation][0]
    return [fetch_metric(base_url, spec, query_ctx) for spec in core_specs]


def detect_anomalies(operation: str, core_results: list[MetricResult]) -> list[Anomaly]:
    anomalies: list[Anomaly] = []
    for result in core_results:
        if result.abnormal:
            title = result.spec.abnormal_note or f"{result.spec.label} is abnormal."
            anomalies.append(Anomaly(metric_id=result.spec.id, title=title))
    return anomalies


def make_skew_metric(operation: str, seed_result: MetricResult) -> MetricResult | None:
    values = [
        (summary.label, summary.worst)
        for summary in seed_result.series_summaries
        if summary.worst > 0
    ]
    if len(values) < 2:
        return None
    ratio = max(value for _, value in values) / min(value for _, value in values)
    status, abnormal = evaluate_metric("cluster.per_instance_skew_ratio", ratio)
    return MetricResult(
        spec=MetricSpec(
            id="cluster.per_instance_skew_ratio",
            label=f"Per-instance skew ({seed_result.spec.label})",
            query=None,
            unit="ratio",
            benchmark_key="cluster.per_instance_skew_ratio",
            interpretation="If one TiKV is much worse than peers, suspect hotspot or local node issues.",
        ),
        value=ratio,
        current_value=ratio,
        status=status,
        benchmark_text=BENCHMARKS["cluster.per_instance_skew_ratio"].benchmark_text,
        interpretation="If one TiKV is much worse than peers, suspect hotspot or local node issues.",
        detail_lines=[f"{label}: {value:.2f}" for label, value in sorted(values)],
        series_summaries=[],
        abnormal=abnormal,
        value_text=format_number(ratio, "ratio"),
    )


def collect_secondary_metrics(operation: str, anomalies: list[Anomaly], ip: str, query_ctx: QueryContext, core_results: list[MetricResult]) -> list[MetricResult]:
    if not anomalies:
        return []
    base_url = build_base_url(ip)
    secondary_specs = OPERATIONS[operation][1]
    results = [fetch_metric(base_url, spec, query_ctx) for spec in secondary_specs]
    seed_metric_id = OPERATIONS[operation][2]
    seed = next((result for result in core_results if result.spec.id == seed_metric_id and result.value is not None), None)
    if seed:
        skew = make_skew_metric(operation, seed)
        if skew:
            results.append(skew)
    return results


def result_map(results: list[MetricResult]) -> dict[str, MetricResult]:
    return {result.spec.id: result for result in results}


def build_findings(operation: str, core_results: list[MetricResult], secondary_results: list[MetricResult]) -> list[str]:
    findings: list[str] = []
    core = result_map(core_results)
    secondary = result_map(secondary_results)
    if operation == "write":
        apply_wait = core.get("write.apply_wait_p99_ms")
        apply_log = secondary.get("write.apply_log_p99_ms")
        append_log = secondary.get("write.append_log_p99_ms")
        disk_write = secondary.get("disk.write_latency_ms")
        skew = secondary.get("cluster.per_instance_skew_ratio")
        if apply_wait and apply_wait.abnormal and apply_log and apply_log.status in {"good", "acceptable"}:
            findings.append("Primary issue is apply-stage queueing or backlog, because apply wait is abnormal while apply log execution remains relatively contained.")
        if append_log and append_log.abnormal and disk_write and disk_write.abnormal:
            findings.append("Append log latency and disk write latency are both elevated, which points to Raft log or storage pressure.")
        if disk_write and not disk_write.abnormal:
            findings.append("Disk write latency is within benchmark, so storage does not look like the primary bottleneck.")
        if skew and skew.abnormal:
            findings.append("Per-instance skew is high; suspect hotspot traffic or a local node issue.")
    elif operation == "read":
        get_p99 = core.get("read.get_p99_us")
        cache_hit = core.get("read.block_cache_hit_ratio_pct")
        disk_read = secondary.get("disk.read_latency_ms")
        cop_handle = secondary.get("read.cop_handle_p99_ms")
        skew = secondary.get("cluster.per_instance_skew_ratio")
        if get_p99 and get_p99.abnormal and cache_hit and cache_hit.abnormal:
            findings.append("High get latency together with low block-cache hit ratio points to cache or storage-side read pressure.")
        if disk_read and disk_read.abnormal:
            findings.append("Disk read latency is elevated, which suggests a storage bottleneck for reads.")
        if cop_handle and cop_handle.abnormal:
            findings.append("Coprocessor handle latency is high, which suggests scan or query-side pressure.")
        if skew and skew.abnormal:
            findings.append("Per-instance skew is high; suspect hotspot reads or local imbalance.")
    elif operation == "system":
        cpu = core.get("system.cpu_pct")
        memory = core.get("system.memory_pct")
        disk_read = secondary.get("disk.read_latency_ms")
        disk_write = secondary.get("disk.write_latency_ms")
        skew = secondary.get("cluster.per_instance_skew_ratio")
        if cpu and cpu.abnormal:
            findings.append("TiKV CPU usage is elevated relative to the host benchmark.")
        if memory and memory.abnormal:
            findings.append("TiKV memory usage is elevated relative to host RAM.")
        if (disk_read and disk_read.abnormal) or (disk_write and disk_write.abnormal):
            findings.append("Disk latency is elevated, which suggests underlying storage pressure.")
        if skew and skew.abnormal:
            findings.append("Per-instance skew is high; resource pressure is uneven across TiKV instances.")
    return findings


def collect_operation(operation: str, ip: str, query_ctx: QueryContext) -> Report:
    core_results = collect_core_metrics(operation, ip, query_ctx)
    anomalies = detect_anomalies(operation, core_results)
    secondary_results = collect_secondary_metrics(operation, anomalies, ip, query_ctx, core_results)
    findings = build_findings(operation, core_results, secondary_results)
    return Report(
        operation=operation,
        target_ip=ip,
        query_context=query_ctx,
        core=core_results,
        anomalies=anomalies,
        secondary=secondary_results,
        findings=findings,
    )


def markdown_escape(value: str) -> str:
    return value.replace("|", "\\|")


def render_table(results: list[MetricResult]) -> str:
    lines = [
        "| Metric | Value | Status | Benchmark | Interpretation |",
        "| --- | ---: | --- | --- | --- |",
    ]
    for result in results:
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_escape(result.spec.label),
                    markdown_escape(result.value_text),
                    markdown_escape(result.status),
                    markdown_escape(result.benchmark_text),
                    markdown_escape(result.interpretation),
                ]
            )
            + " |"
        )
    return "\n".join(lines)


def render_detail_section(title: str, results: list[MetricResult]) -> str:
    lines = [f"## {title}"]
    for result in results:
        if result.detail_lines:
            lines.append(f"- `{result.spec.label}`")
            for detail in result.detail_lines:
                lines.append(f"  {detail}")
    return "\n".join(lines)


def render_markdown_report(report: Report) -> str:
    lines = [
        "# TiKV Performance Report",
        "",
        f"- Target: `{report.target_ip}`",
        f"- Operation: `{report.operation}`",
        f"- Time: `{report.query_context.describe()}`",
        "",
        "## Core Metrics",
        render_table(report.core),
        "",
    ]
    if not report.anomalies:
        lines.append("No abnormal core metrics detected; secondary metrics were not collected.")
        lines.append("")
        lines.append(render_detail_section("Core Metric Details", report.core))
        return "\n".join(lines)

    lines.append("## Anomalies Detected")
    for anomaly in report.anomalies:
        lines.append(f"- {anomaly.title}")
    lines.append("")
    if report.secondary:
        lines.append("## Secondary Metrics Collected")
        lines.append(render_table(report.secondary))
        lines.append("")
    if report.findings:
        lines.append("## Findings")
        for finding in report.findings:
            lines.append(f"- {finding}")
        lines.append("")
    lines.append(render_detail_section("Core Metric Details", report.core))
    if report.secondary:
        lines.append("")
        lines.append(render_detail_section("Secondary Metric Details", report.secondary))
    return "\n".join(lines)


def main() -> int:
    try:
        args = parse_args()
        query_ctx = build_query_context(args)
        report = collect_operation(args.operation, args.ip, query_ctx)
        print(render_markdown_report(report))
        return 0
    except KeyboardInterrupt:
        return 130
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
