const { contextBridge, ipcRenderer, shell } = require("electron");

contextBridge.exposeInMainWorld("desktopAPI", {
  openExternal: (url) => shell.openExternal(url),
  send: (channel, data) => ipcRenderer.send(channel, data),
  on: (channel, callback) => {
    const subscription = (_event, ...args) => callback(...args);
    ipcRenderer.on(channel, subscription);
    return () => ipcRenderer.removeListener(channel, subscription);
  },
});
