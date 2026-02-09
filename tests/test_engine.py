import unittest
from engine.lom_engine import LoMEngine, Reliability, EvidenceStrength, Consensus, UncertaintyVector

class TestLoMEngine(unittest.TestCase):
    def setUp(self):
        self.engine = LoMEngine()

    def test_uncertainty_lattice_min(self):
        v1 = UncertaintyVector(Reliability.HIGH, EvidenceStrength.GRADEA, Consensus.UNIVERSAL)
        v2 = UncertaintyVector(Reliability.MEDIUM, EvidenceStrength.GRADEB, Consensus.MAJORITY)
        v3 = UncertaintyVector(Reliability.LOW, EvidenceStrength.GRADEA, Consensus.UNIVERSAL)

        result = UncertaintyVector.min([v1, v2, v3])
        self.assertEqual(result.reliability, Reliability.LOW)
        self.assertEqual(result.evidence, EvidenceStrength.GRADEB)
        self.assertEqual(result.consensus, Consensus.MAJORITY)

    def test_cycle_detection(self):
        content = """
--- ASSERTION: A1 ---
Supports: A2
--- ASSERTION: A2 ---
Supports: A1
"""
        self.engine.load_document(content)
        self.assertTrue(self.engine.check_cycles(), "Should detect cycle A1 -> A2 -> A1")

    def test_safety_constraint(self):
        content = """
--- PATIENT CONTEXT: PC1 ---
Condition: Pregnancy
--- CONSTRAINT: C1 ---
Rule: Condition: Pregnancy
Target: Ibuprofen
--- ASSERTION: A1 ---
Claim: Use Ibuprofen
"""
        self.engine.load_document(content)
        self.engine.evaluate_constraints()
        self.assertIn("A1", self.engine.forbidden_nodes)
        self.assertTrue(any("SAFETY VIOLATION" in e for e in self.engine.errors))

    def test_uncertainty_propagation(self):
        content = """
--- OBSERVATION: O1 ---
EpistemicState: Low|GradeC|Disputed
--- ASSERTION: A1 ---
Supports: O1
Claim: Uncertain Claim
"""
        self.engine.load_document(content)
        uv = self.engine.get_uncertainty("A1")
        self.assertEqual(uv.reliability, Reliability.LOW)
        self.assertEqual(uv.consensus, Consensus.DISPUTED)

    def test_temporal_anomaly(self):
        content = """
--- ASSERTION: A1 ---
Timestamp: 100
Supports: A2
--- ASSERTION: A2 ---
Timestamp: 200
"""
        self.engine.load_document(content)
        self.engine.check_temporal_consistency()
        self.assertTrue(any("TEMPORAL ANOMALY" in w for w in self.engine.warnings))

if __name__ == '__main__':
    unittest.main()
