import unittest

base = "http://localhost:8080/dist/"

import micropip
await micropip.install(base + "exodide-0.0.3-py3-none-any.whl")


from exodide.install import fetch_install
await fetch_install(base + "exodide_example-0.0.0-cp310-cp310-emscripten_wasm32.whl")

import exodide_example as ee

class TestExample(unittest.TestCase):
    def test_hello_world(self):
        ee.hello_world()

ret = not unittest.main(exit=False).result.wasSuccessful()

