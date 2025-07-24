from agents import Agent, Runner, RunConfig, OpenAIChatCompletionsModel, AsyncOpenAI
import os 
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
gemini_api_key = os.getenv("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
config = RunConfig(tracing_disabled=True)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)

shopping_agent = Agent(
    name="Shopping Assistant",
    instructions="You assist users in finding products and making purchase decisions. ",
    model=model,
)

support_agent = Agent(
    name="Support Agent",
    instructions="You route user queries to the appropriate department.",
    model=model,
)

triage_agent = Agent(
    name="Jarvis",
    instructions="You are a Customer-Facing Agent. ",
    model=model,
)

result = Runner.run_sync(
    starting_agent=triage_agent,
    input="I need help with a recent purchase.",
    run_config=config
)

print(result.final_output)
