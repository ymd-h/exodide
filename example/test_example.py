import unittest

base = "http://localhost:8080/dist/"

import micropip
await micropip.install(base + "<exodide>")


from exodide.install import fetch_install
await fetch_install(base + "<example>")

import exodide_example as ee

class TestExample(unittest.TestCase):
    def test_hello_world(self):
        ee.hello_world()

ret = not unittest.main(exit=False).result.wasSuccessful()

