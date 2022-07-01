#include <pybind11/pybind11>

#include <iostream>

namespace py = pybind11;


void hello_world(){
  std::cout << "Hello World!" << std::endl;
}


PYBIND11_MODULE(example, m){
  m.doc() = "exodide example module";
  m.def("hello_world", &hello_world, "Hello World")
}
