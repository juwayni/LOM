# The Language of Medicine (LoM) Framework v2.2

**A formal, human-centered, executable representation system for medical knowledge and reasoning.**

> **DISCLAIMER**: LoM is **not** a clinical decision system. It is **not** autonomous. It is **not** for real patient care. All outputs are **Educational / Analytical / Non-clinical**.

## 1. Core Purpose
LoM is designed to make medical reasoning **explicit, verifiable, auditable, and safely constrained**. It provides a formal logic system for clinical reasoning, suitable for academic research and LLM integration.

## 2. Advanced Philosophy
- **Lattice-based Uncertainty**: Reliability, Evidence Strength, and Consensus.
- **Allen's Interval Algebra**: Formal temporal reasoning.
- **Conservative Defaults**: Uncertainty and safety constraints block unsafe inferences.
- **Justified Knowledge Graphs**: Every assertion requires a formal justification.

## 3. Repository Structure
- `lom_framework/`: The core framework.
  - `core/`: Lexer and Parser.
  - `logic/`: Inference engine, temporal logic, and uncertainty models.
  - `clinical/`: Clinical types and unit management.
  - `stdlib/`: Standard medical knowledge modules.
- `docs/`: Comprehensive technical documentation.
  - `language_reference.md`: Formal grammar and syntax.
  - `clinical_logic_monograph.md`: Theoretical foundations.
  - `informatics_rationale.md`: Grounding in EBM and standards.
- `examples/`: High-fidelity clinical simulations.
- `tests/`: Extensive unit test suite.

## 4. Getting Started

### 4.1 Running a Simulation
```bash
PYTHONPATH=. python3 lom_runner.py examples/sepsis_multi_system.lom
```

### 4.2 Running Tests
```bash
PYTHONPATH=. python3 -m unittest discover tests
```

## 5. Safety and Ethics
LoM enforces safety through explicit uncertainty propagation and high-priority safety barriers (Constraints). The framework is designed to assist human judgment, never to replace it.
