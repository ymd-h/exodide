import os
from setuptools import setup, find_packages, Extension

from exodide import build

include = os.path.join(os.path.dirname(__file__), "pybind11", "include")

setup(name="exodide-example",
      version="0.0.0",
      packages=find_packages(),
      cmdclass=build.cmdclass(),
      ext_modules=[Extension("exodide_example.example",
                             sources=["exodide-example/example.cc"],
                             extra_compile_args=["-std=c++17",
                                                 f"-I{include}"],
                             language="c++")])
