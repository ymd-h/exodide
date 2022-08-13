# exodide Example: spaCy

[spaCy](https://spacy.io/) is a library for Natural Language
Processing (NLP).


Here, we build spaCy and its dependencies with exodide and run it on
Pyodide. Fortunately, spaCy uses relatively simple build system.

```shell
docker build -t example-spacy:latest .
docker run -it -p 8000:8000 example-spacy:latest
```

then open `localhost:8000/index.html` with your browser.

## Notes

We couldn't download model library on Pyodide, because
* Python `requests` (or network functionality) cannot work on Pyodide
* Official repository (aka. GitHub Releases) doesn't reply with
  `Access-Control-Allow-Origin` header, so that Browser blocks it by
  CORS policy.


## Reference
* [explosion/spaCy](https://github.com/explosion/spaCy)
  * MIT
* [explosion/cymem](https://github.com/explosion/cymem)
  * MIT
* [explosion/preshed](https://github.com/explosion/preshed)
  * MIT
* [explosion/murmurhash](https://github.com/explosion/murmurhash)
  * MIT
* [explosion/thinc](https://github.com/explosion/thinc)
  * MIT
* [explosion/cython-blis](https://github.com/explosion/cython-blis)
  * 3-Clause BSD
* [explosion/srsly](https://github.com/explosion/srsly)
  * MIT

