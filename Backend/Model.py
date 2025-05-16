import cohere
from rich import print
from dotenv import dotenv_values  # Import dotenv to load environment variables from a .env file. 
#Load environment variables from the .env file. 
env_vars =dotenv_values(".env") 
#Retrieve API key. 
CohereAPIKey =env_vars.get("CohereAPIKey") 
#Create a Cohere client using the provided API key. 
co=cohere.Client(api_key=CohereAPIKey) 
#Define a list of recognized function keywords for task categorization. 
funcs = [ 
"exit", "general", "realtime", "open", "close", "play", "generate image", "system", "content", "google search", "youtube search", "reminder" ]
#Initialize an empty list to store user messages. 
messages = [] 
# Define the preamble that guides the Al model on how to categorize queries. 
preamble = """
You are a very accurate Decision-Making-Model, which decides what kind of a query is given to you.
You will decide whether a query is a 'general' query, a 'realtime' query, or if it is asking to perform any task or automation (like 'open Facebook', 'play music', etc.).

*** Do not answer any query, just decide what kind of query is given to you. ***

-> Respond with 'general' if a query can be answered by an LLM model (conversational AI chatbot) and doesn't require up-to-date or real-time information.
-> Respond with 'realtime' if a query cannot be answered by an LLM model and needs real-time data (e.g., current weather, live scores).
-> Respond with 'open (application name or website name)' if a query asks to open any application or website.
-> Respond with 'close (application name)' if a query asks to close any application.
-> Respond with 'play (song name)' if a query asks to play any song.
-> Respond with 'generate image (image prompt)' if a query asks to generate an image.
-> Respond with 'system (task name)' if a query asks to perform system-level tasks (e.g., mute, shutdown).
-> Respond with 'content (topic)' if a query asks to write or create content (e.g., application, email, code, story).
-> Respond with 'google search (topic)' if a query asks to search for something on Google.
-> Respond with 'youtube search (topic)' if a query asks to search for something on YouTube.
-> Respond with 'click (text)' or 'double click (text)' if a query asks to click or double-click on any text or element on the screen.

*** If the query asks for multiple tasks, respond accordingly (combine responses). ***
*** Respond with 'general' if you can't determine the type of query. ***
"""

ChatHistory = [
{"role": "User", "message": "how are you?"},
{"role": "Chatbot", "message": "general how are you?"},
{"role": "User", "message": "do you like pizza?"},
{"role": "Chatbot", "message": "general do you like pizza?"},
{"role": "User", "message": "open chrome and tell me about mahatma gandhi."},
{"role": "Chatbot", "message": "open chrome, general tell me about mahatma gandhi."},
{"role": "User", "message": "open chrome and firefox"},
{"role": "Chatbot", "message": "open chrome, open firefox"},
{"role": "User", "message": "what is today's date and by the way remind me that i have a dancing performance on"},
{"role": "Chatbot", "message": "general what is today's date, reminder 11:00pm 5th aug dancing performance"},
{"role": "User", "message": "chat with me."},
{"role": "Chatbot", "message": "general chat with me."}
]
#Define main function for Decision making 
def FirstLayerDMM(prompt: str = "test"):
    # Add the user's query to the messages list.
    messages.append({"role": "user", "content": f"{prompt}"})

    # Create a streaming chat session with the Cohere model.
    stream = co.chat_stream(
        model='command-r-plus',  # Specify the Cohere model to use.
        message=prompt,  # Pass the user's query.
        temperature=0.7,  # Set the creativity level of the model.
        chat_history=ChatHistory,  # Provide the predefined chat history for context.
        prompt_truncation='OFF',  # Ensure the prompt is not truncated.
        connectors=[],  # No additional connectors are used.
        preamble=preamble  # Pass the detailed instruction preamble.
    )

    # Initialize an empty string to store the generated response.
    response = ""

    # Iterate over events in the stream and capture text generation events.
    for event in stream:
        if event.event_type == "text-generation":
            response += event.text  # Append generated text to the response.

    # Remove newline characters and split responses into individual
    response = response.replace("\n", "") 
    response = response.split(",") 
    #Strip leading and trailing whitespaces from each task. 
    response = [i.strip() for i in response] 
    # Initialize an empty list to filter valid tasks. 
    temp = [] 
    #Filter the tasks based on recognized function keywords. 
    for task in response: 
      for func in funcs: 
         if task.startswith(func): 
             temp.append(task) # Add valid tasks to the filtered list.

    #Update the response with the filtered list of tasks. 
    response =temp 
    #if (query) is in the response, recursively call the function for further clarification. 
    if "(query)" in response: 
     newresponse = FirstLayerDMM(prompt=prompt) 
     return newresponse #Return the clarified response.
 
    else: 
     return response #Return the filtered response. 
    
#Entry point for the script. 

if __name__ == '__main__':
    # Continuously take user input and classify the prompt
    while True:
     print(FirstLayerDMM(input(">>> "))) # Print the categorized response.
   
