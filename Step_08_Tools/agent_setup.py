import os
from openai import AsyncOpenAI
from dotenv import load_dotenv, find_dotenv
from agents import Agent, OpenAIChatCompletionsModel, RunConfig
from tools import get_weather

load_dotenv(find_dotenv())
gemini_api_key = os.getenv("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client,
)
agent = Agent(
    name="weatherAsistant",
    instructions="you are a weather agent that provides current weather information for a given location.",
    tools=[get_weather],
    model=model,
)

config = RunConfig(tracing_disabled=True)

