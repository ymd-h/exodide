import unittest
import os
import platform
import sys

from exodide import build, inspect

class TestBuild(unittest.TestCase):
    def test_cmdclass(self):
        self.assertEqual(build.cmdclass(),
                         {"build": build.build, "build_ext": build.build_ext})

    def test_system_include(self):
        self.assertIsInstance(build.system_include(), str)
        self.assertEqual(build.system_include(), build.system_include())
        self.assertEqual(build.system_include(),
                         os.path.join(sys.prefix, "include", "python"))

    def test_exodide_include(self):
        self.assertIsInstance(build.exodide_include(), list)
        self.assertEqual(len(build.exodide_include()), 2)
        self.assertEqual(list(map(lambda s: os.path.basename(s),
                                  build.exodide_include())),
                         ["cpython", "numpy"])

    def test_adjust_include(self):
        self.assertEqual(build.adjust_include(build.system_include()),
                         build.exodide_include())

    def test_plat_name(self):
        self.assertEqual(build.plat_name(), "emscripten-wasm32")


class TestInstall(unittest.TestCase):
    @unittest.skipIf(platform.system() == 'Emscripten',
                     "Emscripten can import inspect")
    def test_import_error(self):
        with self.assertRaises(ImportError):
            from exodide import install


class TestInspect(unittest.TestCase):
    pass


if __name__ == "__main__":
    unittest.main()
