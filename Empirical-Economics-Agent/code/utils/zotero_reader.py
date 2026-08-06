"""Read a local Zotero library in read-only mode.

Usage examples:
    python code/utils/zotero_reader.py --test
    python code/utils/zotero_reader.py --contains momentum --limit 20
    python code/utils/zotero_reader.py --export-json paper-lib/literature/zotero-index.json

Path resolution order:
1. --db-path argument
2. ZOTERO_DB_PATH environment variable
3. Common Zotero data locations on Windows

This script never writes to the Zotero database.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import json
import os
import sqlite3
import sys
from typing import Iterable


def candidate_db_paths() -> list[Path]:
    candidates: list[Path] = []

    env_path = os.environ.get("ZOTERO_DB_PATH", "").strip()
    if env_path:
        candidates.append(Path(env_path).expanduser())

    home = Path.home()
    appdata = Path(os.environ.get("APPDATA", ""))

    candidates.append(home / "Zotero" / "zotero.sqlite")
    if appdata:
        profiles_dir = appdata / "Zotero" / "Zotero" / "Profiles"
        if profiles_dir.exists():
            for profile in sorted(profiles_dir.glob("*")):
                candidates.append(profile / "zotero.sqlite")

    # Deduplicate while preserving order.
    seen: set[Path] = set()
    resolved: list[Path] = []
    for path in candidates:
        path = path.expanduser()
        if path not in seen:
            seen.add(path)
            resolved.append(path)
    return resolved


def resolve_db_path(explicit: str | None) -> Path:
    if explicit:
        path = Path(explicit).expanduser()
        if path.exists():
            return path
        raise FileNotFoundError(f"Explicit Zotero DB path not found: {path}")

    for candidate in candidate_db_paths():
        if candidate.exists():
            return candidate

    searched = "\n".join(f"- {path}" for path in candidate_db_paths())
    raise FileNotFoundError(
        "No Zotero database was found. Searched:\n"
        f"{searched}\n\n"
        "Set ZOTERO_DB_PATH or pass --db-path explicitly."
    )


def connect_read_only(db_path: Path) -> sqlite3.Connection:
    uri = f"file:{db_path.as_posix()}?mode=ro"
    connection = sqlite3.connect(uri, uri=True)
    connection.row_factory = sqlite3.Row
    return connection


def fetch_items(connection: sqlite3.Connection, contains: str | None, limit: int) -> list[dict[str, str | int | None]]:
    query = """
    WITH title_map AS (
        SELECT itemData.itemID, itemDataValues.value AS title
        FROM itemData
        JOIN fields ON itemData.fieldID = fields.fieldID
        JOIN itemDataValues ON itemData.valueID = itemDataValues.valueID
        WHERE fields.fieldName = 'title'
    ),
    year_map AS (
        SELECT itemData.itemID, itemDataValues.value AS year
        FROM itemData
        JOIN fields ON itemData.fieldID = fields.fieldID
        JOIN itemDataValues ON itemData.valueID = itemDataValues.valueID
        WHERE fields.fieldName = 'date'
    ),
    creator_map AS (
        SELECT itemCreators.itemID,
               GROUP_CONCAT(
                   TRIM(COALESCE(creators.lastName, '') || CASE WHEN creators.firstName IS NOT NULL AND creators.firstName != '' THEN ', ' || creators.firstName ELSE '' END),
                   '; '
               ) AS creators
        FROM itemCreators
        JOIN creators ON itemCreators.creatorID = creators.creatorID
        GROUP BY itemCreators.itemID
    )
    SELECT items.itemID,
           items.key,
           itemTypes.typeName AS item_type,
           title_map.title,
           year_map.year,
           creator_map.creators,
           items.dateAdded,
           items.dateModified
    FROM items
    JOIN itemTypes ON items.itemTypeID = itemTypes.itemTypeID
    LEFT JOIN title_map ON items.itemID = title_map.itemID
    LEFT JOIN year_map ON items.itemID = year_map.itemID
    LEFT JOIN creator_map ON items.itemID = creator_map.itemID
    LEFT JOIN deletedItems ON items.itemID = deletedItems.itemID
    WHERE deletedItems.itemID IS NULL
      AND itemTypes.typeName NOT IN ('attachment', 'note', 'annotation')
      AND (
          :contains IS NULL
          OR LOWER(COALESCE(title_map.title, '')) LIKE :contains_like
          OR LOWER(COALESCE(creator_map.creators, '')) LIKE :contains_like
          OR LOWER(COALESCE(items.key, '')) LIKE :contains_like
      )
    ORDER BY items.dateModified DESC
    LIMIT :limit
    """
    contains_like = None if contains is None else f"%{contains.lower()}%"
    rows = connection.execute(
        query,
        {"contains": contains, "contains_like": contains_like, "limit": limit},
    ).fetchall()
    return [dict(row) for row in rows]


def fetch_library_summary(connection: sqlite3.Connection) -> dict[str, int]:
    query = """
    SELECT itemTypes.typeName AS item_type, COUNT(*) AS n_items
    FROM items
    JOIN itemTypes ON items.itemTypeID = itemTypes.itemTypeID
    LEFT JOIN deletedItems ON items.itemID = deletedItems.itemID
    WHERE deletedItems.itemID IS NULL
      AND itemTypes.typeName NOT IN ('attachment', 'note', 'annotation')
    GROUP BY itemTypes.typeName
    ORDER BY n_items DESC, itemTypes.typeName ASC
    """
    rows = connection.execute(query).fetchall()
    return {row["item_type"]: row["n_items"] for row in rows}


def print_items(items: Iterable[dict[str, str | int | None]]) -> None:
    for item in items:
        title = item.get("title") or "<no title>"
        creators = item.get("creators") or "<no creators>"
        year = item.get("year") or "<no year>"
        key = item.get("key") or "<no key>"
        item_type = item.get("item_type") or "<no type>"
        print(f"[{item_type}] {key} | {year} | {creators} | {title}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Read a local Zotero SQLite library in read-only mode.")
    parser.add_argument("--db-path", help="Explicit path to zotero.sqlite")
    parser.add_argument("--contains", help="Case-insensitive search over title, creators, and key")
    parser.add_argument("--limit", type=int, default=10, help="Maximum number of items to print/export")
    parser.add_argument("--export-json", help="Optional output path for JSON export")
    parser.add_argument("--test", action="store_true", help="Print summary statistics and sample items")
    args = parser.parse_args()

    try:
        db_path = resolve_db_path(args.db_path)
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    with connect_read_only(db_path) as connection:
        items = fetch_items(connection, args.contains, args.limit)
        summary = fetch_library_summary(connection)

    print(f"Zotero DB: {db_path}")
    print(f"Library item types: {len(summary)}")
    if args.test:
        total_items = sum(summary.values())
        print(f"Total non-attachment items: {total_items}")
        for item_type, count in list(summary.items())[:10]:
            print(f"  - {item_type}: {count}")
        print_items(items)
    else:
        print_items(items)

    if args.export_json:
        output_path = Path(args.export_json)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "db_path": str(db_path),
            "summary": summary,
            "items": items,
        }
        output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Exported JSON: {output_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
