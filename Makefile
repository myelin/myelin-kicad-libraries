default:
	rm -f myelin-kicad.lib
	python tools/merge.py * > myelin-kicad.lib_
	mv myelin-kicad.lib_ myelin-kicad.lib
