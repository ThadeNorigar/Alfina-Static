#!/usr/bin/env python3
"""Fix unescaped quotes in status.json text fields.

Strategy: parse line by line. For lines containing "text": "...",
extract the text value, escape any unescaped double quotes inside it,
and reconstruct the line.
"""
import json

with open('buch/status.json', encoding='utf-8') as f:
    lines = f.readlines()

fixed_lines = []
fixes = 0

for i, line in enumerate(lines):
    stripped = line.strip()

    # Match lines like:  "text": "some text with "quotes" inside"
    if stripped.startswith('"text"'):
        # Find the value portion: everything after "text": "
        prefix_end = line.index('"text"') + len('"text"')
        rest = line[prefix_end:]
        # rest is like: : "value here"\n or : "value here",\n
        colon_pos = rest.index(':')
        after_colon = rest[colon_pos + 1:].lstrip()

        if after_colon.startswith('"'):
            # Find the actual end of the string value
            # It ends with " followed by optional , and whitespace and newline
            # Work backwards from the end of the line
            rstripped = line.rstrip()
            if rstripped.endswith(','):
                end_quote_pos = len(rstripped) - 2  # position of closing "
            else:
                end_quote_pos = len(rstripped) - 1  # position of closing "

            # Find the opening quote
            text_start = line.index('"text"')
            after_text = line[text_start + 7:]  # skip "text":
            first_quote = text_start + 7 + after_text.index('"')

            # Extract the inner content
            inner = line[first_quote + 1:end_quote_pos]

            # Check for unescaped quotes inside
            # An unescaped quote is " not preceded by \
            new_inner = []
            j = 0
            while j < len(inner):
                if inner[j] == '\\' and j + 1 < len(inner):
                    new_inner.append(inner[j:j+2])
                    j += 2
                elif inner[j] == '"':
                    new_inner.append("'")
                    fixes += 1
                    j += 1
                else:
                    new_inner.append(inner[j])
                    j += 1

            fixed_inner = ''.join(new_inner)
            line = line[:first_quote + 1] + fixed_inner + line[end_quote_pos:]

    fixed_lines.append(line)

result = ''.join(fixed_lines)

# Also replace any remaining typographic quotes
for old, new in [('\u201e', "'"), ('\u201c', "'"), ('\u201d', "'")]:
    count = result.count(old)
    if count:
        print(f"  Replacing {count}x U+{ord(old):04X}")
        fixes += count
        result = result.replace(old, new)

try:
    json.loads(result)
    print(f"JSON VALID! Fixed {fixes} quotes.")
except json.JSONDecodeError as e:
    print(f"Still invalid: {e}")
    print(f"Context: {repr(result[max(0,e.pos-30):e.pos+30])}")

with open('buch/status.json', 'w', encoding='utf-8') as f:
    f.write(result)
