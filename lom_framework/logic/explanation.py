from typing import List, Dict
from lom_framework.core.parser import BlockNode
from lom_framework.logic.engine import InferenceEngine

class ExplanationEngine:
    def __init__(self, engine: InferenceEngine):
        self.engine = engine

    def explain(self, block_id: str, depth: int = 0) -> List[str]:
        block = self.engine.get_block(block_id)
        if not block: return [f"Error: Block {block_id} not found."]

        indent = "  " * depth
        claim = block.fields.get('Claim') or block.fields.get('Description') or block.id
        lines = [f"{indent}Block: {block.type} | ID: {block.id} | Content: {claim}"]

        # Add Justification
        just_id = block.fields.get('Justification')
        if just_id:
            just_block = self.engine.get_block(just_id)
            if just_block:
                source = just_block.fields.get('Source', 'Unknown')
                lines.append(f"{indent}  Supported by: {source}")

        # Recurse supports
        supports = self.engine.get_supports(block_id)
        if supports:
            lines.append(f"{indent}  Based on evidence:")
            for s_id in supports:
                lines.extend(self.explain(s_id, depth + 2))

        return lines

    def generate_report(self, target_ids: List[str]):
        print("--- LoM Clinical Reasoning Explanation Report ---")
        print("Disclaimer: Educational / Non-clinical\n")
        for tid in target_ids:
            explanation = self.explain(tid)
            for line in explanation:
                print(line)
            print("-" * 40)
