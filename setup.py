import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8") as f:
    README = f.read()


setup(name="exodide",
      author="Yamada Hiroyuki",
      description="build_ext for Pyodide",
      long_description=README,
      long_description_content_type="text/markdown",
      version="0.0.3",
      url="https://github.com/ymd-h/exodide",
      install_requires=["wheel"],
      packages=find_packages(),
      package_data={"exodide":
                    ["cpython/*.h",
                     "cpython/cpython/*.h",
                     "cpython/internal/*.h",
                     "cpython/LICENSE",
                     "numpy/numpy/*.h",
                     "numpy/numpy/libdivide/*",
                     "numpy/numpy/random/*.h",
                     "numpy/LICENSE*"]},
      classifiers=["Programming Language :: Python",
                   "Programming Language :: Python :: 3",
                   "Development Status :: 4 - Beta",
                   "Operating System :: OS Independent",
                   "Intended Audience :: Developers",
                   "Topic :: Software Development :: Libraries"],
      include_package_data=True)
