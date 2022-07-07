#include <pybind11/pybind11.h>

#include <iostream>

namespace py = pybind11;


void hello_world(){
  std::cout << "Hello World!" << std::endl;
}

int add_int(int a, int b){
  return a+b;
}

size_t fibonacci(size_t n){
  if(n<=1){ return n; }
  return fibonacci(n-1) + fibonacci(n-2);
}

PYBIND11_MODULE(example, m){
  m.doc() = "exodide example module";
  m.def("hello_world", &hello_world, "Hello World");
  m.def("add_int", &add_int, "Add int");
  m.def("fibonacci", &fibonacci, "Fibonacci");
}
