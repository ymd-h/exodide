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

    def test_add_int(self):
        for LHS, RHS in [(1, 1),
                         (10, 100),
                         (-5, 10)]:
            with self.subTest(LHS=LHS, RHS=RHS):
                self.assertEqual(ee.add_int(LHS, RHS), LHS+RHS)

    def test_fibonacci(self):
        for i, Truth in enumerate([ 0,  1,   1,  2,    3,
                                    5,  8,  13,  21,  34,
                                   55, 89, 144, 233, 377]):
            with self.subTest(i=i):
                self.assertEqual(ee.fibonacci(i), Truth)


ret = not unittest.main(exit=False).result.wasSuccessful()
