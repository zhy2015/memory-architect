import asyncio
import tempfile
import unittest

from memory_master import MemoryMaster
from workflow_engine import WorkflowEngine, WorkflowNode, WorkflowPipeline, clear_all_contexts


class WorkflowEngineTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.mm = MemoryMaster(self.tmp.name)
        clear_all_contexts()

    def tearDown(self):
        self.tmp.cleanup()

    def test_pipeline_runs_memory_actions(self):
        actions = {
            "write": lambda content: self.mm.write_daily(content),
            "index": lambda: self.mm.build_index(),
            "status": lambda: self.mm.status(),
        }
        pipeline = (
            WorkflowPipeline("memory-flow", "memory flow")
            .add_node(WorkflowNode("write_log", "write", inputs={"content": "LEARNED: pipelines help"}, outputs=["file"]))
            .add_node(WorkflowNode("build_index", "index", outputs=["indexed_chunks"]))
            .add_node(WorkflowNode("status", "status", outputs=["status"]))
            .add_edge("write_log", "build_index")
            .add_edge("build_index", "status")
        )
        result = asyncio.run(WorkflowEngine(actions).execute(pipeline))
        self.assertIn("write_log", result)
        self.assertIn("build_index", result)
        self.assertIn("status", result)


if __name__ == "__main__":
    unittest.main()
