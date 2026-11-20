/* Run Python in a disposable worker with a parent-enforced timeout. */
importScripts('https://cdn.jsdelivr.net/pyodide/v0.27.7/full/pyodide.js');
let runtime;
self.onmessage=async ({data})=>{
 try{
  runtime=runtime||await loadPyodide();
  runtime.runPython(`import sys, io
_capture = io.StringIO()
_old_stdout, _old_stderr = sys.stdout, sys.stderr
sys.stdout = sys.stderr = _capture`);
  try{
   await runtime.runPythonAsync(data.code);
   self.postMessage({ok:true,output:runtime.runPython('_capture.getvalue()')||'(Program completed without printed output)'});
  }finally{runtime.runPython('sys.stdout, sys.stderr = _old_stdout, _old_stderr')}
 }catch(error){self.postMessage({ok:false,output:String(error).slice(0,2500)})}
};
