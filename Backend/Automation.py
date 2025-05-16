# Import required libraries
from AppOpener import close,open as appopen # Import functions to open and close apps
from webbrowser import open as webopen # Import web browser functionality
from pywhatkit import search, playonyt # Import functions for Google search and YouTube playback.
from dotenv import dotenv_values # Import dotenv to manage environment variables.
from bs4 import BeautifulSoup # Import BeautifulSoup for parsing HTML content.
from rich import print # Import rich for styled console output.
from groq import Groq # Import Groq for AI chat functionalities.
from googlesearch import search as gsearch # Import Googlesearch for AI chat functionalities.
import webbrowser # Import webbrowser for opening URLs.
import subprocess # Import subprocess for interacting with the system.
import requests # Import requests for making HTTP requests.
import keyboard # Import keyboard for keyboard-related actions.
import asyncio # Import asyncio for asynchronous programming.
import os # Import os for operating system functionalities.
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Load environment variables from the .env file
env_vars = dotenv_values('.env')
GroqAPIKey = env_vars.get('GroqAPIKey') # Retrieve the Groq API key.

# Define CSS classes for parsing specific elements in HTML content.
classes = {
"zCubwf", "hgKElc", "LTKOO sY7ric", "Z0LcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee", 
"tw-Data-text tw-text-small tw-ta", 
"IZ6rdc", "O5uR6d LTKOO", "vlzY6d", "webanswers-webanswers_table_webanswers-table", 
"dDoNo ikb4Bb gsrt", "sXLaOe", 
"LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"
}

# Define a user-agent for making web requests.
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.76 Safari/537.36'

# Initialize the Groq client with the API key.
client = Groq(api_key=GroqAPIKey)
# Predefined professional responses for user interactions.
professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need—don't hesitate to ask."
]

# List to store chatbot messages.
messages = []

# Initial message to welcome the user.
System = {"role": "system", "content": f"Hello, I am {os.environ['Username']}, You're a content writer. You have to write content like letters, codes, applications, essays"}


# Function to perform a Google search.
def GoogleSearch(Topic):
    # Eventually, this function will perform a Google search and retrieve results.
    return f"Search results for: {Topic}" # Placeholder for search results.
def Content(Topic):
# Function to open a text editor.
 def OpenNotepad(file="notepad.exe"):
    default_text_editor = "notepad.exe" # Default text editor.
    subprocess.Popen([default_text_editor, file]) # Open the file in the text editor.

# Function to get content using the Groq AI chatbot.
 def ContentWritterAI(prompt):
    messages.append({"role": "user", "content": f"{prompt}"})

    stream = client.chat.completions.create(
        model="llama3-8b-8192",  # Use supported model
        messages=messages,
        max_tokens=2048,
        temperature=0.7,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        stream=True  # Enable streaming
    )

    Answer = ""
    for chunk in stream:
        #It ensures your app won't crash if the model sends a partial or empty chunk during streaming.
        if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:#We  explicitly check that delta.content is not None before trying to append it.
            Answer += chunk.choices[0].delta.content  # Only concatenate if content exists

    Answer = Answer.replace("</s", "")  # Clean up token artifacts
    messages.append({"role": "assistant", "content": Answer})
    return Answer


 Topic: str = Topic.replace("Content", "") # Remove "Content" from the topic.
 ContentByAI = ContentWritterAI(Topic) # Generate content using AI.

    # Save the generated content to a text file.
 with open(rf"Data\{Topic.lower().replace(' ', '')}.txt", "w", encoding="utf-8") as file:
        file.write(ContentByAI) # Write the content to the file.
        file.close()

 OpenNotepad(rf"Data\{Topic.lower().replace(' ', '')}.txt") # Open the file in Notepad.
 return True # Indicate success.

# Function to search for a topic on YouTube.
def YouTubeSearch(Topic):
    yt_search = f"https://www.youtube.com/results?search_query={Topic}" # Construct the YouTube search URL.
    webbrowser.open_new_tab(yt_search) # Open the search results in a new tab.
    return True

# Function to play a video on YouTube.
def PlayYoutube(query):
    playonyt(query) # Use pywhatkit's playonyt function to play the video.
    return True

useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"

def OpenApp(app, sess=requests.session()):
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)  # Replace with your own appopen logic
        return True
    except Exception as e:
        print(f"App '{app}' not found locally: {e}")

        def extract_links(html):
                if not html or not isinstance(html, str) or html.strip() == "":
                        print("Invalid or empty HTML content.")
                        return []

                soup = BeautifulSoup(html, 'html.parser')
                links = []
                for a in soup.select('div.yuRUbf > a'):
                        href = a['href']
                        if href.startswith('http'):
                                links.append(href)
                return links

        def search_with_selenium(app):
            from selenium.webdriver.chrome.options import Options

            chrome_options = Options()
            chrome_options.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])
            chrome_options.add_argument("start-maximized")
            chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")

            driver = webdriver.Chrome(options=chrome_options)

            # Perform a Google search for the app download page
            driver.get(f"https://www.{app.lower()}.com")
            try:
                WebDriverWait(driver, 100).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.yuRUbf > a'))
                )
                html = driver.page_source
                print("HTML Content:", html[:500])  # Debug output
                driver.quit()
                return html
            except TimeoutException:
                print("Timed out waiting for search results.")
                driver.quit()
                return None


        html = search_with_selenium(app)
        if not html:
            print("No HTML returned from search.")
            return False

        results = extract_links(html)
        if results:
            print(f"Opening website: {results[0]}")
            webbrowser.open(results[0])  # Opens in the default browser
            return True
        else:
            print(f"No download page found for '{app}'.")
            return False

def CloseApp(app):
    if "chrome" in app:
      pass #Skip if app is Chrome bcz our text to speech is using Chrome
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True) # Try to close the app.
            return True
        except Exception as e:
            return False
#Function to execute system level commands.
def System(command):
    # Nested function to mute the system volume.
    def mute():
        keyboard.press_and_release("volume mute")  # Simulate the mute key press.

    # Nested function to unmute the system volume.
    def unmute():
        keyboard.press_and_release("volume mute")  # Simulate the unmute key press.

    # Nested function to increase the system volume.
    def volume_up():
        keyboard.press_and_release("volume up")  # Simulate the volume up key press.

    # Nested function to decrease the system volume.
    def volume_down():
        keyboard.press_and_release("volume down")  # Simulate the volume down key press.

    # Execute the appropriate command.
    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down()
    
    return True  # Indicate success.

# Asynchronous function to translate and execute user commands.
async def TranslateAndExecute(commands: list[str]):
    funcs = []  # List to store asynchronous tasks.
    
    for command in commands:
        if command.startswith("open "):  # Handle "open" commands.
            if "open it" in command:
                pass  # Ignore "open it" commands.
            if "open file" == command:
                pass  # Ignore "open file" commands.
            else:
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open ")) # Schedule app opening.
                funcs.append(fun)
        elif command.startswith("general "):  # Placeholder for general commands.
            pass

        elif command.startswith("realtime "):  # Placeholder for real-time commands.
            pass

        elif command.startswith("close "):  # Handle "close" commands.
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close "))
            funcs.append(fun)  # Schedule app closing.

        elif command.startswith("play "):  # Handle "play" commands.
            fun = asyncio.to_thread(PlayYoutube, command.removeprefix("play "))
            funcs.append(fun)  # Schedule YouTube playback.

        elif command.startswith("content "):  # Handle "content" commands.
            fun = asyncio.to_thread(Content, command.removeprefix("content "))
            funcs.append(fun)  # Schedule content creation.

        elif command.startswith("google search "):  # Handle Google search commands.
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search "))
            funcs.append(fun)  # Schedule Google search.

        elif command.startswith("youtube search "):  # Handle YouTube search commands.
            fun = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search "))
            funcs.append(fun)  # Schedule YouTube search.

        elif command.startswith("system "):  # Handle system commands.
            fun = asyncio.to_thread(System, command.removeprefix("system "))
            funcs.append(fun)  # Schedule system command.

        else:
            print(f"No Function Found for {command}")  # Print an error for unrecognized commands.

    results = await asyncio.gather(*funcs)  # Execute all tasks concurrently.

    for result in results:  # Process the results.
        if isinstance(result, str):
            yield result
        else:
            yield result

# Asynchronous function to automate command execution.
async def Automation(commands: list[str]):
    async for result in TranslateAndExecute(commands):  # Translate and execute commands.
        pass
    return True  # Indicate success.
if __name__ == "__main__":
    user_input = input("Enter commands separated by comma buddy:")
    commands = [cmd.strip() for cmd in user_input.split(',')]#cmd not any keyword just a variable .strip removes extr whitespaces
    asyncio.run(Automation(commands))
