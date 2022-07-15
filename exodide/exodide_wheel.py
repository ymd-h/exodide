from distutils import log
from distutils.command import build_ext as dist_build_ext
import os

from setuptools.command import build_ext as setup_build_ext
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
import wblog

from exodide.build import (build, build_ext,
                           adjust_include, exodide_links, exodide_unsupported_links,
                           exodide_extension_filename)

logger = wblog.getLogger()

class exodide_wheel(_bdist_wheel):
    """
    wheel Command for exodide
    """
    def initialize_options(self):
        if os.environ.get("EXODIDE_DEBUG", False):
            wblog.start_logging("exodide")
            logger.debug("Enable Logging")
            log.set_verbosity(2)

        self.distribution.cmdclass["build"] = build
        self.distribution.command_obj.pop("build", None)

        build_ext_old = self.distribution.get_command_class("build_ext")
        if not issubclass(build_ext_old, build_ext):
            self.distribution.command_obj.pop("build_ext", None)
            if type(build_ext_old) in [dist_build_ext, setup_build_ext]:
                logger.debug("build_ext is standard. exodide replaces it.")
                self.distribution.cmdclass["build_ext"] = build_ext
            else:
                logger.debug("build_ext is custom. exodide wraps it.")
                class _build_ext(build_ext_old):
                    def run(_self):
                        _self.include_dirs = adjust_include(_self.include_dirs)
                        return build_ext_old.run(_self)

                    def build_extensions(_self):
                        remove_opt = exodide_unsupported_links()
                        _self.compiler.linker_so = [so for so in
                                                    _self.compiler.linker_so
                                                    if (so not in remove_opt)]
                        return build_ext_old.build_extensions(_self)

                    def build_extension(_self, ext):
                        ext.include_dirs = adjust_include(ext.include_dirs)
                        ext.extra_link_args = ext.extra_link_args + exodide_links()
                        return build_ext_old.build_extension(_self, ext)

                    def get_ext_filename(_self, ext_name):
                        return exodide_extension_filename(ext_name)

                self.distribution.cmdclass["build_ext"] = _build_ext

        return super().initialize_options()
