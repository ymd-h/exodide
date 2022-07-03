# Design

This document describes design and technical details of exodide.

## 1. Basic Concepts
To build C/C++ extension easily, we think it is better to separate the
build system from Pyodide itself because of the size and complexity of
Pyodide.

As far as we know, Pyodide package build is a part of Pyodide
build. Although the package build system (aka. `pyodide-build`) is
packaged and distibuted separately, we couldn't figure out to build
custom C/C++ extension modules by the package alone easily. (It raised
error because of missing some environment values, which is usually set
in Pyodide Makefile.)


In addition, we believe separate works will make the ecosystem larger.
We hope standard format will be defined by PEP and C/C++ extension
packages for Pyodide will be hosted at PyPI in the future.


Theoretically, we need only appropriate compiler with correct compiler
options and proper header files.


## 2. Header
In additon to CPython headers, we think NumPy headers are useful to
build C/C++ extension modules. One of the major motivations to make
C/C++ extension is performance, and a large number of packages
utilizes [NumPy C-API](https://numpy.org/doc/stable/reference/c-api/)
through [Cython](https://cython.readthedocs.io/),
[pybind11](https://pybind11.readthedocs.io/) and so on.

Pyodide hosts only patches and doesn't redistribute patched header
files at all.

We patch and redistribute these header files (toghether with their
licenses), so that our users can access correct headers when they
build their C/C++ extension package.


### Header details
In addition to patching, CPython requires `configure` to generate
headers.

Normally, NumPy generates `__multiarray_api.h` and `__ufunc_api.h`
during its build. We modified the code generation scripts and make
them work independently.

Pyodode provides custom `_numpyconfig.h`, however, it doesn't contains
`NPY_API_VERSION` and `NPY_ABI_VERION` for some reason, we append
these definitions as NumPy do (aka. copy from `C_API_VERSION` and
`C_ABI_VERSION` in `numpy/numpy/core_setup_common.py`, respectively).


## 3. Build Options / Build System
In terms of build options, we follows Pyodide. For example,
`-sSIDE_MODULE`, `-sMODULARIZE`, `-sLINKABLE` and so on.

Pyodide utilizes Makefile, however, exodide provides
`distutils`/`setuptools` command classes to enable users to build with
standard `setup()` function.

Inside thse custom command classes, exodide modified include
directories and so on. Additionally, exodide replaces platform name to
produce correct file names. (cf. Pyodide unpacks wheel, renames shared
objects, and repacks them after build.)


Users might have several versions of Emscripten. Simply we let users
specify Emscripten compilers. Fortunately, by setting `CC` and `CXX`
environment values, `build_ext` command class uses them;

```shell
CC=emcc CXX=em++ python3 setup.py bdist_wheel
```


### Build details
`-pthread` option has not supported at Pyodide yet, but it is
automatically added by `customize_compiler()` even though we don't
specify at `Extension.extra_link_args`, so that we manually remove the
option at custom `build_ext.build_extensions()` function.

Specifying `--plat-name` is only supported on Windows, otherwise
`build_ext` raises error. We patch `get_platform()` function, wich
returns default platform name when `--plat-name` is not specified, by
`unittest.mock`. This hack might be abuse of `mock`, so that if we can
find another option, we might change this in future.


## 4. Dynamic Linking
Emscripten provides
[dynamic linking](https://emscripten.org/docs/compiling/Dynamic-Linking.html)
based on [Web Assembly Dynamic Linking specification](https://github.com/WebAssembly/tool-conventions/blob/main/DynamicLinking.md),
which is still in progress.

Futhermore, Emscripten ports `dlopen()`, `dlsym()` etc., so that
Pyodide can `import` dynamic linking module (aka. C/C++ extension
module) as it works on Linux.

One of the biggest limitations is that Chromium doesn't allow us to
compile WebAssembly module lager than 4kB synchronically. Since
CPython `import` is syncrhonical, we must compile and load these
WebAssembly modules asynchronically beforehand. Pyodide manages this
limitation by calling JavaScript async method
`pyodide.loadPacakge("package-name")` outside of Python.

exodide calls Pyodide internal JavaScript API through `JSProxy`, and
compiles WebAssembly during install process.


### Dynamic Linking details
Currently, WebAssembly Dynamic Linking utilizes cutom section to store
necessary metadata like memory layout, depending libraries etc. The
custom section name was `dylink`, then was updated to `dylink.0`.

Old Emscripten can manage only `dylink` section, so that we recommend
to use new Emscripten to build main module, which can manage legacy
`dylink`, too.

Unfortunately, current (July 2022) stable Pyodide v0.20.0 is compiled
with old Emscripten v2.0.27. We dicided to use Pyodide v0.21.0-alpha2
which compiled with latest Emscripten v3.1.14.


exodide can dump such `dylink`/`dylink.0` section with
`exodide.inspect` module. This feature was used to debug exodide
itself, but we have no idea about other usages. We might add some
useful information in the future.
