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
    "dist": write: contents: actions.build.output
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
          }
        ]
      }
      _dir: core.#Subdir & {
        input: _image.output.rootfs
        path: "dist"
      }
      output: _dir.output
    }
    test: {
      _image: docker.#Build & {
        steps: [
          docker.#Copy & {
            input: image.output
            contents: build.output
            dest: "dist"
          },
          docker.#Run & {
            command: {
              name: "find"
              args: ["dist", "-name", "exodide-*.whl",
                     "-exec", "pip3 install {} +"]
            }
          }
        ]
      }
    }
  }
}
