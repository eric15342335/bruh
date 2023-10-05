from setuptools import setup
from Cython.Build import cythonize

# python setup.py build_ext --inplace
setup(
    name="utils",
    ext_modules=cythonize("utils.py"),
    zip_safe=False,
)
