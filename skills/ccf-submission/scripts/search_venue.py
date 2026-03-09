#!/usr/bin/env python3
"""
CCF Venue Search Script

Search the CCF Recommendation Catalog (7th Edition) by various criteria:
- Venue name (abbreviation or full name)
- Field
- CCF Class (A/B/C)
- Type (conference/journal)

Usage:
    python search_venue.py --name "NeurIPS"
    python search_venue.py --field "人工智能"
    python search_venue.py --class A --type 会议
    python search_venue.py --json --name "CVPR"
"""

import json
import argparse
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

# Get the script directory and construct path to catalog
SCRIPT_DIR = Path(__file__).parent.resolve()
CATALOG_DIR = SCRIPT_DIR.parent / "references" / "ccf_catalog"


def load_catalog(filename: str = "all_entries.json") -> List[Dict[str, Any]]:
    """Load the CCF catalog from JSON file."""
    catalog_path = CATALOG_DIR / filename
    try:
        with open(catalog_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Catalog file not found at {catalog_path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in catalog file: {e}", file=sys.stderr)
        sys.exit(1)


def normalize_text(text: str) -> str:
    """Normalize text for case-insensitive search."""
    return text.lower().replace(' ', '').replace('-', '').replace('_', '')


def search_by_name(catalog: List[Dict[str, Any]], query: str, fuzzy: bool = True) -> List[Dict[str, Any]]:
    """
    Search venues by abbreviation or full name.

    Args:
        catalog: List of venue entries
        query: Search query string
        fuzzy: If True, allow partial matching

    Returns:
        List of matching venue entries
    """
    query_norm = normalize_text(query)
    results = []

    for entry in catalog:
        abbrev = entry.get('abbreviation', '') or ''
        full_name = entry.get('full_name', '') or ''

        abbrev_norm = normalize_text(abbrev)
        full_name_norm = normalize_text(full_name)

        # Exact match on abbreviation (case-insensitive)
        if abbrev.lower() == query.lower():
            results.insert(0, entry)  # Prioritize exact abbreviation match
            continue

        # Exact match on full name
        if full_name.lower() == query.lower():
            results.append(entry)
            continue

        if fuzzy:
            # Partial match on abbreviation
            if query_norm in abbrev_norm or abbrev_norm in query_norm:
                results.append(entry)
                continue

            # Partial match on full name
            if query_norm in full_name_norm:
                results.append(entry)
                continue

    # Remove duplicates while preserving order
    seen = set()
    unique_results = []
    for entry in results:
        key = (entry.get('abbreviation'), entry.get('full_name'))
        if key not in seen:
            seen.add(key)
            unique_results.append(entry)

    return unique_results


def search_by_field(catalog: List[Dict[str, Any]], field_query: str) -> List[Dict[str, Any]]:
    """
    Search venues by field/category.

    Args:
        catalog: List of venue entries
        field_query: Field name (partial match supported)

    Returns:
        List of matching venue entries
    """
    query_norm = normalize_text(field_query)
    results = []

    for entry in catalog:
        field = entry.get('field', '')
        if query_norm in normalize_text(field):
            results.append(entry)

    return results


def filter_by_class(catalog: List[Dict[str, Any]], ccf_class: str) -> List[Dict[str, Any]]:
    """Filter venues by CCF class (A, B, or C)."""
    ccf_class = ccf_class.upper()
    return [entry for entry in catalog if entry.get('class') == ccf_class]


def filter_by_type(catalog: List[Dict[str, Any]], venue_type: str) -> List[Dict[str, Any]]:
    """
    Filter venues by type (conference or journal).

    Args:
        catalog: List of venue entries
        venue_type: '会议' or '期刊' (or 'conference'/'journal')
    """
    type_mapping = {
        'conference': '会议',
        'conf': '会议',
        '会议': '会议',
        'journal': '期刊',
        'j': '期刊',
        '期刊': '期刊'
    }

    normalized_type = type_mapping.get(venue_type.lower(), venue_type)
    return [entry for entry in catalog if entry.get('type') == normalized_type]


def format_entry(entry: Dict[str, Any]) -> str:
    """Format a single venue entry for display."""
    lines = [
        f"Abbreviation: {entry.get('abbreviation', 'N/A')}",
        f"Full Name: {entry.get('full_name', 'N/A')}",
        f"CCF Class: {entry.get('class', 'N/A')}",
        f"Type: {entry.get('type', 'N/A')}",
        f"Field: {entry.get('field', 'N/A')}",
        f"Publisher: {entry.get('publisher', 'N/A')}",
        f"URL: {entry.get('url', 'N/A')}",
    ]
    return '\n'.join(lines)


def display_results(results: List[Dict[str, Any]], verbose: bool = False) -> None:
    """Display search results in a formatted manner."""
    if not results:
        print("No matching venues found.")
        return

    print(f"\nFound {len(results)} venue(s):\n")
    print("=" * 80)

    for i, entry in enumerate(results, 1):
        print(f"\n[{i}]")
        print("-" * 80)
        print(format_entry(entry))

    print("\n" + "=" * 80)


def display_table(results: List[Dict[str, Any]]) -> None:
    """Display results in a compact table format."""
    if not results:
        print("No matching venues found.")
        return

    print(f"\nFound {len(results)} venue(s):\n")

    # Header
    print(f"{'Abbrev':<12} {'Class':<6} {'Type':<6} {'Field':<30} {'Full Name':<40}")
    print("-" * 100)

    # Rows
    for entry in results:
        abbrev = entry.get('abbreviation', 'N/A')[:11]
        ccf_class = entry.get('class', 'N/A')
        vtype = entry.get('type', 'N/A')[:5]
        field = entry.get('field', 'N/A')[:29]
        full_name = entry.get('full_name', 'N/A')[:39]
        print(f"{abbrev:<12} {ccf_class:<6} {vtype:<6} {field:<30} {full_name:<40}")


def get_field_mapping() -> Dict[str, str]:
    """Get mapping of field keywords to field names."""
    return {
        'ai': '人工智能',
        'artificial intelligence': '人工智能',
        'machine learning': '人工智能',
        'ml': '人工智能',
        'deep learning': '人工智能',
        'cv': '计算机图形学与多媒体',
        'computer vision': '计算机图形学与多媒体',
        'graphics': '计算机图形学与多媒体',
        'multimedia': '计算机图形学与多媒体',
        'nlp': '人工智能',
        'natural language': '人工智能',
        'security': '网络与信息安全',
        'cryptography': '网络与信息安全',
        'privacy': '网络与信息安全',
        'systems': '计算机体系结构/并行与分布计算/存储系统',
        'architecture': '计算机体系结构/并行与分布计算/存储系统',
        'distributed': '计算机体系结构/并行与分布计算/存储系统',
        'cloud': '计算机体系结构/并行与分布计算/存储系统',
        'network': '计算机网络',
        'networking': '计算机网络',
        'communication': '计算机网络',
        'database': '计算机科学理论/数据工程',
        'data mining': '计算机科学理论/数据工程',
        'ir': '计算机科学理论/数据工程',
        'information retrieval': '计算机科学理论/数据工程',
        'software': '软件工程/系统软件/程序设计语言',
        'software engineering': '软件工程/系统软件/程序设计语言',
        'programming languages': '软件工程/系统软件/程序设计语言',
        'pl': '软件工程/系统软件/程序设计语言',
        'theory': '计算机科学理论/数据工程',
        'algorithms': '计算机科学理论/数据工程',
        'hci': '人机交互与普适计算',
        'human-computer': '人机交互与普适计算',
        'ubiquitous': '人机交互与普适计算',
        'interdisciplinary': '交叉/综合/新兴',
        'bioinformatics': '交叉/综合/新兴',
        'quantum': '交叉/综合/新兴',
    }


def resolve_field_keyword(keyword: str) -> Optional[str]:
    """Resolve a field keyword to full field name."""
    mapping = get_field_mapping()
    keyword_lower = keyword.lower()

    # Direct match
    if keyword_lower in mapping:
        return mapping[keyword_lower]

    # Partial match
    for key, value in mapping.items():
        if keyword_lower in key or key in keyword_lower:
            return value

    return None


def main():
    parser = argparse.ArgumentParser(
        description='Search CCF Recommendation Catalog (7th Edition)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --name "NeurIPS"              # Search by name
  %(prog)s --field "人工智能"            # Search by field
  %(prog)s --field ai                    # Search by field keyword
  %(prog)s --class A --type 会议         # All CCF-A conferences
  %(prog)s --class B --type 期刊         # All CCF-B journals
  %(prog)s --name "CVPR" --json          # Output as JSON
  %(prog)s --table                       # Show all in table format
        """
    )

    parser.add_argument('--name', '-n', type=str, help='Search by venue name (abbreviation or full name)')
    parser.add_argument('--field', '-f', type=str, help='Search by field/category')
    parser.add_argument('--class', '-c', dest='ccf_class', type=str, choices=['A', 'B', 'C'], help='Filter by CCF class')
    parser.add_argument('--type', '-t', type=str, choices=['会议', '期刊', 'conference', 'journal', 'conf', 'j'], help='Filter by venue type')
    parser.add_argument('--json', '-j', action='store_true', help='Output results as JSON')
    parser.add_argument('--table', action='store_true', help='Output in compact table format')
    parser.add_argument('--exact', '-e', action='store_true', help='Exact name match only (no fuzzy search)')
    parser.add_argument('--catalog', type=str, default='all_entries.json', help='Catalog file to use')

    args = parser.parse_args()

    # Load catalog
    catalog = load_catalog(args.catalog)

    # Start with full catalog and filter down
    results = catalog

    # Apply filters
    if args.name:
        results = search_by_name(results, args.name, fuzzy=not args.exact)

    if args.field:
        # Try to resolve field keyword first
        resolved_field = resolve_field_keyword(args.field)
        if resolved_field:
            results = search_by_field(results, resolved_field)
        else:
            results = search_by_field(results, args.field)

    if args.ccf_class:
        results = filter_by_class(results, args.ccf_class)

    if args.type:
        results = filter_by_type(results, args.type)

    # If no filters applied and --table not specified, show help
    if not any([args.name, args.field, args.ccf_class, args.type, args.table]):
        parser.print_help()
        return

    # Output results
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    elif args.table:
        display_table(results)
    else:
        display_results(results)


if __name__ == '__main__':
    main()
