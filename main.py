from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import time
import requests
import os


load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

@tool
def calculator(a: float, b: float) -> str:
    """
    Useful for performing basic arithmetic calculations with numbers
    """
    print("Tool has been called")
    return f"The sum of {a} and {b} is {a + b}"

@tool
def check_weather(city: str) -> str:
    """
    Useful for checking the actual temperature in a specified city
    """

    print("He usado la api weather")

    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temp = round(data['main']['temp'] - 273, 2)
        return f"The temperature in {city} is: {temp} ºC."
    
    else:
        return f"I wasn't able to check the temperature in {city}."

def main():
    model = ChatOpenAI(temperature=0)

    tools = [calculator, check_weather]
    agent_executer = create_react_agent(model, tools)

    print("Welcome! I'm your AI assistant. Type 'quit' to exit.")
    print("You can ask me to perform calculations or chat with me.")

    while True:
        user_input = input("\nYou: ").strip()

        if user_input == "quit":
            break

        print("\nAssistant: ", end="")

        for chunk in agent_executer.stream(
            {"messages": [HumanMessage(content=user_input)]}
        ):
            if "agent" in chunk and "messages" in chunk["agent"]:
                for message in chunk["agent"]["messages"]:
                    print(message.content, end="")
        
        print()

if __name__ == "__main__":
    main()