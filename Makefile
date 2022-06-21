PKG := extodide

.PHONY: all
all: cpython numpy


.PHONY: cpython
cpython:
	cd cpython && \
	find ../pyodide/cpython/patches -type f -name "*.patch" -print0 | \
	sort -zn | xargs -0 -I '{}' patch -p1 --binary --verbose -i '{}'

	cp pyodide/cpython/config.site cpython/

	cd cpython && \
	CONFIG_SITE=./config.site READELF=true emconfigure ./configure \
	PLATFORM_TRIPLET=wasm32-emscripten \
	--without-pymalloc \
	--disable-shared \
	--disable-ipv6 \
	--enable-big-digits=30 \
	--enable-optimizations \
	--host=wasm32-unknown-emscripten \
	--build=$(shell cpython/config.guess)

	cat pyodide/cpython/pyconfig.undefs.h >> cpython/pyconfig.h

	mkdir -p $(PKG)/cpython
	cp -r cpython/Include/* $(PKG)/cpython/


.PHONY: numpy
numpy:
	cd numpy && \
	find ../pyodide/packages/numpy/patches -type f -name "*.patch" -print0 | \
	sort -zn | xargs -0 -I '{}' patch -p1 --binary --verbose -i '{}'
	cp pyodide/packages/numpy/config/_numpyconfig.h numpy/numpy/core/include/

	mkdir -p $(PKG)/numpy
	cp -r numpy/numpy/core/include/* $(PKG)/numpy/


.PHONY: clean
clean:
	rm -rf $(PKG)/cpython/*
	rm -rf $(PKG)/numpy/*
