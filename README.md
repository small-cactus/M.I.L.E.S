# **Miles - GPT 4 Turbo powered voice assistant**

> **M.I.L.E.S (Machine Intelligent Language Enabled System)** is a cutting-edge voice assistant powered by the same technology used in ChatGPT. Enhance your day with magical voice commands and state-of-the-art language processing.

<p align="center">
  <img src="miles_logo.png" width="200">
</p>

## 🌐 **Core Features**
- 📡 **Powered by AI language models:** Operated by **`GPT-3.5-Turbo`** and **`GPT-4-Turbo`** model out of the box for maximum compatibility, but easily switchable to `any other OpenAI model` via asking Miles to change it.
- 🎵 **Integrated with Spotify:** Enjoy `seamless Spotify controls` right from your voice. *(Requires Spotify Premium)*
- ☀️ **Weather Capabilities:** Stay updated with `real-time weather data`.
- 🧠 **Persistant Selective Memory:** Ask Miles to `remember something, ask him to forget it`.
- 🧮 **Calculator:** Don't rely on language model math, Miles can use a `real calculator`.
- 🧩 **Multi-tasker:** Miles can use up to `3 tools at the same time`.
- 🤔 **Context:** `Miles has context` about him, who made him, the app he's in, and who you are through things you ask him to remember.
- 🎙️ **Realistic Voice:** Miles `doesn't sound like a robot, he sounds real`. (Both faster and cheaper than eleven labs for the same quality - OpenAI TTS)
- 🔊 **Wake word:** Our wake word detection is `on par with smart home assistants`.

## 🔥 **Tips and Tricks**
- ‼️ **I strongly recommend you `ask Miles what he can do and what tools he can use`, he is aware of everything he can do when using the `default system prompt`.**
- 💰 **Find it too expensive to run?** Just `ask Miles to be cheaper` and he will switch his language model and ask him to make his system prompt cheaper and he will be more cost effective for you.
- 🪪 **Ask Miles to be Anything** Miles can `manipulate his own personality and instructions`, just ask him to be anything and he will rewrite himself to comply.
- ⚠️ **Things to Note**: When you ask Miles to be cheaper, he will do both of these things:
  1. Switch his model to `GPT-3.5-Turbo`.
  2. Rewrite his system prompt to `reduce the token count by 700 tokens`.
  3. However, in doing both of these things, he will lose most of his functinality and will be less helpful, he `does NOT actually lose any functinality` in doing this, but he may hallucinate that he can't do some of the things you ask him to do. Asking him to write a custom system prompt for a specific list of instructions will help.

💡 **Note:** Before diving in, make sure you have your **`OpenAI API key`**. Place this key within the quotes in the `apikey.py` file.

## 📄 **What commands are there?**
`There are no commands`, Miles is powered by a language model, not code, say anything however you like and it will work, want to play Spotify? You can just say this:
- `"Miles, prithee, lend thine ear to Spotify's sweet melodies and grace us with a song that doth stir the soul."`
  ### or this:
- `"Miles, play that one song that was in the spongebob movie."`
  ### or this:
- `"Miles, in yonder digital realm of Spotify, embark thou upon a quest to unleash the timeless lay 'Never Gonna Give You Up', that we may be ensnared in its melodious rapture most unexpected."`

  <br><br>
  ## 🖥️ M.I.L.E.S Conversation screen
  ![M.I.L.E.S Interface](https://github.com/small-cactus/M.I.L.E.S/blob/main/screenshots/conversation.webp)
  <br><br>
  ## 🔍 M.I.L.E.S Action notifications
  If they look wonky it's because each action has an animation and it's hard to screenshot because it's moving + Miles responds too fast to screenshot it. Sorry about that!
  ![M.I.L.E.S Actions](https://github.com/small-cactus/M.I.L.E.S/blob/main/screenshots/actions.webp)
  - These action notifications are outdated as of today, there are 10 new actions Miles can perform on top of the ones shown, I will update them when I have time.
  <br><br>

## 🚀 **Download and Install (Mac easy install)**

1. **Install Homebrew:**
  ```
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  ```
2. **Install Git:**
  ```
  brew install git
  ```

3. **Clone the Repo:**
  ```
  git clone https://github.com/small-cactus/M.I.L.E.S.git
  ```
4. **Run setup script:**
  ```
   cd ~/M.I.L.E.S/Miles-V2
  ```
   **Next, run:**
  ```
   chmod +x setup.sh
  ```
   **Finally, run:**
  ```
   ./setup.sh
  ```
5. **Config:**

  🥳 The app will guide you through setup once it's open. (You need an `OpenAI API` key, `Picovoice API` key, `Spotify client ID`, `Spotify Client Secret`, `Your city`, and `Your preferred Unit`.) **`All have steps in the app`**.

  - **Do I have to pay?** The only API that requires payment is OpenAI, it is a pay per use model so you won't have unnecessary charges. You also need Spotify Premimum to use Miles` Spotify features, but to get the API key I believe it's free.

<br><br>

## 🔍 **Troubleshooting**
**This is a beta release, troubleshooting steps are based off of nothing but `hopes and dreams` of what I think might go wrong, submit issues in `githubs issue tracker` for now if the steps don't help.**
### **It won't start**
1. Check if you have access to the model this project uses, if you don't, follow the instructions in `OpenAI section` above.
2. Check if you have `python 3.11`, open terminal and run `brew search python`. Check for a `green checkmark` next to `python 3.11`, if there isn't, refer to `inital setup instructions`.

### **Nothing works and I'm going crazy!!!**
1. `Calm down`
2. Using the `same commands` in the inital setup, replace `install` with `uninstall` and click enter.
3. Now we're going to make a `virtual environment`, this seperates my project from anything on your Mac that might be conflicting with it, don't worry, this is easy.
4. **First,** `make a new folder anywhere`, name it anything you want, but let's call it `virtual-env`.
5. **Next,** `right click the folder and click open in terminal`, next enter the following command `python3.11 -m venv myenv`.
6. **Next,** now that we have the environment created, we need to activate it, **run the command** `source myenv/bin/activate`.
7. **Lastly,** if you can see the little (myenv) on the left of the command line, you did it right! if not, delete the folder and try again.
8. **What next?** Now that you have the virtual environment set up, just go through the setup as normal like it's written above. Just make sure you use the `cd` command followed by a file or folder directory instead of opening the terminal directly from the file. Good luck!

### **All hope is lost, I am so lost.**
1. No worries!
2. Log into `ChatGPT`.
3. Paste the entirety of this text into `ChatGPT`. You may need to do small portions and go 1 at a time.
4. Ask ChatGPT "`How do I install this? I'm so confused!`"
5. Hope and pray that it understands.
6. Good luck.

### **All I ask for is mercy, these funny magic words are nonsense, what even is a command????????**
1. **Beginner's Quest:** Google "`Free online coding courses for beginners`" and pick one.
2. **Three-Month Challenge:** Spend the next three months learning the basics of coding.
3. **Immerse Yourself:** Surround your workspace with coding notes and `inspirational quotes`.
4. **YouTube Marathon:** Watch as many coding tutorials as you can until you dream in code.
5. **Community Engagement:** Join online coding forums and share your journey.
6. **The Return:** Armed with knowledge, revisit this project and conquer the commands.
7. **Wisdom of the Ages:** If stuck, seek advice from the `oldest tech wizard` you know.
8. **Celebrate Your Triumph:** Regardless of the outcome, treat yourself for embarking on this coding adventure.





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



## 🆕 **In Progess Features**
- ⚙️ **Graphical settings and config menu** As much as I want the users of Miles to speak their every command and desire to him without ever clicking buttons or typing, I also don't want people to have to physically change lines of code to get Miles to work. Let's say someone doesn't have access to GPT-4-Turbo, most people don't, since you wouldn't be able to ask Miles to switch the model by himself, you'd have to dig into the main code, so instead, right after I get the api key interface working, i'll be putting both the api key interface, and any config settings including speed and cost optimizing features in a settings menu that will be located in the top right of the app.


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

