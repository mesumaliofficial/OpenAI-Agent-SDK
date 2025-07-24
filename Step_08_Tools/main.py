import chainlit as cl
from agent_setup import agent, config
from agents import Runner

@cl.on_message
async def main(message: cl.Message):

    result = await Runner.run(
    starting_agent=agent,
    input=message.content,
    run_config=config,
    )

    await cl.Message(
        content=f"Weather: {result.final_output}"
    ).send()
