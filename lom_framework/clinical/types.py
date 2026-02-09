from dataclasses import dataclass
from typing import Optional, Dict

@dataclass
class ReferenceRange:
    low: float
    high: float
    unit: str

    def is_normal(self, value: float) -> bool:
        return self.low <= value <= self.high

class UnitConverter:
    @staticmethod
    def to_celsius(value: float, from_unit: str) -> float:
        if from_unit.lower() in ['c', 'celsius']: return value
        if from_unit.lower() in ['f', 'fahrenheit']: return (value - 32) * 5/9
        return value

class MeasurementEvaluator:
    def __init__(self):
        # Default ranges for a healthy adult
        self.standards = {
            "Heart Rate": ReferenceRange(60, 100, "bpm"),
            "Temperature": ReferenceRange(36.1, 37.2, "Celsius"),
            "MAP": ReferenceRange(70, 100, "mmHg")
        }

    def evaluate(self, label: str, value: float, unit: str) -> str:
        if label not in self.standards:
            return "UNKNOWN_RANGE"

        std = self.standards[label]
        # Basic conversion if needed
        if label == "Temperature":
            value = UnitConverter.to_celsius(value, unit)

        if std.is_normal(value):
            return "NORMAL"
        return "ABNORMAL"
