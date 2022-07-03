From python:3.10.2

ENV EMSCRIPTEN_VERSION=3.1.13 \
    PATH=$PATH:/emsdk/upstream/emscripten

RUN git clone --depth 1 https://github.com/emscripten-core/emsdk.git /emsdk && \
    cd /emsdk && \
    git pull && \
    ./emsdk install ${EMSCRIPTEN_VERSION} && \
    ./emsdk activate ${EMSCRIPTEN_VERSION}
