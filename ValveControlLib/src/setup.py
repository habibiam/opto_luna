from distutils.core import setup, Extension

setup(
    name="ValveControlLib_module",
    version="1.0",
    ext_modules=[Extension("ValveControlLib_module", ["ValveControl.cpp", "ValveControlLib.cpp", "ValveControlLib_module.c"],
        extra_compile_args = ["-std=c++11"])],
        include_dirs = ['/usr/include', '/usr/local/include', '/usr/include/c++/4.8']
)
