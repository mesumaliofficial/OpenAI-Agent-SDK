## 🔹 Tools
### 🔸Tools
Tools ek helper hota hay jo agent ko koi kam karny ki permission deta hay:
 data fetching.
- running code
- external APIs ko call karna jab need ho.
- aur Computer ka istemal bhi karna


### 🔸What is tool calling ?
Tool calling ka matlab hay jab AI kisi conversation ke waqt decide karta hay usy kis tool ka use karna chahiye.

**Flow:**
- **User:** user ny pucha karachi ka weather kesa hay.
- **AI:** AI ny decide keya mujhy yahan weather Tool ki zaroorat hay.
- **AI calls tool:** Fetch Weather
- **Tool return:** {"temp": 33, "condition": "Cloudy"}
- **AI Answer:** Karachi mausam cloudy hay aur temperature 33°C hay.

### 🔸Why do we need tool ?
- LLMs ky pass live data nh hota hay is leye zaroorat parte hay.
- LLMs khud sy action nh ly sakta jesy mail send karna code run karwana etc.
- Tools se accuracy aur safety barhti hai, taake hum data ko sahi tareqy se hasil kar saken.

### 🔸Hosted Tools:
OpenAI kuch built-in hosted tools provide karta hai, jo OpenAIResponsesModel ka use kar ke access kiye ja sakte hain. In tools ki madad se AI real actions le sakta hai, bina manually intervene kiye.
- `WebSearchTool` Is tool se agent internet par search kar sakta hai.

- `FileSearchTool` Ye tool OpenAI ke Vector Store se documents dhoondhne mein madad karta hai. Agar aap ne kuch data store kar rakha ho (PDFs, policies, patterns waghera), to AI unko retrieve kar sakta hai.

- ` ComputerTool` AI ko apke computer ka limited access deta hai — taake files ko access ya open kiya ja sake (controlled environment mein). 

- `CodeInterpreterTool` AI ko code run karne ki ability deta hai, lekin ek safe sandboxed environment mein.
Sandboxed environment ka matlab hai secure jagah jahan AI sirf limited access ke sath code chala sakta hai.

-  `HostedMCPTool` Is tool se AI kisi remote MCP server ke tools ko use kar sakta hai.

- `ImageGenerationTool` Is tool se AI images generate kar sakta hai based on text prompts.

- `LocalShellTool` Ye AI ko permission deta hai ke woh aapke computer ke command line (terminal) par shell commands run kare.

```bash
from agents import Agent, FileSearchTool, Runner, WebSearchTool

agent = Agent(
    name="Assistant",
    tools=[
        WebSearchTool(),
        FileSearchTool(
            max_num_results=3,
            vector_store_ids=["VECTOR_STORE_ID"],
        ),
    ],
)

async def main():
    result = await Runner.run(agent, "Which coffee shop should I go to, taking into account my preferences and the weather today in SF?")
    print(result.final_output)
```

### 🔸Function Tool:
Ap kisi bhi python function ko ek tool ki tarha use kar sakty hain Agent SDK usko khud automatically setup kardyga.

- Tool ka naam wohi hoga jo function ko dengy.
- Tool ka discription function ky docstring sy leye jata hay recommended hay lazmi dein.
- Function ky aruguments se input schmea LLM khud ready karta hay.
- har input ka discription docstring sy leya jata hay (agar disable na keya gaya ho).

**is process mein:** 
- inspect module: Ye Python ka built-in module hai jo function ke signature ka structure nikalta hai. (signature ka matlab function ka naam use arguments aur return type)
- griffe: ool ko yeh samajhne mein madad deta hai ke har field ka matlab kya hai
- pydantic: Ye ek library hai jo inputs ka data schema banata hai aur unki validation karta hai. for example: Agar koi user `amount="not_a_number"` bhej de, to `pydantic` kahega: ❌ “Yeh float number hona chahiye!”

```bash
import json

from typing_extensions import TypedDict, Any

from agents import Agent, FunctionTool, RunContextWrapper, function_tool


class Location(TypedDict):
    lat: float
    long: float

@function_tool  
async def fetch_weather(location: Location) -> str:
    
    """Fetch the weather for a given location.

    Args:
        location: The location to fetch the weather for.
    """
    # In real life, we'd fetch the weather from a weather API
    return "sunny"


@function_tool(name_override="fetch_data")  
def read_file(ctx: RunContextWrapper[Any], path: str, directory: str | None = None) -> str:
    """Read the contents of a file.

    Args:
        path: The path to the file to read.
        directory: The directory to read the file from.
    """
    # In real life, we'd read the file from the file system
    return "<file contents>"


agent = Agent(
    name="Assistant",
    tools=[fetch_weather, read_file],  
)

for tool in agent.tools:
    if isinstance(tool, FunctionTool):
        print(tool.name)
        print(tool.description)
        print(json.dumps(tool.params_json_schema, indent=2))
        print()
```
<details>
<summary>Expand to see output</summary>

fetch_weather  
Fetch the weather for a given location.

```json
{
  "$defs": {
    "Location": {
      "properties": {
        "lat": {
          "title": "Lat",
          "type": "number"
        },
        "long": {
          "title": "Long",
          "type": "number"
        }
      },
      "required": ["lat", "long"],
      "title": "Location",
      "type": "object"
    }
  },
  "properties": {
    "location": {
      "$ref": "#/$defs/Location",
      "description": "The location to fetch the weather for."
    }
  },
  "required": ["location"],
  "title": "fetch_weather_args",
  "type": "object"
}
fetch_data
{
  "properties": {
    "path": {
      "description": "The path to the file to read.",
      "title": "Path",
      "type": "string"
    },
    "directory": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "The directory to read the file from.",
      "title": "Directory"
    }
  },
  "required": ["path"],
  "title": "fetch_data_args",
  "type": "object"
}
```
</details>
