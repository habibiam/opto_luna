all:
#	~/eclipse/eclipse -nosplash -application org.eclipse.cdt.managedbuilder.core.headlessbuild -import . -build ValveControlLib  -cleanBuild ValveControlLib
	rm -f *.so
	python setup.py build_ext --inplace
	cp -f *.so ..\..\LunaSrv
