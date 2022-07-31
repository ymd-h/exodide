# exodide-example

Setup emscripten, then execute the following,

```shell
CC=emcc CXX=em++ python3 setup.py bdist_wheel
python3 -m http.server
```

1. Simple Exapmle: Access `localhost:8000/index.html` with browser and see console.
2. Example with [PyScript](https://github.com/pyscript/pyscript): Access `localhost:8000/index_pyscript.html` with browser.



## With Docker
We also provide Dockerfile to build and serve this example.

```shell
docker build -t exodide-example .
docker run -it -p 8000:8000 exodide-example
```
