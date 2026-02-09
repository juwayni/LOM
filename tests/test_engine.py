import unittest
from lom_framework.core.parser import parse_lom
from lom_framework.logic.engine import InferenceEngine
from lom_framework.logic.uncertainty import parse_uv, Reliability, EvidenceStrength, Consensus

class TestEngine(unittest.TestCase):
    def test_cycle_detection(self):
        doc = """
--- ASSERTION: A1 ---
Supports: A2
--- ASSERTION: A2 ---
Supports: A1
"""
        blocks = parse_lom(doc)
        engine = InferenceEngine(blocks)
        self.assertTrue(engine.check_cycles())

    def test_uncertainty_propagation(self):
        doc = """
--- OBSERVATION: O1 ---
EpistemicState: Low|GradeC|Disputed
--- ASSERTION: A1 ---
Supports: O1
"""
        blocks = parse_lom(doc)
        engine = InferenceEngine(blocks)
        uv = engine.get_uncertainty("A1")
        self.assertEqual(uv.reliability, Reliability.LOW)
        self.assertEqual(uv.consensus, Consensus.DISPUTED)

    def test_safety_constraint(self):
        doc = """
--- PATIENT CONTEXT: PC1 ---
Condition: Pregnancy
--- CONSTRAINT: C1 ---
Rule: Pregnancy
Target: Ibuprofen
--- ASSERTION: A1 ---
Claim: Use Ibuprofen
"""
        blocks = parse_lom(doc)
        engine = InferenceEngine(blocks)
        engine.evaluate()
        self.assertIn("A1", engine.forbidden_nodes)
        self.assertTrue(any("SAFETY VIOLATION" in e for e in engine.errors))

    def test_temporal_check(self):
        doc = """
--- ASSERTION: A1 ---
Timestamp: 100
Supports: A2
--- ASSERTION: A2 ---
Timestamp: 200
"""
        blocks = parse_lom(doc)
        engine = InferenceEngine(blocks)
        engine.evaluate()
        self.assertTrue(any("TEMPORAL ANOMALY" in w for w in engine.warnings))

if __name__ == '__main__':
    unittest.main()
