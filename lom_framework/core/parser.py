import re
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any

@dataclass
class Token:
    type: str
    value: str
    line: int
    column: int

class Lexer:
    TOKEN_TYPES = [
        ('HEADER', r'^--- ([A-Z0-9 ]+): ([a-zA-Z0-9_]+) ---$'),
        ('FIELD', r'^([A-Z][a-zA-Z0-9]*): (.*)$'),
        ('SEPARATOR', r'^---$'),
    ]

    def __init__(self, content: str):
        self.lines = content.split('\n')
        self.tokens = []

    def tokenize(self):
        for i, line in enumerate(self.lines):
            line = line.strip()
            if not line:
                continue

            matched = False
            for t_type, t_regex in self.TOKEN_TYPES:
                m = re.match(t_regex, line)
                if m:
                    self.tokens.append(Token(t_type, m.groups(), i + 1, 1))
                    matched = True
                    break

            if not matched:
                self.tokens.append(Token('RAW', line, i + 1, 1))
        return self.tokens

@dataclass
class BlockNode:
    type: str
    id: str
    fields: Dict[str, Any] = field(default_factory=dict)
    raw_content: List[str] = field(default_factory=list)

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def peek(self) -> Optional[Token]:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consume(self) -> Optional[Token]:
        t = self.peek()
        self.pos += 1
        return t

    def parse(self) -> List[BlockNode]:
        blocks = []
        while self.peek():
            t = self.peek()
            if t.type == 'HEADER':
                blocks.append(self.parse_block())
            else:
                self.consume()
        return blocks

    def parse_block(self) -> BlockNode:
        header = self.consume()
        b_type, b_id = header.value
        node = BlockNode(type=b_type, id=b_id)

        while self.peek() and self.peek().type != 'HEADER':
            t = self.consume()
            if t.type == 'FIELD':
                key, val = t.value
                # Strip quotes from field values
                val = val.strip().strip('"')
                node.fields[key] = val
            elif t.type == 'SEPARATOR':
                break
            else:
                node.raw_content.append(t.value)

        return node

def parse_lom(content: str) -> List[BlockNode]:
    lexer = Lexer(content)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    return parser.parse()
