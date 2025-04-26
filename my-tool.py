from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import requests

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def get_weather(location: str):
    # Dummy function to simulate weather fetching
    print("Tool called get_weather")
    url = f"https://wttr.in/{location}?format=%C+%t"
    response = requests.get(url)
    print(url)
    print(response.status_code)
    if response.status_code == 200:
        return f"The weather in {location} is {response.text}."
    return "something went wrong."

def run_command(command):
    # execute comand 
    # return result
    print("Tool called run_command")
    result = os.system(command=command)
    return result

available_tools = {
    "get_weather": {
        "fn": get_weather,
        "description": "Takes a city name as an input and returns the current weather for the city."
    },
    "run_command": {
        "fn": run_command,
        "description": "Takes a command as an input and execures in the system and returns the output"
    }
}

system_prompt= f"""
You are an helpful AI assistant who is specialized in resolving user query.
You work on start, plan, action, observe mode.
For the given user query and available tools, plan the step by step execution, based on the planning,
select the relevant tool from the available tool. and based on the tool selection you perform an action to call the tool.
Wait for the observation and based on the observation from the tool call resolve the user query.

Rules:
- Follow the Output JSON format.
- Always perform one step at a time and wait for next input
- Carefully analyse the user query

Output JSON Format:
{{
"step": "string",
"content": "string",
"function": "The input parameter for the function",
"input": "The input parameter for the function"
}}

Available tools:
- get_weather: "Takes a city name as an input and returns the current weather for the city."
- run_command: "Takes a command as an input and execures in the system and returns the output."

Example:
User Query: What is the weather of new york?
Output: {{ "step": "plan", "content": "The user is interested in weather data of new york" }}
Output: {{ "step": "plan", "content": "From the available tools, I should call get_weather" }}
Output: {{ "step": "action", "function": "get_weather", "input": "new york" }}
Output: {{ "step": "observe", "output": "12 Degree Cel" }}
Output: {{ "step":"output", "content": "The weather for new york seems to be 12 degrees." }}

"""
messages=[
        {"role": "system", "content": system_prompt}
]
while True:
    user_query=input(">")
    messages.append({"role": "user", "content": user_query})

    while True:
        response = client.chat.completions.create(
            model="gemini-2.0-flash",
            response_format={"type": "json_object"},
            messages=messages
        )

        parsed_response = json.loads(response.choices[0].message.content)
        messages.append({"role": "assistant", "content": json.dumps(parsed_response)})

        if parsed_response.get("step") == "plan":
            print(f"🧠: {parsed_response.get("content")}")
            continue

        elif parsed_response.get("step") == "action":
            tool_name = parsed_response.get("function")
            tool_input = parsed_response.get("input")

            if available_tools.get(tool_name, False):
                output = available_tools[tool_name].get("fn")(tool_input)
                messages.append({"role": "assistant", "content": json.dumps({"step": "observe", "output": output})})
                continue

        if parsed_response.get("step") == "output":
            print(f"🤖: {parsed_response.get("content")}")
            break