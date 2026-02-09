from typing import List, Dict, Optional, Any, Set
from lom_framework.core.parser import BlockNode
from lom_framework.logic.uncertainty import UncertaintyVector, parse_uv
from lom_framework.logic.temporal import TemporalConsistencyChecker

class InferenceEngine:
    def __init__(self, blocks: List[BlockNode]):
        self.blocks = {b.id: b for b in blocks}
        self.uncertainty_cache: Dict[str, UncertaintyVector] = {}
        self.temporal_checker = TemporalConsistencyChecker()
        self.errors = []
        self.warnings = []
        self.forbidden_nodes = set()

        # Initialize temporal checker
        for b_id, block in self.blocks.items():
            ts = block.fields.get('Timestamp')
            if ts and ts.isdigit():
                self.temporal_checker.add_interval(b_id, float(ts), float(ts))

    def get_block(self, block_id: str) -> Optional[BlockNode]:
        return self.blocks.get(block_id)

    def get_supports(self, block_id: str) -> List[str]:
        block = self.get_block(block_id)
        if not block: return []
        supports = block.fields.get('Supports', '')
        if not supports: return []
        return [s.strip() for s in supports.split(',') if s.strip()]

    def check_cycles(self):
        visited = set()
        path = set()

        def visit(u):
            if u in path: return True
            if u in visited: return False
            visited.add(u)
            path.add(u)
            for v in self.get_supports(u):
                if visit(v): return True
            path.remove(u)
            return False

        for node in self.blocks:
            if visit(node):
                self.errors.append(f"Reasoning cycle detected at {node}")
                return True
        return False

    def get_uncertainty(self, block_id: str) -> UncertaintyVector:
        if block_id in self.uncertainty_cache:
            return self.uncertainty_cache[block_id]

        block = self.get_block(block_id)
        if not block:
            return UncertaintyVector.min_merge([]) # Conservative default

        # Base case: explicitly declared state
        if 'EpistemicState' in block.fields:
            uv = parse_uv(block.fields['EpistemicState'])
        elif block.type in ['OBSERVATION', 'MEASUREMENT', 'PATIENT CONTEXT']:
            uv = UncertaintyVector.min_merge([]) # Should be high, but let's be conservative if not declared
            # In v2.2, we assume undeclared empirical data is HIGH reliability if no reason to doubt
            uv = parse_uv("High|GradeA|Universal")
        else:
            # Recursive case
            supports = self.get_supports(block_id)
            premise_uvs = [self.get_uncertainty(s) for s in supports]

            # Factor in Justification
            just_id = block.fields.get('Justification')
            if just_id:
                just_block = self.get_block(just_id)
                if just_block:
                    just_uv = parse_uv(just_block.fields.get('Strength', 'High|GradeA|Universal'))
                    premise_uvs.append(just_uv)

            uv = UncertaintyVector.min_merge(premise_uvs)

        self.uncertainty_cache[block_id] = uv
        return uv

    def evaluate_constraints(self):
        for c_id, c_block in self.blocks.items():
            if c_block.type == 'CONSTRAINT':
                rule = c_block.fields.get('Rule', '')
                target = c_block.fields.get('Target', '').lower()

                triggered = False
                for b_id, b_block in self.blocks.items():
                    if b_block.type == 'PATIENT CONTEXT':
                        for k, v in b_block.fields.items():
                            if rule.lower() in f"{k}: {v}".lower():
                                triggered = True
                                break

                if triggered:
                    for b_id, b_block in self.blocks.items():
                        claim = (b_block.fields.get('Claim') or b_block.fields.get('Description') or b_id).lower()
                        if target in claim or target == b_id.lower():
                            self.forbidden_nodes.add(b_id)
                            self.errors.append(f"SAFETY VIOLATION: {b_id} is FORBIDDEN by {c_id} ('{target}' matches '{rule}')")

    def evaluate(self):
        if self.check_cycles():
            return

        self.evaluate_constraints()

        for b_id, block in self.blocks.items():
            # Check supports existence
            for s_id in self.get_supports(b_id):
                if s_id not in self.blocks:
                    self.errors.append(f"Block {b_id} references non-existent support {s_id}")
                else:
                    # Temporal consistency check
                    if not self.temporal_checker.check_precedence(s_id, b_id):
                        self.warnings.append(f"TEMPORAL ANOMALY: {b_id} depends on future event {s_id}")

            # Propagate uncertainty
            if block.type == 'ASSERTION':
                uv = self.get_uncertainty(b_id)
                # Logic for flagging weak assertions
                from lom_framework.logic.uncertainty import Reliability
                if uv.reliability < Reliability.MEDIUM:
                    self.warnings.append(f"LOW RELIABILITY: Assertion {b_id} depends on unreliable sources.")

    def run(self):
        self.evaluate()
        print("LoM Framework Engine v2.2 Execution")
        print("Disclaimer: Educational / Analytical / Non-clinical\n")

        if self.errors:
            print("Engine Errors:")
            for e in self.errors: print(f"  - {e}")

        if self.warnings:
            print("\nEngine Warnings:")
            for w in self.warnings: print(f"  - {w}")

        if not self.errors:
            print("\nEngine successfully evaluated reasoning graph.")
