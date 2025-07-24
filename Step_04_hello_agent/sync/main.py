import os
from dotenv import load_dotenv, find_dotenv
from agents import Agent, AsyncOpenAI, Runner, RunConfig, OpenAIChatCompletionsModel

load_dotenv(find_dotenv())

gemini_api_key = os.getenv("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)

config = RunConfig(
    model=model,
    model_provider=client,
    tracing_disabled=True
)

agent = Agent(
    name = "Alexa",
    instructions="You are a helpful agent",
    model=model
)

result = Runner.run_sync(starting_agent=agent, input="what is the situation of karach pakistan current now", run_config=config)

print(result.final_output)