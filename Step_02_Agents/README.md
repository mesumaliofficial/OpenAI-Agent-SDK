## 🔹 Agent
### 🔸Agent
- Agent ek Large Language Model (LLM) hota hai jo instructions aur tools ke sath configure kiya jata hai, Yeh app ka core hissa hota hai jo user input ke mutabiq sochta, decision leta, aur kaam karta hai.

### 🔸Basic Configuration
Agents ki kuch important properties hoti hain jo apko configure karni hoti hain.
- **name:** Ye Agent ki idntification hoti hay. **Required**.

- **instructions:** Ye agent ka persona ya system prompt hota hai jo batata hai ke agent kis tarah behave karega **Optional**.

- **model:** Yeh batata hay konsa LLM use karna hay **Required**.
- **model_settings:** Is mein aap kuch tuning parameters set kar sakte ho jaise: temperature, top_p **Optional**.

- **tools:** ye wo external functions, APIs ya utilities hoti hain jo agent apne task complete ky leye use karta hay **Optional**.

```bash
from agents import Agent, ModelSettings, function_tool

@function_tool
def get_weather(city: str) -> str:
     """returns weather info for the specified city."""
    return f"The weather in {city} is sunny"

agent = Agent(
    name="Neura",
    instructions="Always respond in haiku form",
    model="gemini-2.0-flash",
    tools=[get_weather],
)
```

### 🔸Context

- Agents apne context ky leye generic hoty hain, Context ek dependency-injection tool hay: yeh ek object hota hay jo hum create karty hain aur `Runner.run()` ko pass karty hain, har agent tool handoff wagera ko deya jata hay, aur yeh agentrun ky leye dependencies aur state ky leye ek grab bag ka kam karta hay. ap kisi bhi python object ko context ky tor per dy sakty hain.

- Jo context `Runner.run` mein pass keya jaye wo local context hota hay, aur ye kuch is tarha sy work karta hay keh jesy hum 1 greet agent bana rahy ho, jo greet kary aur uska naam use kary tw out put kuch is tarha ka hoga. "Hello Mesum! How can I help you today?"

```bash
@dataclass
class UserContext:
    name: str
    uid: str
    is_pro_user: bool

    async def fetch_purchases() -> list[Purchase]:
        return ...

agent = Agent[UserContext](
    ...,
)
```

### 🔸Output Types
- By default, agent plain text yani (str) output deta hai.
- Lekin agar aap chahen ke agent kisi specific type ka output de, to aap `output_type` parameter ka use karke output ki type define kar sakte hain.
- Ek common choice hoti hai ke `Pydantic object` ka use kiya jaye.
- Iske ilawa, agent kisi bhi type ka object support karta hai jo Pydantic TypeAdapter mein wrap ho sakta ho. jesy: dataclasses, lists, TypedDict, etc.

```bash 
from pydantic import BaseModel
from agents import Agent


class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

agent = Agent(
    name="Calendar extractor",
    instructions="Extract calendar events from text",
    output_type=CalendarEvent,
)
```
**Note:** Jab output type ka use karty hain, tw yeh model ko batata hay ke wo regular plain text ky bajaye [structured output](https://platform.openai.com/docs/guides/structured-outputs) ka use kare.


### 🔸Handoffs
- Handoffs aesy sub agents hoty hain jinhy main agent apna kam delegate karta sakta hay.
- Ap ek agents ki list provide karty ho aur agar agent decide karta hay delagate kary agar revelant ho,
- Yeh aik powerful pattern hai jo tumhein allow karta hai ke tum orchestrating modular, specialized agents bana sako, jis mein har ek agent ka specific task hota hay jis m wo expert ho.

```bash
from agents import Agent

booking_agent = Agent(...)
refund_agent = Agent(...)

triage_agent = Agent(
    name="Triage agent",
    instructions=(
        "Help the user with their questions."
        "If they ask about booking, handoff to the booking agent."
        "If they ask about refunds, handoff to the refund agent."
    ),
    handoffs=[booking_agent, refund_agent],
)
```

### 🔸Dynamic Instructions
- Aksar cases mein ap insturctuction agent create karty waqt hi dy sakty hain,
- Lekin agar ap chahen tw dynamic Instruction bhi dy sakty hain ek function ky zariye,
- Yeh function agent aur context ko receive karega, aur prompt return karyga.
- is mein dono function use keye jaa sakty hain `async` aur normal.

```bash
def dynamic_instructions(
    context: RunContextWrapper[UserContext], agent: Agent[UserContext]
) -> str:
    return f"The user's name is {context.context.name}. Help them with their questions."


agent = Agent[UserContext](
    name="Triage agent",
    instructions=dynamic_instructions,
)
```

### 🔸Lifecycle events (hooks)
- Kabhi kabhi ap chahty hain ke ap agent ki lifecycle ko observe karen for example ap events ko log karna chahtay hain, ya jab kuch khaas events hon to data pehlay se hi fetch kar lena chahtay hain, tw ap `hooks` property ka use karky hook kar sakty hain `AgentHooks` class ko subclass karen aur un method ko override karden jin mein ap intrested hain.

### 🔸Guardials
- Guardials ka matlab hota hay aesy checks ya validation chalana jo user ky input per lagty hain aur yeh agent ky sath parallel chalty hain, For example: Aap yeh dekh sakte ho ke user ka input relevant hai ya nahi, ya koi banned word to nahi use kiya gaya.


### 🔸Cloning/copying agents
- colne() method ky zariye ap kisi bhi agent ka clone kar sakty hain aur jo chahen usko override kar sakty hain

```bash
pirate_agent = Agent(
    name="Pirate",
    instructions="Write like a pirate",
    model="o3-mini",
)

robot_agent = pirate_agent.clone(
    name="Robot",
    instructions="Write like a robot",
)
```

### 🔸Forcing tool use
- Tool ki list dena hamehsa ye matlab nh hota keh agent tool ka istemal karyga, agar ap chahen tw zabardasti bhi tool ka istemal karwa sakty hain `ModelSettings.tool_choice` set karky.

- `auto` By default, ye option LLM ko decide karne deta hai ke tool use karna hai ya nahi.
- `required` Ye LLM ko force karta hai ke lazmi tool use kare lekin konsa tool use karna hai, ye wo khud decide karta hai.
- `none` Ye LLM ko force karta hai ke koi bhi tool use na kare.
- `my_tool` Koi specific tool ka naam dena, jo LLM ko force karega ke wahi tool lazmi use kare. 

```bash
from agents import Agent, Runner, function_tool, ModelSettings

@function_tool
def get_weather(city: str) -> str:
    """Returns weather info for the specified city."""
    return f"The weather in {city} is sunny"

agent = Agent(
    name="Weather Agent",
    instructions="Retrieve weather details.",
    tools=[get_weather],
    model_settings=ModelSettings(tool_choice="get_weather") 
)
```

### 🔸Tool Use Behavior
- `tool_use_behavior` jab agent koi tool use karta hay tw uska output LLM ko kesy deya jaye usko control karta hay.
- `run_llm_again` Ye default setting hay, jab Tools run hota hay aur phr LLM unka result process karky final response banata hay.
- `stop_on_first_tool` Sirf Tool run hota hay, aur usi ka output user ko deya jata hay LLM dubara nh chalta.

```bash
from agents import Agent, Runner, function_tool, ModelSettings

@function_tool
def get_weather(city: str) -> str:
    """Returns weather info for the specified city."""
    return f"The weather in {city} is sunny"

agent = Agent(
    name="Weather Agent",
    instructions="Retrieve weather details.",
    tools=[get_weather],
    tool_use_behavior="stop_on_first_tool"
)
```

`StopAtTools(stop_at_tool_names=[...])` Agar koi spcific tool call hota hay tw ye usi waqt rukh jata hay aur usi tool ka output final response ky tor per use karta hay.

```bash
from agents import Agent, Runner, function_tool
from agents.agent import StopAtTools

@function_tool
def get_weather(city: str) -> str:
    """Returns weather info for the specified city."""
    return f"The weather in {city} is sunny"

@function_tool
def sum_numbers(a: int, b: int) -> int:
    """Adds two numbers."""
    return a + b

agent = Agent(
    name="Stop At Stock Agent",
    instructions="Get weather or sum numbers.",
    tools=[get_weather, sum_numbers],
    tool_use_behavior=StopAtTools(stop_at_tool_names=["get_weather"])
)
```

`ToolsToFinalOutputFunction`Ek custom function hota hay jo tools ky results ko process karta hay aur yeh decide karta hay keh LLm ko continue karna hay ya nh.

```bash
from agents import Agent, Runner, function_tool, FunctionToolResult, RunContextWrapper
from agents.agent import ToolsToFinalOutputResult
from typing import List, Any

@function_tool
def get_weather(city: str) -> str:
    """Returns weather info for the specified city."""
    return f"The weather in {city} is sunny"

def custom_tool_handler(
    context: RunContextWrapper[Any],
    tool_results: List[FunctionToolResult]
) -> ToolsToFinalOutputResult:
    """Processes tool results to decide final output."""
    for result in tool_results:
        if result.output and "sunny" in result.output:
            return ToolsToFinalOutputResult(
                is_final_output=True,
                final_output=f"Final weather: {result.output}"
            )
    return ToolsToFinalOutputResult(
        is_final_output=False,
        final_output=None
    )

agent = Agent(
    name="Weather Agent",
    instructions="Retrieve weather details.",
    tools=[get_weather],
    tool_use_behavior=custom_tool_handler
)
```

**Note:** Infinite Loops sy bachny ky leye framework automatically `tool_choice` ko "auto" per reset kar deta hay har tool ky bad, Infinite loop is wajah sy  hota hay tool ka result LLM ko wapas deya jata hay aur phr LLM `tool_choice` ki wajah sy dubara tool call generate karta hay aur yeh chalta rehta hay (ad infinitum).