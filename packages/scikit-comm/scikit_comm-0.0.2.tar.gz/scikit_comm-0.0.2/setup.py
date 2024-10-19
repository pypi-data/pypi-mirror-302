from setuptools import setup
from Cython.Build import cythonize

setup(
    name='Reveiver Cython implementation',
    ext_modules=cythonize("src/scikit-comm/cython_mods/rx_cython.pyx", annotate=True, language_level = "3"),
    zip_safe=False,
)
