# file: setup.py
from distutils.core import setup, Extension
from Cython.Build import cythonize

# setup(name='utils', version='1.0', ext_modules=cythonize("utils.pyx"))
# setup(name='home', version='1.0', ext_modules=cythonize("home.pyx"))
setup(ext_modules=cythonize(Extension(
    name='home',
    sources=['home.pyx'],
    language='c',
    include_dirs=[],
    library_dirs=[],
    libraries=[],
    extra_compile_args=[],
    extra_link_args=[]
)))
setup(ext_modules=cythonize(Extension(
    name='utils',
    sources=['utils.pyx'],
    language='c',
    include_dirs=[],
    library_dirs=[],
    libraries=[],
    extra_compile_args=[],
    extra_link_args=[]
)))
