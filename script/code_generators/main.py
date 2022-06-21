import os
import sys

codegen_dir = os.path.dirname(__file__)
output_dir = os.path.join(codegen_dir, "..", "..", "numpy", "numpy", "core", "src")

def main():
    sys.path.insert(0, codegen_dir)

    def generate_api(module_name):
        script = os.path.join(codegen_dir, module_name + '.py')

        m = __import__(module_name)
        h_file, c_file, doc_file = m.generate_api(output_dir)
        return (h_file,)

    generate_api('generate_numpy_api')
    generate_api('generate_ufunc_api')

if __name__ == "__main__":
    main()
