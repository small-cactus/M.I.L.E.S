const io = require('socket.io-client');
const socket = io('http://localhost:3000', {
    reconnection: true, // Default is true, but being explicit for clarity
    reconnectionDelay: 1000, // Attempt to reconnect every 1 second
    reconnectionAttempts: Infinity // Keep trying to reconnect
});
const outputDiv = document.getElementById('output');
const statusIndicator = document.getElementById('status-indicator');
const { shell } = require('electron');
const applocation = "Clearwater"; //This is a beta release, change this city to your city otherwise weather popups won't display the correct info. This doesn't affect Miles' speech or responses.

let isErrorDetected = false; // Global flag to track error state


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
    console.log('Received pythonOutput:', data);
    const messageRegex = /(Miles:|User:|\[.*?\])/g;
    let startIndex = 0;
    let match;

    while ((match = messageRegex.exec(data)) !== null) {
        const message = data.substring(startIndex, match.index).trim();
        if (message) {
            processMessage(message, false);
        }
        startIndex = match.index;
    }
    if (startIndex < data.length) {
        processMessage(data.substring(startIndex).trim(), false);
    }
});

socket.on('pythonError', (errorMessage) => {
    console.log('Received pythonError:', errorMessage);
    let customMessage;
    const rateLimitErrorPattern = /openai\.RateLimitError/;

    // Setting the flag to true regardless of the error type for simplicity
    isErrorDetected = true;

    if (rateLimitErrorPattern.test(errorMessage)) {
        customMessage = "Error Detected: No more OpenAI Credits";
    } else {
        customMessage = "Error Detected: Please Restart Miles";
    }

    // Process the message with the error flag set to true
    processMessage(customMessage, true);
});

function processMessage(message, isError) {
    if (isError) {
        setStatus(message, 'status-error', 'fas fa-exclamation-triangle');
        return;
    }
    // Check if an error has been detected previously
    if (isErrorDetected) {
        console.log("Blocking message due to prior error.");
        return; // Exit early
    }
    let messageClass = '';
    
    // Detect and wrap LaTeX with spans for MathJax processing
    message = message.replace(/\\\(.*?\\\)/g, function(match) {
        return `<span class="mathjax-latex">${match}</span>`;
    });

    MathJax.typesetPromise().then(() => {
        console.log('MathJax has processed the new content.');
      }).catch((err) => console.log('Error in MathJax processing:', err));
    
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
        } else if (actionText.startsWith('Config Complete!')) {
            console.log('Configuration is complete.');
            document.getElementById('config-page').style.display = 'none';
            document.querySelectorAll('.content').forEach(el => el.style.display = 'none');
            document.getElementById('status-indicator').style.display = 'none';
            document.getElementById('app-container').style.display = 'none';
            showPage('restart-page');
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

        MathJax.typesetPromise().catch((err) => console.error('MathJax processing error:', err));
    }
}

// Ensure 'require' is available for Electron's ipcRenderer
const { ipcRenderer } = require('electron');

var isCurrentPageValid = true;
var currentPageId = 'openai'; // Initialize with the default page ID
var setupValues = {};
var textboxValidity = {}; // Object to keep track of each textbox's validity

// Function to show the selected page and hide others
function showPage(pageId) {
    if (currentPageId === pageId) return; // No action if already on the page
    
    var pages = document.querySelectorAll('.content');
    pages.forEach(function(page) {
        // Set display to 'none' for all pages except the one to be shown
        if (page.id !== pageId) {
            page.style.display = 'none';
        }
    });
    
    var requestedPage = document.getElementById(pageId);
    if (requestedPage) {
        requestedPage.style.display = 'block'; // Show the requested page
    }
    
    // Handle navigation menu visibility
    const navMenu = document.querySelector('.nav-menu');
    if (pageId === 'welcome-page' || pageId === 'completion-page' || pageId === 'restart-page') {
        navMenu.style.display = 'none';
    } else {
        navMenu.style.display = 'flex';
    }
    
    // Play incorrect animation if the current page is invalid
    // This part is now moved here to be checked after the page change
    if (!isCurrentPageValid && pageId !== 'welcome-page' && pageId !== 'completion-page') {
        document.querySelectorAll('.nav-menu li').forEach(function(li) {
            li.classList.add('incorrect-animation');
            setTimeout(function() { li.classList.remove('incorrect-animation'); }, 500);
        });
    }
    
    currentPageId = pageId; // Update the current page ID
}


const totalInputs = 5; // Update this if the number of inputs changes
Object.keys(textboxValidity).forEach(key => textboxValidity[key] = false);

function initializeButtonAndTextbox(buttonId, textboxId, defaultText, tooltipText) {
    var button = document.getElementById(buttonId);
    var textbox = document.getElementById(textboxId);
    var tooltip = button.nextElementSibling.nextElementSibling;
    var originalText = '';
    var refreshButtonId = 'refresh-button-' + buttonId.split('-').slice(2).join('-');
    
    button.addEventListener('click', function() {
        textbox.style.display = 'block';
        textbox.value = originalText;
        textbox.focus();
        button.style.display = 'none';
        tooltip.style.display = 'none';
    });
    
    textbox.addEventListener('blur', function() {
        // Check if the textbox is empty and reset if necessary
        if (textbox.value.trim() === '') {
            originalText = '';
            button.textContent = defaultText;
            button.style.display = 'block';
            textbox.style.display = 'none';
            tooltip.style.display = 'none';
            return; // Exit the function early since no further validation is needed
        }
        
        originalText = textbox.value.trim();
        let isValid = false;
        
        // Custom validation logic
        if (buttonId.includes('openai')) {
            isValid = originalText.startsWith('sk-');
        //} else if (buttonId.includes('picovoice')) {
            //isValid = originalText.endsWith('==');
        } else if (buttonId.includes('unit')) {
            let lowerCaseText = originalText.toLowerCase();
            isValid = lowerCaseText === 'metric' || lowerCaseText === 'imperial';
        } else if (buttonId.includes('city')) {
            isValid = /^[A-Z]/.test(originalText);
        } else {
            // For Spotify ID and Secret, since no format is specified
            isValid = true; // Consider always valid
        }
        
        // Update button text and tooltip based on validation
        isCurrentPageValid = isValid;
        textboxValidity[textboxId] = isValid; // Update validity status
        
        if (isValid) {
            setupValues[textboxId] = originalText;
        } else {
            setupValues[textboxId] = null;
        }
        
        // Update UI based on validation
        let verificationSymbol = isValid ? '✅ ' : '❌ ';
        button.textContent = verificationSymbol + (originalText.length > 10 ? originalText.substring(0, 10) + "..." : originalText);
        tooltip.textContent = tooltipText;
        tooltip.style.display = isValid ? 'none' : 'block';
        textbox.style.display = 'none';
        button.style.display = 'block';
        
        // Check if all inputs are valid
        if (Object.values(textboxValidity).filter(Boolean).length === totalInputs) {
            saveApiKeys();
        }
    });
    
    document.getElementById(refreshButtonId).addEventListener('click', function() {
        originalText = '';
        textbox.value = '';
        textbox.style.display = 'none';
        button.style.display = 'block';
        button.textContent = defaultText;
        tooltip.style.display = 'none';
        isCurrentPageValid = false;
        textboxValidity[textboxId] = false; // Reset validity on refresh
    });
}

// Initialize all buttons and textboxes with their respective IDs and messages
initializeButtonAndTextbox('dynamic-button-openai', 'dynamic-textbox-openai', 'Enter your OpenAI API key', 'Hmm... it seems like this isn\'t an OpenAI API key.');
initializeButtonAndTextbox('dynamic-button-spotify-id', 'dynamic-textbox-spotify-id', 'Enter your Spotify Client ID', 'Hmm... it seems like this isn\'t a Spotify Client ID.');
initializeButtonAndTextbox('dynamic-button-spotify-secret', 'dynamic-textbox-spotify-secret', 'Enter your Spotify Client Secret', 'Hmm... it seems like this isn\'t a Spotify Client Secret.');
initializeButtonAndTextbox('dynamic-button-city', 'dynamic-textbox-city', 'Enter your Preferred City', 'Please enter a valid city name (Capitalized).');
initializeButtonAndTextbox('dynamic-button-unit', 'dynamic-textbox-unit', 'Enter your Default Unit (Metric or Imperial)', 'Please enter \'Imperial\' for Fahrenheit or \'Metric\' for Celsius.');



// Function to navigate to the configuration page
function navigateToConfigPage() {
    showPage('config-page');
}

// Function triggered upon setup completion
function onSetupComplete() {
    navigateToConfigPage(); // Navigate to the config page directly
}

// IPC listener for initialization signal from the main process
ipcRenderer.on('initialize-setup', () => {
        // Hide main app content
        document.getElementById('status-indicator').style.display = 'none';
        document.getElementById('app-container').style.display = 'none';
        
        // Hide all content sections
        document.querySelectorAll('.content').forEach(el => el.style.display = 'none');
        
        // Show only the welcome page
        showPage('welcome-page');
        document.getElementById('welcome-page').style.display = 'block';
});

// Function to save API keys, called when setup form is submitted
function saveApiKeys(apiKeys) {
    // Example of how apiKeys might be used or stored
    console.log('API Keys:', apiKeys);

    // Signal the main process that API keys have been saved
    ipcRenderer.send('saveApiKeys', setupValues);

    // Mark setup as complete and navigate to the config page
    onSetupComplete();
    ipcRenderer.send('saveApiKeys', setupValues);
    document.querySelector('.nav-menu').style.display = 'none';
}

// Listening for the 'config-complete' event from the main process
ipcRenderer.on('config-complete', () => {
    // Disconnect and reconnect the socket connection
    socket.disconnect();
    socket.connect();
    console.log('Configuration is complete.');
    document.getElementById('config-page').style.display = 'none';
    document.querySelectorAll('.content').forEach(el => el.style.display = 'none');
    document.getElementById('status-indicator').style.display = 'none';
    document.getElementById('app-container').style.display = 'block';
    isErrorDetected = false;
    showPage('restart-page');
    // Potential actions to take after configuration is complete
});

document.getElementById('start-config-script').addEventListener('click', function() {
    ipcRenderer.send('start-config');
    document.getElementById('status-indicator').style.display = 'block';
});