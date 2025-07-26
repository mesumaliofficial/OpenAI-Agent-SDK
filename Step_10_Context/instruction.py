import asyncio
from config import model
from agents import Agent, Runner, RunContextWrapper
from dataclasses import dataclass

@dataclass
class UserInfo:
    name: str
    age: int

class UserContextWrapper(RunContextWrapper):
    def __call__(self, context: UserInfo ):
        return f"The user name is {context.name} and age is {context.age}"


async def main():
    user_info = UserInfo(name="Mesum", age=18 )

    agent: Agent[UserInfo] = Agent(
        name="Irona",
        instructions=f"You are a Helpful Asistant and ",
        model=model,
        context_wrapper=UserContextWrapper(),
    )

    res = await Runner.run(
        starting_agent=agent,
        input="what is my name",
        context=user_info,
    )
    print(res.final_output)

asyncio.run(main())