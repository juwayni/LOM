import unittest
from lom_framework.core.parser import parse_lom

class TestParser(unittest.TestCase):
    def test_basic_block(self):
        doc = "--- TEST: T1 ---\nK1: V1\n---"
        blocks = parse_lom(doc)
        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0].type, "TEST")
        self.assertEqual(blocks[0].id, "T1")
        self.assertEqual(blocks[0].fields["K1"], "V1")

    def test_multi_blocks(self):
        doc = """
--- B1: ID1 ---
F1: V1
---
--- B2: ID2 ---
F2: V2
"""
        blocks = parse_lom(doc)
        self.assertEqual(len(blocks), 2)
        self.assertEqual(blocks[1].fields["F2"], "V2")

if __name__ == '__main__':
    unittest.main()
