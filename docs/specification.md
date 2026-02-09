# LoM Formal Specification (Version 2.0)

## 1. Formal Grammar (EBNF)

```ebnf
LoMDocument    = { Block } ;
Block          = Header , NL , FieldList , NL , [ "---" ] ;
Header         = "--- " , BlockType , ": " , ID , " ---" ;
BlockType      = "PATIENT CONTEXT" | "TEMPORAL CONTEXT" | "OBSERVATION"
               | "MEASUREMENT" | "BIOMARKER" | "PHYSIOLOGICAL PROCESS"
               | "INTERVENTION" | "ASSERTION" | "JUSTIFICATION"
               | "CONSTRAINT" | "OUTCOME" ;

FieldList      = { Field , NL } ;
Field          = Key , ": " , Value ;
Key            = [A-Z][a-zA-Z0-9]* ;
Value          = String | Number | List | TemporalExpr | EpistemicState ;

List           = ID , { "," , ID } ;
TemporalExpr   = "at(" , Time , ")" | "during(" , ID , ")" | "relative(" , ID , "," , Delta , ")" ;
EpistemicState = Reliability , "|" , EvidenceStrength , "|" , Consensus ;
Reliability    = "High" | "Medium" | "Low" | "Unreliable" ;
EvidenceStrength = "GradeA" | "GradeB" | "GradeC" | "GradeD" ;
Consensus      = "Universal" | "Majority" | "Disputed" ;

ID             = [a-zA-Z0-9_]+ ;
String         = '"' , { any_character } , '"' ;
Number         = [ "-" ] , digits , [ "." , digits ] ;
Time           = digits ; (* ISO8601 or Relative T-scale *)
NL             = "\n" ;
```

## 2. Formal Semantics

LoM reasoning is interpreted as a **Justified Knowledge Graph (JKG)**.

### 2.1 Assertion Semantics
An assertion $A$ is valid if and only if:
$$\exists J \in \text{Justifications}, \exists S \subseteq (\text{Observations} \cup \text{Measurements} \cup \text{Assertions})$$
$$\text{Supports}(A, S) \land \text{Justifies}(J, A, S) \land \nexists C \in \text{Constraints} : \text{Violates}(A, C)$$

### 2.2 Uncertainty Propagation
Let $\mathcal{U}(n)$ be the uncertainty vector of node $n$.
For an inferred assertion $A$ from premises $P = \{p_1, \dots, p_n\}$:
$$\mathcal{U}(A) = \min(\mathcal{U}(p_1), \dots, \mathcal{U}(p_n), \text{Strength}(\text{Justification}(A)))$$
*Note: LoM uses a lattice-based min-operator across dimensions.*

### 2.3 Temporal Consistency
A reasoning chain $C = \{b_1, \dots, b_k\}$ is temporally consistent if:
$$\forall (b_i, b_j) \in C, \text{precedes}(b_i, b_j) \implies \text{Timestamp}(b_i) \leq \text{Timestamp}(b_j)$$

### 2.4 Constraint Enforcement
A constraint $C$ with rule $R$ and target $T$:
$$\forall b \in \text{Blocks}, \text{matches}(b, T) \land \text{eval}(R, \text{State}) = \text{True} \implies \text{Forbidden}(b)$$

## 3. Advanced Semantics of Mechanistic Primitives

### 3.1 Physiological Process
Models a state change over time.
- $P(t_1, t_2) \implies \text{Effect}(P)$ is active during $[t_1, t_2]$.
- Assertions linked to $P$ must respect the interval $[t_1, t_2]$.

### 3.2 Intervention (Drug)
- Requires `Dose`, `Route`, and `Indication`.
- Triggers `Interaction` checks against `PatientContext` and other `Interventions`.
