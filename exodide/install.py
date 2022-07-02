"""
exodide.install module

This module provides functionalities
to install custom extension package to Pyodide.

This module is intended to use inside Pyodide.


Examples
--------
The following example must run inside JavaScript `pyodide.runPythonAsync()`.

>>> from exodide import install
>>> await install.fetch_install("https://example.com/your-package.whl")


Notes
-----
Dependencies are not resolved. User must take care by yourself.
"""
import asyncio
import importlib

import pyodide_js
from pyodide import http, JsProxy


async def fetch_install(wheel_url: str):
    """
    Fetch wheel file then install it.

    Parameters
    ----------
    wheel_url : str
       URL where wheel is hosted.

    Notes
    -----
    Dependencies are not resolved. User must take care by yourself.
    """
    response = await http.pyfetch(wheel_url)
    wheel_buffer = await response.buffer()
    await install_wheel_buffer(wheel_buffer)


async def install_wheel_buffer(wheel_buffer: JsProxy):
    """
    Install wheel

    Parameters
    ----------
    wheel_buffer
        wheel as Javascript buffer

    Notes
    -----
    Dependencies are not resolved. User must take care by yourself.
    """
    so_list = http.unpack_buffer(wheel_buffer,
                                 filename=".whl",
                                 installer="exodide",
                                 target="site",
                                 format="whl",
                                 calculate_dynlibs=True)
    importlib.invalidate_caches()
    await asyncio.gather(*(pyodide_js._api.loadDynlib(so) for so in so_list))
