#from distutils.core import setup, Extension

# define the extension module
#SpectroLib_module = Extension('SpectroLib', sources=['SpectroLib_module.c'])

# run the setup
#setup(ext_modules=[SpectroLib_module])



from distutils.core import setup, Extension

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
		extra_link_args = ["-L../DLNWare/bin/x64", "-ldln", "-lQtCore"])],
		include_dirs = [
			'/usr/include',
			'/usr/local/include',
			'/usr/include/c++/4.8',
			'../DLNWare/include'
		],

	

)
