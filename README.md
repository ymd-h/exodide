# exodide: build_ext for Pyodide

![PyPI](https://img.shields.io/pypi/v/exodide)

## 1. Overview


[Pyodide](https://pyodide.org/en/stable/index.html) is a WebAssembly
variant of [CPython](https://www.python.org/). By using it, we can run
Python code inside web browser.

Although we can run most of pure-Python packages on Pyodide, however,
available C/C++ extension packages are limited to
[builtin packages](https://pyodide.org/en/stable/usage/packages-in-pyodide.html).
(Update: From v0.21.0, Pyodide started to accept non-builtin C/C++ packages.)

The motivation of this project (exodide) is providing C/C++ extension
builder for Pyodide, and enables users to run your own custom
C/C++ extension packages on Pyodide.

## 2. Usage

### 2.1 Requirement Summary

* 2.3: Build
  * [Emscripten](https://emscripten.org/) v3.1.14
  * [wheel](https://github.com/pypa/wheel)
  * C/C++ package source working on CPython 3.10.2
* 2.4: Run
  * Pyodide v0.21.0
* 2.5: Inspect
  * [NumPy](https://numpy.org/)


### 2.2 Install exodide

#### 2.2.1 Install from PyPI
You can install exodide from [PyPI](https://pypi.org/project/exodide/)

* `pip install exodide`
* `pip install exodide[build]`
  * With build dependencies
* `pip install exodide[inspect]`
  * With inspect dependencies
* `pip install exodide[all]`
  * With all dependencies

#### 2.2.2 Use docker image
We provide docker image

```shell
docker run -it -v <your package source path>:/src ghcr.io/ymd-h/exodide:latest bash

# Inside docker container
source /emsdk/emsdk_env.sh # Set PATH for emcc/em++
```

#### 2.2.3 Install from Source
Since this repository doesn't contains patched headers, you cannot
install directly from GitHub like `pip install git+https://github.com/ymd-h/exodide`.

```shell
git clone --recursive --depth 1 https://github.com/ymd-h/exodide.git
cd exodide

make

pip install .
```

### 2.3 Build with exodide
The followings are reuired;

* Emscripten v3.1.14
  * Set up `emcc` and `em++` as [the official document](https://emscripten.org/docs/getting_started/downloads.html)
* C/C++ extension package source working on Python 3.10
* `wheel` (`pip install exodide[build]` install it, too.)


#### 2.3.1 Method 1: Main Usage
```python:setup.py
from setuptools import setup
from exodide import build

# omit

setup(
    # omit
    cmdclass=build.cmdclass(), # {'build': build.build, 'build_ext': build.build_ext}
)
```

then `CC=emcc CXX=em++ python setup.py bdist_wheel`.


#### 2.3.2 Method 2: Fine tuning for Power User
If your package has special build flow, you might need to call exodide internal API.

All internal build API are implemented at `exodide.build` module.

* `system_include() -> str`: System include directory of host Python
* `exodide_include() -> List[str]`: Include directories inside exodide package.
* `adjust_include(include: List[str]) -> List[str]`: Adjust include directories
  * Internally `system_include()` and `exodide_include()` are used
* `exodide_links() -> List[str]`: Linker arguments
* `exodide_unsupported_links() -> List[str]`: Unsupported linker arguments
* `exodide_platform_tag() -> str`: Platform name tag for wheel



#### 2.3.3 Method 3: Quick Usage
We also provide custom setup command `exodide_wheel`.
The following command have same effect with the first option at '2.3.1 Main Usage'.

```shell
CC=emcc CXX=em++ python setup.py --command-packages exodide exodide_wheel
```


#### 2.3.4 Notes

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

### 2.4 Install extension package to Pyodide
> **Note**
> Since from Pyodide v0.21.0 `micropip.install()` accepts custom URL,
> `exodide.install` module become deprecated.


Pyodide v0.21 is required.


```javascript
const pyodide = await loadPyodide();

await pyodide.runPythonAsync(`
import micropip
micropip.install("example.com/your-package.whl")

import your_package
# omit
`);
```

### 2.5 Inspect Shared Object (for Debugging)
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


## 4. Technical Details
Technical details are described [here](https://github.com/ymd-h/exodide/blob/master/design.md)
