# The Language of Medicine (LoM)

**A formal, human-centered, executable representation system for medical knowledge, reasoning, and education.**

> **DISCLAIMER**: LoM is **not** a clinical decision system. It is **not** autonomous. It is **not** for real patient care. All outputs are **Educational / Analytical / Non-clinical**.

## 1. Core Purpose
LoM is designed to make medical reasoning **explicit, verifiable, auditable, teachable, and safely constrained**. It bridges the gap between natural language clinical notes and formal logical systems, specifically optimized for LLM integration and reproducible reasoning.

## 2. Fundamental Philosophy
- **Reasoning under Uncertainty**: Medicine relies on incomplete evidence. LoM exposes reasoning instead of hiding it.
- **Explicit Epistemic Status**: Every assertion must declare its status (e.g., `observed`, `hypothesized`, `inferred`).
- **Traceability**: Every claim must link to its evidence (Supports) and its authority (Justification).

## 3. Repository Structure
- `docs/`: Comprehensive documentation.
  - `ontology.md`: Core primitives and epistemic states.
  - `specification.md`: Formal grammar and semantics.
  - `validation_safety.md`: Rules for logical consistency and safety guarantees.
  - `failure_cases.md`: Examples of invalid reasoning.
  - `rationale.md`: Design decisions and philosophy.
- `examples/`: Domain-specific examples of LoM documents.
  - `cardiology_differential.lom`: Differential reasoning for chest pain.
  - `lab_uncertainty.lom`: Handling measurement error and uncertainty propagation.
  - `guideline_safety.lom`: Enforcement of clinical safety constraints.
- `validator/`: Reference implementation.
  - `lom_validator.py`: A Python tool to parse and validate LoM reasoning graphs.

## 4. Getting Started

### 4.1 Running the Validator
To validate a LoM document and check its reasoning consistency:

```bash
python validator/lom_validator.py examples/cardiology_differential.lom
```

### 4.2 LoM Syntax Example
```
--- PATIENT CONTEXT: PC_01 ---
Age: 45
Sex: Female

--- MEASUREMENT: MEAS_01 ---
Label: "Troponin"
Value: 0.5
Unit: "ng/mL"
Range: 0.0-0.04
Status: observed
Uncertainty: "+/- 0.01"

--- ASSERTION: AS_01 ---
Claim: "Elevated Troponin"
Status: inferred
Supports: MEAS_01
Justification: J_LAB_REF

--- JUSTIFICATION: J_LAB_REF ---
Source: "Hospital Lab Standards"
```

## 5. Non-Goals
LoM is **NOT**:
- Optimized for performance or real-time monitoring.
- A replacement for clinical judgment.
- A system to provide treatment plans or autonomous diagnoses.
- A comprehensive database of all medical knowledge.

## 6. Safety and Ethics
LoM enforces safety through:
1. **Explicit Uncertainty**: Prevents the "collapse" of doubt into false certainty.
2. **Safety Constraints**: Active blocking of reasoning paths that violate clinical safety rules.
3. **Human-in-the-Loop**: Execution is limited to evaluating logical consistency; the final interpretation always belongs to the human expert.
