# OpenAI-Agent-SDK

A flexible Python SDK for building AI-powered workflows using OpenAI's API, OpenRouter, and LiteLLM. Create smart agents that automate tasks, use tools, and manage conversation context with ease.

## Table of Contents
- [What is OpenAI-Agent-SDK?](#what-is-openai-agent-sdk)
- [Key Concepts](#key-concepts)
- [Project Structure](#project-structure)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## What is OpenAI-Agent-SDK?
The **OpenAI-Agent-SDK** is a Python library I developed to make it easy to create intelligent AI applications. It uses OpenAI's API, OpenRouter, and LiteLLM to build **agents**—AI programs that follow instructions, process user inputs, and perform tasks like answering questions or automating workflows. The SDK supports multi-agent systems, custom tools, and context management to keep track of conversations. Whether you're building a chatbot, automating tasks, or experimenting with AI, this SDK simplifies the process.

To see the full code and step-by-step implementation, visit the [repository](https://github.com/mesumaliofficial/OpenAI-Agent-SDK).

## Key Concepts
- **Agents**: Agents are like virtual assistants powered by AI models (e.g., GPT-4o). Each agent has specific instructions, like "answer questions about weather" or "book appointments." They can work alone or pass tasks to other agents.  
  *// Roman Urdu: Agent ek AI program hai jo instructions follow karta hai aur tasks perform karta hai, jaise kisi sawal ka jawab dena ya kaam automate karna.*
- **Tools**: Tools are Python functions you create that agents can call to do specific tasks, like fetching data or calculating results. The SDK connects these tools to the AI automatically.  
  *// Roman Urdu: Tools aapke banaye hue functions hain jo agent use karta hai, masalan data lena ya koi calculation karna.*
- **Context Management**: Context is the conversation history that agents remember to give coherent responses. For example, if you ask follow-up questions, the agent knows what you talked about before.  
  *// Roman Urdu: Context woh purani baat-cheet hai jo agent yaad rakhta hai taake jawab mein continuity ho.*
- **Workflows**: Workflows let multiple agents work together. For example, one agent might decide what task to do, then pass it to another agent for action.  
  *// Roman Urdu: Workflow mein kaee agents mil kar kaam karte hain, jaise ek agent decide karta hai aur doosra usko complete karta hai.*

Explore the repository for code examples of these concepts.

## Project Structure
The project is organized into steps, each building on the previous one to create a complete AI agent system:

- **Step_02_OpenRouter**: Integrates OpenRouter for unified access to multiple AI models.  
  *// Roman Urdu: OpenRouter se kaee AI models ko ek sath use karna.*
- **Step_03_LiteLLM**: Adds LiteLLM for provider-agnostic model access (supports OpenAI, Anthropic, etc.).  
  *// Roman Urdu: LiteLLM se different AI providers ke models use karna.*
- **Step_04_hello_agent**: Creates a basic AI agent.  
  *// Roman Urdu: Pehla simple agent banaya gaya.*
- **Step_05_Chainlit-Hello**: Sets up a Chainlit interface for interactive agent testing.  
  *// Roman Urdu: Chainlit se agent ke sath baat-cheet ka interface.*
- **Step_07_Streaming**: Implements streaming for real-time agent responses.  
  *// Roman Urdu: Real-time jawab ke liye streaming add ki.*
- **Step_08_Tools**: Adds support for custom tools that agents can use.  
  *// Roman Urdu: Agent ke liye custom tools banaye.*
- **Step_09_Agent_as_tool**: Allows agents to act as tools for other agents.  
  *// Roman Urdu: Ek agent doosre agent ke liye tool ban sakta hai.*
- **Step_10_Context**: Manages conversation history for consistent interactions.  
  *// Roman Urdu: Baat-cheet ka context save aur use karna.*

Check the `Projects/Local_Projects` folder in the repository for the code.

## Features
- **Multi-Agent Workflows**: Coordinate multiple agents for complex tasks.
- **Custom Tools**: Integrate Python functions as tools for agents.
- **Context Management**: Store and use conversation history for better responses.
- **Streaming Support**: Get real-time responses from agents.
- **Provider Flexibility**: Use OpenAI, OpenRouter, or other models via LiteLLM.
- **Interactive UI**: Test agents with a Chainlit-based interface.
- **Scalable Design**: Build simple to advanced workflows with ease.

## Installation
Clone the repository and install dependencies:

```bash
git clone https://github.com/mesumaliofficial/OpenAI-Agent-SDK.git
cd OpenAI-Agent-SDK
pip install -r requirements.txt
```

Set environment variables for API keys:
```bash
export OPENAI_API_KEY="your-openai-api-key"
export OPENROUTER_API_KEY="your-openrouter-api-key"
```

## Quick Start
Create a simple agent to answer questions:

```python
from agents import Agent, Runner

# Agent banayein
agent = Agent(
    name="ChatBot",
    instructions="Answer questions about general knowledge.",
    model="gpt-4o-mini"
)

# Agent chalayein
result = Runner.run_sync(agent, "What is the capital of France?")
print(result.final_output)  # Output: The capital of France is Paris.
```

See `Step_04_hello_agent` in the repository for the full code.

## Usage
### Creating an Agent with Tools
Define an agent with a custom tool:

```python
from agents import Agent, function_tool

@function_tool
def get_weather(city: str) -> str:
    """Returns weather info for a city."""
    return f"Weather in {city} is sunny"

agent = Agent(
    name="WeatherBot",
    instructions="Provide weather updates for cities.",
    tools=[get_weather]
)
```

### Running with Context
Use context to maintain conversation history:

```python
from agents import Runner

result = Runner.run_sync(agent, "What's the weather in Lahore?")
print(result.final_output)  # Output: Weather in Lahore is sunny
result = Runner.run_sync(agent, "And in Karachi?")  # Uses context
print(result.final_output)  # Output: Weather in Karachi is sunny
```

See `Step_10_Context` for context management code.

### Multi-Agent Workflow
Set up agents that collaborate:

```python
from agents import Agent, Runner

info_agent = Agent(name="InfoAgent", instructions="Answer general questions.")
weather_agent = Agent(name="WeatherAgent", instructions="Handle weather queries.", tools=[get_weather])
main_agent = Agent(
    name="MainAgent",
    instructions="Route queries to the right agent.",
    handoffs=[info_agent, weather_agent]
)

result = Runner.run_sync(main_agent, "What's the weather in Islamabad?")
print(result.final_output)  # Routes to WeatherAgent
```

Check `Step_09_Agent_as_tool` for agent handoff code.

## Examples
The `Projects/Local_Projects` folder contains examples:
- **Hello Agent**: A basic agent for simple queries (`Step_04_hello_agent`).
- **Chainlit Interface**: Interactive UI for testing agents (`Step_05_Chainlit-Hello`).
- **Streaming**: Real-time response handling (`Step_07_Streaming`).
- **Tools**: Custom tool integration (`Step_08_Tools`).
- **Context Management**: Conversation history handling (`Step_10_Context`).

Run an example:
```bash
python Projects/Local_Projects/Step_04_hello_agent/hello_agent.py
```

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a branch (`git checkout -b feature/your-feature`).
3. Commit changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License
Licensed under the MIT License. See [LICENSE](LICENSE) for details.