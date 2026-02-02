![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

# 🐧 Linux-Agent (Linu-Agent)

An **offline Linux troubleshooting agent** built using **LangChain**, **LangGraph**, and **Ollama** with **open-source LLMs**.

This project helps users **understand, debug, and fix Linux issues** through a **multi-agent system** that preserves conversational context.

---

## 🧠 What is Linux-Agent?

Linux-Agent acts like a **Linux support team** working together:

- One agent improves and clarifies the user’s question
- One agent decides how the system should respond
- One agent specializes in Linux troubleshooting

All processing happens **locally and offline** using **Ollama**.

---

## ✨ Features

- Fully **offline** (open-source models via Ollama)
- **Multi-agent architecture** using LangGraph
- **Conversation memory** across turns
- Linux-focused troubleshooting
- Modular and extensible design

---

## 🧱 Architecture

The system follows a **manager–specialist flow**:

User
↓
Orchestration Agent
↓
Prompt Refining Agent
↓
Linux Agent


**Analogy:**  
- Orchestration Agent → Decides the next step  
- Prompt Refining Agent → Clarifies the problem  
- Linux Agent → Solves the Linux issue  

---

## 🤖 Agents

### Orchestration Agent
- Controls conversation flow
- Routes tasks between agents
- Maintains state and context

### Prompt Refining Agent
- Refines vague or unclear user input
- Produces structured, actionable prompts

### Linux Agent
- Linux troubleshooting expert
- Handles commands, errors, logs, and system issues

---

## 💬 Conversation Memory

The agent keeps track of previous messages, allowing:
- Natural follow-up questions
- Step-by-step debugging
- Context-aware responses

---

## 🗂 Project Structure
'''text
src/
├── agents/
│ ├── orchestration_agent.py
│ ├── prompt_refining_agent.py
│ └── linux_agent.py
├── chains/
│ └── agent_chains.py
├── commands/
│ ├── info.py
│ └── utils.py
├── common/
│ ├── messages/
│ │ └── terminal_messages.py
│ └── system_information.py
├── graph/
│ └── linux_assistant.py
├── llm_models/
│ ├── factory.py
│ ├── enums.py
│ └── info.py
├── my_logging/
│ └── config.py
├── prompts/
├── main.py


---

## 🧪 Tech Stack

![Python](https://img.shields.io/badge/Python-3.x-blue)
![LangChain](https://img.shields.io/badge/LangChain-powered-green)
![LangGraph](https://img.shields.io/badge/LangGraph-enabled-purple)
![Ollama](https://img.shields.io/badge/Ollama-offline-orange)
- Open-source LLMs (offline)

---

## 🚀 Getting Started

### Install dependencies
```bash
pip install -r requirements.txt
