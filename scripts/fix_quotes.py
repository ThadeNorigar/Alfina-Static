import re, json, sys

path = 'C:/Users/micro/StudioProjects/Alphina-Static/buch/zeitleiste.json'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
fixed_lines = []
problem_count = 0

for i, line in enumerate(lines):
    m = re.match(r'^(\s*"[^"]+"\s*:\s*)"(.+)"(,?)$', line)
    if m:
        prefix = m.group(1)
        value = m.group(2)
        suffix = m.group(3)
        if '"' in value:
            value = value.replace('"', "'")
            line = f'{prefix}"{value}"{suffix}'
            problem_count += 1
            print(f'Fixed line {i+1}: {line.strip()[:120]}')
    fixed_lines.append(line)

content = '\n'.join(fixed_lines)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

try:
    json.load(open(path, encoding='utf-8'))
    print(f'\nJSON valid! Fixed {problem_count} lines.')
except json.JSONDecodeError as e:
    print(f'\nStill invalid: {e}')
    sys.exit(1)
