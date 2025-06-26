import os
from dotenv import load_dotenv
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel
from tools import get_weather, search_web

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider
)

agent = Agent(
    name="Jarvis",
    instructions=(
        "You are a Customer-Facing Agent. "
        "If the user asks about weather, extract the city name and call the get_weather tool with it."
    ),
    model=model,
    tools=[get_weather, search_web]
)
