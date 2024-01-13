const io = require('socket.io-client');
const socket = io('http://localhost:3000');
const outputDiv = document.getElementById('output');
const statusIndicator = document.getElementById('status-indicator');
const { shell } = require('electron');
const applocation = "Clearwater"; //This is a beta release, change this city to your city otherwise weather popups won't display the correct info. This doesn't affect Miles' speech or responses.

document.addEventListener('click', function(event) {
    if (event.target.tagName === 'A' && event.target.href.startsWith('http')) {
        event.preventDefault();
        shell.openExternal(event.target.href);
    }
});

function scrollToBottom() {
    const appContainer = document.getElementById('app-container');
    const lastChild = appContainer.lastElementChild;
    if (lastChild && typeof lastChild.scrollIntoView === 'function') {
        lastChild.scrollIntoView({ behavior: 'smooth' });
    }
}

socket.on('pythonOutput', (data) => {
    const messageRegex = /(Miles:|User:|\[.*?\])/g;
    let startIndex = 0;
    let match;

    while ((match = messageRegex.exec(data)) !== null) {
        const message = data.substring(startIndex, match.index).trim();
        if (message) {
            processMessage(message);
        }
        startIndex = match.index;
    }
    if (startIndex < data.length) {
        processMessage(data.substring(startIndex).trim());
    }
});

const apiKey = "c8b138cd625d476fbdb31921231507";  // My personal FREE weather api key, don't steal it.

function fetchWeather() {
    const apiUrl = `http://api.weatherapi.com/v1/forecast.json?key=${apiKey}&q=${applocation}&days=1`;

    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            if ('current' in data && 'forecast' in data && data['forecast']['forecastday']) {
                const conditionText = data.current.condition.text;
                const temp = data.current.temp_f;
                const chanceOfRain = data.forecast.forecastday[0].day.daily_chance_of_rain;
                const isDay = data.current.is_day;

                displayWeatherCard(conditionText, temp, chanceOfRain, isDay);
            } else {
                console.error("Unexpected data structure from weather API.");
            }
        })
        .catch(error => {
            console.error("Error fetching weather data:", error);
        });
}

function getWeatherIcon(conditionText, isDay) {
    switch (conditionText.toLowerCase()) {
        case "clear":
            return isDay ? "fas fa-sun" : "fas fa-moon";
        case "cloudy":
            return "fas fa-cloud";
        case "rain":
            return "fas fa-cloud-rain";
        default:
            return "fas fa-cloud";
    }
}

function displayWeatherCard(conditionText, temp, chanceOfRain, isDay) {
    const weatherIconClass = getWeatherIcon(conditionText, isDay);

    const weatherDiv = document.createElement('div');
    weatherDiv.id = 'weather-card';
    weatherDiv.innerHTML = `
        <i class="${weatherIconClass} weather-icon"></i>
        <div>${applocation}</div>
        <div>${temp}°F</div>
        <div>${chanceOfRain}% chance of rain</div>
    `;

    document.body.appendChild(weatherDiv);

    setTimeout(() => {
        weatherDiv.classList.add('hide-weather-card');
    }, 10000);
}

function processMessage(message) {
    let messageClass = '';

    if (message.includes("Listening for 'Miles'")) {
        setStatus("Listening for 'Miles'", 'status-miles', 'fas fa-microphone');
        return;
    } else if (message.includes("Listening for prompt...")) {
        setStatus('Listening for Prompt', 'status-prompt', 'fas fa-user');
        return;
    } else if (message.includes("[Processing request...]")) {
        setStatus('Processing Request', 'status-processing', 'fas fa-cog');
        return;
    } else if (message.startsWith("Miles:")) {
        messageClass = 'miles';
    } else if (message.startsWith("User:")) {
        messageClass = 'user';
    } else if (message.startsWith("[Miles is")) {
        const actionText = message.match(/\[Miles is (.+)\]/)[1];
        let iconClass;

        if (actionText.startsWith('calculating')) {
            iconClass = 'fas fa-calculator';
        } else if (actionText.startsWith('finding the current weather')) {
            iconClass = 'fas fa-cloud';
            fetchWeather();
        } else if (actionText.startsWith('finding the current time')) {
            iconClass = 'fas fa-clock';
        } else if (actionText.startsWith('retrieving his memory')) {
            iconClass = 'fas fa-server';
        } else if (actionText.startsWith('searching for')) {
            iconClass = 'fab fa-spotify';
        } else if (actionText.startsWith('showing the weather')) {
            iconClass = 'fas fa-window-restore';
            fetchWeather();
        } else if (actionText.startsWith('updating Spotify playback')) {
            iconClass = 'fab fa-spotify';
        } else if (actionText.startsWith('switching the model')) {
            iconClass = 'fas fa-microchip';
        } else if (actionText.startsWith('changing Spotify volume')) {
            iconClass = 'fab fa-spotify';
        } else if (actionText.startsWith('setting system volume')) {
            iconClass = 'fas fa-volume-high';
        } else if (actionText.startsWith('changing system prompt')) {
            iconClass = 'fas fa-id-card';
        } else if (actionText.startsWith('generating speech')) {
            iconClass = 'fas fa-cog';
        } else if (actionText.startsWith('speaking a response')) {
            iconClass = 'fas fa-comment-dots';
        } else if (actionText.startsWith('taking longer than expected')) {
            iconClass = 'fas fa-hourglass-half';
        } else {
            iconClass = 'fas fa-robot';
        }


        setStatus(actionText.charAt(0).toUpperCase() + actionText.slice(1), 'status-action', iconClass);
        return;
    }

    function setStatus(text, className, iconClass = '') {
        if (iconClass === 'fas fa-microphone' || iconClass === 'fas fa-user' ||
            iconClass === 'fas fa-comment-dots' ||
            iconClass === 'fas fa-hourglass-half') {
            statusIndicator.innerHTML = `<i class="${iconClass} jiggling"></i> ${text}`;
        } else if (iconClass === 'fas fa-cog') {
            statusIndicator.innerHTML = `<i class="${iconClass} rotating"></i> ${text}`;
        } else if (iconClass) {
            statusIndicator.innerHTML = `<i class="${iconClass} bouncing"></i> ${text}`;
        } else {
            statusIndicator.innerHTML = text;
        }
        statusIndicator.className = className;
    }

    if (messageClass === 'miles' || messageClass === 'user') {
            const messageDiv = document.createElement('div');
            messageDiv.className = messageClass + ' common-style';

            const formattedText = message
                .replace(/(User:|Miles:)/g, '<span class="bold-glow">$1</span>')
                .replace(/\n/g, '<br>');
            
            messageDiv.innerHTML = formattedText;
            messageDiv.style.minHeight = '40px';
            outputDiv.appendChild(messageDiv);
            scrollToBottom();
        }
    }

// Define the setup steps
const setupSteps = [
    {
        instruction: "Welcome to <b>Miles</b>!. You'll have to go through some setup before you can use <b>Miles<b/>. <br><br>Please enter your <b>OpenAI API key</b>. You can obtain it <a href='https://openai.com/api/' target='_blank' class='setup-link'>here</a>:<br><br><b>1. Sign in</b> <br><b>2. Navigate to your account</b> <br><b>3. Click API keys</b> <br><b>4. Click 'Create new secret key'</b> <br><b>5. Copy and paste it here</b>.",
        field: { name: "api_key", label: "OpenAI API key"}
    },
    {
        instruction: "Please enter your <b>Picovoice API key</b>. You can obtain it <a href='https://console.picovoice.ai' target='_blank' class='setup-link'>here</a>:<br><br><b>1. To sign in, find the passion project sign in button <br>(CMD+f then type 'passion').</b> <br><b>2. Type your name</b> <br><b>3. In the dropdown box, choose 'Porcupine Wake Word'</b> <br><b>4. For where did you hear about it, type 'GitHub'</b> <br><b>5. For project description, type 'Voice assistant'.</b> <br><b>6. Wait for the key to generate and then copy and paste it here.</b>.",
        field: { name: "wake_word_key", label: "Picovoice wake word key"}
    },
    {
        instruction: "Enter your <b>Spotify Client ID</b>:<br><br>" +
                     "<b>1.</b> Create or access your Spotify account at the <a href='https://developer.spotify.com/dashboard/' target='_blank' class='setup-link'>Spotify Developer Dashboard</a>.<br>" +
                     "<b>2.</b> Create a new app with:<br>" +
                     "&nbsp;&nbsp;&nbsp;&nbsp;<b>- App Name:</b> Miles<br>" +
                     "&nbsp;&nbsp;&nbsp;&nbsp;<b>- App Description:</b> Helpful voice assistant<br>" +
                     "&nbsp;&nbsp;&nbsp;&nbsp;<b>- Redirect URL:</b> http://localhost:8080/callback<br>" +
                     "<b>3.</b> Your Client ID is located on your app's dashboard.",
        field: { name: "spotify_client_id", label: "Spotify Client ID" }
    },    
    {
        instruction: "Enter your <b>Spotify Client Secret</b>:<br><br>" +
                     "<b>1.</b> In the <a href='https://developer.spotify.com/dashboard/' target='_blank' class='setup-link'>Spotify Developer Dashboard</a>, select your 'Miles' app.<br>" +
                     "<b>2.</b> Click 'Show Client Secret' on your app's dashboard to retrieve your Client Secret.",
        field: { name: "spotify_client_secret", label: "Spotify Client Secret" }
    },
    {
        instruction: "Please enter your <b>Default Location</b>: <br><br>(The default city you want Miles to get the weather for)",
        field: { name: "DEFAULT_LOCATION", label: "Default Location" }
    },
    {
        instruction: "Please choose your preferred <b>unit</b> <br><br>(Drop down menu click blank field to populate it):",
        field: { name: "UNIT", label: "Unit", type: "select", options: ["Imperial", "Metric"] }
    },
    // other setup pages here
];

let currentStep = 0;
let setupValues = {};

// Function to initialize the setup screen
function initializeSetupScreen() {
    document.getElementById('status-indicator').style.display = 'none';
    document.getElementById('app-container').style.display = 'none';
    document.getElementById('api-key-setup-container').style.display = 'block';
    const instructionsDiv = document.getElementById('setup-instructions');
    const inputsDiv = document.getElementById('api-key-inputs');

    // Function to update the setup screen based on the current step
    function updateSetupScreen() {
        const step = setupSteps[currentStep];
        instructionsDiv.innerHTML = `<p>${step.instruction}</p>`;

        inputsDiv.innerHTML = '';
        const inputField = document.createElement(step.field.type === "select" ? 'select' : 'input');
        inputField.id = step.field.name;

        if (step.field.type === "select") {
            step.field.options.forEach(option => {
                const optionElement = document.createElement('option');
                optionElement.value = option;
                optionElement.textContent = option;
                inputField.appendChild(optionElement);
            });
        } else {
            inputField.type = 'text';
            inputField.placeholder = step.field.label;
        }

        inputField.value = setupValues[step.field.name] || '';
        inputsDiv.appendChild(inputField);
    }

    updateSetupScreen();

    // Function to navigate through setup steps
window.navigateSetup = function(direction) {
    const inputField = document.getElementById(setupSteps[currentStep].field.name);
    setupValues[setupSteps[currentStep].field.name] = inputField.value;

    currentStep += direction;

    // Prevent going before the first step or beyond the last step
    if (currentStep < 0) {
        currentStep = 0;
        return; // Exit the function early
    } else if (currentStep >= setupSteps.length) {
        // All steps completed, save the API keys
        saveApiKeys();
    } else {
        updateSetupScreen();
    }
}};


// Function to save API keys
function saveApiKeys() {
    const { ipcRenderer } = require('electron');
    ipcRenderer.send('saveApiKeys', setupValues);

    document.getElementById('api-key-setup-container').style.display = 'none';
    document.getElementById('app-container').style.display = 'block';
    document.getElementById('status-indicator').style.display = 'block';

}

const { ipcRenderer } = require('electron');

ipcRenderer.on('initialize-setup', () => {
    initializeSetupScreen();
});

ipcRenderer.on('setup-complete', (event, message) => {
    console.log(message); 
    fetch('http://localhost:3000/triggerPython');
});
