from setuptools import setup, find_packages

setup(name="extodide",
      description="build_ext for Pyodide",
      version="0.0.0",
      packages=find_packages(),
      package_data={"extodide":
                    ["cpython/*.h",
                     "cpython/cpython/*.h",
                     "cpython/internal/*.h",
                     "numpy/numpy/*.h",
                     "numpy/numpy/libdivide/*",
                     "numpy/numpy/random/*.h"]},
      include_package_data=True)
