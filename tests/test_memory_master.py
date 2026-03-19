import tempfile
import unittest
from pathlib import Path

from memory_master import MemoryMaster


class MemoryMasterTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.mm = MemoryMaster(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_write_daily_creates_file(self):
        result = self.mm.write_daily("DECISION: keep memory simple")
        self.assertEqual(result["status"], "success")
        files = list((Path(self.tmp.name) / "memory" / "daily").glob("*.md"))
        self.assertEqual(len(files), 1)
        self.assertIn("keep memory simple", files[0].read_text(encoding="utf-8"))

    def test_consolidate_extracts_patterns(self):
        daily = Path(self.tmp.name) / "memory" / "daily" / "2026-03-20.md"
        daily.parent.mkdir(parents=True, exist_ok=True)
        daily.write_text(
            "FAILED: deployment broke\nSUCCESS(cache warmup)\nDECISION: use local index\nLEARNED: keep repo lean\n",
            encoding="utf-8",
        )
        result = self.mm.consolidate()
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["insights_extracted"], 4)
        core = Path(self.tmp.name) / "memory" / "core" / "MEMORY.md"
        text = core.read_text(encoding="utf-8")
        self.assertIn("deployment broke", text)
        self.assertIn("use local index", text)
        self.assertIn("keep repo lean", text)

    def test_index_and_search(self):
        self.mm.write_daily("LEARNED: semantic search helps recall")
        self.mm.build_index()
        result = self.mm.search("semantic search", limit=3)
        self.assertEqual(result["status"], "success")
        self.assertGreaterEqual(len(result["results"]), 1)


if __name__ == "__main__":
    unittest.main()
