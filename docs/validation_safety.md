# LoM Validation and Safety Framework

## 1. Validation Rules

To ensure medical reasoning is explicit and verifiable, LoM documents must pass the following validation checks.

### 1.1 Logical Consistency
- **Justification Integrity**: Every `Observation`, `Measurement`, and `Assertion` must have an associated `Justification` or be marked as `unknowable`.
- **Evidence Traceability**: An assertion with status `inferred` must list at least one existing block ID in its `Supports` field.
- **Circular Reasoning Detection**: Reasoning chains must be a Directed Acyclic Graph (DAG). Loops are forbidden.
- **Reference Range Validation**: Measurements with values outside the defined `Range` must be flagged as "Abnormal".

### 1.2 Epistemic State Rules
- An assertion cannot have status `observed` (unless it's an observation/measurement).
- If any supporting evidence for an assertion has a status of `hypothesized` or `unresolved`, the assertion itself cannot have a status higher than `hypothesized` or `unresolved`.

### 1.3 Contradiction Handling
- If a block ID is listed in both `Supports` and `Contradicts` for the same assertion, a validation error is raised.
- If an assertion has both `Supports` and `Contradicts` evidence, it must be flagged for manual review and cannot be marked as `inferred` without a specific justification explaining the resolution of the conflict.

## 2. Uncertainty Propagation

Uncertainty is not just a label; it must affect the reasoning graph.

- **Mandatory Declaration**: If a measurement is provided without an `Uncertainty` field, it is flagged as "Incomplete Data".
- **Propagation**: If a premise is `uncertain`, any conclusion derived from it must also be `uncertain`.
- **Unknowable Propagation**: If a critical piece of information is `unknowable`, dependent assertions must be marked `unresolved`.

## 3. Safety and Ethical Guarantees

LoM is designed with "Conservative Defaults" to prevent unsafe medical reasoning.

### 3.1 Explicit Non-Conclusion
- If the reasoning chain for a dangerous condition (e.g., "Acute MI") contains any `unresolved` or `contradicted` nodes, the final assertion MUST NOT be "confirmed". It must remain `hypothesized` or `unresolved`.
- **The "No Guessing" Rule**: If data is missing for a critical exclusion criteria, the reasoning path is blocked.

### 3.2 Human-in-the-Loop Requirement
- LoM execution identifies inconsistencies but **never** provides a recommendation for action.
- Every output from a LoM validator must include the disclaimer:
  > **Educational / Analytical / Non-clinical: This output is for reasoning analysis only and must not be used for patient care.**

### 3.3 Contraindication Enforcement
- `Constraint` blocks are evaluated with highest priority. If a constraint is triggered (e.g., "Patient is child, exclude Aspirin"), any assertion or reasoning path violating that constraint is marked as `forbidden`.

## 4. Execution Model Safety
- The "Execution" of LoM is limited to evaluating the logical graph.
- It will identify:
  - Missing premises.
  - Logical contradictions.
  - Unsafe inferences.
  - Violation of clinical guidelines (constraints).
