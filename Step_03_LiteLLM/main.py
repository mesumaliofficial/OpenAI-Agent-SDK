import chainlit as cl
from agent_setup import handle_gemini
import json

@cl.on_chat_start
async def handle_chat_start():
  cl.user_session.set("chat_history", [])
  res = await cl.AskUserMessage(content="What is your name?", timeout=30).send()
  if res:
    await cl.Message(
        content=f"Hello! {res['output']} Nice to Meet You.").send()


@cl.on_message
async def handle_on_message(message: cl.Message):
   history = cl.user_session.get('chat_history', [])
   history.append({"role": "user", "content": message.content})
   
   conversation_text ="\n".join(f"{m['role'].capitalize()}: {m['content']}" for m in history)
   
   result = handle_gemini(conversation_text)
   await cl.Message(content=result).send()
   history.append({'role':'Alexa', "content": result})

   cl.user_session.set("chat_history", history)

@cl.on_chat_end
async def handle_chat_end():
  history = cl.user_session.get('chat_history', [])
  with open("chat_history.json", "w") as f:
    json.dump(history, f, indent=2)