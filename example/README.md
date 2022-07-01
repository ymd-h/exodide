# exodide-example

Setup emscripten, then execute the following,

```shell
CC=emcc CXX=em++ python3 setup.py bdist_whell
python3 -m http.server
```

Access `localhost:8000/index.html` with browser and see console.
