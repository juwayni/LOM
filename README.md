# The Language of Medicine (LoM)

**A formal, human-centered, executable representation system for medical knowledge, reasoning, and education.**

> **DISCLAIMER**: LoM is **not** a clinical decision system. It is **not** autonomous. It is **not** for real patient care. All outputs are **Educational / Analytical / Non-clinical**.

## 1. Core Purpose
LoM is designed to make medical reasoning **explicit, verifiable, auditable, teachable, and safely constrained**. It bridges the gap between natural language clinical notes and formal logical systems, specifically optimized for LLM integration and reproducible reasoning.

## 2. Advanced Philosophy
- **Reasoning under Uncertainty**: Medicine relies on incomplete evidence. LoM uses a multi-dimensional lattice of Reliability, Evidence Strength, and Consensus.
- **Explicit Epistemic Status**: Every assertion must declare its state.
- **Traceability**: Every claim must link to its evidence (Supports) and its authority (Justification).
- **Temporal Consistency**: Reasoning chains must respect the temporal ordering of events.

## 3. Repository Structure
- `docs/`: Comprehensive documentation.
  - `ontology.md`: Advanced primitives and multi-dimensional epistemic model.
  - `specification.md`: Formal EBNF grammar and predicate logic semantics.
  - `informatics_rationale.md`: Theoretical grounding in EBM, SNOMED CT, and GRADE.
  - `validation_safety.md`: Rules for logical consistency and safety guarantees.
- `examples/`: High-fidelity LoM documents covering complex cases (Sepsis, Polypharmacy).
- `engine/`: The reference reasoning engine.
  - `lom_engine.py`: A Python-based graph inference engine.
- `tests/`: Unit test suite for verifying reasoning logic.

## 4. Getting Started

### 4.1 Running the Engine
To execute a LoM document and evaluate its reasoning graph:

```bash
PYTHONPATH=. python3 engine/lom_engine.py examples/sepsis_multi_system.lom
```

### 4.2 Running Tests
```bash
PYTHONPATH=. python3 tests/test_engine.py
```

## 5. Non-Goals
LoM is **NOT**:
- Optimized for performance or real-time monitoring.
- A replacement for clinical judgment.
- A system to provide treatment plans or autonomous diagnoses.

## 6. Safety and Ethics
LoM enforces safety through:
1. **Explicit Uncertainty Propagation**: Prevents the "collapse" of doubt into false certainty.
2. **Safety Constraints**: Active blocking of reasoning paths that violate clinical safety rules (e.g., contraindications).
3. **Human-in-the-Loop**: The engine identifies logical inconsistencies; the final interpretation remains with the human expert.
