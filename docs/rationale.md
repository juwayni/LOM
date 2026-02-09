# LoM Design Rationale

## 1. Syntax Choice: Block-Based Declarative
We chose a block-based, dash-separated syntax instead of JSON, YAML, or a Lisp-like DSL to ensure the language remains **human-centered**.
- **Readability**: It resembles structured clinical notes.
- **Formality**: The triple-dash headers and strict field-value pairs provide the necessary formality for deterministic execution.
- **Separation**: Clear boundaries between primitives prevent "spaghetti reasoning".

## 2. Epistemic Status vs. Probabilities
LoM uses discrete epistemic states (`observed`, `hypothesized`, `inferred`, etc.) instead of numerical probabilities.
- **Rationale**: Clinical reasoning often relies on qualitative thresholds and evidence strength rather than precise Bayesian updates. Numerical probabilities in medicine can provide a false sense of certainty (pseudo-precision).
- **Safety**: Forcing a choice of state requires the reasoner to explicitly declare their level of commitment to a claim.

## 3. Mandatory Uncertainty and Propagation
Uncertainty is a first-class citizen in LoM.
- **Rationale**: Most clinical errors stem from ignoring uncertainty or missing data. By forcing uncertainty propagation, LoM ensures that "shaky" premises lead to "shaky" conclusions.
- **Auditability**: It makes it immediately obvious when a "confirmed" assertion is actually based on "hypothesized" evidence.

## 4. Constraint-First Execution
Constraints are evaluated with the highest priority.
- **Rationale**: Safety is non-negotiable. If a patient state triggers a safety rule (e.g., pregnancy or allergy), the language must immediately flag any violating reasoning path as `forbidden`.

## 5. Non-Goals: Why LoM is not a "Solver"
LoM is intentionally NOT a system that "solves" a case or provides a "diagnosis".
- **Rationale**: Autonomous medical AI poses significant ethical and safety risks. LoM's goal is to **assist human reasoning**, not replace it. By only validating consistency and flagging missing premises, it keeps the human in the loop as the ultimate authority.
