import re, sys

HEADER = """EESchema-LIBRARY Version 2.3
#encoding utf-8
"""

FOOTER = """#
#End Library"""

class Part:
    def __init__(self, name, lines):
        self.name = name
        self.lines = lines
    def dumps(self):
        return "#\n# %s\n#\n%s" % (
            self.name,
            "\n".join(self.lines),
        )
    def __eq__(self, o):
        return self.name == o.name and self.lines == o.lines
    def sanitized_name(self):
        return self.name.lower().replace("/", "-")

class Library:
    def __init__(self, fn=None):
        self.fn = fn
        self.parts = {}
    def items(self):
        return self.parts.items()
    def __setitem__(self, name, part):
        if self.parts.has_key(name):
            if self.parts[name] == part:
                print>>sys.stderr, "re-adding part %s in library %s" % (name, self.fn)
            else:
                print>>sys.stderr, "updating part %s in library %s" % (name, self.fn)
        self.parts[name] = part
    def parse_part(self, lines):
        name = re.search("^DEF ([^ ]+) ", lines[0]).group(1)
        self[name] = Part(name, lines)
    def dumps(self):
        return HEADER + "\n".join(part.dumps() for name, part in sorted(self.items())) + "\n" + FOOTER

def read(fn):
    print>>sys.stderr, "reading %s" % fn
    lib = Library(fn)
    f = open(fn)
    assert f.readline().strip() == 'EESchema-LIBRARY Version 2.3', 'header incorrect in %s' % fn
    part = []
    for line in f:
        line = line.rstrip()
        if line.startswith("#"): continue
        #print line
        if len(part) or line.startswith("DEF "):
            part.append(line)
        if line == 'ENDDEF':
            lib.parse_part(part)
            part = []
    assert part == [], "unparsed lines: %s" % `part`
    return lib
