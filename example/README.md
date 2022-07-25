# exodide-example

Setup emscripten, then execute the following,

```shell
CC=emcc CXX=em++ python3 setup.py bdist_wheel
python3 -m http.server
```

Access `localhost:8000/index.html` with browser and see console.


> *Note*
> If you use Docker container, please pass `-p 8000:8000` option to `docker run` command in order to access the container port from local machine.
