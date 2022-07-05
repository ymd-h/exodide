const { loadPyodide } = await import("pyodide/pyodide.js");
const pyodide = await loadPyodide({ indexURL: "/pyodide-node/pyodide" });

await pyodide.loadPackage("micropip");
await pyodide.runPythonAsync(await (await fetch("http://localhost:8080/example/test_example.py")).text());
