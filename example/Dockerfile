FROM ghcr.io/ymd-h/exodide:v1.0.3 AS build
COPY exodide_example /src/exodide_example/
COPY pybind11 /src/pybind11/
COPY setup.py /src/
WORKDIR /src
RUN source /emsdk/emsdk_env.sh && \
    CC=emcc CXX=em++ python setup.py bdist_wheel -d /dist

FROM python:3.10 AS server
COPY --from=build /dist /app/dist/
COPY index.html index_pyscript.html /app/
WORKDIR /app
CMD ["python", "-m", "http.server"]
