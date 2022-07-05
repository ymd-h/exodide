const pyodide_pkg = await import("pyodide/pyodide.js");
const pyodide = await pyodide_pkg.loadPyodide();

await pyodide.loadPackage("micropip");
await pyodide.runPythonAsync(await (await fetch("http://localhost:8080/example/test_example.py")).text());
