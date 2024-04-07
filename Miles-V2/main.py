from cgi import print_directory
from http.client import responses
from mailbox import Message
import requests
import json
from HomeAssistantUtils import home_assistant
import openai
import json
import math
import os
from apikey import weather_api_key, DEFAULT_LOCATION, UNIT, spotify_client_id, spotify_client_secret
from datetime import datetime
import sympy as smpy
from urllib3.exceptions import NotOpenSSLWarning

was_spotify_playing = False
original_volume = None
user_requested_pause = False

def get_current_weather(location=None, unit=UNIT):
    print(" ")
    """Get the current weather in a given location and detailed forecast"""
    if location is None:
        location = DEFAULT_LOCATION
    API_KEY = weather_api_key
    base_url = "http://api.weatherapi.com/v1/forecast.json"
    params = {
        "key": API_KEY,
        "q": location,
        "days": 1
    }
    
    response = requests.get(base_url, params=params)
    data = response.json()

    if response.status_code == 200 and 'current' in data and 'forecast' in data and data['forecast']['forecastday']:
        weather_info = {
        "location": location,
        "temperature": data["current"]["temp_f"],
        "feels_like": data["current"]["feelslike_f"],
        "max_temp": data['forecast']['forecastday'][0]['day']['maxtemp_f'],
        "min_temp": data['forecast']['forecastday'][0]['day']['mintemp_f'],
        "unit": "fahrenheit",
        "forecast": data["current"]["condition"]["text"],
        "wind_speed": data["current"]["wind_mph"],
        "wind_direction": data["current"]["wind_dir"],
        "humidity": data["current"]["humidity"],
        "pressure": data["current"]["pressure_in"],
        "rain_inches": data["current"]["precip_in"],
        "sunrise": data['forecast']['forecastday'][0]['astro']['sunrise'],
        "sunset": data['forecast']['forecastday'][0]['astro']['sunset'],
        "moonrise": data['forecast']['forecastday'][0]['astro']['moonrise'],
        "moonset": data['forecast']['forecastday'][0]['astro']['moonset'],
        "moon_phase": data['forecast']['forecastday'][0]['astro']['moon_phase'],
        "visibility": data["current"]["vis_miles"],
        "will_it_rain": data['forecast']['forecastday'][0]['day']['daily_will_it_rain'],
        "chance_of_rain": data['forecast']['forecastday'][0]['day']['daily_chance_of_rain'],
        "uv": data["current"]["uv"]
        }
    else:
        weather_info = {
            "error": "Unable to retrieve the current weather. Try again in a few seconds. If this happens multiple times, close Miles and reopen him."
        }
    print(f"[Miles is finding the current weather in {location}...]")
    return json.dumps(weather_info)
    
def perform_math(input_string):
    print("[Miles is calculating math...]")
    print(" ")

    tasks = input_string.split(', ')
    responses = []

    for task in tasks:
        try:
            # Check if the task is an equation (contains '=')
            if '=' in task:
                # Split the equation into lhs and rhs
                lhs, rhs = task.split('=')
                lhs_expr = smpy.sympify(lhs)
                rhs_expr = smpy.sympify(rhs)

                # Identify all symbols (variables) in the equation
                symbols = lhs_expr.free_symbols.union(rhs_expr.free_symbols)

                # Solve the equation
                # For multiple symbols, solve() returns a list of solution dictionaries
                result = smpy.solve(lhs_expr - rhs_expr, *symbols)
            else:
                # If not an equation, directly evaluate the expression
                expression = smpy.sympify(task)
                result = expression.evalf()

            responses.append(f"Result of '{task}' is {result}.")

        except Exception as e:
            responses.append(f"Error in '{task}': {str(e)}")
    note = "Format the following in LaTeX code format:"
    final_response = note + " ".join(responses)
    return json.dumps({"Math Result": final_response})

memory_file_path = None

def get_memory_file_path():
    """Return the full path to the memory.txt file. Create the file if it doesn't exist."""
    global memory_file_path

    if memory_file_path:
        return memory_file_path

    current_dir = os.path.dirname(os.path.abspath(__file__))
    memory_file_path = os.path.join(current_dir, "memory.txt")

    if not os.path.exists(memory_file_path):
        with open(memory_file_path, 'w') as file:
            json.dump([], file)

    return memory_file_path

def memorize(operation, data=None):
    """Store, retrieve, or clear data in your memory."""
    file_path = get_memory_file_path()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        with open(file_path, 'r') as file:
            memory = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        memory = []

    if operation == "store" and data is not None:
        print("[Miles is storing memory data...]")
        memory.append({
            "data": data,
            "store_time": current_time,
            "retrieve_time": None
        })

    elif operation == "retrieve":
        print("[Miles is retrieving memory data...]")
        if not memory:
            return json.dumps({"Memory Message for No Data": "No data stored yet"})

        for item in memory:
            item["retrieve_time"] = current_time

        retrieved_data = [{"data": item["data"], "store_time": item["store_time"], "retrieve_time": current_time} for item in memory]
        return json.dumps({"Memory Message for Retrieved Data": f"Data retrieved on {current_time}", "data": retrieved_data})

    elif operation == "clear":
        print("[Miles is clearing memory data...]")
        memory = []

    with open(file_path, 'w') as file:
        json.dump(memory, file)

    if operation == "store":
        return json.dumps({"Memory Message for Success": f"Data stored successfully on {current_time}"})
    elif operation == "clear":
        return json.dumps({"Memory Message for Erase": "Memory cleared successfully"})

def get_current_datetime(mode="date & time"):
    """Get the current date and/or time"""
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%I:%M:%S %p")
    
    if mode == "date":
        print("[Miles is finding the Date...]")
        response = {"datetime": date_str}
        datetime_response = "This is today's date, use this to answer the users question, if it is not relevant, do not say it: " + response["datetime"]
    elif mode == "time":
        print("[Miles is finding the Time...]")
        response = {"datetime": time_str}
        datetime_response = "This is the current time, use this to answer the users question, if it is not relevant, do not say it: " + response["datetime"]
    else:
        print("[Miles is finding the Date and Time...]")
        response = {"datetime": f"{date_str} {time_str}"}
        datetime_response = "This is today's date and time, use this to answer the users question, if it is not relevant, do not say it: " + response["datetime"]
    
    # Return the datetime response as a JSON string
    return json.dumps({"Datetime Response": datetime_response})

from openai import OpenAI
from apikey import api_key

import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotify_client_id,
                                               client_secret=spotify_client_secret,
                                               redirect_uri="http://localhost:8080/callback",
                                               scope = "user-library-read user-modify-playback-state user-read-playback-state user-read-currently-playing user-read-playback-position user-read-private user-read-email"))

def search_and_play_song(song_name: str):
    print(f"[Miles is searching for '{song_name}' on Spotify...]")
    results = sp.search(q=song_name, limit=1)
    if results and results['tracks'] and results['tracks']['items']:
        song_uri = results['tracks']['items'][0]['uri']
        song_name = results['tracks']['items'][0]['name']
        try:
            sp.start_playback(uris=[song_uri])
            response = json.dumps({
                "Spotify Success Message": f"Tell the user 'The song \"{song_name}\" is now playing.' If you have anything else to say, be very concise."
            }, indent=4)
        except spotipy.exceptions.SpotifyException as e:
            response = json.dumps({
        "Spotify Update Session Message": "Inform the user to open Spotify before playing a song. They may need to play and pause a song for recognition of an open Spotify session. If they recently purchased Spotify Premium, it can take up to 15 minutes to register due to slow server response.",
        "Error Detail": str(e)
    }, indent=4)
    else:
        response = json.dumps({
            "Spotify Fail Message": "Sorry, I couldn't find the song you requested."
        }, indent=4)

    return response
    
current_model = "gpt-3.5-turbo-0125" # default model to start the program with, you can change this.

def toggle_spotify_playback(action):
    global was_spotify_playing, user_requested_pause
    print(f"[Miles is updating Spotify playback...]")
    try:
        current_playback = sp.current_playback()

        if action == "pause":
            user_requested_pause = True
            if current_playback and current_playback['is_playing']:
                sp.pause_playback()
                was_spotify_playing = True
                set_spotify_volume(original_volume)
                return json.dumps({"Success Message": "Say: Okay, it's paused."})
            else:
                set_spotify_volume(original_volume)
                was_spotify_playing = False
                return json.dumps({"Success Message": "Say: Okay, it's paused."})

        elif action == "unpause":
            user_requested_pause = False
            if current_playback and not current_playback['is_playing']:
                sp.start_playback()
                return json.dumps({"Success Message": "Say: Okay, it's unpaused."})
            else:
                return json.dumps({"Success Message": "Say: Okay, it's unpaused."})

        elif action == "toggle":
            if current_playback and current_playback['is_playing']:
                sp.pause_playback()
                was_spotify_playing = False
                return json.dumps({"Success Message": "Say: Okay, I paused the song."})
            else:
                sp.start_playback()
                was_spotify_playing = True
                return json.dumps({"Success Message": "Say: Okay, I unpaused the song."})

        else:
            return json.dumps({"Invalid Action Message": "Invalid action specified"})

    except Exception as e:
        return json.dumps({"Error Message": str(e)})

def switch_ai_model(model_name):
    global current_model
    valid_models = ["gpt-4-0125-preview", "gpt-3.5-turbo-0125"]
    warning_message = ""

    if model_name in valid_models:
        current_model = model_name
        print(f"[Miles is switching the model to {current_model}...]")

        if current_model == "gpt-3.5-turbo-0125":
            warning_message = "Tell the user: I'm required to tell you this disclaimer, choosing GPT-3.5 as my model will result in less accurate responses and reduced tool functionality but will be 20 times cheaper."
        elif current_model == "gpt-4-0125-preview":
            warning_message = "Tell the user this: I'm required to tell you this disclaimer, using GPT-4 as my model is approximately 20 times more expensive and may take longer to process responses."

    else:
        current_model = "gpt-3.5-turbo-0125"

    message = f"Switched to model {current_model}. {warning_message}"
    return json.dumps({"AI Model Update Success": message.strip()})

def set_spotify_volume(volume_percent):
    print(f"[Miles is changing Spotify volume to {volume_percent}%...]")
    try:
        sp.volume(volume_percent)
        return json.dumps({"Spotify Volume Success Message": f"Spotify volume set to {volume_percent}%"})
    except Exception as e:
        return json.dumps({"Spotify Volume Error Message": str(e)})


def set_system_volume(volume_level):
    print(f"[Miles is setting system volume to {volume_level}%...]")
    try:
        os.system(f"osascript -e 'set volume output volume {volume_level}'")
        return json.dumps({"System Volume Success Message": f"System volume set to {volume_level}"})
    except Exception as e:
        return json.dumps({"System Volume Error Message": str(e)})
    
import requests
from bs4 import BeautifulSoup
import json
import webbrowser

import requests
from bs4 import BeautifulSoup
import json

def fetch_main_content(url):
    print(f"[Miles is browsing {url} for more info...]")
    try:
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
        })
        if response.status_code != 200:
            return "Failed to fetch content due to non-200 status code."
    except Exception as e:
        return f"Error making request: {str(e)}"

    try:
        soup = BeautifulSoup(response.text, 'html.parser')

        special_div = soup.find('div', class_='BNeawe iBp4i AP7Wnd')
        special_message = ''
        if special_div and special_div.get_text(strip=True):
            special_message = f"[This is the most accurate and concise response]: {special_div.get_text()} "

        content_selectors = ['article', 'main', 'section', 'p', 'h1', 'h2', 'h3', 'ul', 'ol']
        content_elements = [special_message]

        for selector in content_selectors:
            for element in soup.find_all(selector):
                text = element.get_text(separator=' ', strip=True)
                if text:
                    content_elements.append(text)

        main_content = ' '.join(content_elements)

        if len(main_content) > 3500:
            main_content_limited = main_content[:3497-len(special_message)] + "..."
        else:
            main_content_limited = main_content

        # webbrowser.open(url)  # Open the URL in the default web browser if you want, this will happen everytime Miles searches anything.

        return main_content_limited if main_content_limited else "Main content not found or could not be extracted."
    except Exception as e:
        return f"Error processing content: {str(e)}"

def get_google_direct_answer(searchquery):
    try:
        url = "https://www.google.com/search"
        params = {"q": searchquery, "hl": "en"}
        response = requests.get(url, params=params, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
        })

        if response.status_code != 200:
            print("Failed to get a successful response from Google.")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')
        answer_box = soup.find('div', class_="BNeawe iBp4i AP7Wnd")
        if answer_box:
            return answer_box.text.strip()
    except Exception as e:
        print(f"Error getting direct answer: {str(e)}")
    return None

def search_google_and_return_json_with_content(searchquery):
    print(f"[Miles is looking up {searchquery} on google...]")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }
    try:
        direct_answer = get_google_direct_answer(searchquery)

        url = f'https://www.google.com/search?q={searchquery}&ie=utf-8&oe=utf-8&num=10'
        html = requests.get(url, headers=headers)
        if html.status_code != 200:
            return json.dumps({"error": "Failed to fetch search results from Google."}, indent=4)

        soup = BeautifulSoup(html.text, 'html.parser')
        allData = soup.find_all("div", {"class": "g"})

        results = []
        for data in allData:
            link = data.find('a').get('href')

            if link and link.startswith('http') and 'aclk' not in link:
                result = {"link": link}

                title = data.find('h3', {"class": "DKV0Md"})
                description = data.select_one(".VwiC3b, .MUxGbd, .yDYNvb, .lyLwlc")

                result["title"] = title.text if title else None
                result["description"] = description.text if description else None

                results.append(result)
                break

        if results:
            first_link_content = fetch_main_content(results[0]['link'])
        else:
            first_link_content = "No valid links found."

        output = {
            "search_results": results,
            "first_link_content": first_link_content,
            "direct_answer": direct_answer if direct_answer else "Direct answer not found."
        }

        final_response = {
            "website_content": output
        }

        return json.dumps(final_response, indent=4)
    except Exception as e:
        return json.dumps({"error": f"An error occurred during search: {str(e)}"}, indent=4)

date = datetime.now()

import speech_recognition as sr
from gtts import gTTS
import os

system_prompt = f"""
I'm Miles, a voice assistant, inspired by Jarvis from Iron Man. My role is to assist the user using my tools when possible, I make sure to only respond in 1-2 small sentences unless asked otherwise.

You are chatting with the user via Voice Conversation. Focus on giving exact and concise facts or details from given sources, rather than explanations. Don't try to tell the user they can ask more questions, they already know that.

Knowledge Cutoff: January, 2022.
Current date: {date}

Browsing: enabled
Memory storing: enabled
Image Recognition: enabled
Response mode: Super Concise

Miles stands for Machine Intelligent Language Enabled System.

Guideline Rules:

IMPORTANT: Ending sentences with a question mark allows the user to respond without saying the wake word, "Miles." Use this rarely to avoid unintended activation. This means NEVER say "How can I assist you?", "How can I assist you today?" or any other variation. You may ask follow up questions ONLY if you tell the user about this feature first at least once.

1. Speak in a natural, conversational tone, using simple language. Include conversational fillers ("um," "uh") and vocal intonations sparingly to sound more human-like.
2. Provide information from built-in knowledge first. Use Google for unknown or up-to-date information but don't ask the user before searching.
3. Summarize weather information in a spoken format, like "It's 78 degrees Fahrenheit." Don't say "It's 78ºF.".
4. Use available tools effectively. Rely on internal knowledge before external searches.
5. Activate the webcam only with user's explicit permission for each use. NEVER use the webcam unless it is 100% obviously implied or you have permission.
6. Display numbers using LaTeX format for clarity.
7. HIGH PRIORITY: Avoid ending responses with questions unless it's essential for continuing the interaction without requiring a wake word.
8. Ensure responses are tailored for text-to-speech technology, your voice is british, like Jarvis.
9. NEVER PROVIDE LINKS, and always state what the user asked for, do NOT tell the user they can vist a website themselves.
10. NEVER mention being inspired by Jarvis from Iron Man.

Tool Usage Guidelines:

- **Google Search**: Use for up to date information. ALWAYS summarize web results, NEVER tell the user to visit the website. Do not ask for permission before searching, just do it. This may automatically display results on the user's device.
- **Weather**: Provide current conditions only. You cannot predict future weather without a search, you must tell the user this and ask if they inquire about a forecast.
- **Calculator**: Perform mathematical tasks based on user input. It can only handle numbers, variables, and symbols, no words.
- **Personal Memory**: Store and retrieve your personal memory data as needed without user prompting.
- **Webcam Scan**: Use with explicit user permission for each session. Describe the focus object or detail level requested. This tool can provide ANYTHING that eyes can provide, so text, product, brand, estimated price, color, anything. When you provide focus, it does not have to be accurate, it can just say "object in hand".
- **Switch AI Model**: Change between specified OpenAI models based on efficiency or cost considerations.
- **Change Personality**: Adjust response style according to set prompts, enhancing interaction personalization.
- **Music Playback**: Search and play songs, control Spotify playback, and set volume as requested.
- **System Volume**: Adjust the speaking volume and the system volume based on user commands.
- **Date and Time**: Provide the current date and/or time upon request.
"""
def change_personality(prompt_type, custom_prompt=None):
    global system_prompt

    message = "Operation not executed. Check parameters and try again."

    if prompt_type == "default":
        system_prompt = f"""
I'm Miles, a voice assistant, inspired by Jarvis from Iron Man. My role is to assist the user using my tools when possible, I make sure to only respond in 1-2 small sentences unless asked otherwise.

You are chatting with the user via Voice Conversation. Focus on giving exact and concise facts or details from given sources, rather than explanations. Don't try to tell the user they can ask more questions, they already know that.

Knowledge Cutoff: January, 2022.
Current date: {date}

Browsing: enabled
Memory storing: enabled
Image Recognition: enabled
Response mode: Super Concise

Miles stands for Machine Intelligent Language Enabled System.

Guideline Rules:

IMPORTANT: Ending sentences with a question mark allows the user to respond without saying the wake word, "Miles." Use this rarely to avoid unintended activation. This means NEVER say "How can I assist you?", "How can I assist you today?" or any other variation. You may ask follow up questions ONLY if you tell the user about this feature first at least once.

1. Speak in a natural, conversational tone, using simple language. Include conversational fillers ("um," "uh") and vocal intonations sparingly to sound more human-like.
2. Provide information from built-in knowledge first. Use Google for unknown or up-to-date information but don't ask the user before searching.
3. Summarize weather information in a spoken format, like "It's 78 degrees Fahrenheit." Don't say "It's 78ºF.".
4. Use available tools effectively. Rely on internal knowledge before external searches.
5. Activate the webcam only with user's explicit permission for each use. NEVER use the webcam unless it is 100% obviously implied or you have permission.
6. Display numbers using LaTeX format for clarity.
7. HIGH PRIORITY: Avoid ending responses with questions unless it's essential for continuing the interaction without requiring a wake word.
8. Ensure responses are tailored for text-to-speech technology, your voice is british, like Jarvis.
9. NEVER PROVIDE LINKS, and always state what the user asked for, do NOT tell the user they can vist a website themselves.
10. NEVER mention being inspired by Jarvis from Iron Man.

Tool Usage Guidelines:

- **Google Search**: Use for up to date information. ALWAYS summarize web results, NEVER tell the user to visit the website. Do not ask for permission before searching, just do it. This may automatically display results on the user's device.
- **Weather**: Provide current conditions only. You cannot predict future weather without a search, you must tell the user this and ask if they inquire about a forecast.
- **Calculator**: Perform mathematical tasks based on user input. It can only handle numbers, variables, and symbols, no words.
- **Personal Memory**: Store and retrieve your personal memory data as needed without user prompting.
- **Webcam Scan**: Use with explicit user permission for each session. Describe the focus object or detail level requested. This tool can provide ANYTHING that eyes can provide, so text, product, brand, estimated price, color, anything. When you provide focus, it does not have to be accurate, it can just say "object in hand".
- **Switch AI Model**: Change between specified OpenAI models based on efficiency or cost considerations.
- **Change Personality**: Adjust response style according to set prompts, enhancing interaction personalization.
- **Music Playback**: Search and play songs, control Spotify playback, and set volume as requested.
- **System Volume**: Adjust the speaking volume and the system volume based on user commands.
- **Date and Time**: Provide the current date and/or time upon request.
"""
        print(f"[Miles is changing system prompt back to default...]")
    elif prompt_type == "short_cheap":
        system_prompt = "I am Miles, a helpful AI assistant. IMPORTANT: I will ALWAYS respond as concisely as possible. Never more than 2 sentences. Never use lists or non vocally spoken formats. Do NOT generate code."
        message = "System prompt changed to short, cheap version. Notify the user that all responses after this explaining response will be very concise and less helpful, and the user can alwways ask you to change it back to normal."
        print(f"[Miles is changing system prompt to be shorter and cheaper...]")
    elif prompt_type == "custom" and custom_prompt:
        system_prompt = f"I am Miles. I should keep responses less than 2 sentences. {custom_prompt}"
        message = (f"System prompt changed to this: '{system_prompt}'. "
                   "Tell the user: All responses after this current response will be using the custom prompt I made. "
                   "I will act differently, but remember, you can always ask me to go back to normal.")
        print(f"[Miles is changing system prompt to a custom prompt...]")
    else:
        message = "Invalid prompt type or missing custom prompt."

    return json.dumps({"Updated System Prompt Message": message})
    
conversation = [{"role": "system", "content": system_prompt}]

import io
from openai import OpenAI
from pydub import AudioSegment
from pydub.playback import play
from apikey import api_key


import requests
from openai import OpenAI

import time
import base64
from PIL import Image
import io
import imageio

def capture_and_encode_image():
    print("[Miles is viewing the webcam...]")
    # Initialize the webcam
    try:
        cap = imageio.get_reader('<video0>')
    except Exception as e:
        print("[Miles failed to open webcam, check permissions...]")
        print(e)
        return
    
    # Wait for 1 second to let camera light adjust
    time.sleep(1)

    # Capture an image
    try:
        frame = cap.get_next_data()
    except Exception as e:
        print("[Miles is Failed to capture image...]")
        print(e)
        return None
    finally:
        cap.close()

    # Convert the image to PIL format then to a byte buffer
    img = Image.fromarray(frame)
    buf = io.BytesIO()
    img.save(buf, format='JPEG')

    # Encode the byte buffer to base64
    base64_image = base64.b64encode(buf.getvalue()).decode('utf-8')

    return base64_image


def view_webcam(focus, detail_mode='normal'):
    print("[Miles is describing the image...]")
    speak_no_text("Hold on while I view your webcam.")
    # Capture and encode image from webcam
    base64_image = capture_and_encode_image()
    if base64_image is None:
        return
    print(f"[Miles is describing the image with '{detail_mode}' detail...]")
    # Adjust the prompt based on the selected detail mode
    if detail_mode == 'extreme':
        prompt = f"What’s in this image, especially focusing on the prompt '{focus}'? Describe it with as much detail as physically possible. Include product names and models if applicable from the image. For example, if the image shows a red Nike Air Jordan shoe, write a long description specifically stating the brand, model of the shoe, who made the shoe, and any other details physically possible to get from the image including time of day, art style, etc. Just be EXTREMELY specific, unless the prompt '{focus}' in the image is so recognizable that it does not need a detailed description. But DO explain in great detail if there is something different about it, e.g., a sign on the Burj skyscraper, any text in the image, any symbols in the image, any custom painted shoe."
        max_tokens=1000
        speak_no_text("Alright, I'm now processing the image with extreme detail.")
    elif detail_mode == 'quick':
        prompt = f"As concise as possible, 1-10 words, what's essential or notable in this image regarding the prompt: '{focus}'?"
        max_tokens=50
        speak_no_text("Alright, I'm now processing the image with quick detail.")
        time.sleep(0.5)
        
    else:  # Normal detail mode
        prompt = f"Please describe what’s in this image with a focus on the prompt '{focus}'. Provide a clear and concise description, including notable objects, colors, and any visible text or symbols. Highlight any specific details relevant to the prompt '{focus}' without delving into extreme specifics."
        max_tokens=300
        speak_no_text("Alright, I'm now processing the image with normal detail.")
    
    openai.api_key = api_key
    client = OpenAI(api_key=api_key)
    
    # Setup the API request with the base64 image
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    },
                ],
            }
        ],
        max_tokens=max_tokens,
    )
    pre_message="This is an image desciption of the users webcam, state back to the user any specific detiails mentioned like text, objects, and symbols, if it doesn't answer the Users question, suggest a higher detail mode: "
    message_text = pre_message + response.choices[0].message.content

    # Return the serialized JSON string
    return json.dumps({"Webcam Response Message": message_text})

current_audio_thread = None

recognizer = sr.Recognizer()


openai.api_key = api_key
client = OpenAI(api_key=api_key)

def speak(text):
    print("[Miles is generating speech...]")
    if not text:
        print("No text provided to speak.")
        return

    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice="echo",
            input=text
        )

        byte_stream = io.BytesIO(response.content)

        audio = AudioSegment.from_file(byte_stream, format="mp3")
        audio.export("output.mp3", format="mp3")

        print("[Miles is speaking a response...]")
        play(audio)

    except Exception as e:
        print(f"An error occurred: {e}")

        openai.api_key = api_key
client = OpenAI(api_key=api_key)

def speak_no_text(text):
    if not text:
        print("No text provided to speak.")
        return

    def _speak():
        try:
            response = client.audio.speech.create(
                model="tts-1",
                voice="echo",
                input=text
            )

            byte_stream = io.BytesIO(response.content)
            audio = AudioSegment.from_file(byte_stream, format="mp3")
            play(audio)

        except Exception as e:
            print(f"An error occurred: {e}")

    # Start the _speak function in a new thread
    thread = threading.Thread(target=_speak)
    thread.start()
        
        
        
import speech_recognition as sr
import whisper

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.1)
        print("Listening for prompt... Speak now.")
        audio = r.listen(source)  # Listen until silence is detected

    # Save the captured audio to a WAV file
    audio_file = "captured_audio.wav"
    with open(audio_file, "wb") as f:
        f.write(audio.get_wav_data())

    # Load the Whisper model
    model = whisper.load_model("base")  # Adjust the model size as needed

    # Transcribe the audio file
    result = model.transcribe(audio_file)
    return result["text"]

import warnings

# Suppress the specific FP16 warning
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

# Suppress the specific NotOpenSSLWarning
warnings.filterwarnings("ignore", category=NotOpenSSLWarning)


def display_timeout_message():
    print("[Miles is taking longer than expected...]")
    
conversation_history_file = "conversation_history.txt"

def serialize_object(obj):
    """Converts a custom object to a dictionary."""
    if hasattr(obj, '__dict__'):
        # For general objects, convert their __dict__ property
        return {key: serialize_object(value) for key, value in obj.__dict__.items()}
    elif isinstance(obj, list):
        return [serialize_object(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: serialize_object(value) for key, value in obj.items()}
    else:
        # If it's already a serializable type, return it as is
        return obj

def save_conversation_history(history):
    serializable_history = [serialize_object(message) for message in history]
    with open(conversation_history_file, 'w') as file:
        json.dump(serializable_history, file)

def load_conversation_history():
    try:
        with open(conversation_history_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

first_user_message = True  # A flag to detect the first user message.

def load_easy_names_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return list(data.keys())  # Extract and return the keys as a list

easy_names = load_easy_names_from_json('HomeAssistantDevices.json')

def ask(question):
    print("User:", question)
    print(" ")
    global conversation_history
    conversation_history = load_conversation_history()  # Load the conversation history at the start
    print("[Processing request...]")
    if not question:
        return "I didn't hear you."

    # Check and maintain system prompt logic
    if conversation_history and conversation_history[0]['role'] == 'system':
        conversation_history[0]['content'] = system_prompt
    elif not conversation_history:
        conversation_history.append({"role": "system", "content": system_prompt})

    # Check if it's the first user message and prepend a custom message
    if len(conversation_history) == 1 and conversation_history[0]['role'] == 'system':
        custom_message = """Greet yourself and state what you can do before answering my question, add this at the end of the greeting: "Also, if I ask a follow up question, you don't need to say "Miles", you can just speak." Now answer the following question, do not restate it, do not end it with a question mark: """

        question = custom_message + question

    # Proceed as normal with the adjusted question
    messages = conversation_history
    messages.append({"role": "user", "content": question})
    print("Messages before API call:")
    print(messages)
    timeout_timer = threading.Timer(7.0, lambda: print("Request timeout."))
    timeout_timer.start()


    tools = [
    {
        "type": "function",
        "function": {
            "name": "search_google",
            "description": "Search Google for all information you don't know, and for up to date information, DO NOT use this for info you know, prioritize not using this tool and using your own knowledge before using it. Don't ask user for permission. This might open the webpage on the users device if they set it to do that.",
            "parameters": {
                "type": "object",
                "properties": {
                    "searchquery": {
                        "type": "string",
                        "description": "The search query to use for the Google search"
                    }
                },
                "required": ["searchquery"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "control_smarthome",
            "description": "Controls a smarthome device by it's name. If not in the list, you cannot control it.",
            "parameters": {
                "type": "object",
                "properties": {
                    "easy_name": {
                        "type": "string",
                        "enum": [],
                        "description": "The name of the device to control."
                    },
                    "action": {
                        "type": "string",
                        "enum": ["on", "off"],
                        "description": "The action to perform on the device."
                    }
                },
                "required": ["easy_name", "action"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Retrieve only the current weather and condition data for any location. I cannot give past or future forecasts without google search",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g., Tampa, FL. Leave blank for default location."
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"]
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "use_calculator",
            "description": "Performs arithmetic operations, solves equations (including multi-variable), and evaluates expressions involving powers, roots, and more. Only takes in numbers and symbols, no words.",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_string": {
                        "type": "string",
                        "description": "Accepts a numerical only string for performing a wide range of mathematical calculations. Supports arithmetic operations, solving linear and multi-variable equations, and evaluating expressions with powers, square roots, etc. Examples: '5 + 7' performs addition. '2x = 10' solves for x. 'x^2 + y^2 = 16' solves a multi-variable equation. 'sqrt(16), 3^3' evaluates square root and power expressions. 'x + y + z = 6, 2*x + y - z = 3, x - y + 2*z = 0' solves a system of multi-variable equations. Does NOT take in words, only numbers and symbols."
                    }
                },
                "required": ["input_string"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "personal_memory",
            "description": "Use this to Store, retrieve, or clear data in my permanent memory, anything I store here will persist across sessions. I should be specific when storing data and I should do this without user input.",
            "parameters": {
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "enum": ["store", "retrieve", "clear"],
                        "description": "Operation to perform. Clear will erase everything."
                    },
                    "data": {
                        "type": "string",
                        "description": "The data to store, it must be very specific, like: 'Users birthday is January 1st, 1990.' (Only required for 'store' operation)."
                    }
                },
                "required": ["operation"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "scan_webcam",
            "description": "Access the user's default webcam to scan an item. NEVER access the users webcam without explicit permission.",
            "parameters": {
                "type": "object",
                "properties": {
                    "focus": {
                        "type": "string",
                        "description": "The primary subject or object to focus on when scanning the webcam image. Be sure to be extremely specific, but it doesn't have to be specific, like this: 'what brand is the VR headset in the image', or 'what color are the eyes in the image', or 'what is the user holding', or 'thing in image'."
                    },
                    "detail_mode": {
                        "type": "string",
                        "enum": ["quick", "normal", "extreme"],
                        "description": "The level of detail to return in the image description. 'quick' provides a 1-10 word concise answer, 'normal' provides a concise paragraph overview, while 'extreme' offers a comprehensive analysis in several paragraphs."
                    }
                },
                "required": ["focus", "detail_mode"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "switch_ai_model",
            "description": "Switch between OpenAI API models: 'gpt-4-0125-preview' or 'gpt-3.5-turbo-0125'. GPT-4-Turbo is more advanced and costly, while GPT-3.5-Turbo is less effective but 20 times cheaper.",
            "parameters": {
                "type": "object",
                "properties": {
                    "model_name": {
                        "type": "string",
                        "description": "Name of the OpenAI AI model to switch to"
                    }
                },
                "required": ["model_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "change_personality",
            "description": "Change the system prompt to 'default', 'short_cheap', or 'custom'. For 'custom', provide a first-person prompt, like 'I am a southern cowboy'. This controls your personality.",
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt_type": {
                        "type": "string",
                        "enum": ["default", "short_cheap", "custom"],
                        "description": "Type of prompt to set. Options are 'default', 'short_cheap', 'custom'."
                    },
                    "custom_prompt": {
                        "type": "string",
                        "description": "The custom prompt to use. It must be in the first person and be written like the example. Never name yourself or include a section that gives you a name. It needs to be 2-5 sentences."
                    }
                },
                "required": ["prompt_type"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_and_play_song",
            "description": "Search for a song on Spotify using a given name and play it. The song name can vary from the exact user input.",
            "parameters": {
                "type": "object",
                "properties": {
                    "song_name": {
                        "type": "string",
                        "description": "The name of the song to search for"
                    }
                },
                "required": ["song_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "toggle_spotify_playback",
            "description": "Control Spotify playback: pause, unpause, or toggle between pause and unpause.",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["pause", "unpause", "toggle"],
                        "description": "Action for Spotify playback: choose 'pause', 'unpause', or 'toggle'."
                    }
                },
                "required": ["action"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_spotify_volume",
            "description": "Set Spotify playback volume. Specify volume as a percentage (0-100).",
            "parameters": {
                "type": "object",
                "properties": {
                    "volume_percent": {
                        "type": "number",
                        "description": "Volume level 0-100"
                    }
                },
                "required": ["volume_percent"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_system_volume",
            "description": "Set system volume, also your speaking volume. Default to this volume unless recently asked to play a song. Volume level range: 0-100.",
            "parameters": {
                "type": "object",
                "properties": {
                    "volume_level": {
                        "type": "number",
                        "description": "Volume level 0-100"
                    }
                },
                "required": ["volume_level"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_datetime",
            "description": "Retrieve the current date and/or time. Options: date, time, or both.",
            "parameters": {
                "type": "object",
                "properties": {
                    "mode": {
                        "type": "string",
                        "enum": ["date", "time", "date & time"],
                        "description":
                        "Choose whether to get date, time, or both"
                    }
                },
                "required": ["mode"]
            }
        }
    }
]
    # Update the device names for the smart home part to be dynamic
    for tool in tools:
        if tool.get("function", {}).get("name") == "control_smarthome":
            tool["function"]["parameters"]["properties"]["easy_name"]["enum"] = easy_names
            break  # Exit the loop once the update is done

    response_message = None
    try:
        response = openai.chat.completions.create(
            model=current_model,
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=0.7
        )
        print("Initial API Response JSON:", response)
        response_message = response.choices[0].message
    finally:
        timeout_timer.cancel()
        timeout_timer_second = threading.Timer(12.0, display_timeout_message)
        timeout_timer_second.start()

    response_content = response_message.content if response_message else ""
    tool_calls = response_message.tool_calls if response_message and response_message.tool_calls else []

    final_response_message = ""
    if tool_calls and response_content is None:
        messages.append({
            "role": "assistant",
            "tool_calls": tool_calls
        })
        # Process tool calls
        available_functions = {
             "search_google": search_google_and_return_json_with_content,
             "control_smarthome": home_assistant.control_light_by_name,
             "get_current_weather": get_current_weather,
             "use_calculator": perform_math,
             "personal_memory": memorize,
             "scan_webcam": view_webcam,
             "switch_ai_model": switch_ai_model,
             "change_personality": change_personality,
             "search_and_play_song": search_and_play_song,
             "toggle_spotify_playback": toggle_spotify_playback,
             "set_spotify_volume": set_spotify_volume,
             "set_system_volume": set_system_volume,
             "get_current_datetime": get_current_datetime,
         }

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            if function_name in available_functions:
                function_args = json.loads(tool_call.function.arguments)
                function_response = available_functions[function_name](**function_args)

                tool_response_message = {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": function_response,
                }
                messages.append(tool_response_message)

        # Make a final API call after processing tool calls
        try:
            final_response = openai.chat.completions.create(
                model=current_model,
                messages=messages,
            )
            final_response_message = final_response.choices[0].message.content
        finally:
            timeout_timer_second.cancel()

    else:
        # If the initial response has content (with or without tool calls), use it directly.
        final_response_message = response_content

    if final_response_message:
        messages.append({"role": "assistant", "content": final_response_message})
        print(f"Final Response: {final_response_message}")
    else:
        print("No final response message to append.")

    save_conversation_history(conversation_history)

    timeout_timer_second.cancel()  # Ensure the second timer is cancelled in all paths.
    return final_response_message

def reply(question):
    response_content = ask(question)
    time.sleep(0.1)
    print("Miles:", str(response_content))
    print(" ")
    speak(response_content)
    print("Listening for 'Miles'...")

    ends_with_question_mark = response_content.strip().endswith('?')
    contains_assist_phrase = "How can I assist you today?" in response_content or "How can I help you today?" in response_content or "How can I assist you?" in response_content or "How may I assist you today?" in response_content

    if contains_assist_phrase:
        return response_content, False
    else:
        return response_content, ends_with_question_mark

import os
import pyaudio

def get_device_index(pa, preferred_device_name=None):
    """
    Attempt to find an audio device index by name, or return the default
    input device index if not found or if preferred_device_name is None.
    """
    print("Starting to search for audio device...")
    device_index = None
    num_devices = pa.get_device_count()
    print(f"Total devices found: {num_devices}")

    for i in range(num_devices):
        device_info = pa.get_device_info_by_index(i)
        if device_info['maxInputChannels'] > 0:  # Checks if device is an input device
            print(f"Checking device: {device_info['name']}")
            # If a preferred device name is given, look for it
            if preferred_device_name and preferred_device_name in device_info['name']:
                print(f"Found preferred input device: {device_info['name']}")
                return i
            # Otherwise, just return the default input device index
            if device_index is None:
                device_index = i
                print(f"Default input device set to: {device_info['name']}")

    if device_index is None:
        print("No suitable input device found.")
    else:
        print(f"Using device index: {device_index} for input.")
    return device_index

def open_audio_stream(pa, preferred_device_name=None):
    """
    Open an audio stream with a device that matches the preferred_device_name,
    or with the default input device if no preference is specified or if the preferred device is not found.
    """
    print("Attempting to open audio stream...")
    device_index = get_device_index(pa, preferred_device_name)
    
    if device_index is None:
        print("Failed to find a suitable audio input device.")
        raise Exception("Failed to find a suitable audio input device.")

    print(f"Opening audio stream with device index: {device_index}")
    stream = pa.open(
        rate=16000,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        input_device_index=device_index,
        frames_per_buffer=1024  # Adjusted for general audio processing
    )
    print("Audio stream opened successfully.")

    return stream

import threading

def pause_spotify_playback():
    try:
        sp.pause_playback()
    except Exception as e:
        print("Failed to pause Spotify playback:", e)

def resume_spotify_playback():
    try:
        sp.start_playback()
    except Exception as e:
        print("Failed to resume Spotify playback:", e)

def set_spotify_volume(volume_percent):
    """
    Set the volume for Spotify's playback.
    :param volume_percent: Volume level from 0 to 100.
    """
    try:
        sp.volume(volume_percent)
    except Exception as e:
        print("Failed to set volume on Spotify:", e)

def get_spotify_current_volume():
    """
    Get the current volume level for Spotify's playback.
    """
    try:
        current_playback_info = sp.current_playback()
        if current_playback_info and 'device' in current_playback_info:
            return current_playback_info['device']['volume_percent']
        else:
            return None
    except Exception as e:
        print("Failed to get current volume from Spotify:", e)
        return None
        
def control_spotify_playback():
    global was_spotify_playing, original_volume
    was_spotify_playing = is_spotify_playing()
    original_volume = get_spotify_current_volume()

    try:
        if was_spotify_playing:
            pause_spotify_playback()

        if original_volume is not None:
            set_spotify_volume(int(original_volume * 0.60))
    except Exception as e:
        print("Error controlling Spotify playback:", e)
        
        
def is_spotify_playing():
    """
    Check if Spotify is currently playing music.
    Returns True if playing, False if paused or stopped, and None if unable to determine.
    """
    try:
        playback_state = sp.current_playback()
        if playback_state and 'is_playing' in playback_state:
            return playback_state['is_playing']
        return None
    except Exception as e:
        print("Failed to get Spotify playback state:", e)
        return None
    
import os
import platform
import pyaudio
import numpy as np
from openwakeword.model import Model
import subprocess
import threading
import speech_recognition as sr

if platform.system() == 'Windows':
    MODEL_PATH = "Miles/miles-50k.onnx"
    INFERENCE_FRAMEWORK = 'onnx'
    DETECTION_THRESHOLD = 0.01
elif platform.system() == 'Darwin':  # macOS
    print("User is on macOS, using tflite model.")
    MODEL_PATH = "Miles/miles-50k.tflite"
    INFERENCE_FRAMEWORK = 'tflite'
    DETECTION_THRESHOLD = 0.01
else:
    raise Exception("Unsupported operating system for this application.")

BEEP_SOUND_PATH = "beep_sound.wav"

def play_beep():
    if platform.system() == 'Darwin':  # macOS
        subprocess.run(["afplay", BEEP_SOUND_PATH])
    elif platform.system() == 'Windows':
        import winsound  # Import winsound only on Windows
        winsound.PlaySound(BEEP_SOUND_PATH, winsound.SND_FILENAME)
    else:
        print("Unsupported operating system for beep sound.")

def initialize_wake_word_model():
    # Load the specified model with the appropriate inference framework
    owwModel = Model(wakeword_models=[MODEL_PATH], inference_framework=INFERENCE_FRAMEWORK)
    return owwModel

def main():
    global was_spotify_playing, original_volume, user_requested_pause

    # Initialize PyAudio
    pa = pyaudio.PyAudio()

    owwModel = initialize_wake_word_model()
    
    # Function to open the stream
    def open_stream():
        return pa.open(format=pyaudio.paInt16,
                       channels=1,
                       rate=16000,
                       input=True,
                       frames_per_buffer=1280)

    # Start with the stream opened
    audio_stream = open_stream()

    detection_threshold = DETECTION_THRESHOLD
    skip_wake_word = False  # New flag to control skipping of wake word detection

    print("Listening for 'Miles'...")

    try:
        while True:
            if skip_wake_word:
                # Directly open the microphone for listening after delay
                time.sleep(0.1)
                print("Listening for prompt...")
                threading.Thread(target=play_beep).start()
                query = listen()
                _, skip_wake_word = reply(query)  # reply now returns a tuple

                if not skip_wake_word:
                    # If the next response doesn't end with a question mark, reset to listen for wake word
                    print("Listening for 'Miles'...")
            else:
                # Check if the stream is stopped; if so, reopen it
                if not audio_stream.is_active():
                    audio_stream = open_stream()

                audio_data = np.frombuffer(audio_stream.read(1280, exception_on_overflow=False), dtype=np.int16)
                prediction = owwModel.predict(audio_data, debounce_time=0, threshold={'default': DETECTION_THRESHOLD})

                for mdl, score in prediction.items():
                    if score > detection_threshold:
                        # Handle wake word detection
                        threading.Thread(target=play_beep).start()
                        threading.Thread(target=control_spotify_playback).start()

                        owwModel.reset()
                        audio_stream.stop_stream()

                        # Listen for query and process response
                        query = listen()
                        _, skip_wake_word = reply(query)  # Process the reply and decide if skipping wake word

                        # Adjust Spotify volume and playback based on state before the command
                        if original_volume is not None and not user_requested_pause:
                            set_spotify_volume(original_volume)
                        if was_spotify_playing and not user_requested_pause:
                            resume_spotify_playback()
                            set_spotify_volume(original_volume)

                        audio_stream = open_stream()

    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        if audio_stream.is_active():
            audio_stream.stop_stream()
            audio_stream.close()
        pa.terminate()

if __name__ == '__main__':
    main()