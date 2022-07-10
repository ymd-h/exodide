import os
from setuptools import setup, find_packages, Extension

include = os.path.join(os.path.dirname(__file__), "pybind11", "include")

setup(name="exodide-example",
      version="0.0.1",
      packages=find_packages(),
      ext_modules=[Extension("exodide_example.example",
                             sources=["exodide_example/example.cc"],
                             extra_compile_args=["-std=c++17",
                                                 f"-I{include}"],
                             language="c++")])
