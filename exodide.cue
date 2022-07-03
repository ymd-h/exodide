import (
  "dagger.io/dagger"
  "dagger.io/dagger/core"
  "universe.dagger.io/docker"
)


dagger.#Plan {
  client: filesystem: {
    ".": {
      read: {
        exclude: [".git", ".github", "cue.mod", "*.cue", "dist", "build", "example"]
      }
    }
    "dist": write: contents: actions.build.output
  }
  actions: {
    build: {
      image: docker.#Build & {
        steps: [
          docker.#Dockerfile & {
            source: client.filesystem.".".read.contents
          },
          docker.#Copy & {
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
      dir: core.#Subdir & {
        input: image.output.rootfs
        path: "dist"
      }
      output: dir.output
    }
  }
}
