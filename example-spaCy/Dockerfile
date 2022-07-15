FROM python:3.10 AS deps
RUN pip download numpy cython \
    cymem==2.0.6 \
    preshed==3.0.6 \
    murmurhash==1.0.7 \
    thinc==8.1.0 \
    blis==0.7.8 \
    -d /deps


FROM ghcr.io/ymd-h/exodide:v1.0.2 AS build-base
COPY --from=deps /deps /deps/
RUN pip install /deps/*


FROM build-base AS spacy
COPY third_party/spaCy /spaCy
WORKDIR /spaCy
RUN source /emsdk/emsdk_env.sh && \
    CC=emcc CXX=em++ python setup.py \
    --command-packages exodide exodide_wheel -d /dist


FROM build-base AS cymem
COPY third_party/cymem /cymem
WORKDIR /cymem
RUN source /emsdk/emsdk_env.sh && \
    CC=emcc CXX=em++ python setup.py \
    --command-packages exodide exodide_wheel -d /dist


FROM build-base AS preshed
COPY third_party/preshed /preshed
WORKDIR /preshed
RUN source /emsdk/emsdk_env.sh && \
    CC=emcc CXX=em++ python setup.py \
    --command-packages exodide exodide_wheel -d /dist


FROM build-base AS murmurhash
COPY third_party/murmurhash /murmurhash
WORKDIR /murmurhash
RUN source /emsdk/emsdk_env.sh && \
    CC=emcc CXX=em++ python setup.py \
    --command-packages exodide exodide_wheel -d /dist


FROM build-base AS thinc
COPY third_party/thinc /thinc
WORKDIR /thinc
RUN source /emsdk/emsdk_env.sh && \
    CC=emcc CXX=em++ python setup.py \
    --command-packages exodide exodide_wheel -d /dist


FROM build-base AS cython-blis
COPY third_party/cython-blis /cython-blis
WORKDIR /cython-blis
RUN source /emsdk/emsdk_env.sh && \
    ./bin/update-vendored-source && \
    ./bin/generate-make-jsonl linux generic --export && \
    BLIS_ARCH=generic CC=emcc CXX=em++ python setup.py \
    --command-packages exodide exodide_wheel -d /dist


FROM build-base AS srsly
COPY third_party/srsly /srsly
WORKDIR /srsly
RUN source /emsdk/emsdk_env.sh && \
    CC=emcc CXX=em++ python setup.py \
    --command-packages exodide exodide_wheel -d /dist


FROM python:3.10 AS model
RUN pip download https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.4.0/en_core_web_sm-3.4.0-py3-none-any.whl --no-deps -d /dist


FROM scratch AS result
COPY --from=spacy /dist /dist/
COPY --from=cymem /dist /dist/
COPY --from=preshed /dist /dist/
COPY --from=murmurhash /dist /dist/
COPY --from=thinc /dist /dist/
COPY --from=cython-blis /dist /dist/
COPY --from=srsly /dist /dist/
COPY --from=model /dist /dist/


FROM python:3.10 AS server
COPY --from=result /dist /app/
COPY index.html /app/
WORKDIR /app
CMD ["python", "-m", "http.server"]
