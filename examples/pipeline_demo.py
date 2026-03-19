#!/usr/bin/env python3
"""Demo pipeline: write -> consolidate -> index -> search -> status."""

from __future__ import annotations

import asyncio
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from memory_master import MemoryMaster
from workflow_engine import (
    WorkflowEngine,
    WorkflowNode,
    WorkflowPipeline,
    WorkflowRunStore,
    build_memory_registry,
)


async def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        workspace = Path(tmp)
        mm = MemoryMaster(workspace)
        registry = build_memory_registry(mm)
        run_store = WorkflowRunStore(workspace / "workflow-runs")

        pipeline = (
            WorkflowPipeline("memory-demo", "memory demo")
            .add_node(WorkflowNode("write_log", "write", inputs={"content": "LEARNED: workflow demos make adoption easier"}, outputs=["file"]))
            .add_node(WorkflowNode("consolidate", "consolidate", outputs=["insights_merged"]))
            .add_node(WorkflowNode("index", "index", outputs=["indexed_chunks"]))
            .add_node(WorkflowNode("search", "search", inputs={"query": "workflow demos", "limit": "3"}, outputs=["results"]))
            .add_node(WorkflowNode("status", "status", outputs=["status"]))
            .add_edge("write_log", "consolidate")
            .add_edge("consolidate", "index")
            .add_edge("index", "search")
            .add_edge("search", "status")
        )

        result = await WorkflowEngine(registry.as_dict(), run_store=run_store).execute(pipeline)
        print(json.dumps({"result": result, "run_state": run_store.load_pipeline_state("memory-demo")}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())
