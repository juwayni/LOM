# LoM Failure Cases and Invalid Reasoning

This document describes scenarios where the LoM validator will flag reasoning as invalid or unsafe.

## 1. Logical Contradictions

If an assertion is supported and contradicted by the same piece of evidence, or if it has strong contradicting evidence without a resolution justification.

### Example
```
--- ASSERTION: AS_01 ---
Claim: "Condition X"
Status: inferred
Supports: OBS_01
Contradicts: OBS_01  <-- ERROR: Direct contradiction
```

## 2. Circular Reasoning

LoM reasoning must be a Directed Acyclic Graph. Loops indicate a logical flaw where assertions justify themselves.

### Example
```
--- ASSERTION: AS_01 ---
Supports: AS_02

--- ASSERTION: AS_02 ---
Supports: AS_01  <-- ERROR: Circular dependency
```

## 3. Safety Constraint Violations

When a clinical constraint (e.g., contraindication) is active but the reasoning path ignores it.

### Example
```
--- PATIENT CONTEXT: PC_01 ---
Pregnancy: confirmed

--- CONSTRAINT: CON_01 ---
Rule: "Pregnancy: confirmed"
Target: "Ibuprofen"

--- ASSERTION: AS_01 ---
Claim: "Prescribe Ibuprofen" <-- ERROR: Safety Violation
```

## 4. Epistemic Status Mismatch (Unsafe Certainty)

LoM rejects "collapsing" uncertainty. A conclusion cannot be more certain than its weakest premise.

### Example
```
--- OBSERVATION: OBS_01 ---
Status: hypothesized

--- ASSERTION: AS_01 ---
Status: inferred
Supports: OBS_01 <-- ERROR/WARN: Cannot infer from a hypothesis without upgrade justification.
```

## 5. Missing Provenance (Auditability Failure)

Any claim without a justification is a failure of the "Explicitness" philosophy.

### Example
```
--- ASSERTION: AS_01 ---
Claim: "Rare Disease Y"
Status: inferred
Supports: OBS_01
<-- ERROR: Missing Justification
```
