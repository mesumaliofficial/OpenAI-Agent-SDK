import os
import asyncio
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
gemini_api_key = os.getenv("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key= gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)

config = RunConfig(model=model, model_provider=client, tracing_disabled=True)

agent_one = Agent(
    name = "Alexa",
    instructions="Aap sirf Roman Urdu mein jawab dein. Kisi bhi surat mein English sentences ya Urdu script use na karein."
)   

result = Runner.run_sync(agent_one, "what is open ai agent sdk", run_config=config)

print(result.final_output)