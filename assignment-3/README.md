# 📘 Assignment 3: Convert Static Instructions into Dynamic Instructions

## 🎯 Objective
Convert static instructions into dynamic ones using OpenAI's Agent SDK.

### 📋 Requirements
- Base work on the hotel booking and information retrieval example
- Update so a single agent can store and retrieve details for multiple hotels  
- Use context to return the correct hotel information based on user queries
- Implement dynamic instruction generation

### **Read the following links**
 - Agents [https://openai.github.io/openai-agents-python/agents/](https://openai.github.io/openai-agents-python/agents/)
 - Tools [https://openai.github.io/openai-agents-python/tools/](https://openai.github.io/openai-agents-python/tools/)
 - Context and Dynamic Instructions [https://openai.github.io/openai-agents-python/ref/agent/](https://openai.github.io/openai-agents-python/ref/agent/)

---

## 📘 Steps to Execute the Code 

### 🔐 1. Configure Environment Variables
- Add your **Gemini API Key** to the `.env` file as `GEMINI_API_KEY=your_key_here`

### 🚀 2. Run the Assignment
```bash
uv run assignment-3/main.py
```

---

## 🔧 What This Assignment Implements
- **Dynamic Instructions**: Context-aware instruction generation
- **Multi-Hotel Management**: Store and retrieve information for multiple hotels
- **Context-Driven Responses**: Personalized responses based on user context
- **Hotel Booking System**: Complete booking workflow with dynamic context

---

## 💡 Key Features Demonstrated
- Dynamic instruction functions with `RunContextWrapper`
- Context-based decision making
- Multi-entity data management
- Personalized agent behavior
- Runtime instruction modification
