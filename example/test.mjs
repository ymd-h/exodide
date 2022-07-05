const { loadPyodide } = await import("pyodide/pyodide.js");
const pyodide = await loadPyodide({ indexURL: "/pyodide-node/pyodide" });

console.log("before loadPackage");
try{
    await pyodide.loadPackage("micropip");
}catch(error){
    console.error({error});
    throw error;
}
console.log("after loadPackage");

try{
    const ret = await pyodide.runPythonAsync(await (await fetch("http://localhost:8080/example/test_example.py")).text());
    process.exit(ret);
}catch(error){
    console.error({error});
    process.exit(1);
}
