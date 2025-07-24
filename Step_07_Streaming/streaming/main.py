import os
from dotenv import load_dotenv, find_dotenv
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner, RunConfig
from openai.types.responses import ResponseTextDeltaEvent
import asyncio

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

async def main():
    agent = Agent(
        name="Alexa",
        instructions="Aap sirf aur sirf roman urdu mein jawab doge chahy user english m puchy ya English mein."
    )

    result = Runner.run_streamed(
    starting_agent=agent,
    input='Who is the president of israel',
    run_config=config
    )

    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)

asyncio.run(main())

