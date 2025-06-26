import chainlit as cl
from agents import Runner
from openai.types.responses import ResponseTextDeltaEvent
from agent_setup import agent
from agents import RunConfig

config = RunConfig(tracing_disabled=True)

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set('history', [])
    await cl.Message(
        content="👋 Hello! I am **Neura**, your smart assistant — created by **Mesum Ali**. Ask me anything — I'm here to help!"
    ).send()


@cl.on_message
async def on_message(message: cl.Message):
    history = cl.user_session.get('history')
    history.append({"role": "user", "content": message.content})

    msg = cl.Message(content="")

    conversation_text = "\n".join(f"{m['role'].capitalize()}: {m['content']}" for m in history)

    result = Runner.run_streamed(
        starting_agent=agent,
        input=conversation_text,
        run_config=config
    )

    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            await msg.stream_token(event.data.delta)

    history.append({"role": "Neura", "content": result.final_output})
