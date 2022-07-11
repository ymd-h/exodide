from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

from exodide.build import build, build_ext


class exodide_wheel(_bdist_wheel):
    """
    wheel Command for exodide
    """
    def initialize_options(self):
        self.distribution.cmdclass["build"] = build
        self.distribution.cmdclass["build_ext"] = build_ext
        self.distribution.command_obj.pop("build", None)
        self.distribution.command_obj.pop("build_ext", None)

        return super().initialize_options()
