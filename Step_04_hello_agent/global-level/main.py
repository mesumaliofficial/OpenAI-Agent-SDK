import os
from agents import Agent, AsyncOpenAI, Runner, set_default_openai_client, set_tracing_disabled, set_default_openai_api
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
gemini_api_key = os.getenv("GEMINI_API_KEY")

set_tracing_disabled(True)
set_default_openai_api("chat_completions")

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

set_default_openai_client(client)

agent: Agent = Agent(
    name="Elon",
    instructions="ap usi language m usi tarha jawab denge jis tarha user bat karyga",
    model="gemini-2.0-flash"
)

result = Runner.run_sync(
    agent,
    "Kesy Hain ap"
)

print(result.final_output)