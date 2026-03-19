import asyncio
import json
import tempfile
import unittest
from pathlib import Path

from memory_master import MemoryMaster
from workflow_engine import (
    WorkflowEngine,
    WorkflowNode,
    WorkflowPipeline,
    WorkflowRunStore,
    build_memory_registry,
)


class AdapterPersistenceTest(unittest.TestCase):
    def test_build_memory_registry_exposes_actions(self):
        with tempfile.TemporaryDirectory() as tmp:
            mm = MemoryMaster(tmp)
            registry = build_memory_registry(mm)
            names = registry.names()
            self.assertIn("write", names)
            self.assertIn("search", names)
            self.assertIn("status", names)

    def test_pipeline_persistence_writes_run_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            mm = MemoryMaster(tmp)
            registry = build_memory_registry(mm)
            store = WorkflowRunStore(Path(tmp) / "workflow-runs")

            pipeline = (
                WorkflowPipeline("persist-demo", "persist demo")
                .add_node(WorkflowNode("write", "write", inputs={"content": "LEARNED: persistence matters"}, outputs=["file"]))
                .add_node(WorkflowNode("index", "index", outputs=["indexed_chunks"]))
                .add_edge("write", "index")
            )

            result = asyncio.run(WorkflowEngine(registry.as_dict(), run_store=store).execute(pipeline))
            self.assertIn("index", result)

            run_file = Path(tmp) / "workflow-runs" / "persist-demo.json"
            self.assertTrue(run_file.exists())
            payload = json.loads(run_file.read_text(encoding="utf-8"))
            self.assertEqual(payload["event"], "completed")
            self.assertEqual(payload["pipeline"]["pipeline_id"], "persist-demo")


if __name__ == "__main__":
    unittest.main()
