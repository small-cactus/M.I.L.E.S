const io = require('socket.io-client');
const socket = io('http://localhost:3000');
const outputDiv = document.getElementById('output');
const statusIndicator = document.getElementById('status-indicator');
const applocation = "New York"; // Change the city to your city for this to work in the beta release.

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
            fetchWeather();  // Fetch and display the weather card
        } else if (actionText.startsWith('finding the current time')) {
            iconClass = 'fas fa-clock';
        } else if (actionText.startsWith('retrieving his memory')) {
            iconClass = 'fas fa-server';
        } else if (actionText.startsWith('searching a song')) {
            iconClass = 'fab fa-spotify';
        } else if (actionText.startsWith('showing the weather')) {
            iconClass = 'fas fa-window-restore';
            fetchWeather();
        } else {
            iconClass = 'fas fa-robot';
        }

        setStatus(actionText.charAt(0).toUpperCase() + actionText.slice(1), 'status-action', iconClass);
        return;
    }

    function setStatus(text, className, iconClass = '') {
        if (iconClass === 'fas fa-microphone' || iconClass === 'fas fa-user') {
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

        const formattedText = message.replace(/\n/g, '<br>');
        messageDiv.innerHTML = formattedText;
        messageDiv.style.minHeight = '40px';
        outputDiv.appendChild(messageDiv);
        scrollToBottom();
    }
}






fetch('http://localhost:3000/triggerPython');
