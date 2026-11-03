import re

_DEV = re.compile(r'[\u0900-\u097F]')
_BLOCK = re.compile(r'(```[ \t]*(?:python|py)[ \t]*\n)(.*?)(```)', re.S | re.I)


def _fix_block(m):
    head, body, tail = m.group(1), m.group(2), m.group(3)
    if '"""' in body or "'''" in body:
        return m.group(0)
    out = []
    for line in body.split('\n'):
        s = line.strip()
        if (s and _DEV.search(s) and not s.startswith('#')
                and '"' not in s and "'" not in s
                and '#' not in s and '=' not in s):
            indent = line[:len(line) - len(line.lstrip())]
            out.append(indent + '# ' + s)
        else:
            out.append(line)
    return head + '\n'.join(out) + tail


def fix_code_blocks(text):
    try:
        if not isinstance(text, str) or '```' not in text:
            return text
        return _BLOCK.sub(_fix_block, text)
    except Exception:
        return text
