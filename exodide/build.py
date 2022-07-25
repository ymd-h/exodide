"""
exodide.build module

This module provides functionalities
to build C/C++ extension package for Pyodide.
"""

import os
import sys
from typing import Dict, List
from unittest import mock

from distutils.command.build import build as _build
from setuptools import Command
from setuptools.command.build_ext import build_ext as _build_ext
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
from wblog import getLogger

logger = getLogger()

def system_include() -> str:
    """
    Get system include directory

    Returns
    -------
    str
        Include directory of host Python
    """
    return os.path.join(sys.prefix, "include", "python")


def exodide_include() -> List[str]:
    """
    Get exodide include directories

    Returns
    -------
    list of str
        Include directories in exodide package
    """
    dirname = os.path.dirname(__file__)
    return [os.path.join(dirname, "cpython"),
            os.path.join(dirname, "numpy")]


def adjust_include(include: List[str]) -> List[str]:
    """
    Adjust include list

    Parameters
    ----------
    include : list of str
        Original include directories

    Returns
    -------
    list of str
        Adjusted include directories
    """
    s = [system_include()]
    try:
        import numpy as np
        s.append(np.get_include())
    except ImportError:
        pass

    ret = exodide_include() + [I for I in include
                               if all(ss not in I for ss in s)]
    logger.debug(f"adjust_include: {include} -> {ret}")
    return ret


def exodide_links() -> List[str]:
    """
    Get exodide link args

    Returns
    -------
    list of str
        Link arguments for exodide
    """
    return ["-s", "MODULARIZE=1",
            "-s", "LINKABLE=1",
            "-s", "EXPORT_ALL=1",
            "-s", "WASM=1",
            "-s", "LZ4=1",
            "-s", "WASM_BIGINT",
            "-s", "SIDE_MODULE=1"]


def exodide_unsupported_links() -> List[str]:
    """
    Get exodide unsupported link args

    Returns
    -------
    list of str
        Unsupported link arguments for exodide
    """
    return ["-shared", "-pthread",
            "-Wl,-Bsymbolic-functions",
            "-Wl,--strip-all",
            "-Wl,-strip-all",
            "-Wl,--sort-common",
            "-Wl,--as-needed"]


def exodide_platform_tag() -> str:
    """
    Platform name tag for wheel

    Returns
    -------
    str
        platform tag
    """
    return "emscripten-wasm32"


def exodide_extension_filename(ext_name: str) -> str:
    """
    Extention file name

    Parameters
    ----------
    ext_name : str
        Extension module name

    Returns
    -------
    str
        Extension file name
    """
    ext_path = ext_name.split(".")
    return os.path.join(*ext_path) + ".cpython-310-wasm32-emscripten.so"


class build(_build):
    """
    Build Command for exodide

      * Replace platform name of wheel
    """
    def finalize_options(self):
        with mock.patch("distutils.command.build.get_platform") as get_platform:
            get_platform.return_value = exodide_platform_tag()
            return super().finalize_options()


class build_ext(_build_ext):
    """
    Build Extension Command for exodide

      * Remove system Python from include directory
      * Add exodide Python and NumPy to include directory
      * Add linker options for Emscripten
      * Remove not supported linker options
    """
    def run(self):
        self.include_dirs = adjust_include(self.include_dirs)

        for ext in self.extensions:
            ext.extra_link_args = ext.extra_link_args + exodide_links()
        return super().run()

    def build_extensions(self):
        logger.debug(f"include_dirs: {self.include_dirs}")
        remove_opt = exodide_unsupported_links()
        self.compiler.linker_so = [so for so in self.compiler.linker_so
                                   if (so not in remove_opt)]
        logger.debug(f"linker_so: {self.compiler.linker_so}")

        return super().build_extensions()

    def build_extension(self, ext):
        ext.include_dirs = adjust_include(ext.include_dirs)
        return super().build_extension(ext)

    def get_ext_filename(self, ext_name):
        return exodide_extension_filename(ext_name)


def cmdclass() -> Dict[str, Command]:
    """
    Get command classes for exodide

    Returns
    -------
    dict
       Command definitions

    Examples
    --------
    >>> from setuptools import setup
    >>> from exodide import build
    >>> setup(...,
    ...       cmdclass=build.cmdclass())
    """
    return {"build": build,
            "build_ext": build_ext}
