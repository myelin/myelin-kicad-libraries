import os, sys
import kicadlib

src, = sys.argv[1:]

here = os.path.abspath(os.path.split(__file__)[0])

lib = kicadlib.read(src)

for name, part in lib.items():
	l = kicadlib.Library()
	l[name] = part
	print>>open(os.path.join(here, '..', '%s.lib' % part.sanitized_name()), 'w'), l.dumps()

