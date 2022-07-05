import unittest

import micropip
await micropip.install("localhost:8080/dist/exodide.whl")

import exodide
await exodide.fetch_install("localhost:8080/dist/exodide_example.whl")

import exodide_example as ee

class TestExample(unittest.TestCase):
    def test_hello_world(self):
        ee.hello_world()

unittest.main()
