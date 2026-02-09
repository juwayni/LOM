# LoM: Informatics and Clinical Rationale

## 1. Theoretical Foundation
The Language of Medicine (LoM) is grounded in **Formal Epistemology** and **Evidence-Based Medicine (EBM)**. Unlike traditional Expert Systems that use black-box heuristics, LoM utilizes a **Justified Knowledge Graph** where every node must be anchored in empirical evidence or established clinical guidelines.

## 2. Alignment with EBM Standards
LoM's multi-dimensional uncertainty model is directly inspired by the **GRADE (Grading of Recommendations, Assessment, Development and Evaluations)** framework:
- **Evidence Strength**: Maps Grade A-D to LoM's `EvidenceStrength` lattice.
- **Reliability**: Addresses the source of data (e.g., peer-reviewed RCT vs. observational case report).
- **Consensus**: Reflects the clinical agreement, essential for navigating conflicting guidelines.

## 3. Medical Informatics Integration
LoM is designed to be compatible with major informatics standards:
- **SNOMED CT**: LoM primitives (Observation, PhysiologicalProcess) are designed to map to SNOMED concepts.
- **LOINC**: Measurement and Biomarker blocks use fields (Label, Unit, Range) that align with LOINC coding structures.
- **FHIR**: The block-based structure is conceptually similar to FHIR Resources, facilitating future interoperability.

## 4. Temporal Reasoning in Clinical Workflows
Clinical diagnosis is a time-dependent process. LoM's temporal consistency checks prevent "hindsight bias" in reasoning by ensuring that conclusions are only supported by data available at the time of the claim ($T_{assertion} \geq T_{evidence}$).

## 5. Safety and Constraints
The `ConstraintEngine` implements the principle of **Primum non nocere** (First, do no harm). By making safety barriers (Constraints) high-priority nodes that can "prune" the reasoning graph, LoM ensures that potentially harmful assertions are flagged before they can be considered "inferred".
