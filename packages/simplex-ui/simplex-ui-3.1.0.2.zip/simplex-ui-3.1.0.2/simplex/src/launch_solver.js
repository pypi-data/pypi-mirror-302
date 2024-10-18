"use strict";

importScripts("simplex_solver.js");
//importScripts("simplex_solver_debug.js"); // for debugging

function SetOutput(dataname, data)
{
    self.postMessage({data: data, dataname: dataname});
}

Module.onRuntimeInitialized = () => {
    self.addEventListener("message", (msgobj) => {
        Module.simplex_solver(msgobj.data.serno, msgobj.data.data);
        self.postMessage({data: null, dataname: ""});
        self.close();
    });
    self.postMessage("ready");    
}