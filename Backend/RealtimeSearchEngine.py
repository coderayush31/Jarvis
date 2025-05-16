from groq import Groq
import json
import datetime
from dotenv import dotenv_values
from googlesearch import search

# Load environment variables from the .env file.
env_vars = dotenv_values(".env")

# Retrieve specific environment variables for username, assistant name, and API key.
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Initialize the Groq client using the provided API key.
client = Groq(api_key=GroqAPIKey)

# Initialize an empty list to store chat messages.
messages = []

# Define a system message that provides context to the AI chatbot about its role and behavior.
System = f"""Hello, I am {Username}, you are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time u
Do not tell time until I ask, do not talk too much, just answer the question.
Reply in only English, even if the question is in Hindi, reply in English.
Do not provide notes in the output, just answer the question and never mention your training data.
* * * Provide Answers In a Professional Way , make sure to add full stops , commas , question marks , and use proper grammar . * * *
* * * Just answer the question from the provided data in a professional way . * * * * * " * "
"""
# Function to perform a Google search and format the results.
def GoogleSearch(query):
    results = list(search(query, advanced=True, num_results=5))
    Answer = f"The search results for '{query}' are:\n[start]\n"
    for i in results:
        Answer += f"Title : {i.title}\nDescription : {i.description}\n\n"
    Answer += "[end]"
    return Answer

# Function to clean up the answer by removing empty lines.
def AnswerModifier(Answer):
    Lines = Answer.split('\n')
    non_empty_Lines = [line for line in Lines if line.strip()]
    modified_answer = '\n'.join(non_empty_Lines)
    return modified_answer
# Predefined chatbot conversation system message and an initial user message.
SystemChatBot = [
    {"role": "system", "content": System},
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello, how can I help you?"}
]

# Function to get real-time information like the current date and time.
def Information():
    data = {}
    current_datetime = datetime.datetime.now()
    data["day_name"] = current_datetime.strftime("%A")
    data["day"] = current_datetime.strftime("%d")
    data["month_name"] = current_datetime.strftime("%B")
    data["year"] = current_datetime.strftime("%Y")
    data["hour"] = current_datetime.strftime("%I")
    data["minute"] = current_datetime.strftime("%M")
    data["second"] = current_datetime.strftime("%S")
    data["am_pm"] = current_datetime.strftime("%p")
    data["date"] = current_datetime.strftime("%x")
    data["time"] = current_datetime.strftime("%X")
    data["formatted"] = f"{data['hour']}:{data['minute']} {data['am_pm']}, {data['day_name']}, {data['month_name']} {data['day']}, {data['year']}"
    return data

# Function to handle real-time search and response generation.
def RealtimeSearchEngine(prompt):
    global SystemChatBot, messages
    # Load the chat log from the JSON file.
    try:
        with open(r"Data\ChatLog.json", "r") as f:
            messages = json.load(f)
    except FileNotFoundError:
        messages = []
    except json.JSONDecodeError:
        messages = []

    messages.append({"role": "user", "content": prompt})

    # Add Google search results to the system chatbot messages
    SystemChatBot.append({"role": "system", "content": GoogleSearch(prompt)})

    # Generate a response using the Groq client.
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=SystemChatBot + [{"role": "system", "content": f"The current time is {Information()['formatted']} in Chennai, Tamil Nadu, India. Use this information if needed."}] + messages,
        temperature=0.7,
        max_tokens=2048,
        top_p=1,
        stream=True,
        stop=None
    )

    Answer = ""

    # Concatenate response chunks from the streaming output.
    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content

    # Clean up the response.
    Answer = Answer.strip().replace("</s > ", " ")
    messages.append({"role": "assistant", "content": Answer})

    # Save the updated chat log back to the JSON file.
    with open(r"Data\ChatLog.json", "w") as f:
        json.dump(messages, f, indent=4)

    # Remove the most recent system message from the chatbot conversation.
    SystemChatBot.pop()
    return AnswerModifier(Answer)

if __name__ == "__main__":
    while True:
        prompt = input("Enter your query : ")
        print(RealtimeSearchEngine(prompt))