import os
from dotenv import load_dotenv, find_dotenv
from agents import Agent, AsyncOpenAI, Runner, RunConfig, OpenAIChatCompletionsModel
import asyncio

load_dotenv(find_dotenv())

gemini_api_key = os.getenv("GEMINI_API_KEY")

client = AsyncOpenAI(api_key=gemini_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)

config = RunConfig(
    model=model,
    model_provider=client,
    tracing_disabled=True
)

async def main():
    agent = Agent(
        name="Jarvis",
        instructions="You are helpful Assistent.",
        model=model
    )

    result = await Runner.run(agent, "Tell me about recursion in programming", run_config=config)

    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())