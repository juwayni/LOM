# LoM Ontology: Advanced Medical Knowledge Primitives

## 1. Core Philosophy
LoM is a formal system designed to represent the complexity of clinical reasoning. It moves beyond simple "if-then" logic to incorporate temporal progression, physiological mechanisms, and a multi-dimensional model of uncertainty.

## 2. Advanced Primitives (The "PhD" Grade)

### 2.1 Contextual Primitives
- **PatientContext**: Multi-faceted state including demographics, genetic markers, and socio-economic determinants.
- **TemporalContext**: Represents time intervals (`[T_start, T_end]`), points (`T_0`), and sequences. Supports relative time (e.g., "3 days post-op").

### 2.2 Empirical Primitives
- **Observation**: Qualitative clinical signs and symptoms.
- **Measurement**: Quantitative data with associated error margins and device-specific reference ranges.
- **Biomarker**: Specific measurements with diagnostic or prognostic significance (e.g., Troponin I, PCT).

### 2.3 Mechanistic Primitives
- **PhysiologicalProcess**: Models the underlying biological mechanism (e.g., "Systemic Inflammatory Response").
- **Intervention**: Any clinical action, including `Drug` (pharmacological), `Procedure` (surgical/invasive), or `Counseling`.

### 2.4 Logical Primitives
- **Assertion**: A reasoned claim about a state or entity.
- **Justification**: Formal reference to evidence (EBM), guidelines (CPG), or physiological principles.
- **Constraint**: Strict safety or ethical boundaries that prune the reasoning graph.
- **Outcome**: A hypothesized or observed result of an intervention or process.

## 3. The Multi-Dimensional Epistemic Model
Instead of a single "status", LoM evaluates assertions across three dimensions:

1. **Reliability**: How dependable is the source of the data? (Scale: High, Medium, Low, Unreliable)
2. **Evidence Strength**: What is the quality of the supporting justification? (Grade: A, B, C, D per EBM standards)
3. **Clinical Consensus**: Is there widespread agreement on this reasoning path? (Scale: Universal, Majority, Disputed, Minority)

## 4. Relation Types
- `causes`: Mechanistic link.
- `indicates`: Probabilistic or diagnostic link.
- `prevents`: Inhibitory link.
- `aggravates`: Exacerbating link.
- `precedes`: Temporal ordering.
- `overlaps`: Temporal intersection.

## 5. Formal Schema Requirements
Every primitive MUST include:
- `UUID`: Globally unique identifier.
- `Timestamp`: When the primitive was created or observed.
- `Provenance`: Source of the information.
- `Metadata`: Key-value pairs for domain-specific extension.
