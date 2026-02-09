# LoM Formal Language Specification

## 1. Syntax Overview
LoM uses a block-based, declarative syntax. Each block represents a primitive and is separated by triple-dashes and a header.

### 1.1 Grammar (Human-Readable)

```
Document      ::= Block+
Block         ::= ContextBlock | ObservationBlock | MeasurementBlock | AssertionBlock | ConstraintBlock | JustificationBlock

ContextBlock  ::= "--- PATIENT CONTEXT: " ID " ---" NL FieldMap
ObservationBlock ::= "--- OBSERVATION: " ID " ---" NL FieldMap
MeasurementBlock ::= "--- MEASUREMENT: " ID " ---" NL FieldMap
AssertionBlock   ::= "--- ASSERTION: " ID " ---" NL FieldMap
ConstraintBlock  ::= "--- CONSTRAINT: " ID " ---" NL FieldMap
JustificationBlock ::= "--- JUSTIFICATION: " ID " ---" NL FieldMap

FieldMap      ::= (Key ": " Value NL)+
Key           ::= [A-Za-z]+
Value         ::= String | Number | List | EpistemicStatus
List          ::= ID (", " ID)*
EpistemicStatus ::= "observed" | "inferred" | "hypothesized" | "excluded" | "unresolved" | "unknowable"
```

## 2. Constructs and Semantics

### 2.1 Patient Context
Defines the state of the patient at the start of the reasoning process.
- **Fields**: Age, Sex, Pregnancy Status, Comorbidities, History.
- **Semantics**: Values are treated as `observed` by default.

### 2.2 Observation
Qualitative empirical data.
- **Fields**: Status, Description, Onset, Justification.
- **Semantics**: Represents what the clinician or patient sees/feels.

### 2.3 Measurement
Quantitative empirical data.
- **Fields**: Label, Value, Unit, Range, Status, Uncertainty.
- **Semantics**: `Range` defines the reference interval. If `Value` is outside `Range`, it triggers a "Value Out of Range" flag in the execution model. `Uncertainty` must be declared if known.

### 2.4 Assertion
A step in the reasoning chain.
- **Fields**: Claim, Status, Supports, Contradicts, Justification.
- **Semantics**:
    - `Supports` lists IDs of blocks that provide evidence for the claim.
    - `Contradicts` lists IDs of blocks that argue against the claim.
    - An assertion with status `inferred` MUST have at least one supporting block.
    - If a contradiction is present, the status should typically be `unresolved` or `excluded` unless the justification explains how to weigh the conflicting evidence.

### 2.5 Justification
Provenance and rationale.
- **Fields**: Source, Type (Guideline/Evidence/Principle), Strength.
- **Semantics**: Provides the authority for an assertion or observation.

### 2.6 Constraint
Safety barriers.
- **Fields**: Rule, Target, Action (Block/Warn).
- **Semantics**: If `Target` meets `Rule`, the `Action` is triggered. Usually used to prevent unsafe inferences (e.g., "If Pregnancy is True, exclude Ibuprofen recommendation").

## 3. Native Construct Examples

### Patient Context
```
--- PATIENT CONTEXT: PC_001 ---
Age: 62
Sex: Male
Smoking: 30 pack-years
```

### Observation
```
--- OBSERVATION: OBS_01 ---
Status: observed
Description: "Shortness of breath on exertion"
Justification: J_01
```

### Measurement
```
--- MEASUREMENT: MEAS_01 ---
Label: "Heart Rate"
Value: 110
Unit: "bpm"
Range: 60-100
Status: observed
Uncertainty: "+/- 5 bpm"
```

### Assertion
```
--- ASSERTION: AS_01 ---
Claim: "Tachycardia"
Status: inferred
Supports: MEAS_01
Justification: J_02
```
