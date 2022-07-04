package exodide

import (
  "dagger.io/dagger"
  "dagger.io/dagger/core"
  "universe.dagger.io/docker"
)


dagger.#Plan & {
  client: filesystem: {
    ".": {
      read: {
        exclude: [".git", ".github", "cue.mod", "*.cue", "dist", "build", "example"]
      }
    }
    "dist": write: contents: actions.build.dist
  }
  actions: {
    image: docker.#Dockerfile & {
      source: client.filesystem.".".read.contents
    }
    build: {
      _image: docker.#Build & {
        steps: [
          docker.#Copy & {
            input: image.output
            contents: client.filesystem.".".read.contents
          },
          docker.#Run & {
            command: {
              name: "make"
            }
          },
          docker.#Run & {
            command: {
              name: "python3"
              args: ["setup.py", "bdist_wheel"]
            }
          },
          docker.#Run & {
            command: {
              name: "pip3"
              args: ["install", "."]
            }
          }
        ]
      }
      _dist: core.#Subdir & {
        input: _image.output.rootfs
        path: "dist"
      }
      dist: _dist.output
      _output: docker.#Copy & {
        input: image.output
        contents: _image.output
        exclude: ["numpy", "cpython", "pyodide", "script", "Makefile",
                  "build", "dist", ".git"]
      }
      output: _output.output
    }
    test: {
      _image: docker.#Build & {
        steps: [
          docker.#Run & {
            input: build.output
            command: {
              name: "python3"
              args: ["-m", "unittest", "discover", "test"]
            }
          }
        ]
      }
    }
  }
}
