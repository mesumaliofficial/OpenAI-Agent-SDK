import chainlit as cl
from agent import get_conversion_response

@cl.on_message
async def handle_message(message: cl.Message):
    response_text = get_conversion_response(message.content)
    await cl.Message(content=response_text).send()
  