"""
exodide.build module

This module provides functionalities
to build C/C++ extension package for Pyodide.
"""

import os
import sys
from typing import Dict, List
from unittest import mock

from distutils.cmd import Command
from distutils.command.build import build as _build
from setuptools.command.build_ext import build_ext as _build_ext
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

system_include = os.path.join(sys.prefix, "include", "python")

def cpython_get_include() -> str:
    return f"{os.path.dirname(__file__)}/cpython"

def numpy_get_include() -> str:
    return f"{os.path.dirname(__file__)}/numpy"


def LDFLAGS() -> List[str]:
    return ["-s", "MODULARIZE=1",
            "-s", "LINKABLE=1",
            "-s", "EXPORT_ALL=1",
            "-s", "WASM=1",
            "-s", "LZ4=1",
            "-s", "WASM_BIGINT",
            "-s", "SIDE_MODULE=1"]


def plat_name() -> str:
    return "emscripten-wasm32"


class build(_build):
    def finalize_options(self):
        with mock.patch("distutils.command.build.get_platform") as get_platform:
            get_platform.return_value = plat_name()
            return super().finalize_options()


class build_ext(_build_ext):
    def run(self):
        self.include_dirs = [
            cpython_get_include(),
            numpy_get_include()
        ] + [d for d in self.include_dirs if (system_include not in d)]

        for ext in self.extensions:
            ext.extra_link_args = ext.extra_link_args + LDFLAGS()
        return super().run()

    def build_extensions(self):
        self.compiler.linker_so = [so for so in self.compiler.linker_so
                                   if (so not in ["-shared", "-pthread"])]
        return super().build_extensions()

    def get_ext_filename(self, ext_name):
        ext_path = ext_name.split('.')
        return os.path.join(*ext_path) + ".cpython-310-wasm32-emscripten.so"


def cmdclass() -> Dict[str, Command]:
    return {"build": build,
            "build_ext": build_ext}
