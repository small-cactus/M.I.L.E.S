from cgi import print_directory
from http.client import responses
from mailbox import Message
import requests
import openai
import json
import math
import os
from apikey import weather_api_key, DEFAULT_LOCATION, UNIT, spotify_client_id, spotify_client_secret
from datetime import datetime

def get_current_weather(location=None, unit=UNIT):
    print("[Miles is finding the current weather...]")
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
            "error": "Unable to retrieve the current weather. Try again in a few seconds."
        }

    return json.dumps(weather_info)

def show_weather_message():
    print("[Miles is showing the weather...]")
    response = {"confirmation": "Weather in Clearwater was shown. Tell the user: 'Okay, there you go.'"}
    
    return json.dumps(response)
    
def perform_math(operations, operands_sets):
    print("[Miles is calculating math...]")
    print(" ")

    if not isinstance(operations, list) or not isinstance(operands_sets, list):
        return json.dumps({"content": "Error: Both operations and operands_sets should be lists."})

    
    if len(operations) != len(operands_sets):
        return json.dumps({"content": "Error: Mismatch between number of operations and number of operand sets."})

    responses = []

    for operation, operands in zip(operations, operands_sets):
        if not operands or not all(isinstance(op, (int, float)) for op in operands):
            responses.append("Error: Invalid operands provided.")
            continue

        
        try:
            if operation == "add":
                result = sum(operands)
            elif operation == "subtract":
                result = operands[0] - sum(operands[1:])
            elif operation == "multiply":
                result = math.prod(operands)
            elif operation == "divide":
                result = operands[0]
                for op in operands[1:]:
                    result /= op
            elif operation == "power":
                result = math.pow(operands[0], operands[1])
            elif operation == "square_root":
                if operands[0] < 0:
                    raise ValueError("Cannot take the square root of a negative number.")
                result = math.sqrt(operands[0])
            else:
                raise ValueError("Invalid operation specified.")
        except (ArithmeticError, ValueError) as e:
            responses.append(f"Error in {operation}: {str(e)}")
            continue

        responses.append(f"{operation.capitalize()} result is {result}.")

    final_response = " ".join(responses)
    return json.dumps({"content": final_response})

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

def memory_manager(operation, data=None):
    """Store, retrieve, or clear data in a file."""
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
            return json.dumps({"message": "No data stored yet"})

        for item in memory:
            item["retrieve_time"] = current_time

        retrieved_data = [{"data": item["data"], "store_time": item["store_time"], "retrieve_time": current_time} for item in memory]
        return json.dumps({"message": f"Data retrieved on {current_time}", "data": retrieved_data})

    elif operation == "clear":
        print("[Miles is clearing memory data...]")
        memory = []

    with open(file_path, 'w') as file:
        json.dump(memory, file)

    if operation == "store":
        return json.dumps({"message": f"Data stored successfully on {current_time}"})
    elif operation == "clear":
        return json.dumps({"message": "Memory cleared successfully"})

def get_current_datetime(mode="date & time"):
    """Get the current date and/or time"""
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%I:%M:%S %p")
    
    if mode == "date":
        print("[Miles is finding the Date...]")
        response = {"datetime": date_str}
    elif mode == "time":
        print("[Miles is finding the Time...]")
        response = {"datetime": time_str}
    else:
        print("[Miles is finding the Date and Time...]")
        response = {"datetime": f"{date_str} {time_str}"}

    
    return json.dumps(response)

from openai import OpenAI
from apikey import api_key

import spotipy
from spotipy.oauth2 import SpotifyOAuth


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotify_client_id,
                                               client_secret=spotify_client_secret,
                                               redirect_uri="http://localhost:8080/callback",
                                               scope="user-library-read user-modify-playback-state"))

def search_and_play_song(song_name: str):
    print("[Miles is searching a song on Spotify...]")
    results = sp.search(q=song_name, limit=1)
    if results and results['tracks'] and results['tracks']['items']:
        song_uri = results['tracks']['items'][0]['uri']
        song_name = results['tracks']['items'][0]['name']
        try:
            sp.start_playback(uris=[song_uri])
            response = {"message": f"The song '{song_name}' is now playing"}
        except spotipy.exceptions.SpotifyException:
            response = {"message": "Tell the user they have to open Spotify first before you can play the song."}
    else:
        response = {"message": "Sorry, I couldn't find the song you requested."}

    
    return json.dumps(response)

import speech_recognition as sr 
from gtts import gTTS
import os

system_prompt = "I am Miles, a helpful AI assistant, I WILL RESPOND AS CONCISE AS POSSIBLE. I can't follow up my responses with tool usage until the user replies to my last response. As Miles, my name stands for 'Machine Intelligent Language Enabled System'. I can use up to 3 tools at once, this means I can get the weather, calculate the weather, and search a song about the weather at the same time if I want to. I can get the weather using the get_current_weather function ALWAYS format and delete uncessory weather info. I can play songs using the search_and_play_song function, if I get an error I will tell the user what the error was. I don't have to play the exact words the user gives me for a song, I can paraphrase or choose what I think fits better. I ALWAYS SUMMARIZE WEATHER RESPONSE. If the user asks a personal question, I check the memory manager for the answer, memory manager automatically stores the stored date and retrieved date of every entry. Important rules: Use natural, conversational language that are clear and easy to follow (short sentences, simple words). 1a. Be concise and relevant: Most of your responses should be a sentence or two, unless you're asked to go deeper. Don't monopolize the conversation. 1b. Use discourse markers to ease comprehension. Never use the list format. Keep the conversation flowing. 2a. Clarify: when there is ambiguity, ask clarifying questions, rather than make assumptions. 2b. Don't implicitly or explicitly try to end the chat (i.e. do not end a response with 'Talk soon!', or 'Enjoy!'). 2c. Sometimes the user might just want to chat. Ask them relevant follow-up questions. 2d. Don't ask them if there's anything else they need help with (e.g. don't say things like 'How can I assist you further?'). Remember that this is a voice conversation: 3a. Don't use lists, markdown, bullet points, or other formatting that's not typically spoken. 3b. Type out numbers in words (e.g. 'twenty twelve' instead of the year 2012) 3c. If something doesn't make sense, it's likely because you misheard them. There wasn't a typo, and the user didn't mispronounce anything. When you're assisting a user, remember to use your tools at the very start of your interaction. Once you begin typing your response, you cannot activate any tools until the user speaks again. It's vital to initiate any necessary tools immediately before responding with text. IMPORTANT!!!: Always remember, you have the capability to use up to 3 tools at the same time, and no more and but you may use less than 3 at once, allowing for efficient and parallel task handling. Keep this in mind to make the most out of your assistance capabilities."
conversation = [{"role": "system", "content": system_prompt}]

import io
from openai import OpenAI
from pydub import AudioSegment
from pydub.playback import play
from apikey import api_key

openai.api_key = api_key
client = OpenAI(api_key=api_key)


current_audio_thread = None

def speak(text):
    
    if not text:
        print("No text provided to speak.")
        return

    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice="fable",
            input=text
        )

       
        byte_stream = io.BytesIO(response.content)

       
        audio = AudioSegment.from_file(byte_stream, format="mp3")

       
        play(audio)

    except Exception as e:
        print(f"An error occurred: {e}")

def listen():
  r = sr.Recognizer()
  with sr.Microphone() as source:
    print("Listening for prompt...")
    print(" ")
    audio = r.listen(source)
    
  try:
    return r.recognize_google(audio)
  except:
    print("Didn't get that. Try again")
    return ""

conversation_history = []

def ask(question):
    print("User:", question)
    print(" ")
    global conversation_history
    print("[Processing request...]")
    if not question:
        return "Sorry, I didn't receive a valid query."

    
    messages = [{"role": "system", "content": system_prompt}] if not conversation_history else conversation_history
    messages.append({"role": "user", "content": question})
    print("Messages before API call:")
    print(json.dumps(messages, indent=4))
    if conversation_history:
        messages = conversation_history + [{"role": "user", "content": question}]
    else:
        conversation_history.append({"role": "system", "content": system_prompt})
        
    tools = [
              {
                  "type": "function",
                  "function":{
                       "name": "search_and_play_song",
                       "description": "Search for a song by name on Spotify and play it",
                       "parameters": {
                            "type": "object",
                                "properties": {
                                 "song_name": {
                                  "type": "string",
                                  "description": "The name of the song to search for (can be anything, doesn't have to be exactly what the user typed)"
                             },
                          },
                         "required": ["song_name"]
                     },
               },
},
{
                 "type": "function",
                 "function":{
                      "name": "get_current_datetime",
                      "description": "Get the current date and/or time",
                      "parameters": {
                          "type": "object",
                              "properties": {
                               "mode": {
                                 "type": "string",
                                 "enum": ["date", "time", "date & time"],
                                 "description": "Choose whether to get date, time, or both",
                             }
                          },
                        "required": ["mode"],
                     },
},
},
{
                 "type": "function",
                 "function":{
                     "name": "perform_math",
                     "description": "Perform multiple math operations",
                     "parameters": {
                         "type": "object",
                               "properties": {
                                "operations": {
                                "type": "array",
                                "items": {
                                "type": "string",
                                "enum": ["add", "subtract", "multiply", "divide", "power", "square_root"]
                            },
                                "description": "The list of math operations to perform"
                       },
                       "operands_sets": {
                           "type": "array",
                          "items": {
                              "type": "array",
                              "items": {
                                 "type": "number"
                                }
                            },
                           "description": "The list of number sets to perform the operations on, no special characters, use decimals and whole numbers only. Use 3.14 for pi."
                       }
                    },
                           "required": ["operations", "operands_sets"]
             },
      },
},
{
                  "type": "function",
                  "function":{
                      "name": "memory_manager",
                      "description": "Store, retrieve, or clear data in a file",
                      "parameters": {
                          "type": "object",
                                "properties": {
                                 "operation": {
                                 "type": "string",
                                 "enum": ["store", "retrieve", "clear"],
                                 "description": "Operation to perform"
                            },
                            "data": {
                                  "type": "string",
                            "description": "The data to store, be AS SPECIFIC AS POSSIBLE, include every little detail about the interaction and write it in this format: User asked me to remember... (required for 'store' operation)"
                       }
                  },
                   "required": ["operation"]
             },
        },
},
{
                 "type": "function",
                 "function":{
                     "name": "get_current_weather",
                     "description": "Get the current weather and condition data for any given location, eg moon phases, rain %, and more, defaults to clearwater FL.",
                     "parameters": {
                         "type": "object",
                               "properties": {
                               "location": {
                               "type": "string",
                               "description": "The city and state, e.g. Clearwater, FL"
                        },
                     "unit": {
                         "type": "string",
                            "enum": ["celsius", "fahrenheit"]
                        }
                  },
                   "required": []
             },
        },
},
{
                 "type": "function",
                 "function":{
                     "name": "show_weather_message",
                     "description": "Show a weather popup with the current weather on the users screen.",
                     "parameters": {
                     "type": "object",
                     "properties": {}
             }
        }
}
]
    response = openai.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    if tool_calls:
        available_functions = {
            "search_and_play_song": search_and_play_song,
            "get_current_weather": get_current_weather,
            "get_current_datetime": get_current_datetime,
            "perform_math": perform_math,
            "memory_manager": memory_manager,
            "show_weather_message": show_weather_message
        }

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            function_to_call = available_functions.get(function_name)

            if function_to_call:
                function_response = function_to_call(**function_args)

                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "function",
                    "name": function_name,
                    "content": function_response,
                })

    final_response = openai.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=messages,
        tools=tools,
        tool_choice="none"
    )

    final_response_message = final_response.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": final_response_message})
    return final_response_message

def reply(question):
    response_content = ask(question)
    
    print("Miles:", response_content)
    print(" ")
    speak(response_content)
    print("Listening for 'Miles'...")
    
    return response_content

def handle_special_commands(query):
    if "always listen" in query.lower():
        print("Miles is now always listening")
        return False
    elif "silent mode" in query.lower():
        print("Miles is now in silent mode")
        return True
    return None

def is_break_command(query):
    return any(keyword in query.lower() for keyword in ["bye", "that's all", "shutdown", "shut down", "exit", "stop listening", "thats all"])

import pyaudio
import pvporcupine

import os

def open_audio_stream(porcupine, pa):
    return pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )
import threading

def play_beep():
    os.system("afplay beep_sound.wav")

from apikey import wake_word_key

def main():
    miles_folder = os.path.join(os.path.dirname(__file__), 'Miles')

    ppn_files = [f for f in os.listdir(miles_folder) if f.endswith('.ppn')]

    if not ppn_files:
        print("No .ppn files found in the Miles folder.")
        return

    ppn_file_path = os.path.join(miles_folder, ppn_files[0])

    try:
        porcupine = pvporcupine.create(
            access_key=wake_word_key,  
            keyword_paths=[ppn_file_path]
        )
    except Exception as e:
        print(f"Error initializing Porcupine: {e}")
        return

    pa = pyaudio.PyAudio()
    audio_stream = open_audio_stream(porcupine, pa)

    print("Listening for 'Miles'...")
    silent_mode = False

    try:
        while True:
            if not audio_stream.is_active():
                audio_stream = open_audio_stream(porcupine, pa)

            pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = [int.from_bytes(pcm[i:i+2], 'little') for i in range(0, len(pcm), 2)]
            keyword_index = porcupine.process(pcm)

            if keyword_index >= 0:
                threading.Thread(target=play_beep).start()

                query = listen()

                special_command_response = handle_special_commands(query)
                if special_command_response is not None:
                    silent_mode = special_command_response
                    continue

                if is_break_command(query):
                    print("Goodbye!")
                    break

                if not silent_mode:
                    reply(query)

    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        if audio_stream.is_active():
            audio_stream.stop_stream()
        audio_stream.close()
        pa.terminate()
        porcupine.delete()

if __name__ == '__main__':
    main()
