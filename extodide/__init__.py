import os
from typing import List

from setuptools.command.build_ext import build_ext as _build_ext


def cpython_get_include() -> str:
    return f"{os.dirname(__file__)}/cpython"

def numpy_get_include() -> str:
    return f"{os.dirname(__file__)}/numpy"


class build_ext(_build_ext):
    pass
