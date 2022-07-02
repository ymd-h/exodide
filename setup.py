from setuptools import setup, find_packages

setup(name="exodide",
      description="build_ext for Pyodide",
      version="0.0.0",
      install_requires=["wheel"],
      packages=find_packages(),
      package_data={"exodide":
                    ["cpython/*.h",
                     "cpython/cpython/*.h",
                     "cpython/internal/*.h"
                     "cpython/LICENSE",
                     "numpy/numpy/*.h",
                     "numpy/numpy/libdivide/*",
                     "numpy/numpy/random/*.h",
                     "numpy/LICENSE*"]},
      include_package_data=True)
