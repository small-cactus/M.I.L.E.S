const PORT = 3000;
const { app, BrowserWindow, ipcMain } = require('electron');
const express = require('express');
const { spawn } = require('child_process');
const path = require('path');
const http = require('http');
const socketIo = require('socket.io');
const fs = require('fs');

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

    win.on('close', (event) => {
        if (pythonProcess !== null) {
            pythonProcess.kill('SIGTERM');
        }
        app.quit();
    });
}

function checkApiKeys() {
    try {
        const apiKeysContent = fs.readFileSync(path.join(__dirname, 'apikey.py'), 'utf8');
        return apiKeysContent.includes("empty");
    } catch (error) {
        console.error("Error reading apikey.py:", error);
        return true; // Assume setup is needed if there's an error reading the file
    }
}

function startServerAndBackend() {
    const expressApp = express();
    const server = http.createServer(expressApp);
    const io = socketIo(server);

    server.listen(PORT, () => {
        console.log(`Server started on http://localhost:${PORT}`);
        // Start Python process here if API keys are not empty
        if (!checkApiKeys()) {
            try {
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
                    console.log(`Python script exited with code: ${code}`);
                    pythonProcess = null;
                });

            } catch (error) {
                console.error("Failed to start Python script:", error);
            }
        }
    });

    expressApp.get('/triggerPython', (req, res) => {
        if (pythonProcess === null) {
            console.log("Attempting to trigger Python script...");
    
        try {
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
                console.log(`Python script exited with code: ${code}`);
                pythonProcess = null;
            });
    
            res.send("Python script triggered");
        } catch (error) {
            console.error("Failed to trigger Python script:", error);
            res.status(500).send("Failed to trigger Python script");
        }
    }});

    server.listen(PORT, () => {
        console.log(`Server started on http://localhost:${PORT}`);
    });
}

ipcMain.on('saveApiKeys', (event, apiKeys) => {
    writeApiKeys(apiKeys);

    // Check again if API keys are now set
    if (!checkApiKeys()) {
        startServerAndBackend();
    }

    event.reply('setup-complete', 'Setup completed successfully');
});

app.whenReady().then(() => {
    createWindow(); // Create the window in all cases

    if (checkApiKeys()) {
        console.log("API keys are empty, initializing setup screen...");
        win.webContents.on('did-finish-load', () => {
            win.webContents.send('initialize-setup');
        });
    } else {
        console.log("API keys are set, starting server and backend...");
        startServerAndBackend();
    }
});


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

function writeApiKeys(apiKeys) {
    const apiKeyContent = `
api_key="${apiKeys.api_key || 'empty'}"
weather_api_key="c8b138cd625d476fbdb31921231507"
DEFAULT_LOCATION="${apiKeys.DEFAULT_LOCATION || 'empty'}"
UNIT="${apiKeys.UNIT || 'empty'}"
spotify_client_id="${apiKeys.spotify_client_id || 'empty'}"
spotify_client_secret="${apiKeys.spotify_client_secret || 'empty'}"
wake_word_key="${apiKeys.wake_word_key || 'empty'}"
`;

    fs.writeFileSync(path.join(__dirname, 'apikey.py'), apiKeyContent);
}

ipcMain.on('saveApiKeys', (event, apiKeys) => {
    writeApiKeys(apiKeys);
});
