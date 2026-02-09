import re
import sys
from enum import IntEnum
from dataclasses import dataclass
from typing import List, Dict, Set, Optional, Any

class Reliability(IntEnum):
    UNRELIABLE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class EvidenceStrength(IntEnum):
    GRADED = 0
    GRADEC = 1
    GRADEB = 2
    GRADEA = 3

class Consensus(IntEnum):
    DISPUTED = 0
    MINORITY = 1
    MAJORITY = 2
    UNIVERSAL = 3

@dataclass(frozen=True)
class UncertaintyVector:
    reliability: Reliability
    evidence: EvidenceStrength
    consensus: Consensus

    def __lt__(self, other):
        return (self.reliability < other.reliability or
                self.evidence < other.evidence or
                self.consensus < other.consensus)

    @classmethod
    def min(cls, vectors: List['UncertaintyVector']):
        if not vectors:
            return UncertaintyVector(Reliability.UNRELIABLE, EvidenceStrength.GRADED, Consensus.DISPUTED)
        return UncertaintyVector(
            reliability=Reliability(min(v.reliability for v in vectors)),
            evidence=EvidenceStrength(min(v.evidence for v in vectors)),
            consensus=Consensus(min(v.consensus for v in vectors))
        )

    def __str__(self):
        return f"{self.reliability.name}|{self.evidence.name}|{self.consensus.name}"

class LoMEngine:
    def __init__(self):
        self.blocks = {}
        self.graph = {} # ID -> List of supporting IDs
        self.uncertainty_cache = {}
        self.errors = []
        self.warnings = []
        self.forbidden_nodes = set()

    def parse_uncertainty(self, s: str) -> UncertaintyVector:
        try:
            parts = s.split('|')
            return UncertaintyVector(
                reliability=Reliability[parts[0].strip().upper()],
                evidence=EvidenceStrength[parts[1].strip().upper()],
                consensus=Consensus[parts[2].strip().upper()]
            )
        except (KeyError, IndexError, AttributeError):
            return UncertaintyVector(Reliability.LOW, EvidenceStrength.GRADED, Consensus.DISPUTED)

    def load_document(self, content: str):
        parts = re.split(r'--- (.*?): (.*?) ---', content)
        for i in range(1, len(parts), 3):
            b_type = parts[i].strip()
            b_id = parts[i+1].strip()
            b_content = parts[i+2].strip()

            fields = {}
            for line in b_content.split('\n'):
                line = line.strip()
                if not line or line == '---': continue
                if ':' in line:
                    k, v = line.split(':', 1)
                    fields[k.strip()] = v.strip().strip('"')

            self.blocks[b_id] = {'type': b_type, 'id': b_id, 'fields': fields}

            supports = [s.strip() for s in fields.get('Supports', '').split(',') if s.strip()]
            self.graph[b_id] = supports

    def check_cycles(self):
        visited = set()
        path = set()

        def visit(u):
            if u in path: return True
            if u in visited: return False
            visited.add(u)
            path.add(u)
            for v in self.graph.get(u, []):
                if v in self.blocks and visit(v): return True
            path.remove(u)
            return False

        for node in self.graph:
            if visit(node):
                self.errors.append(f"Circular reasoning detected in node {node}")
                return True
        return False

    def get_uncertainty(self, b_id: str) -> UncertaintyVector:
        if b_id in self.uncertainty_cache:
            return self.uncertainty_cache[b_id]

        block = self.blocks.get(b_id)
        if not block:
            return UncertaintyVector(Reliability.UNRELIABLE, EvidenceStrength.GRADED, Consensus.DISPUTED)

        fields = block['fields']

        if 'EpistemicState' in fields:
            uv = self.parse_uncertainty(fields['EpistemicState'])
        elif block['type'] in ['OBSERVATION', 'MEASUREMENT', 'PATIENT CONTEXT', 'BIOMARKER']:
            uv = UncertaintyVector(Reliability.HIGH, EvidenceStrength.GRADEA, Consensus.UNIVERSAL)
        else:
            supporting_ids = self.graph.get(b_id, [])
            if not supporting_ids:
                uv = UncertaintyVector(Reliability.LOW, EvidenceStrength.GRADED, Consensus.DISPUTED)
            else:
                premise_uvs = [self.get_uncertainty(s) for s in supporting_ids]
                just_id = fields.get('Justification')
                if just_id and just_id in self.blocks:
                    just_uv = self.parse_uncertainty(self.blocks[just_id]['fields'].get('Strength', 'High|GradeA|Universal'))
                    premise_uvs.append(just_uv)
                uv = UncertaintyVector.min(premise_uvs)

        self.uncertainty_cache[b_id] = uv
        return uv

    def evaluate_constraints(self):
        for c_id, c_block in self.blocks.items():
            if c_block['type'] == 'CONSTRAINT':
                rule = c_block['fields'].get('Rule', '')
                target = c_block['fields'].get('Target', '').lower()

                triggered = False
                for b_id, b_block in self.blocks.items():
                    if b_block['type'] == 'PATIENT CONTEXT':
                        for k, v in b_block['fields'].items():
                            if rule.lower() in f"{k}: {v}".lower():
                                triggered = True
                                break

                if triggered:
                    for b_id, b_block in self.blocks.items():
                        claim = b_block['fields'].get('Claim', '').lower()
                        if target in claim or target == b_id.lower():
                            self.forbidden_nodes.add(b_id)
                            self.errors.append(f"SAFETY VIOLATION: {b_id} is FORBIDDEN by {c_id} ('{target}' matches '{rule}')")

    def check_temporal_consistency(self):
        for b_id, supports in self.graph.items():
            b_block = self.blocks.get(b_id)
            if not b_block: continue
            b_ts = b_block['fields'].get('Timestamp')
            if not b_ts: continue

            for s_id in supports:
                s_block = self.blocks.get(s_id)
                if not s_block: continue
                s_ts = s_block['fields'].get('Timestamp')
                if s_ts and s_ts > b_ts:
                    self.warnings.append(f"TEMPORAL ANOMALY: {b_id} (T={b_ts}) depends on future event {s_id} (T={s_ts})")

    def run_inference(self):
        print("LoM Reasoning Engine v2.0 Execution")
        print("Disclaimer: Educational / Analytical / Non-clinical\n")

        if self.check_cycles(): return
        self.evaluate_constraints()
        self.check_temporal_consistency()

        for b_id, block in self.blocks.items():
            if block['type'] == 'ASSERTION':
                if b_id in self.forbidden_nodes:
                    print(f"[ASSERTION] {b_id}: FORBIDDEN (Safety Constraint)")
                    continue

                uv = self.get_uncertainty(b_id)
                claim = block['fields'].get('Claim', 'Unknown')
                print(f"[ASSERTION] {b_id}: {claim}")
                print(f"  Uncertainty: {uv}")

                if uv.reliability < Reliability.MEDIUM:
                    self.warnings.append(f"{b_id}: Assertion relies on unreliable data.")
                if uv.evidence < EvidenceStrength.GRADEB:
                    self.warnings.append(f"{b_id}: Weak evidence strength for claim.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python engine/lom_engine.py <file.lom>")
        sys.exit(1)

    try:
        with open(sys.argv[1], 'r') as f:
            content = f.read()

        engine = LoMEngine()
        engine.load_document(content)
        engine.run_inference()

        if engine.errors:
            print("\nERRORS:")
            for e in engine.errors:
                print(f"  - {e}")

        if engine.warnings:
            print("\nWARNINGS:")
            for w in engine.warnings:
                print(f"  - {w}")
    except Exception as e:
        print(f"Engine Failure: {e}")
        sys.exit(1)
