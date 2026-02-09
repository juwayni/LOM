# Clinical Logic Monograph: Formalizing Medical Thought

## Abstract
Clinical reasoning is the process of making decisions under conditions of significant uncertainty. Traditionally, this process is implicit and prone to cognitive biases. The **Language of Medicine (LoM)** framework formalizes this reasoning into an explicit, auditable, and checkable logic.

## 1. The Epistemology of Medicine
Medicine is not a pure deductive science. It is a mix of:
- **Deduction**: Applying universal guidelines to specific cases.
- **Induction**: Learning from patient data.
- **Abduction**: Finding the best explanation for a set of observations.

LoM represents these via `Assertion` statuses and `Justification` strengths.

## 2. Uncertainty as a First-Class Citizen
In LoM, uncertainty is not a single number (probability). It is a multidimensional vector. This recognizes that 50% probability based on a high-quality RCT is fundamentally different from 50% probability based on expert opinion.

## 3. The "Conservative Default" Principle
LoM's safety engine implements **Conservative Defaults**. If a critical piece of information is missing, or if a safety constraint is triggered, the system defaults to "Blocked" or "Hypothesized" rather than "Confirmed".

## 4. Integration with Standard Ontologies
LoM is designed to be the "Reasoning Layer" on top of terminological ontologies like SNOMED CT. While SNOMED defines *what* a thing is, LoM defines *why* we believe it and *what* it implies for the patient.

## 5. Conclusion
By formalizing clinical logic, we move from "Expert systems" that act as black boxes to "Reasoning assistants" that explain their logic, invite critique, and ensure safety.
