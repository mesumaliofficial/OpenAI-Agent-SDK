import os
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled
from dotenv import find_dotenv, load_dotenv
import asyncio

load_dotenv(find_dotenv())
gemini_api_Key = os.getenv("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=gemini_api_Key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
set_tracing_disabled(disabled=True)

async def main():
    agent_1 = Agent(
        name = "Jarvis",
        instructions="You giving the best and correct information",
        model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)
    )

    result = await Runner.run(
        starting_agent=agent_1,
        input="What is the capital of Pakistan?",
    )
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
