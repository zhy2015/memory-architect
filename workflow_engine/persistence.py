"""Simple JSON persistence for workflow runs."""

from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, Any


def _json_default(value):
    if hasattr(value, "value"):
        return value.value
    raise TypeError(f"Object of type {type(value).__name__} is not JSON serializable")


class WorkflowRunStore:
    def __init__(self, root: str | Path):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def save_pipeline_state(self, pipeline, *, event: str, extra: Dict[str, Any] | None = None) -> Path:
        payload = {
            "event": event,
            "saved_at": datetime.now().isoformat(),
            "pipeline": {
                "pipeline_id": pipeline.pipeline_id,
                "name": pipeline.name,
                "nodes": {nid: asdict(node) for nid, node in pipeline.nodes.items()},
                "edges": pipeline.edges,
            },
            "extra": extra or {},
        }
        path = self.root / f"{pipeline.pipeline_id}.json"
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, default=_json_default), encoding="utf-8")
        return path

    def load_pipeline_state(self, pipeline_id: str) -> Dict[str, Any]:
        path = self.root / f"{pipeline_id}.json"
        return json.loads(path.read_text(encoding="utf-8"))
