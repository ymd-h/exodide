From python:3.10.2 AS base
ENV EMSCRIPTEN_VERSION=3.1.13 \
    PATH=$PATH:/emsdk/upstream/emscripten
RUN apt update && \
    apt install --no-install-recommends -y build-essential gfortran && \
    apt clean && \
    rm -rf /var/lib/apt/lists/* && \
    git clone --depth 1 https://github.com/emscripten-core/emsdk.git /emsdk && \
    cd /emsdk && \
    git pull && \
    ./emsdk install ${EMSCRIPTEN_VERSION} && \
    ./emsdk activate ${EMSCRIPTEN_VERSION} && \
    rm -rf /emsdk/.git


FROM node:latest AS pyodide-node
RUN npm i -g pyodide@0.21.0-alpha.2 http-server


FROM base AS build
ADD Makefile exodide numpy cpython pyodide script /exodide/
WORKDIR /exodide
RUN make && rm -rf numpy cpython pyodide script && rm -f Makefile
ADD setup.py README.md LICENSE /exodide/
RUN python3 setup.py bdist_wheel -d /dist && rm -rf /exodide


FROM base AS exodide
COPY --from=build /dist /dist
RUN pip3 install /dist/* && rm -rf /dist


FROM exodide AS test
ADD test /test
WORKDIR /test
RUN pip3 install coverage unittest-xml-reporting && \
    coverage run -m unittest discover . && \
    coverage report && \
    mkdir -p /coverage/html && coverage html -d /coverage/html && \
    mkdir -p /coverage/xml && cp *.xml /coverage/xml/ && \
    rm -rf /test


FROM exodide AS example-build
ADD example /example
WORKDIR /example
RUN CC=emcc CXX=em++ python3 setup.py bdist_wheel -d /dist && rm -rf /example


FROM pyodide-node AS example-test
COPY --from=build /dist/exodide-*.whl /dist/exodide.whl
COPY --from=example-build /dist/exodide_example-*.whl /dist/exodide_example.whl
ADD example/test.js example/test_example.py /example/
WORKDIR /
RUN http-server / &; \
    node --experimental-repl-await test.js


FROM scratch AS result
COPY --from=build /dist/exodide-*whl /dist/
COPY --from=test /coverage /coverage
