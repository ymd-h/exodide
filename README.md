# exodide: build_ext for Pyodide

## 1. Overview

> **Warning**
> This project is still under development, and doesn't work yet.


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
[Emscripten](https://emscripten.org/).

Since Pyodide is built with Python 3.10, we only prepare headers for
the version. Your custom package must run on Python 3.10.

### 2.2 Build with exodide

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

### 2.4 Inspect Shared Object

```shell
python3 -m exodide.inspect your-package/your-module.so
```


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
  * MIT


## 4. Build exodide

```shell
git clone --recursive --depth 1 https://github.com/ymd-h/exodide.git
cd exodide

make

pip install .
```


## 5. Trial & Error

### #1: Solved: pyodide/pyodide-env doesn't have Python and Emscripten

Official source build image
[pyodide/pyodide-env](https://hub.docker.com/r/pyodide/pyodide-env)
doesn't have Python and Emscripten, since these tools will be built, too.

For the convenience, we utilize official
[python](https://hub.docker.com/_/python) image and setup Emscripten
on it with Emsdk (Emscripten SDK). Emsdk downloads large compiler
toolchain, so that we recommend downloading it to mounted host
directory and reusing afterwards.



### #2: Solved: `error: "LONG_BIT definition appears wrong for platform (bad gcc/glibc config?)."`

Header files installed at host are incompatible. We use patched and
correctly configured headers.

### #3: Solved: `SIZEOF_VOID_P` is not equal to `sizeof(void*)`

Header files installed at host are incompatible. We use patched and
correctly configured headers.


### #4: Solved: `__multiarray_api.h` and `__ufunc_api.h` are missing.

They are auto generated headers. We copied
`numpy/numpy/core/code_generators` codes and modified them to work
stand-alone.


### #5: Solved: `NPY_API_VERSION` and `NPY_ABI_VERSION` are not defined.

In ordinary build, these are defined at `_numpyconfig.h`, but Pyodide
provides custom `_numpyconfig.h` without these definitions.

We manually extract the original definitions (aka. `C_API_VERSION` and
`C_ABI_VERSION`) from `numpy/numpy/core/setup_common.py` and append
them to `_numpyconfig.h`


### #6: Solved: `error: pthreads + MODULARIZE currently require you to set -sEXPORT_NAME=Something (see settings.js) to Something != Module, so that the .worker.js file can work`

Even though we remove `-pthread` from `Extension.extra_link_args`,
still linker gets `-pthread` option from somewhere...

It seems that `customize_compiler()` sets comlier executables, we
manually remove `-pthread` at `build_ext.build_extensions()`.


### #7: Solved: `error: --plat-name only supported on Windows (try using './configure --help' on your platform)`

Instead of setting at `build.finalize_options()`, we patch
`get_platform()` by `unittest.mock`.


### #8: Solved: `ImportError: Could not load dynamic lib: FOO.so`


The current stable Pyodide v0.20.0 uses old Emscripten v2.0.27, which
supports only legacy "dylink" section, but "dylink.0" section yet.

LLVM in the latest Emscripten emits "dylink.0", then Pyodide fails `dlopen()`

Ref: [Web Assembly Dynamic Linking](https://github.com/WebAssembly/tool-conventions/blob/main/DynamicLinking.md) and its [PR](https://github.com/WebAssembly/tool-conventions/pull/170).


By using Pyodide v0.21.0-alpha2, which compiled with Emscripten
v3.1.14, "dylink.0" custom section is recognized correctly.


### #9: Solved: `RangeError: WebAssembly.Compile is disallowed on the main thread, if the buffer size is larger than 4KB. Use WebAssembly.compile, or compile on a worker thread.`


This is the Chromium limitation. See [Limitations](https://emscripten.org/docs/compiling/Dynamic-Linking.html#limitations).


We must compile asyncrhonically, so that we use Pyodide internal API
`loadDynlib(lib, sharad)`.



### #10: WIP: `Pyodide has suffered a fatal error.` / `TypeError: Cannot read properties of undefined (reading 'apply')`

It seems that stack overflow happens, since `__handle_stack_overflow`,
called from Wasm, raises the `TypeError`.

Maybe `_emscripten_stack_get_end()` and/or
`_emscripten_stack_get_base()` have the problem. (We couldn't find
these definitions, yet....)
