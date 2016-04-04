import os.path, glob, sys
import kicadlib

here = os.path.abspath(os.path.split(__file__)[0])

lib = kicadlib.Library()

for f in glob.glob(os.path.join(here, '..', '*.lib')):
    for name, part in kicadlib.read(f).items():
        lib[name] = part

print lib.dumps().rstrip()
