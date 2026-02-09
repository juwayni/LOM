from enum import IntEnum
from dataclasses import dataclass
from typing import List

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

    @classmethod
    def min_merge(cls, vectors: List['UncertaintyVector']):
        if not vectors:
            # Conservative Default: Minimum certainty if no evidence provided
            return UncertaintyVector(Reliability.UNRELIABLE, EvidenceStrength.GRADED, Consensus.DISPUTED)
        return UncertaintyVector(
            reliability=Reliability(min(v.reliability for v in vectors)),
            evidence=EvidenceStrength(min(v.evidence for v in vectors)),
            consensus=Consensus(min(v.consensus for v in vectors))
        )

    def __str__(self):
        return f"R:{self.reliability.name} | E:{self.evidence.name} | C:{self.consensus.name}"

def parse_uv(s: str) -> UncertaintyVector:
    try:
        parts = s.split('|')
        return UncertaintyVector(
            reliability=Reliability[parts[0].strip().upper()],
            evidence=EvidenceStrength[parts[1].strip().upper()],
            consensus=Consensus[parts[2].strip().upper()]
        )
    except:
        return UncertaintyVector(Reliability.LOW, EvidenceStrength.GRADED, Consensus.DISPUTED)
