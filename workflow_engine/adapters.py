"""Adapters for exposing MemoryMaster actions to the workflow engine."""

from __future__ import annotations

from typing import Dict

from memory_master import MemoryMaster
from .registry import ActionRegistry


def build_memory_registry(mm: MemoryMaster) -> ActionRegistry:
    registry = ActionRegistry()
    registry.register_many(
        {
            "write": lambda content, metadata=None: mm.write_daily(content, metadata=metadata),
            "consolidate": lambda dry_run=False: mm.consolidate(dry_run=dry_run),
            "archive": lambda days=7: mm.archive(days=days),
            "index": lambda: mm.build_index(),
            "search": lambda query, limit=5: mm.search(query=query, limit=limit),
            "status": lambda: mm.status(),
        }
    )
    return registry


def export_memory_actions(mm: MemoryMaster) -> Dict[str, object]:
    return build_memory_registry(mm).as_dict()
