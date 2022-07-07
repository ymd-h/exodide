# exodide: build_ext for Pyodide

![PyPI](https://img.shields.io/pypi/v/exodide)

## 1. Overview

> **Warning**
> This project is still under development.


[Pyodide](https://pyodide.org/en/stable/index.html) is a WebAssembly
variant of [CPython](https://www.python.org/). By using it, we can run
Python code inside web browser.

Although we can run most of pure-Python packages on Pyodide, however,
available C/C++-extension packages are limited to
[builtin packages](https://pyodide.org/en/stable/usage/packages-in-pyodide.html).

The motivation of this project (exodide) is providing C/C++-extension
builder for Pyodide, and enables users to run your own custom
C/C++-extension packages on Pyodide.

## 2. Usage

### 2.1 Prerequest
To build C/C++ to WebAssembly, you need
[Emscripten](https://emscripten.org/). We assume you set up `emcc` and
`em++` commands as
[the official document](https://emscripten.org/docs/getting_started/downloads.html).

Since Pyodide is built with Python 3.10, we only prepare headers for
the version. Your custom package must run on Python 3.10.

### 2.2 Build with exodide
To build custom extension, you also need `wheel` package, which can be
installed by `pip install exodide[build]`.


```python:setup.py
from setuptools import setup
from exodide import build

# omit

setup(
    # omit
    cmdclass=build.cmdclass(), # {'build': exodide.build, 'build_ext': exodide.build_ext}
)
```

then `CC=emcc CXX=em++ python setup.py bdist_wheel`.


Pyodide doesn't provide all the functionalities of CPython, so that
you might need to modify your package. You can detect Emscripten
compiler by `__EMSCRIPTEN__` macro ([ref](https://emscripten.org/docs/compiling/Building-Projects.html#detecting-emscripten-in-preprocessor)).

```cpp
#ifdef __EMSCRIPTEN__
// Code for Pyodide
#else
// Code for Others
#endif
```

### 2.3 Install to Pyodide
```javascript
const pyodide = await loadPyodide();

await pyodide.runPythonAsync(`
import micropip
micropip.install("exodide")

from exodide.install import fetch_install

await fetch_install("example.com/your-package.whl")

import your_package
# omit
`);
```

### 2.4 Inspect Shared Object (for Debugging)
Fot inspect, `numpy` is also required, and you can install with
`pip install exodide[inspect]`.


```shell
python3 -m exodide.inspect your-package/your-module.so
```

Currently, `exodide.inspect` module prints `dylink` / `dylink.0`
custom section, which are used for metadata of Wasm dynamic link.


## 3. LICENSEs

We utilize other projects and these codes obey their original lisences.
We distribute patched header files of CPython and NumPy, too.

* CPython: https://www.python.org/
  * `cpython` directory
  * [PYTHON SOFTWARE FOUNDATION LICENSE VERSION 2](https://github.com/python/cpython/blob/main/LICENSE)
* NumPy: https://numpy.org/
  * `numpy` directory and `script/code_generators` directory
  * [BSD 3-Clause](https://github.com/numpy/numpy/blob/main/LICENSE.txt)
* Pyodide: https://pyodide.org/en/stable/
  * `pyodide` directory
  * [MPL-2.0](https://github.com/pyodide/pyodide/blob/main/LICENSE)
* Others (exodide original codes)
  * [MIT](https://github.com/ymd-h/exodide/blob/master/LICENSE)


## 4. Build exodide

```shell
git clone --recursive --depth 1 https://github.com/ymd-h/exodide.git
cd exodide

make

pip install .
```
