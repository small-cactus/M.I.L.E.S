const PORT = 3000;
const { app, BrowserWindow } = require('electron');
const express = require('express');
const { spawn } = require('child_process');
const path = require('path');
const http = require('http');
const socketIo = require('socket.io');

let win;
let pythonProcess = null;

function createWindow() {
    win = new BrowserWindow({
        width: 1920,
        height: 1080,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        },
            icon: path.join(__dirname, 'miles_logo.icns')
    });
    win.loadFile('index.html');

    // Handle the window close event
    win.on('close', (event) => {
        if (pythonProcess !== null) {
            pythonProcess.kill('SIGTERM');
        }
        app.quit();
    });
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});

const expressApp = express();
const server = http.createServer(expressApp);
const io = socketIo(server);

expressApp.get('/triggerPython', (req, res) => {
    console.log("Triggering Python script...");

    const python = spawn('python3', ['-u', path.join(__dirname, 'main.py')]);
    pythonProcess = python;

    python.stdout.on('data', (data) => {
        console.log("Python Output:", data.toString());
        io.emit('pythonOutput', data.toString());
    });

    python.stderr.on('data', (data) => {
        console.error("Python Error:", data.toString());
    });

    python.on('close', (code) => {
        console.log(`Python script completed with code: ${code}`);
        res.send("Python script completed");
        pythonProcess = null; 
    });
});

server.listen(PORT, () => {
    console.log(`Server started on http://localhost:${PORT}`);
});
