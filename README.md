# **Miles - GPT 4 Turbo powered voice assistant**

> Miles, or the **Machine Intelligent Language Enabled System**, is a revolutionary voice assistant powered by the cutting-edge GPT-4 Turbo and GPT-3.5 Turbo AI models from ChatGPT. Get ready to experience magical voice commands and state-of-the-art language processing! 🔥

<p align="center">
  <img src="miles_logo.png" width="200">
</p>

## 🌟 Core Features

- 🧠 **AI Language Models**: Miles is powered by the advanced GPT-4 Turbo and GPT-3.5 Turbo models from OpenAI, providing state-of-the-art natural language understanding and generation capabilities. You can easily switch between models as needed just by asking.

- 🎵 **Spotify Integration**: Control Spotify entirely with your voice. Miles can play, pause, skip tracks, adjust volume, and more, all through your voice. (Requires Spotify Premium)

- ☔ **Weather Data**: Get real-time weather information by casually mentioning it in your requests. No need to use specific prompts or keywords – Miles will understand the context.

- 💾 **Persistent Memory**: Ask Miles to remember important details, dates, or information, and he'll store it in his memory for easy retrieval later on.

- ➕ **Built-in Calculator**: Miles can use a real calculator and will provide math results in LaTeX format.

- 👨‍💻 **Multi-tasking**: Miles can handle up to 3 tools or tasks simultaneously, streamlining your productivity.

- 🔍 **Contextual Awareness**: Miles understands context about himself, his creator, the app he's in, and you – based on the information you provide him.

- 🎤 **Realistic Voice**: Powered by OpenAI's Text-to-Speech technology, Miles has a natural, human-like voice that enhances the overall experience.

- 👂 **Wake Word Detection**: Miles responds accurately to Miles, hey Miles, Yo Miles or just anything you want, as long as it ends with Miles.
  
- 🌐 **Internet Browsing:** Miles can search the internet for anything you ask about, you don't even have to be direct.


## 💡 Tips and Tricks

- 🤔 **Ask About Capabilities**: Not sure what Miles can do? Just ask him! He'll tell you everything.

- 💰 **Cost-Effective Mode**: Find Miles too pricey? Ask him to be cheaper, and he'll switch to a more cost-effective model and system prompt. 💸

- 🎭 **Personality Customization**: Miles can rewrite his own personality and instructions on command! Tell him to be anything you want. 🤯

- 🔑 **API Keys**: You'll need a few API keys to use Miles, but the app will guide you. Only OpenAI requires payment. 💳

## 🗣️ Natural Language Commands

Miles is powered by a language model, so no specific commands are needed. Just speak naturally, and he'll understand! For example:

- 🎶 "Miles, play that funky tune that gets me groovin'!" 
- 💃 "Yo Miles, what's the weather gonna be like for my pool party this weekend?"
- 🤖 "Miles, please store the date of my bestie's birthday so I don't forget it again!" 

Let your imagination run wild with Miles!

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


## 🚀 **Download and Installation**

### M.I.L.E.S is designed to be fully cross-platform, ensuring a seamless experience on both macOS and Windows. Depending on your operating system, follow the corresponding guide for installation instructions:

- **macOS Users**: Enjoy a straightforward installation with our easy install script. [Install on macOS (easy install guide)](https://github.com/small-cactus/M.I.L.E.S/wiki/Install-Miles-on-MacOS-(Easy-Install-method))

- **Windows Users**: Due to platform limitations, the installation process involves a few more steps. But don't worry, we've got you covered with a detailed guide. [Install on Windows (detailed guide)](https://github.com/small-cactus/M.I.L.E.S/wiki/Install-Miles-On-Windows)
  
  - **Do I have to pay?** The only API that requires payment is OpenAI, it is a pay per use model so you won't have unnecessary charges. You also need Spotify Premimum to use Miles` Spotify features, but to get the API key I believe it's free.

<br><br>

## 🔍 Troubleshooting Guide

**Disclaimer:** This guide is the product of a collaboration between the world's most advanced AI, which powers M.I.L.E.S, and a human expert who has meticulously reviewed it for accuracy and clarity.

### Before You Begin

- Run command lines as Administrator on Windows or prefix commands with `sudo` on Mac/Linux.
- Ensure a stable internet connection.
- Verify there's enough disk space and you have the necessary permissions for installations.
- Keep your operating system updated to prevent compatibility issues.

### Specific Issues and Solutions

1. **Chocolatey Installation Failure:**
   - **Error:** "Cannot connect to Chocolatey website."
     - **Solution:** Check your internet connection. For proxy users, configure Chocolatey to utilize your proxy settings.
   - **Error:** "ExecutionPolicy restriction."
     - **Solution:** Execute `Set-ExecutionPolicy AllSigned` or `Set-ExecutionPolicy Bypass -Scope Process` in PowerShell as Administrator.

2. **Python Installation Failure via Chocolatey:**
   - **Error:** "Python package not found."
     - **Solution:** Update Chocolatey with `choco upgrade chocolatey`. If unresolved, install Python manually from its official website and adjust your PATH accordingly.
   - **Error:** "Error during installation."
     - **Solution:** Consult the Chocolatey logs at `C:\ProgramData\chocolatey\logs\chocolatey.log`. Retry the installation ensuring a stable internet connection.

3. **Virtual Environment Activation Error:**
   - **Error:** "Virtual environment not activating."
     - **Solution:** Confirm you're in the directory where `Miles-env` was created before attempting activation. Reinstall Python with the 'Add Python to PATH' option selected if issues persist.

4. **Git Installation Failure:**
   - **Error:** "Git is not recognized as an internal or external command."
     - **Solution:** Check Git installation with `choco install git -y`. For persistent issues, add Git manually to your system PATH.

5. **Node.js and npm Installation Issues:**
   - **Error:** "npm commands not recognized."
     - **Solution:** Reinstall Node.js through Chocolatey using an Administrator PowerShell window. Add Node.js to your PATH manually if necessary.

6. **Project Repository Clone Failure:**
   - **Error:** "Repository not found."
     - **Solution:** Verify the repository URL. Ensure Git is installed and you have an active internet connection.

7. **Setup Script Execution Error:**
   - **Error:** "Setup script fails to execute."
     - **Solution:** Change execution policy with `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`. Ensure the script's path is correct before retrying.

8. **Node.js/npm Dependency Installation Failure:**
   - **Error:** "npm ERR! code EACCESS."
     - **Solution:** Operate your terminal as Administrator or use `sudo` on Mac/Linux. Consider using nvm for easier version and permission management.

9. **API Key Configuration Issues:**
   - **Error:** "Invalid API Key."
     - **Solution:** Recheck your API keys for accuracy. Ensure they're correctly placed in your configuration files or environment variables.

10. **Spotify API Connection Failure:**
    - **Error:** "Could not reach Spotify API."
      - **Solution:** Confirm your Spotify client ID and secret. Check if your firewall or antivirus is blocking the connection. For proxy users, adjust your system or application settings accordingly.

### Advanced Troubleshooting

- **Reinstalling Chocolatey Packages:** Uninstall problematic packages with `choco uninstall package-name` and reinstall them.
- **Firewall/Antivirus Interference:** Temporarily disable these to check if they're blocking installations, remembering to enable them afterward.
- **Updating System Dependencies:** Ensure all necessary system libraries are up to date by running system updates.

### Final Resort

- **Log Analysis:** Check installation logs for specific error messages. For Chocolatey, refer to `C:\ProgramData\chocolatey\logs\chocolatey.log`.
- **Seek Help Online:** Use error messages to search for solutions on platforms like Stack Overflow, official documentation, or through the GitHub issues page of the software.

**Note:** The AI and I have combined our knowledge and expertise to provide you with detailed solutions. Yet, some issues may require adjustments based on your specific system setup.

For further assistance, feel encouraged to use the GitHub issues tab to report unresolved problems.






## ✨ **Highlights & Features**
- **Unrestricted Interaction**: M.I.L.E.S has `no token limit`, this means you might be twiddling your thumbs if you submit a long request.
  
- **Intuitive Understanding & Action**: Powered by an advanced `language model`, M.I.L.E.S not only grasps even the most uniquely phrased commands but also proactively executes actions when it deems necessary. It's basically `magic in a bottle`, but not it a bottle, or magic.
  
- **Customization**: Just `ask M.I.L.E.S to change his model` and he will. Miles can also `change his own system prompt on command` or by himself to whatever he wants.
  
- **World Class Wake Word Invocation**: Whether you say `"Hey Miles"`, `"Hi Miles"`, `"What's up Miles"`, `"Miles"`, or literaly any starting phrase that ends with `"Miles"`, the system WILL respond accurately. We have about a `10% fail rate` for hearing if it's been activated, and a 0% accidental activation error rate.
  
- **Advanced Audio Processing**: M.I.L.E.S excels in noisy environments, ensuring accurate command interpretation.
  
- **Graphics & Interface**: Features a `dynamic interface` displaying Spotify song playback, weather cards, user interactions, and ongoing actions.

## 📜 **Changelog**
- 🔊 **Realistic Voice Upgrade with `OpenAI TTS`**: M.I.L.E.S now utilizes `OpenAI TTS` for Text-To-Speech, elevating the voice quality to `ultra-realistic` levels. M.I.L.E.S will seamlessly switch to a `basic TTS` if any errors are detected.
- 📢 **Enhanced Wake Word Detection**: M.I.L.E.S now leverages the same technology used in `leading smart home products` like `Google Home` and `Alexa` for `unmatched wake word detection accuracy`, this means you don't have to wait for the program to listen and stop listening, now it's `always listening`!
- 🔢 **Enhanced Calculator Operations**: M.I.L.E.S now efficiently handles `multiple simultaneous calculations` at the same time.
- 💡 **Improved UI**: Introducing a `graphical interface` for better user interactions.
- 🌦️ **Enhancements**: Augmented `weather data`, `permanent memory`, and `date + time support`.
- 🎲 **Multi-Task Mode** M.I.L.E.S can use up to `3 tools` at once, this means M.I.L.E.S can find the weather in `Shanghai`, calculate the temp difference if it were to drop `23.883 degrees`, and then store it in memory to call upon later, all before he even responds to you. That's the future.
- 💻 **Cross Platform!** M.I.L.E.S now supports `MacOS` and `Windows 10/11`.
- 🎧 **Full Playback Controls** M.I.L.E.S can now `pause`, `unpause`, `toggle playback`, set `spotify volume`, and set `system volume`.
- 🔇 **Smart Audio Management** If you request Miles while a song is playing, he will `pause it to listen`, `unpause at a low volume` while he speaks, and return to the `orginal volume` when he's done talking. Miles also remembers `playback states` and `volume levels`.
- 💾 **Internal Automatic Model Switching** Find that `GPT-4-Turbo` is too expensive? Just ask Miles to change it to the `cheaper one`. It's that simple.
- 🌘 **Dynamic Action Notifications** Miles' UI now shows `what specifically he is doing`, instead of "Searching a song" it'll now say "Searching for `Never gonna give you up`". This is applied for all Actions.
- 🪪 **Internal Automatic Personality switching** M.I.L.E.S can now change his own `system prompt` from what you ask, or by himself. This lets him or you specify `personality traits`, `ways of responding`, and `topics to talk about or avoid`. Think of it like a `instruction set` combined with a `personality desctiption`.
- ⚙️ **Graphical Setup Process** Once you start the app, it will `automaticaly show a setup screen` if you don't already have API keys setup.
- 🧠 **Default Model Change** The **default LLM is now `GPT-3.5-Turbo`**, the only reason for this is that most people `don't have access to GPT-4-Turbo` so `Miles would crash instantly`. If you have access and want to use `GPT-4-Turbo` just **ask Miles to change it to `GPT-4-Turbo`**.
- 🐛 **Error Handling on Front End**: Errors will now display in the action notification when they occur, enhancing user experience by providing immediate feedback.
- 🎧 **Better Audio Input Management**: Automatically switches without giving errors and allows low bitrate devices to work, improving accessibility and reliability.
- 🧮 **LaTeX Math Formatting**: Miles will reply to all math questions in LaTeX format, ensuring that mathematical expressions are displayed correctly and are easy to read.

## 🆕 **In Progress Features**
### Progress on feature: 0% (Not prioritized)
- ⚙️ **Graphical settings and config menu** As much as I want the users of Miles to speak their every command and desire to him without ever clicking buttons or typing, I also don't want people to have to physically change lines of code to get Miles to work. Let's say someone doesn't have access to GPT-4-Turbo, most people don't, since you wouldn't be able to ask Miles to switch the model by himself, you'd have to dig into the main code, so instead, right after I get the api key interface working, i'll be putting both the api key interface, and any config settings including speed and cost optimizing features in a settings menu that will be located in the top right of the app.

### Progress on feature: 50% (Missing front end code to implement)
- 🪙 **Real time response streaming** I am "trying" to add real time streaming on a token by token basis for all responeses, now this by itself doesn't seem like a hard task, but no, this is the most challenging part of Miles that I have ever attempted. Right now, (future employers look away) I literally take print statements and format them to appear on the main interface, this works with responeses that show all at once, but this is "probably" not gonna work with streaming, typically each chunk would be printed at a time, and I would have to print a start and end token, as well as a tool call token to infer when to start and stop the stream on the front end, which is literally not possible with my skill level, it's just too over engineered. So I have to learn socket io management and figure out how to implement that into the app to replace the current method, I *REALLY* don't wanna do this, so I'm just gonna wait for GPT-5 so it can do it for me :).

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

🔍 **My Work Ethic**: At the core of my development philosophy is simplicity and accessibility. I firmly believe that everyone, irrespective of their expertise or financial standing—be it novice or advanced, rich or poor—should have access to cutting-edge technology like M.I.L.E.S. It's for this reason I've committed to keeping M.I.L.E.S free, permanently. Despite the costs I bear to keep this vision alive. I strive to create an interface so intuitive that anyone can harness its full potential with ease, making AI-driven assistance universally accessible.

🌱 **The Origin**: My journey into this world of voice assistants began when I recognized the limitations of platforms like Siri. Eager to bring a more competent solution to the table, I embarked on a self-taught coding expedition. This led to the birth of my initial project, **JarvisChatGPT**, available in my other repository. While JarvisChatGPT was a step in the right direction, emphasizing simplicity, I knew I had the potential to create something even more advanced. Hence, M.I.L.E.S was conceived, a culmination of weeks of learning, testing, and innovating.

Your support fuels my passion, and I'm excited to continue this journey with all of you!

## 🤝 **Contribute to Development**
Your feedback shapes M.I.L.E.S! Though this is a beta release, we eagerly await your feature requests and issue reports for our final launch on GitHub.

**Contact:** anthonyhayward1000@gmail.com

