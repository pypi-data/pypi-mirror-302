# run with python3.11
# run using python3.11 setup.py build_ext --inplace
# or pip3.11 install -e .
from setuptools import setup, Extension

pickle_module = Extension('_pickle',
                          sources=['_pickle.c'],
                          include_dirs=['Include/internal', 'Include'],
                          extra_compile_args=['-fno-strict-overflow', '-Wsign-compare', '-Wunreachable-code', '-DNDEBUG', '-g', '-O3', '-Wall'],
                          )

setup(
    name='fastpickle',
    version='0.0.1',
    author='Yongjoo Park',
    author_email='yongjoo@illinois.edu',
    description='A pickle module extension',
    ext_modules=[pickle_module],
    py_modules=['pickle'],
)
