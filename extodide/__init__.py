import os
from typing import List

from setuptools.command.build_ext import build_ext as _build_ext


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

class build_ext(_build_ext):
    pass
