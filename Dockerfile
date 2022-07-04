From python:3.10.2 AS base

ENV EMSCRIPTEN_VERSION=3.1.13 \
    PATH=$PATH:/emsdk/upstream/emscripten

RUN git clone --depth 1 https://github.com/emscripten-core/emsdk.git /emsdk && \
    cd /emsdk && \
    git pull && \
    ./emsdk install ${EMSCRIPTEN_VERSION} && \
    ./emsdk activate ${EMSCRIPTEN_VERSION} && \
    rm -rf /emsdk/.git


FROM base AS build

ADD Makefile exodide numpy cpython pyodide script /exodide

WORKDIR /exodide

RUN make && rm -rf numpy cpython pyodide script && rm -f Makefile

ADD setup.py README.md LICENSE

RUN python3 setup.py bdist_wheel -d /dist && rm -rf /exodide



FROM base AS exodide

COPY --from=build /dist /dist

RUN pip3 install /dist/* && rm -rf /dist


FROM exodide AS test

ADD test /test

WORKDIR /test

RUN python3 -m unittest discover . && rm -rf /test


FROM exodide AS example

ADD example /example

WORKDIR /example

RUN CC=emcc CXX=em++ python3 setup.py bdist_wheel -d /dist && rm -rf /example
