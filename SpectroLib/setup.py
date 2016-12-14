#from distutils.core import setup, Extension

# define the extension module
#SpectroLib_module = Extension('SpectroLib', sources=['SpectroLib_module.c'])

# run the setup
#setup(ext_modules=[SpectroLib_module])



from distutils.core import setup, Extension
import struct
bit_size = struct.calcsize("P") * 8
dln_path = ""
if bit_size == 64:
	dln_path = "../DLNWare/bin/x64"
elif bit_size == 32:
	dln_path = "../DLNWare/bin/x86"
	
	

setup(
	name="SpectroLib_module", 
	version="1.0", 
	#py_modules = ['SpectroLib.py'],
	ext_modules=[Extension("SpectroLib_module", 
		[
		"SpectroLib_module.c",
		"SpectroLib.cpp",
		"SpectroController.cpp",
		],
		extra_compile_args = ["-std=c++11"],
		extra_link_args = ["-L"+dln_path, "-ldln", "-lQtCore"])],
		include_dirs = [
			'/usr/include',
			'/usr/local/include',
			'/usr/include/c++/4.8',
			'../DLNWare/include'
		],

	

)
