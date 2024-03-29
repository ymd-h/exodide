import glob
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
        self.assertEqual(build.adjust_include([build.system_include()]),
                         build.exodide_include())

    def test_exodide_links(self):
        links = build.exodide_links()
        self.assertIsInstance(links, list)
        self.assertEqual(len(links) % 2, 0)
        for i in range(0, len(links), 2):
            self.assertEqual(links[i], "-s")

    def test_exodided_unsupported_links(self):
        self.assertEqual(build.exodide_unsupported_links(),
                         ["-shared", "-pthread",
                          "-Wl,-Bsymbolic-functions",
                          "-Wl,--strip-all",
                          "-Wl,-strip-all",
                          "-Wl,--sort-common",
                          "-Wl,--as-needed"])

    def test_platform_tag(self):
        self.assertEqual(build.exodide_platform_tag(), "emscripten_3.1.14_wasm32")

    def test_extension_filename(self):
        self.assertEqual(build.exodide_extension_filename("test.somodule"),
                         "test/somodule.cpython-310-wasm32-emscripten.so")


class TestInstall(unittest.TestCase):
    @unittest.skipIf(platform.system() == 'Emscripten',
                     "Emscripten can import inspect")
    def test_import_error(self):
        with self.assertRaises(ImportError):
            from exodide import install


class TestInspect(unittest.TestCase):
    def test_metadata(self):
        so = glob.glob("/example/exodide_example/*.so")
        self.assertIsInstance(so, list)
        self.assertEqual(len(so), 1)
        meta = inspect.MetaData(so[0])
        self.assertTrue(meta.valid)


if __name__ == "__main__":
    unittest.main()
