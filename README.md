# 🎙️ **M.I.L.E.S**

> **M.I.L.E.S (Machine Intelligent Language Enabled System)** is a cutting-edge voice assistant powered by the same technology used in ChatGPT. Enhance your day with magical voice commands and state-of-the-art language processing.

<p align="center">
  <img src="miles_logo.png" width="200">
</p>

## 🌐 **Core Features**
- 📡 **Powered by AI language models:** Operated by **GPT-4-Turbo** model out of the box, but easily switchable to **any other OpenAI model** via `main.py`.
- 🎵 **Integrated with Spotify:** Enjoy seamless Spotify controls right from your voice, and via the UI. *(Requires Spotify Premium)*
- ☀️ **Weather Capabilities:** Stay updated with real-time weather data.

💡 **Note:** Before diving in, make sure you have your **OpenAI API key**. Place this key within the quotes in the `apikey.py` file.
  <br><br>
  ## 🖥️ M.I.L.E.S Conversation screen
  ![M.I.L.E.S Interface](https://github.com/small-cactus/M.I.L.E.S/blob/main/screenshots/conversation.webp)
  <br><br>
  ## 🔍 M.I.L.E.S Action notifications
  If they look wonky it's because each action has an animation and it's hard to screenshot because it's moving + Miles responds too fast to screenshot it. Sorry about that!
  ![M.I.L.E.S Actions](https://github.com/small-cactus/M.I.L.E.S/blob/main/screenshots/actions.webp)
  <br><br>

## 🚀 **Prerequisites (Mac install)**

Before starting, ensure the following are installed on your Mac:

- **Homebrew**: If Homebrew is not installed on your Mac, open Terminal and run the following command (copied from [brew.sh](https://brew.sh/)):
  ```
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  ```
  
- **Python**: Install Python via Homebrew. Open Terminal and run:
  ```
  brew install python
  ```

- **Node.js and npm**: Install Node.js (which includes npm) using Homebrew:
  ```
  brew install node
  ```

  <br><br>

## 🛠️ **Getting Started (Windows and Mac)**

Follow these steps to set up the project on your local machine:

1. **Clone the repository**: Clone the project to your computer.
   ```
   git clone https://github.com/small-cactus/M.I.L.E.S.git
   ```

2. **Install Python dependencies**: In the project directory, run the following command to install all required Python packages:
   ```
   pip install requests openai spotipy SpeechRecognition gTTS pydub PyAudio pvporcupine socketio os-mac
   ```

3. **Install Node.js dependencies**: Still in the project directory, install the Node.js packages.
   ```
   npm install
   ```

4. **Run the app**: Complete the steps in Configurations section before starting the app, after that's done, while in the project directory, run this command in the terimnal:
   ```
   npm start
   ```
  <br><br>

# ⚙️ **Configurations:**
Follow these steps to set up Miles.

## 🔑 OpenAI API Integration (REQUIRED)
### 1️⃣ Sign Up for OpenAI
- Begin by signing up for an OpenAI account, if you don't already have one. Visit the [OpenAI API portal](https://beta.openai.com/signup/) to register.

### 2️⃣ Access Your API Key
- After logging in, choose "API", then click your profile in the top right, navigate to the API section to find your API key.

### 3️⃣ Update the `apikey.py` File
- Copy the API key from OpenAI.
- Locate the `apikey.py` file in your local copy of the Miles project.
- Insert your OpenAI API key into the `apikey.py` file where it says OpenAI api key.


<br><br>

## 🎵 Spotify Integration
Follow the steps below to set up Spotify integration:

### 1️⃣ Create a Spotify Account
Start by [creating or accessing your Spotify account](https://www.spotify.com/).

### 2️⃣ Access the Spotify Developer Dashboard
- Navigate to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/) and sign in.

### 3️⃣ Create a New App
- After logging in, click on the "Create an App" button.
- Fill in:
  - **App Name**: `Miles`
  - **App Description**: `Helpful voice assistant`
  - **Redirect URL**: `http://localhost:8080/callback`

### 4️⃣ Get Your Client ID and Client Secret
- On your app's dashboard, locate your **Client ID** and enter it in the `apikey.py` file.
- Click "Show Client Secret" to retrieve your **Client Secret** and add it to the `apikey.py` file as well.

### 5️⃣ Music With Miles
Initiate Miles and request your favorite songs!


<br><br>
## 🗣️ Picovoice Porcupine Wake Word Setup (REQUIRED)
For enabling wake word detection in Miles, you'll need to obtain an API key from Picovoice Porcupine. Here's how to do it:

### 1️⃣ Create a Picovoice Account
- Sign up for a Picovoice account or log in if you already have one. You can do so [here](https://console.picovoice.ai/signup).

### 2️⃣ Access the Picovoice Console
- After logging in, head over to the [Picovoice Console](https://console.picovoice.ai/).

### 3️⃣ Obtain Your API Key
- In the console, you'll find an option to generate an API key. Follow the instructions to create one.
- Once you have your API key, copy it.

### 4️⃣ Update Your `apikey.py` File
- In your local copy of the Miles project, locate the `apikey.py` file.
- Paste the copied API key into this file, following the format provided in the file.

- **All done! 🥳**

<br><br>

## 🔍 **Troubleshooting**
**This is a beta release, there are no troubleshooting steps at the moment, submit issues in githubs issue tracker for now.**
- [Placeholder for Troubleshooting Step 1]
- [Placeholder for Troubleshooting Step 2]
- [Placeholder for Troubleshooting Step 3]

## ✨ **Highlights & Features**
- **Unrestricted Interaction**: M.I.L.E.S has no token limit, this means you might be twiddling your thumbs if you submit a long request.
  
- **Intuitive Understanding & Action**: Powered by an advanced language model, M.I.L.E.S not only grasps even the most uniquely phrased commands but also proactively executes actions when it deems necessary. It's basically magic in a bottle, but not it a bottle, or magic.
  
- **Customization**: Modify system prompts and wake word within the `main.py` file. (Shhh don't tell anyone but... Miles is soon gonna be able to update his own system prompt if he finds that it limits him in helping you, don't worry, it reverts back to anything you had it set to after miles is finished with it! And yes you can turn this feature off.)
  
- **World Class Wake Word Invocation**: Whether you say "Hey Miles", "Hi Miles", "What's up Miles", "Miles", or literaly any starting phrase that ends with "Miles", the system WILL respond accurately. We have about a 10% fail rate for hearing if it's been activated, and a 0% accidental activation error rate.
  
- **Advanced Audio Processing**: M.I.L.E.S excels in noisy environments, ensuring accurate command interpretation.
  
- **Graphics & Interface**: Features a dynamic interface displaying Spotify song playback, weather cards, user interactions, and ongoing actions.

## 📜 **Changelog**
- 🔊 **Realistic Voice Upgrade with OpenAI TTS**: M.I.L.E.S now utilizes OpenAI TTS for Text-To-Speech, elevating the voice quality to ultra-realistic levels. M.I.L.E.S will seamlessly switch to a basic TTS if any errors are detected.
- 📢 **Enhanced Wake Word Detection**: M.I.L.E.S now leverages the same technology used in leading smart home products like Google Home and Alexa for unmatched wake word detection accuracy, this means you don't have to wait for the program to listen and stop listening, now it's always listening!
- 🔢 **Enhanced Calculator Operations**: M.I.L.E.S now efficiently handles multiple simultaneous calculations at the same time.
- 💡 **Improved UI**: Introducing a graphical interface for better user interactions.
- 🌦️ **Enhancements**: Augmented weather data, permanent memory, and date + time support.
- 🎲 **Multi-Task Mode** M.I.L.E.S can use up to 3 tools at once, this means M.I.L.E.S can find the weather in Shanghai, calculate the temp difference if it were to drop 23.883 degrees, and then store it in memory to call upon later, all before he even responds to you. That's the future.
- 💻 **Cross Platform!** M.I.L.E.S now supports MacOS and Windows 10/11.

## 🆕 **Upcoming Features**
- 🌐 **Web Browsing**: M.I.L.E.S will soon be able to search anything on the entire internet to gain more knowledge and assist you further.
- 📜 **Chat History**: An upcoming feature to keep track of your previous interactions.
- 🖥️ **Typing Interface**: Soon, you won't be restricted to voice. Type your commands and queries for M.I.L.E.S.
- ⏸️ **Interrupt Capabilities**: Interrupt M.I.L.E.S in the middle of a speech to provide new instructions or queries.
- 📝 **Formatted Code Blocks**: M.I.L.E.S will have the ability to display formatted code blocks inline, although these won't be spoken.
- 📊 **Tables**: Introducing the ability to display tables, which will not be spoken.
- 📄 **Text File Submission**: Submit text files to M.I.L.E.S for it to read and gain context about them.
- 💡 **Smart Light Control**:
  - **LIFX Lights**: M.I.L.E.S is gearing up to seamlessly integrate with LIFX lights, allowing users to control their home lighting with just their voice. From adjusting brightness levels to changing colors, experience the future of smart lighting control.
  - **Philips Hue**: Following the integration with LIFX, we'll be extending our support to Philips Hue lights. Immerse yourself in a vibrant ambiance by directing M.I.L.E.S to set your preferred lighting moods and scenes.

## 🚀 **Future Roadmap**

As we continue to push the boundaries of voice assistant technology with M.I.L.E.S, here's a sneak peek into the exciting journey ahead:

- 📱 **Android App**: We envision M.I.L.E.S on every Android device. An intuitive app designed to seamlessly blend with your daily tasks, offering AI-powered assistance at your fingertips. Experience unparalleled convenience and intelligence on-the-go.

- 🌐 **Web App**: Accessibility is our top priority. Soon, you'll be able to interact with M.I.L.E.S right from your browser, ensuring assistance is just a tab away. Ideal for work, research, or casual browsing.

- 💻 **1-Click Install for Desktop App**: Simplifying the user experience is at the heart of our mission. Our upcoming 1-click install ensures a hassle-free setup, letting you dive into the world of M.I.L.E.S without a hitch.

- 🍎 **iOS App**: M.I.L.E.S is gearing up to join the Apple ecosystem. Our iOS app will bring the same intelligence and flair to Apple devices, tailored to meet the high standards of iOS users.

- 🖥️ **Mac Support (Completed!)**: Completed!

- 🏠 **Packaged Smart Home Product**: Transforming houses into smarter homes. The future will see M.I.L.E.S integrated into dedicated smart home products. Imagine a world where M.I.L.E.S orchestrates your lights, thermostats, security systems, and more, all through voice commands.

## 🙋‍♂️ **About Me**

Hello! I'm a one-man developer team, currently navigating the world of high school. Balancing between academics and passion projects means it might take me a few months to roll out new features for M.I.L.E.S, but I'm always dedicated to delivering the best.

🔍 **My Work Ethic**: At the core of my development philosophy is simplicity and accessibility. I firmly believe that everyone, irrespective of their expertise or financial standing—be it novice or advanced, rich or poor—should have access to cutting-edge technology like M.I.L.E.S. It's for this reason I've committed to keeping M.I.L.E.S free, permanently. Despite the costs I bear to keep this vision alive, put simple: "I stomach costs, so you can stomach productivity." I strive to create an interface so intuitive that anyone can harness its full potential with ease, making AI-driven assistance universally accessible.

🌱 **The Origin**: My journey into this world of voice assistants began when I recognized the limitations of platforms like Siri. Eager to bring a more competent solution to the table, I embarked on a self-taught coding expedition. This led to the birth of my initial project, **JarvisChatGPT**, available in my other repository. While JarvisChatGPT was a step in the right direction, emphasizing simplicity, I knew I had the potential to create something even more advanced. Hence, M.I.L.E.S was conceived, a culmination of weeks of learning, testing, and innovating.

Your support fuels my passion, and I'm excited to continue this journey with all of you!

## 🤝 **Contribute to Development**
Your feedback shapes M.I.L.E.S! Though this is a placeholder release, we eagerly await your feature requests and issue reports for our official launch on GitHub.
