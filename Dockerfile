From python:3.10.2 AS base
ENV EMSCRIPTEN_VERSION=3.1.13
RUN git clone --depth 1 https://github.com/emscripten-core/emsdk.git /emsdk && \
    cd /emsdk && \
    git pull && \
    ./emsdk install ${EMSCRIPTEN_VERSION} && \
    ./emsdk activate ${EMSCRIPTEN_VERSION} && \
    rm -rf /emsdk/.git


FROM base AS build-base
SHELL ["/bin/bash", "-c"]
COPY Makefile /exodide/
COPY exodide  /exodide/exodide/
COPY numpy    /exodide/numpy/
COPY cpython  /exodide/cpython/
COPY pyodide  /exodide/pyodide/
COPY script   /exodide/script/
WORKDIR /exodide
RUN source /emsdk/emsdk_env.sh && \
    make && rm -rf numpy cpython pyodide script && rm -f Makefile


FROM build-base AS build
COPY setup.py README.md LICENSE /exodide/
RUN python3 setup.py bdist_wheel -d /dist && rm -rf /exodide


FROM build-base AS build-no-readme
COPY setup.py LICENSE /exodide/
RUN python3 setup.py bdist_wheel -d /dist && rm -rf /exodide


FROM base AS exodide
SHELL ["/bin/bash", "-c"]
COPY --from=build /dist /dist/
RUN pip3 install /dist/* wheel && rm -rf /dist


FROM base AS exodide-no-readme
SHELL ["/bin/bash", "-c"]
COPY --from=build /dist /dist/
RUN pip3 install /dist/* wheel && rm -rf /dist



FROM exodide-no-readme AS test
COPY test /test/
WORKDIR /test
RUN pip3 install coverage unittest-xml-reporting numpy && \
    coverage run -m xmlrunner discover . && \
    coverage report && \
    mkdir -p /coverage/html && coverage html -d /coverage/html && \
    mkdir -p /coverage/xml && cp *.xml /coverage/xml/ && \
    rm -rf /test


FROM exodide-no-readme AS example-build
COPY example/setup.py /example/
COPY example/pybind11 /example/pybind11/
COPY example/exodide_example /example/exodide_example/
WORKDIR /example
RUN source /emsdk/emsdk_env.sh && \
    CC=emcc CXX=em++ python3 setup.py bdist_wheel -d /dist && rm -rf /example


FROM node:latest AS pyodide-node
WORKDIR /pyodide-node
RUN npm i pyodide@0.21.0-alpha.2 && \
    npm i -g http-server && \
    curl -LO https://github.com/pyodide/pyodide/releases/download/0.21.0a2/pyodide-build-0.21.0a2.tar.bz2 && \
    tar xvf pyodide-build-0.21.0a2.tar.bz2 && \
    rm -f pyodide-build-0.21.0a2.tar.bz2


FROM pyodide-node AS example-test
ENV DIST=/pyodide-node/dist/ TEST=example/test
COPY --from=build /dist $DIST
COPY --from=example-build /dist $DIST
COPY ${TEST}/test.mjs ${TEST}/test_example.py ${TEST}/run.sh /pyodide-node/example/
RUN sed -i \
    -e s/"<exodide>"/$(find $DIST -name "exodide-*.whl" -exec basename {} \;)/ \
    -e s/"<example>"/$(find $DIST -name "*_example-*.whl" -exec basename {} \;)/\
    example/test_example.py && \
    bash ./example/run.sh /pyodide-node && \
    touch /example-test


FROM scratch AS result
COPY --from=build /dist /dist/
COPY --from=example-build /dist /dist/
COPY --from=test /coverage /coverage/
COPY --from=example-test /example-test /example-test
CMD [""]
