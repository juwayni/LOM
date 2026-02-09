from dataclasses import dataclass
from enum import Enum, auto

class IntervalRelation(Enum):
    BEFORE = auto()
    MEETS = auto()
    OVERLAPS = auto()
    STARTS = auto()
    DURING = auto()
    FINISHES = auto()
    EQUAL = auto()

@dataclass(frozen=True)
class TimeInterval:
    start: float
    end: float

    def __post_init__(self):
        if self.start > self.end:
            raise ValueError("Start must be <= End")

    def relation_to(self, other: 'TimeInterval') -> IntervalRelation:
        s1, e1 = self.start, self.end
        s2, e2 = other.start, other.end

        if e1 < s2: return IntervalRelation.BEFORE
        if e1 == s2: return IntervalRelation.MEETS
        if s1 < s2 and e1 > s2 and e1 < e2: return IntervalRelation.OVERLAPS
        if s1 == s2 and e1 < e2: return IntervalRelation.STARTS
        if s1 > s2 and e1 < e2: return IntervalRelation.DURING
        if s1 > s2 and e1 == e2: return IntervalRelation.FINISHES
        if s1 == s2 and e1 == e2: return IntervalRelation.EQUAL
        # Add inverse relations if needed, but this covers the basics
        return None

class TemporalConsistencyChecker:
    def __init__(self):
        self.intervals = {}

    def add_interval(self, node_id: str, start: float, end: float):
        self.intervals[node_id] = TimeInterval(start, end)

    def check_precedence(self, before_id: str, after_id: str) -> bool:
        if before_id not in self.intervals or after_id not in self.intervals:
            return True
        i1 = self.intervals[before_id]
        i2 = self.intervals[after_id]
        return i1.start <= i2.start
