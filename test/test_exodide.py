import unittest
import platform

from exodide import build, inspect

class TestBuild(unittest.TestCase):
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
