import re
import sys
import json

class LoMValidator:
    def __init__(self):
        self.blocks = {}
        self.errors = []
        self.warnings = []

    def parse(self, content):
        # Split by triple dashes and header
        # Pattern: --- HEADER: ID ---
        parts = re.split(r'--- (.*?): (.*?) ---', content)

        for i in range(1, len(parts), 3):
            block_type = parts[i].strip()
            block_id = parts[i+1].strip()
            block_content = parts[i+2].strip()

            fields = {}
            for line in block_content.split('\n'):
                line = line.strip()
                if not line: continue
                if ':' in line:
                    key, value = line.split(':', 1)
                    val = value.strip().strip('"') # Strip quotes for easier logic
                    fields[key.strip()] = val

            self.blocks[block_id] = {
                'type': block_type,
                'id': block_id,
                'fields': fields
            }

    def validate(self):
        print("Starting LoM Validation...")
        print("Disclaimer: Educational / Analytical / Non-clinical. Not for patient care.\n")

        if not self.blocks:
            print("No blocks found to validate.")
            return

        for block_id, block in self.blocks.items():
            self._check_basic_fields(block)
            self._check_traceability(block)
            self._check_measurement_ranges(block)
            self._check_uncertainty_propagation(block)
            self._check_constraints(block)

        self._check_circular_reasoning()

        if self.errors:
            print("ERRORS FOUND:")
            for err in self.errors:
                print(f"  - [ERROR] {err}")
        else:
            print("No critical validation errors found.")

        if self.warnings:
            print("\nWARNINGS:")
            for warn in self.warnings:
                print(f"  - [WARN] {warn}")

        print("\nValidation Summary:")
        print(f"Total Blocks: {len(self.blocks)}")
        print(f"Errors: {len(self.errors)}")
        print(f"Warnings: {len(self.warnings)}")

    def _check_basic_fields(self, block):
        b_type = block['type']
        fields = block['fields']
        b_id = block['id']

        if b_type == 'OBSERVATION':
            if 'Status' not in fields: self.errors.append(f"{b_id}: Missing 'Status'")
            if 'Description' not in fields: self.errors.append(f"{b_id}: Missing 'Description'")

        elif b_type == 'MEASUREMENT':
            if 'Value' not in fields: self.errors.append(f"{b_id}: Missing 'Value'")
            if 'Uncertainty' not in fields: self.warnings.append(f"{b_id}: Missing 'Uncertainty' (Incomplete Data)")

        elif b_type == 'ASSERTION':
            if 'Claim' not in fields: self.errors.append(f"{b_id}: Missing 'Claim'")
            if 'Status' not in fields: self.errors.append(f"{b_id}: Missing 'Status'")
            if fields.get('Status') == 'inferred' and 'Supports' not in fields:
                self.errors.append(f"{b_id}: Inferred assertion must have 'Supports' field")

    def _check_traceability(self, block):
        fields = block['fields']
        b_id = block['id']
        for field in ['Supports', 'Contradicts']:
            if field in fields:
                ids = [i.strip() for i in fields[field].split(',')]
                for ref_id in ids:
                    if ref_id and ref_id not in self.blocks:
                        self.errors.append(f"{b_id}: {field} references non-existent ID '{ref_id}'")

    def _check_measurement_ranges(self, block):
        if block['type'] == 'MEASUREMENT':
            fields = block['fields']
            if 'Value' in fields and 'Range' in fields:
                try:
                    val = float(fields['Value'].replace(',', ''))
                    r_match = re.match(r'([\d\.]+)-([\d\.]+)', fields['Range'])
                    if r_match:
                        low, high = map(float, r_match.groups())
                        if val < low or val > high:
                            self.warnings.append(f"{block['id']}: Value {val} is outside reference range {fields['Range']}")
                except ValueError:
                    pass

    def _check_uncertainty_propagation(self, block):
        if block['type'] == 'ASSERTION':
            fields = block['fields']
            supports = [i.strip() for i in fields.get('Supports', '').split(',') if i.strip()]

            for s_id in supports:
                if s_id in self.blocks:
                    s_block = self.blocks[s_id]
                    s_fields = s_block['fields']
                    if s_fields.get('Status') in ['hypothesized', 'unresolved']:
                        if fields.get('Status') not in ['hypothesized', 'unresolved', 'excluded']:
                            self.warnings.append(f"{block['id']}: Higher status than supporting premise {s_id} ({s_fields.get('Status')})")

    def _check_constraints(self, block):
        if block['type'] == 'ASSERTION':
            claim = block['fields'].get('Claim', '').lower()
            # Find all constraints
            for c_id, c_block in self.blocks.items():
                if c_block['type'] == 'CONSTRAINT':
                    c_fields = c_block['fields']
                    rule = c_fields.get('Rule', '')
                    target = c_fields.get('Target', '').lower()

                    # Simple rule matching: check PatientContext for the rule
                    triggered = False
                    for p_id, p_block in self.blocks.items():
                        if p_block['type'] == 'PATIENT CONTEXT':
                            p_fields = p_block['fields']
                            # Check if rule matches a field value
                            for k, v in p_fields.items():
                                if rule.lower() in f"{k}: {v}".lower():
                                    triggered = True
                                    break

                    if triggered and target in claim:
                        self.errors.append(f"SAFETY VIOLATION: Assertion {block['id']} violates constraint {c_id} ('{target}' forbidden by rule '{rule}')")

    def _check_circular_reasoning(self):
        # Build graph
        adj = {}
        for b_id, block in self.blocks.items():
            adj[b_id] = []
            fields = block['fields']
            for f in ['Supports', 'Contradicts', 'Depends-on']:
                if f in fields:
                    refs = [i.strip() for i in fields[f].split(',') if i.strip()]
                    adj[b_id].extend(refs)

        visited = set()
        path = set()

        def has_cycle(v):
            visited.add(v)
            path.add(v)
            for neighbor in adj.get(v, []):
                if neighbor not in visited:
                    if has_cycle(neighbor): return True
                elif neighbor in path:
                    return True
            path.remove(v)
            return False

        for node in adj:
            if node not in visited:
                if has_cycle(node):
                    self.errors.append(f"Circular reasoning detected involving block '{node}'")
                    break

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validator/lom_validator.py <file.lom>")
        sys.exit(1)

    try:
        with open(sys.argv[1], 'r') as f:
            content = f.read()

        validator = LoMValidator()
        validator.parse(content)
        validator.validate()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
