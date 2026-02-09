# LoM Language Reference Manual (v2.1)

## 1. Introduction
The Language of Medicine (LoM) is a formal, block-based declarative language for representing clinical reasoning. It is designed to be human-readable, machine-executable, and safely constrained.

## 2. Syntax and Grammar
LoM documents consist of multiple **Blocks**. Each block starts with a header and contains field-value pairs.

### 2.1 Block Structure
```
--- TYPE: ID ---
Field: Value
---
```

### 2.2 Core Block Types
- **PATIENT CONTEXT**: Defines the patient state.
- **OBSERVATION**: Qualitative findings.
- **MEASUREMENT**: Quantitative findings with units and ranges.
- **ASSERTION**: Reasoned claims.
- **JUSTIFICATION**: Evidence sources (RCTs, Guidelines).
- **CONSTRAINT**: Safety barriers.
- **PHYSIOLOGICAL PROCESS**: Biological mechanisms.

## 3. Epistemic Model
LoM uses a multi-dimensional uncertainty vector:
- **Reliability**: Data source quality.
- **Evidence Strength**: GRADE-based evidence quality.
- **Consensus**: Degree of clinical agreement.

## 4. Reasoning Logic
Reasoning in LoM is a **Justified Knowledge Graph**.
- Nodes are linked via `Supports` and `Contradicts` relations.
- Inferred assertions must have at least one supporting node and a valid justification.
- Safety constraints act as high-priority filters that can invalidate reasoning paths.

## 5. Temporal Reasoning
LoM implements Allen's Interval Algebra.
- Events can have timestamps or intervals.
- The engine checks for temporal causality (evidence must precede conclusion).
