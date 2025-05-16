# Import required libraries and modules
from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values
from os import environ

from yarl import Query

# Load environment variables from .env file
env_vars = dotenv_values(".env")

#Retrieve specific environment variables for username, assistant name, and API key. 
Username = env_vars.get("Username") 
Assistantname  = env_vars.get("Assistantname") 
GroqAPIKey = env_vars.get("GroqAPIKey")

# Initialize the Groq API client
client = Groq(api_key=GroqAPIKey)
#Initialize an empty list to store chat messages
messages =[]

# Define system message and system chat history
System = (
    f"Hello, I am {Username}, you are a very accurate and advanced AI chatbot named {Assistantname} "
    f"which also has real-time up-to-date information from the internet.\n"
    "*** Do not tell time unless I ask, do not talk too much, just answer the question. ***\n"
    "*** Provide answers in a professional way. Make sure to use proper grammar with full stops, commas, and question marks. ***\n"
    "*** Reply in the same language as the question: Hindi in Hindi, English in English. ***\n"
    "*** Do not mention your training data or provide notes in the output. Just answer the question. ***"
) #f"" allows embedding variables inside strings.

SystemChatBot = [
    {'role': 'system', 'content': System},
    {'role': 'user', 'content': 'Hi'},
    {'role': 'assistant', 'content': 'Hello, how can I help you?'}
]

# Load chat history from ChatLog.json 
try:
    with open(r'Data\ChatLog.json', 'r') as f:
        messages = load(f) #Load existing messages from the chat log
except FileNotFoundError:
    #If the file doesn't exist , create an empty JSON file to store chat logs
    with open(r'Data\ChatLog.json', 'w') as f:
        dump([], f)
        #r'...' tells Python: “Don’t interpret backslashes as escape characters.”
        #Data\Chatlog not Chatlog because than ChatLog.json shoul be in same folder as our Python Script
def RealtimeInformation():
    """
    Provides real-time information including the current day, date, and time.
    """
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime('%A')
    date = current_date_time.strftime('%d')
    month = current_date_time.strftime('%B')
    year = current_date_time.strftime('%Y')
    hour = current_date_time.strftime('%H')
    minute = current_date_time.strftime('%M')
    second = current_date_time.strftime('%S')

    data = (
        f"Please use this real-time information if needed:\n"
        f"Day: {day}\n"
        f"Date: {date}\n"
        f"Month: {month}\n"
        f"Year: {year}\n"
        f"Time: {hour} hours :{minute} minutes :{second} seconds.\n"
    )
    return data

def AnswerModifier(answer):
    """
    Modifies the answer by removing any empty lines.
    """
    lines = answer.split('\n')
    non_empty_lines = [line.strip() for line in lines if line.strip()]
    modified_answer='\n'.join(non_empty_lines) #Join cleaned lines back together
    return modified_answer
def ChatBotAI(Query):
    """
    Handles the chatbot's logic, sending the prompt to the Groq API and updating the chat history.
    """
    try:
        # Load existing chat log
        with open(r'Data\ChatLog.json', 'r') as f: #opening the file to read its contents.
            messages = load(f)
            #Append the user's query to the message List.
        messages.append({"role":"user","content": f"{Query}"})

        # Send request to the Groq API with real-time information
        completion = client.chat.completions.create(
            model='llama3-70b-8192', #Ai model
            messages=SystemChatBot + [{'role': 'system', 'content': RealtimeInformation()}] + messages,
            max_tokens=1024,
            temperature=0.7,
            top_p=1, #Use nucleus sampling to control diversity
            stream=True, #Enable Streaming response
            stop=None #Allow model to determine when to stop
        )
           
        

        # Collect the response
        answer = ''
        for chunk in completion:
            if chunk.choices[0].delta.content: #Check if there is content in current chunk
                answer += chunk.choices[0].delta.content#appends  the chunk in the answer 
        answer = answer.replace("</s","")#cleans any unwanted tokens or substrings
        # Append the assistant's answer to the chat log
        messages.append({'role': 'assistant', 'content': answer})
        
        # Save updated chat history
        with open(r'Data\ChatLog.json', 'w') as f: #w so that we can write in file
            dump(messages, f, indent=4)

        # Return the modified answer
        return AnswerModifier(answer=answer)

    except Exception as e:
        # Log the error and reset the chat log if an error occurs
        print(f"Error: {e}")
        with open(r'Data\ChatLog.json', 'w') as f:
            dump([], f, indent=4)
        return ChatBotAI(Query)  # Retry after resetting the log

if __name__ == '__main__':
    while True:
        user_input = input('Enter Your Question: ')
        print(ChatBotAI(user_input))