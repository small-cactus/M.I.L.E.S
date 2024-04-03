# **Miles - GPT 4 Turbo powered voice assistant**

> A voice assistant beyond anything that currently exists. Other voice assistants are slow, inaccurate, and just don't work. Miles fixes those problems. Custom trained wake word trained on 50,000 samples, self adapting prompts, a unbelievably realistic voice, and unmatched conceptual language understanding. Welcome to M.I.L.E.S (Machine Intelligent Language Enabled System).

<p align="center">
  <img src="miles_logo.png" width="200">
</p>

<h2 align="center">🚀 <b>Download and Installation</b></h2>

<p align="center">
<a href="https://github.com/small-cactus/M.I.L.E.S/wiki/Install-Miles-on-MacOS-(Easy-Install-method)">Install for macOS </a>
</p>

<p align="center">
<a href="https://github.com/small-cactus/M.I.L.E.S/wiki/Install-Miles-On-Windows">Install for Windows ⊞</a>
</p>

<h2 align="center">🌟 Core Features</b></h2>

- 🧠 **AI Language Models**: Miles is powered by text-centric AI models developed to closely understand meaning in language, and when provided with tools, becomes an unmatched experience when compared to any other voice assistant.

- 🎵 **Spotify Integration**: Control Spotify entirely with your voice. Miles can play, pause, skip tracks, adjust volume, and more, all through your voice. (Requires Spotify Premium)

- ☔ **Weather Data**: Get real-time weather information. No need to use specific keywords – Miles will understand you.

- 💾 **Persistent Memory**: Ask Miles to remember important details, dates, or information, and he'll store it in his memory for retrieval later on.

- ➕ **Built-in Calculator**: Miles can use a calculator and will provide math results in LaTeX format.

- 👨‍💻 **Multi-tasking**: Miles can handle up to 3 tools or tasks simultaneously.

- 🔍 **Contextual Awareness**: Miles understands context about himself, his creator, the app he's in, and you – based on the information you provide him.

- 🎤 **Realistic Voice**: Powered by OpenAI's Text-to-Speech technology, Miles has a natural, human-like voice that enhances the overall experience.

- 👂 **Wake Word Detection**: Miles accurately recognizes "Miles," trained on 50,000 samples.
  
- 🌐 **Internet Browsing:** Miles can search the internet for anything you ask about, you don't have to be direct.

- 📷 **Image Recognition**: Utilizing your webcam, Miles can analyze and describe images in real-time, offering insights and information about what it sees. This feature enhances interactions by bringing visual understanding into conversations.


  <br><br>
  ## 🖥️ M.I.L.E.S Conversation screen
  ![M.I.L.E.S Interface](https://github.com/small-cactus/M.I.L.E.S/blob/main/screenshots/conversation.webp)
  <br><br>
  ## 📸 Screenshots of Welcome and Setup Pages
### Welcome Page
The most simple of them all. Miles Welcome Page:
![M.I.L.E.S Welcome Page](https://github.com/small-cactus/M.I.L.E.S/blob/main/screenshots/welcome-page.png)

### Setup Page
The Setup page walks users through the process of entering their API keys and other necessary configurations for M.I.L.E.S.
![M.I.L.E.S Setup Page](https://github.com/small-cactus/M.I.L.E.S/blob/main/screenshots/setup-page.png)
<br><br>


## 💡 Tips and Tricks

- 🤔 **Ask About Capabilities**: Not sure what Miles can do? Just ask him.

- 💰 **Cost-Effective Mode**: Find Miles too pricey? Ask him to be cheaper, and he'll switch to a more cost-effective model and system prompt. 💸

- 🎭 **Personality Customization**: Miles can rewrite his own personality and instructions on command! Tell him to be anything you want. 🤯

- 🔑 **API Keys**: You'll need a few API keys to use Miles, but the app will guide you. Only OpenAI requires payment. 💳

- ⚙️ **Smart Wake Word**: Miles will automatically detect when or when not to use the wake word, so if he asks a follow up question, he won't make you say 'Miles' again.

## 🔒 **Your Privacy Matters**

Here is an in-depth look at how Miles ensures `your information is safe and secure`:

- **Local Processing**: All voice commands, images captured by the webcam, and other inputs are `processed locally on your device`. This includes `wake word detection, image recognition, and audio processing for voice commands`.

- **Secure Data Transmission**: When data needs to be sent to the OpenAI API (for example, to fetch responses from `GPT-4 Turbo` or `GPT-3.5 Turbo`), it is `securely encrypted and transmitted over a protected connection`. `Your API keys and any sensitive information never leave the app`.

- **Voice and Image Data**: 
  - Voice audio is `processed in real-time on your device`. Absolutely no voice data is sent anywhere outside your computer.
  - Images captured for recognition are `encrypted in Base64 format` before being `securely sent to the necessary service for analysis`.

- **Spotify Integration**: Communication with Spotify is `encrypted, adhering to Spotify's security protocols`. This ensures that your music preferences and commands are `securely handled`.

- **Persistent Memory and Calculations**:
  - The persistent memory feature, where you can ask Miles to remember certain information, is `stored locally on your device`. This data is not transmitted outside unless explicitly required for a query.
  - Calculations and the use of the built-in calculator are `performed locally`, with results generated without the need to communicate with external servers.

- **Local Features**:
  - Multi-tasking, contextual awareness, and other intelligent features of Miles are `primarily processed on your device`. This limits the amount of data that needs to be transmitted and ensures `faster, more secure responses`.
  - Internet browsing and information retrieval are done securely, with precautions to `anonymize and protect your queries`.

- **Wake Word Detection**: Utilizes `short-term listening windows` to ensure that continuous audio recording is not stored or transmitted. This ensures that your ambient conversations remain `private and are not processed` by Miles.

- **Data Retention**: Miles is designed to `respect your privacy by not retaining data longer than necessary`. For example, audio recordings are immediately discarded after processing your command, and any remembered information is deleted upon your request or when it is no longer needed.

- **Local Storage and Encryption**: All data stored by Miles for operational purposes, such as your preferences or the information you've asked to be remembered, is `encrypted and stored locally on your device`.



## 🗣️ Natural Language Commands

Miles is powered by a language model, so no specific commands are needed. Just speak naturally, and he'll understand! For example:

- 🎶 "Miles, play that funky tune that gets me groovin'!" 
- 💃 "Miles, do I have RBF?"
- 🤖 "Miles, please store the date of my bestie's birthday so I don't forget it again!" 

Let your imagination run wild with Miles!
<br><br/>

# Planned upcoming features with progress %

> These are all planned features that will soon be implemented, you'll see the date last updated, and current progress as of that date.

### Plugins
> 3-29-24 - 15% complete - conceptual frameworks in place, I have ideas how to make this possible
- Allows anyone to add a python function or group of python functions to Miles' tool list.
- LLM auto writes code to fit into place - only if I can't hard code it.

### Home Assistant integration
> 3-29-24 - 80% complete - entire python backend is complete, setup complete, just need to fix overall logic.
- During setup, you can provide your Home Assistant tokens and choose which devices you want Miles to control.

### Settings and Config Menu
> 3-31-24 - 10% complete - extremely hard to do, would have to change every python variable to an import
- Allows you to change API keys and preferences after setup.

### Dynamic Background Learning
> 3-29-24 - 0% complete - rough ideas in place, still researching
- Everytime you aren't talking to Miles, he is processing, compacting, and researching your past conversations to learn how to better assist you.
- Agentic behavior behind the scenes
- Allowed to set schedules for tasks, learn common commands and at what time you ask them, and act upon them autonomously when trends are strong.

### Projection UI
> 3-31-24 - 95% complete - finished, need way to switch between UI's
- Changes UI to simplistic black background with smooth animations meant for projecting onto a wall

https://github.com/small-cactus/M.I.L.E.S/assets/125771841/b3286b3c-f88b-4315-bbe5-850e8d681e9d

> This is a realtime demo of the projection UI with sound (modulated to emulate jarvis, not sure if I will keep it), the black background makes it appear on the wall as if it has a transparent background


## 🤝 **Contribute to Development**
Your feedback shapes M.I.L.E.S! Though this is a beta release, I eagerly await your feature requests and issue reports for our final launch on GitHub.

**Contact:** anthonyhayward1000@gmail.com

