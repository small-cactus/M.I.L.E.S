const io = require('socket.io-client');
const socket = io('http://localhost:3000', {
  reconnection: true,
  reconnectionDelay: 1000,
  reconnectionAttempts: Infinity
});
const { shell, ipcRenderer } = require('electron');

// DOM elements
const messageContainer = document.querySelector('.message-container');
const animatedCircle = document.querySelector('.animatedCircle');

  let currentAnimationClass = ''; // Tracks the current animation class

  function applyAnimation(animationClass) {
    // Remove the current animation class if it exists
    if (currentAnimationClass) {
      animatedCircle.classList.remove(currentAnimationClass);
      // Trigger reflow to allow animation restart
      void animatedCircle.offsetWidth;
    }
    
    // Apply the new animation class
    currentAnimationClass = animationClass;
    animatedCircle.classList.add(currentAnimationClass);
  }
  
  function switchToNextAnimation() {
    if (nextAnimationClass && nextAnimationClass !== currentAnimationClass) {
      applyAnimation(nextAnimationClass);
      nextAnimationClass = ''; // Clear the next animation class after applying
    } else {
      // No switch needed, reapply current animation if there is one
      applyAnimation(currentAnimationClass);
    }
  }
  
  // Listen for the end of an animation, then decide whether to loop or switch
  animatedCircle.addEventListener('animationend', switchToNextAnimation);
  
  // Function to decide the next animation based on data, simplified for brevity
  function applyCircleAnimation(data) {
    let newClass = ''; // Determine this based on your data logic
    
    // Example condition
     if (data.includes("'Miles'")) {
    newClass = 'pulse';
  } else if (data.includes("Listening for prompt")) {
    newClass ='pulseBig';
  } else if (data.includes("[Miles is finding the current weather")) {
    newClass = 'rotate'; // Example condition
  } else if (data.includes("[Miles is speaking a response...]")) {
    newClass = 'pulseWhite';
  } else if (data.includes("User:")) {
    newClass = 'rotate';
  }
  
    if (newClass && newClass !== currentAnimationClass) {
      nextAnimationClass = newClass;
      // If the circle is not currently animating, apply immediately
      if (!currentAnimationClass) {
        switchToNextAnimation();
      }
    }
  }

  function showMessage(content, isMiles) {
    const messageTypeClass = isMiles ? 'miles-message' : 'user-message';
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', messageTypeClass, 'fadeIn');

    // Assuming your content is LaTeX wrapped in \( ... \) or \[ ... \]
    // If it's not exclusively LaTeX, you'll need additional handling
    messageDiv.innerHTML = content; // Use innerHTML to allow HTML interpretation
    messageContainer.appendChild(messageDiv);

    // Ask MathJax to typeset the new message
    MathJax.typesetPromise([messageDiv]).catch(function (err) {
        console.warn('MathJax typeset failed:', err);        
    });
}

function handleIncomingMessage(data) {
    // First, check for the specific "Listening for 'Miles'" message
    if (data.includes("Listening for 'Miles'")) {
        console.log("detected listening for miles");
        fadeOutMessages();
        return; // Stop further processing since we found our specific case
    }

    // Process only if the message starts with "Miles:" or "User:"
    const isMiles = data.startsWith("Miles:");
    const isUser = data.startsWith("User:");
  
    if (isMiles || isUser) {
        // Extract the content by removing the prefix and any bracketed text
        const content = data.replace(/^User:|^Miles:/, '').trim().replace(/\[.*?\]/g, '');

        console.log("detected response");
        showMessage(content, isMiles);
    }
}

function fadeOutMessages() {
    // Select all current messages
    const messages = document.querySelectorAll('.message');
    messages.forEach(message => {
        // Add the 'fadeOut' class to each message to start the fade-out animation
        message.classList.remove('fadeIn');
        message.classList.add('fadeOut');

        // Listen for the end of the fade-out animation, then remove the message
        message.addEventListener('animationend', () => {
            console.log('Animation ended for', message);
            message.remove();
        });
    });
}

document.addEventListener('click', function(event) {
    if (event.target.tagName === 'A' && event.target.href.startsWith('http')) {
        event.preventDefault();
        shell.openExternal(event.target.href);
    }
});

socket.on('pythonOutput', (data) => {
  handleIncomingMessage(data); // Keep handling incoming messages as before
  if (data.includes("[Miles is speaking a response...]")) {
    loadAndProcessMP3(); // Call this function when the specific message is received
  }

  applyCircleAnimation(data); // Continue with your existing animation logic
});

function loadAndProcessMP3() {
  const audioUrl = 'output.mp3';
  const audioContext = new (window.AudioContext || window.webkitAudioContext)();

  fetch(audioUrl)
    .then(response => response.arrayBuffer())
    .then(arrayBuffer => audioContext.decodeAudioData(arrayBuffer))
    .then(audioBuffer => {
        const source = audioContext.createBufferSource();
        source.buffer = audioBuffer;
        const analyser = audioContext.createAnalyser();
        
        // Connect the source to the analyser only, not to the audioContext.destination
        source.connect(analyser);
        // Remove the connection to audioContext.destination to prevent sound playback
        // analyser.connect(audioContext.destination); // This line is commented out or removed

        source.start();

        // Setup visualizer update
        const dataArray = new Uint8Array(analyser.frequencyBinCount);
        const updateVisualizer = () => {
            requestAnimationFrame(updateVisualizer);

            analyser.getByteFrequencyData(dataArray);

            // Simplified volume calculation
            let sum = 0;
            for (let i = 0; i < dataArray.length; i++) {
                sum += dataArray[i];
            }
            let average = sum / dataArray.length;

            // Adjustments based on volume for both height and width
            let newHeight = 50 + (average * 1.5); // Adjust sensitivity if needed
            let newWidth = 200 + (average * 1.5);
              animatedCircle.style.opacity = '1';

            animatedCircle.style.height = `${newHeight}px`;
            animatedCircle.style.width = `${newWidth}px`;
        };

        updateVisualizer();
    })
    .catch(error => console.error('Error with fetching the audio file', error));
}
