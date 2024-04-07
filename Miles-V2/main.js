// Main process entry point
const PORT=3000
const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const fs = require('fs');


const expressApp = express();
const server = http.createServer(expressApp); // HTTP server based on express
const io = require('socket.io')(server);

let win;
let pythonProcess = null;

let configServer;
let configSocketIO;

function createConfigServer() {
  configServer = http.createServer();
  configSocketIO = require('socket.io')(configServer, {
    cors: {
      origin: '*',
    },
  });

  configServer.listen(3000, () => {
    console.log(`Config server started on port ${3000}`);
  });

  configSocketIO.on('connection', (socket) => {
    console.log('Config socket connection established');
  });
}

// Helper function to get the correct Python command based on the platform
function getPythonCommand() {
    return process.platform === 'win32' ? 'python' : 'python3';
}

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
        if (server !== null) {
            server.close(() => {
                console.log('Server stopped');
            });
        }
        app.quit();
        win = null;
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
    const io = require('socket.io')(server, {
        cors: {
            origin: '*',
        },
    });

    function startPython() {
        if (pythonProcess) {
            console.log('Python backend is already running.');
            return;
        }
        try {
            const python = spawn(getPythonCommand(), ['-u', path.join(__dirname, 'main.py')]);
            pythonProcess = python;

            python.stdout.on('data', (data) => {
                const output = data.toString();
                console.log("Python Output:", output);
                io.emit('pythonOutput', output);
            });

            python.stderr.on('data', (data) => {
                console.error("Python Error:", data.toString());
                io.emit('pythonError', data.toString());
            });

            python.on('close', (code) => {
                console.log(`Python script exited with code: ${code}`);
                pythonProcess = null;
            });

        } catch (error) {
            console.error("Failed to start Python script:", error);
        }
    }

    if (!server.listening) {
        server.listen(PORT, () => {
            console.log(`Server started on http://localhost:${PORT}`);
            win.webContents.send('server-ready');
            // Server has started, now start Python backend if API keys are set
            if (!checkApiKeys()) {
                startPython();
            }
        });
    } else {
        // Server is already running, check if we need to start Python backend
        console.log('Server is already running on port ' + PORT);
        if (!checkApiKeys()) {
            startPython();
        }
    }
}

    expressApp.get('/triggerPython', (req, res) => {
        if (pythonProcess === null) {
            console.log("Attempting to trigger Python script...");

            try {
                const python = spawn(getPythonCommand(), ['-u', path.join(__dirname, 'main.py')]);
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
        }
    });
let configProcess = null;

function triggerConfigScript() {
    if (configProcess) {
      console.log('Config script is already running.');
      return;
    }
  
    const pythonCommand = getPythonCommand();
    configProcess = spawn(pythonCommand, ['-u', path.join(__dirname, 'config.py')]);
  
    configProcess.stdout.on('data', (data) => {
        const output = data.toString();
        console.log("Python Output:", output);
    
        // Check if win is defined and not destroyed
        if (win && !win.isDestroyed()) {
            win.webContents.send('pythonOutput', output);
        }
    
        io.emit('pythonOutput', output);
    });
  
    configProcess.stderr.on('data', (data) => {
      const errorMessage = data.toString();
      console.error("Config Python Error:", errorMessage);
  
      // Check if win is defined and not destroyed
      if (win && !win.isDestroyed()) {
        win.webContents.send('configpythonError', errorMessage);
      }
  
      // Emit the error event using the configSocketIO instance
      io.emit('configpythonError', errorMessage);
    });
  
    configProcess.on('close', (code) => {
      console.log(`Config script exited with code ${code}`);
      configProcess = null;
    });
  }

ipcMain.on('start-config', () => {
    triggerConfigScript();
  });

  // Make sure the server listens on the specified port
server.listen(PORT, () => {
    console.log(`Server started on http://localhost:${PORT}`);
    if (win && !win.isDestroyed() && win.webContents) {
        win.webContents.send('server-ready');
        // Other code that uses win.webContents
      }
  });

// Function to write API keys to a file
function writeApiKeys(apiKeys) {
    const apiKeyContent = `
api_key="${apiKeys['dynamic-textbox-openai'] || 'empty'}"
weather_api_key="c8b138cd625d476fbdb31921231507"
DEFAULT_LOCATION="${apiKeys['dynamic-textbox-city'] || 'empty'}"
UNIT="${apiKeys['dynamic-textbox-unit'] || 'empty'}"
spotify_client_id="${apiKeys['dynamic-textbox-spotify-id'] || 'empty'}"
spotify_client_secret="${apiKeys['dynamic-textbox-spotify-secret'] || 'empty'}"
HomeAssistant_URL_IP="${apiKeys['dynamic-textbox-home-assistant-url'] || 'empty'}"
HomeAssistant_Token="${apiKeys['dynamic-textbox-home-assistant-token'] || 'empty'}"
`;

    fs.writeFileSync(path.join(__dirname, 'apikey.py'), apiKeyContent);
}

// IPC listener for saving API keys
ipcMain.on('saveApiKeys', (event, apiKeys) => {
    writeApiKeys(apiKeys);

    // Send a response back to the renderer indicating success
    event.reply('setup-complete', 'Setup completed successfully');
    // Note: Don't automatically start the server here
});

ipcMain.on('start-server-backend', (event) => {
    console.log('Configuration is complete, starting server and backend...');
    startServerAndBackend();
});

app.whenReady().then(() => {
    // Create the window in all cases
    createWindow();

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

ipcMain.on('start_homeassistant_fetch', (event) => {    
    // Start the Python script with PYTHONWARNINGS set to "ignore"
    const pythonProcess = spawn(getPythonCommand(), ['-u', path.join(__dirname, 'HomeAssistantUtils.py'), '--entity-mode'], {
        env: {
            ...process.env, // Inherit the current environment
            PYTHONWARNINGS: "ignore" // Suppress Python warnings
        }
    });

    pythonProcess.stdout.on('data', (data) => {
        console.log(`stdout: ${data}`);
        // Handle the Python script output here. Possibly send it back to renderer process.
        win.webContents.send('entity-data', data.toString());
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    });

    pythonProcess.on('close', (code) => {
        console.log(`Python script exited with code ${code}`);
        // Handle the script exit if needed.
    });
});

ipcMain.on('save-devices', (event, devices) => {
    const filePath = path.join(__dirname, 'HomeAssistantDevices.json');
    fs.writeFile(filePath, JSON.stringify(devices, null, 2), (err) => {
        if (err) {
            console.error('Failed to save devices', err);
            event.reply('save-devices-reply', 'error');
            return;
        }
        console.log('Devices saved successfully');
        event.reply('save-devices-reply', 'success');
    });
});