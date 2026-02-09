# LoM Ontology and Conceptual Definition

## 1. Conceptual Definition
The Language of Medicine (LoM) is a formal, human-centered, executable representation system for medical knowledge, reasoning, and education. It is designed to make medical reasoning explicit, verifiable, auditable, and safely constrained.

**LoM is NOT a clinical decision system, NOT autonomous, and NOT for real patient care.**

Its primary goal is to provide a structured way to represent how clinical conclusions are reached, emphasizing uncertainty, evidence, and safety.

## 2. Core Philosophy
- **Reasoning under Uncertainty**: Medicine is never 100% certain. LoM forces the declaration of uncertainty at every step.
- **Explicitness**: Every claim must be linked to evidence and a justification.
- **Safety First**: Reasoning chains that lack sufficient evidence or violate safety constraints must not converge on a conclusion.
- **Educational and Analytical**: Designed for learning, reflection, and critique of medical logic.

## 3. Primitives
Everything in LoM is composed from these atomic primitives:

### 3.1 Entity
A thing being reasoned about.
- **PatientContext**: Static or slowly changing patient attributes (e.g., age, sex, relevant history).
- **Observation**: Empirical data gathered (e.g., symptoms, signs).
- **Measurement**: Quantifiable data (e.g., lab values, vitals) with units and ranges.
- **Claim**: A proposition about a disease, condition, or state.

### 3.2 Assertion
A statement about an Entity with an associated **Epistemic Status**.

### 3.3 Justification
The rationale, evidence, or clinical guideline supporting an assertion. It provides the "why" behind the logic.

### 3.4 Constraint
A rule that limits reasoning. These are often safety or ethical boundaries (e.g., "Contraindicated if patient is pregnant").

### 3.5 Relation
How primitives connect to each other:
- `supports`: Evidence that strengthens an assertion.
- `contradicts`: Evidence that weakens or refutes an assertion.
- `depends-on`: Logical dependency between assertions.
- `excludes`: Mutual exclusivity.

### 3.6 State
The current evaluation status of a reasoning node:
- `known`: Verified and certain.
- `uncertain`: Known but with a margin of error or doubt.
- `excluded`: Ruled out.
- `unknowable`: Information that cannot be obtained.
- `forbidden`: Reasoning paths that are blocked for safety reasons.

## 4. Epistemic Status
Every assertion must declare exactly one epistemic status:
- `observed`: Directly seen or measured.
- `inferred`: Derived from other observations/assertions via logical reasoning.
- `hypothesized`: A possible explanation being explored.
- `excluded`: Explicitly ruled out based on evidence.
- `unresolved`: A hypothesis that cannot yet be confirmed or excluded.
- `unknowable`: Information that is missing and cannot be retrieved.

## 5. Uncertainty
Uncertainty is typed and must be propagated:
- **Measurement Uncertainty**: Error margins in lab tests or vitals.
- **Evidence Uncertainty**: Weakness or conflict in clinical studies/guidelines.
- **Ethical/Safety Uncertainty**: Ambiguity in patient preference or safety profiles.
- **Temporal Uncertainty**: Progression or onset timing doubt.
