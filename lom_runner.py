import sys
from lom_framework.core.parser import parse_lom
from lom_framework.logic.engine import InferenceEngine
from lom_framework.logic.explanation import ExplanationEngine

def main():
    if len(sys.argv) < 2:
        print("Usage: python lom_runner.py <file.lom>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        content = f.read()

    blocks = parse_lom(content)
    engine = InferenceEngine(blocks)
    engine.run()

    explainer = ExplanationEngine(engine)
    # Automatically explain all Assertions
    assertions = [b.id for b in blocks if b.type == 'ASSERTION']
    explainer.generate_report(assertions)

if __name__ == "__main__":
    main()
