<div align="center">

# `AnancyIO`

## 🧬 Evolution Roadmap

**AnancyIO** represents the next evolution of AI agent frameworks, building upon the foundation of **Agent Zero** to create the first truly general-purpose agentic system.

### The Journey: From Agent Zero to 5D Octopus Engine

This project is not just a tool - it's the beginning of a transformative journey through successive stages of AI evolution:

1. **Agent Zero** (Foundation) - The original open-source agent framework
2. **AnancyIO** (Current) - Enhanced multi-agent orchestration with browser automation, web UI, and advanced tooling
3. **Thought Daw** - Cognitive enhancement phase with advanced reasoning and multi-modal understanding
4. **MW0 (Multi-World Zero)** - Ecosystem phase with interconnected agent networks and universal standards
5. **5D Octopus Engine** - The final synthesis: fifth-dimensional agent cognition with fully autonomous agent swarms

**"From Zero to Infinity - The Evolution of Agentic AI"**

---

# `AnancyIO`

## Documentation:

[Introduction](#a-personal-organic-agentic-framework-that-grows-and-learns-with-you) •
[Installation](./docs/installation.md) •
[Development](./docs/development.md) •
[Extensibility](./docs/extensibility.md) •
[Connectivity](./docs/connectivity.md) •
[How to update](./docs/installation.md#how-to-update-anancyio) •
[Documentation](./docs/README.md) •
[Usage](./docs/usage.md)

Or see DeepWiki generated documentation:

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/anancyioai/anancyio)

</div>


<div align="center">

> ### 🚨 **PROJECTS!** 🚨
AnancyIO now supports **Projects** – isolated workspaces with their own prompts, files, memory, and secrets, so you can create dedicated setups for each use case without mixing contexts.
</div>



## A personal, organic agentic framework that grows and learns with you



- AnancyIO is not a predefined agentic framework. It is designed to be dynamic, organically growing, and learning as you use it.
- AnancyIO is fully transparent, readable, comprehensible, customizable, and interactive.
- AnancyIO uses the computer as a tool to accomplish its (your) tasks.

# 💡 Key Features

1. **General-purpose Assistant**

- AnancyIO is not pre-programmed for specific tasks (but can be). It is meant to be a general-purpose personal assistant. Give it a task, and it will gather information, execute commands and code, cooperate with other agent instances, and do its best to accomplish it.
- It has a persistent memory, allowing it to memorize previous solutions, code, facts, instructions, etc., to solve tasks faster and more reliably in the future.

2. **Computer as a Tool**

- AnancyIO uses the operating system as a tool to accomplish its tasks. It has no single-purpose tools pre-programmed. Instead, it can write its own code and use the terminal to create and use its own tools as needed.
- The only default tools in its arsenal are online search, memory features, communication (with the user and other agents), and code/terminal execution. Everything else is created by the agent itself or can be extended by the user.
- Tool usage functionality has been developed from scratch to be the most compatible and reliable, even with very small models.
- **Default Tools:** AnancyIO includes tools like knowledge, code execution, and communication.
- **Creating Custom Tools:** Extend AnancyIO's functionality by creating your own custom tools.
- **Instruments:** Instruments are a new type of tool that allow you to create custom functions and procedures that can be called by AnancyIO.

3. **Multi-agent Cooperation**

- Every agent has a superior agent giving it tasks and instructions. Every agent then reports back to its superior.
- In the case of the first agent in the chain (Agent 0), the superior is the human user; the agent sees no difference.
- Every agent can create its subordinate agent to help break down and solve subtasks. This helps all agents keep their context clean and focused.

4. **Completely Customizable and Extensible**

- Almost nothing in this framework is hard-coded. Nothing is hidden. Everything can be extended or changed by the user.
- The whole behavior is defined by a system prompt in the **prompts/default/agent.system.md** file. Change this prompt and change the framework dramatically.
- The framework does not guide or limit the agent in any way. There are no hard-coded rails that agents have to follow.
- Every prompt, every small message template sent to the agent in its communication loop can be found in the **prompts/** folder and changed.
- Every default tool can be found in the **python/tools/** folder and changed or copied to create new predefined tools.

5. **Communication is Key**

- Give your agent a proper system prompt and instructions, and it can do miracles.
- Agents can communicate with their superiors and subordinates, asking questions, giving instructions, and providing guidance. Instruct your agents in the system prompt on how to communicate effectively.
- The terminal interface is real-time streamed and interactive. You can stop and intervene at any point. If you see your agent heading in the wrong direction, just stop and tell it right away.
- There is a lot of freedom in this framework. You can instruct your agents to regularly report back to superiors asking for permission to continue. You can instruct them to use point-scoring systems when deciding when to delegate subtasks. Superiors can double-check subordinates' results and dispute. The possibilities are endless.

## 🚀 Things you can build with AnancyIO

- **Development Projects** - `"Create a React dashboard with real-time data visualization"`

- **Data Analysis** - `"Analyze last quarter's NVIDIA sales data and create trend reports"`

- **Content Creation** - `"Write a technical blog post about microservices"`

- **System Admin** - `"Set up a monitoring system for our web servers"`

- **Research** - `"Gather and summarize five recent AI papers about CoT prompting"`



# ⚙️ Installation

You can run AnancyIO **without Docker** using Conda. See **[RUN_WITHOUT_DOCKER.md](RUN_WITHOUT_DOCKER.md)** and use `run-web.ps1` (Windows) or `run-web.sh` (macOS/Linux).

A detailed setup guide for Windows, macOS, and Linux can be found in the AnancyIO Documentation at [this page](./docs/installation.md).

### ⚡ Quick Start

**Run with Conda (no Docker):**
```bash
# Windows
.\run-web.ps1

# macOS / Linux
./run-web.sh
```
Requires Conda. Then open **http://localhost:5000**. See [RUN_WITHOUT_DOCKER.md](RUN_WITHOUT_DOCKER.md) for details.

**Or run with Docker:**
```bash
docker pull anancyioai/anancyio
docker run -p 50001:80 anancyioai/anancyio
# Visit http://localhost:50001 to start
```

## 🐳 Fully Dockerized, with Speech-to-Text and TTS

- Customizable settings allow users to tailor the agent's behavior and responses to their needs.
- The Web UI output is very clean, fluid, colorful, readable, and interactive; nothing is hidden.
- You can load or save chats directly within the Web UI.
- The same output you see in the terminal is automatically saved to an HTML file in **logs/** folder for every session.
- Agent output is streamed in real-time, allowing users to read along and intervene at any time.
- No coding is required; only prompting and communication skills are necessary.
- With a solid system prompt, the framework is reliable even with small models, including precise tool usage.

## 👀 Keep in Mind

1. **AnancyIO Can Be Dangerous!**

- With proper instruction, AnancyIO is capable of many things, even potentially dangerous actions concerning your computer, data, or accounts. Always run AnancyIO in an isolated environment (like Docker) and be careful what you wish for.

2. **AnancyIO Is Prompt-based.**

- The whole framework is guided by the **prompts/** folder. Agent guidelines, tool instructions, messages, utility AI functions, it's all there.


## 📚 Read the Documentation

| Page | Description |
|-------|-------------|
| [Installation](./docs/installation.md) | Installation, setup and configuration |
| [Usage](./docs/usage.md) | Basic and advanced usage |
| [Development](./docs/development.md) | Development and customization |
| [Extensibility](./docs/extensibility.md) | Extending AnancyIO |
| [Connectivity](./docs/connectivity.md) | External API endpoints, MCP server connections, A2A protocol |
| [Architecture](./docs/architecture.md) | System design and components |
| [Contributing](./docs/contribution.md) | How to contribute |
| [Troubleshooting](./docs/troubleshooting.md) | Common issues and their solutions |


## 🎯 Changelog

### v0.9.7 - Projects
- Projects management
    - Support for custom instructions
    - Integration with memory, knowledge, files
    - Project specific secrets 
- New Welcome screen/Dashboard
- New Wait tool
- Subordinate agent configuration override support
- Support for multiple documents at once in document_query_tool
- Improved context on interventions
- Openrouter embedding support
- Frontend components refactor and polishing
- SSH metadata output fix
- Support for windows powershell in local TTY utility
- More efficient selective streaming for LLMs
- UI output length limit improvements



### v0.9.6 - Memory Dashboard
- Memory Management Dashboard
- Kali update
- Python update + dual installation
- Browser Use update
- New login screen
- LiteLLM retry on temporary errors
- Github Copilot provider support


### v0.9.5 - Secrets

- Secrets management - agent can use credentials without seeing them
- Agent can copy paste messages and files without rewriting them
- LiteLLM global configuration field
- Custom HTTP headers field for browser agent
- Progressive web app support
- Extra model params support for JSON
- Short IDs for files and memories to prevent LLM errors
- Tunnel component frontend rework
- Fix for timezone change bug
- Notifications z-index fix

### v0.9.4 - Connectivity, UI

- External API endpoints
- Streamable HTTP MCP A_IO server
- A2A (Agent to Agent) protocol - server+client
- New notifications system
- New local terminal interface for stability
- Rate limiter integration to models
- Delayed memory recall
- Smarter autoscrolling in UI
- Action buttons in messages
- Multiple API keys support
- Download streaming
- Tunnel URL QR code
- Internal fixes and optimizations

### v0.9.3 - Subordinates, memory, providers Latest

- Faster startup/restart
- Subordinate agents can have dedicated prompts, tools and system extensions
- Streamable HTTP MCP server support
- Memory loading enhanced by AI filter
- Memory AI consolidation when saving memories
- Auto memory system configuration in settings
- LLM providers available are set by providers.yaml configuration file
- Venice.ai LLM provider supported
- Initial agent message for user + as example for LLM
- Docker build support for local images
- File browser fix


### v0.9.2 - Kokoro TTS, Attachments


- Kokoro text-to-speech integration
- New message attachments system
- Minor updates: log truncation, hyperlink targets, component examples, api cleanup


### v0.9.1 - LiteLLM, UI improvements

- Langchain replaced with LiteLLM
    - Support for reasoning models streaming
    - Support for more providers
    - Openrouter set as default instead of OpenAI
- UI improvements
    - New message grouping system
    - Communication smoother and more efficient
    - Collapsible messages by type
    - Code execution tool output improved
    - Tables and code blocks scrollable
    - More space efficient on mobile
- Streamable HTTP MCP servers support
- LLM API URL added to models config for Azure, local and custom providers
    

### v0.9.0 - Agent roles, backup/restore

- subordinate agents can use prompt profiles for different roles
- backup/restore functionality for easier upgrades
- security and bug fixes

### v0.8.7 - Formatting, Document RAG Latest

- markdown rendering in responses
- live response rendering
- document Q&A tool

### v0.8.6 - Merge and update

- Merge with Hacking Edition
- browser-use upgrade and integration re-work
- tunnel provider switch

### v0.8.5 - **MCP Server + Client**


- AnancyIO can now act as MCP Server
- AnancyIO can use external MCP servers as tools

### v0.8.4.1 - 2
Default models set to gpt-4.1
- Code execution tool improvements
- Browser agent improvements
- Memory improvements
- Various bugfixes related to context management
- Message formatting improvements
- Scheduler improvements
- New model provider
- Input tool fix
- Compatibility and stability improvements

### v0.8.4


- **Remote access (mobile)**

### v0.8.3.1


- **Automatic embedding**


### v0.8.3


- ***Planning and scheduling***

### v0.8.2


- **Multitasking in terminal**
- **Chat names**

### v0.8.1


- **Browser Agent**
- **UX Improvements**

### v0.8


- **Docker Runtime**
- **New Messages History and Summarization System**
- **Agent Behavior Change and Management**
- **Text-to-Speech (TTS) and Speech-to-Text (STT)**
- **Settings Page in Web UI**
- **SearXNG Integration Replacing Perplexity + DuckDuckGo**
- **File Browser Functionality**
- **KaTeX Math Visualization Support**
- **In-chat File Attachments**

### v0.7


- **Automatic Memory**
- **UI Improvements**
- **Instruments**
- **Extensions Framework**
- **Reflection Prompts**
- **Bug Fixes**

## 🤝 Community and Support

- [Join our Discord](https://discord.gg/B8KZKNsPpj) for live discussions or [visit our Skool Community](https://www.skool.com/anancyio).
- [Report Issues](https://github.com/HammazoneRecords/anancy-io-main/issues) for bug fixes and features
