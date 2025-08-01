import chainlit as cl
import os
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig

# Load environment variables
load_dotenv(find_dotenv())
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Provider setup
provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Model setup
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider,
)

# Agent setup
agent1 = Agent(name="Neura", instructions="You are a helpful assistant.", model=model)

config = RunConfig(
    tracing_disabled=True
)


# Handle chat session start
@cl.on_chat_start
async def handle_chat_start():
    cl.user_session.set('history', [])
    await cl.Message(
        content="👋 Hello! I am **Neuro**, developed by **Mesum Ali**.\n\nAsk me anything — I'm here to help!"
    ).send()


# Handle incoming user messages
@cl.on_message
async def handle_message(message: cl.Message):
    history = cl.user_session.get('history')
    history.append({"role": "user", "content": message.content})

    conversation_text = "\n".join(f"{m['role'].capitalize()}: {m['content']}" for m in history)


    result = Runner.run_sync(
        input=conversation_text,
        run_config=config,
        starting_agent=agent1
    )

    history.append({"role": "assistant", "content": result.final_output})
    cl.user_session.set("history", history)

    await cl.Message(content=result.final_output).send()
