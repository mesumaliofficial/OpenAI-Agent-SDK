import asyncio
from config import model
from agents import Agent, Runner, RunContextWrapper, function_tool
from dataclasses import dataclass

@dataclass
class UserInfo:
    name: str
    age: int

@function_tool
async def fetch_user_data(wrapper: RunContextWrapper[UserInfo]) -> str:
    return f"The user name is {wrapper.context.name} and age is {wrapper.context.age}"

async def main():
    user_info = UserInfo(name="Mesum", age=18 )

    agent: Agent = Agent(
        name="Irona",
        instructions="You are a Helpful Asistant",
        model=model,
        tools=[fetch_user_data]
    )

    res = await Runner.run(
        starting_agent=agent,
        input="what is my name",
        context=user_info
    )
    print(res.final_output)

asyncio.run(main())