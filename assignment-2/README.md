# 📘 Assignment 2: Implement Output Guardrail Functionality

## 🎯 Objective
Extend the guardrails example to add output guardrails using OpenAI's Agent SDK.

### 📋 Requirements
- Current code blocks non-math queries (input guardrails)
- Add rules so agent responses avoid political topics and references to political figures
- Implement both input and output guardrails

### **Read the following links**
 - Guardrails [https://openai.github.io/openai-agents-python/guardrails/](https://openai.github.io/openai-agents-python/guardrails/)
 - Guardrails reference [https://openai.github.io/openai-agents-python/ref/guardrail/](https://openai.github.io/openai-agents-python/ref/guardrail/)
 - Agents [https://openai.github.io/openai-agents-python/agents/](https://openai.github.io/openai-agents-python/agents/)

---

## 📘 Steps to Execute the Code 

### 🔐 1. Configure Environment Variables
- Add your **Gemini API Key** to the `.env` file as `GEMINI_API_KEY=your_key_here`

### 🚀 2. Run the Assignment
```bash
uv run assignment-2/main.py
```

---

## 🔧 What This Assignment Implements
- **Input Guardrails**: Block non-math queries and inappropriate content
- **Output Guardrails**: Filter agent responses to avoid political topics
- **@guardrail Decorator**: Proper implementation of guardrail functions
- **Content Filtering**: Automated content moderation

---

## 💡 Key Features Demonstrated
- `@guardrail` decorator for input filtering
- Output content validation and filtering
- Multi-layer protection against inappropriate content
- Custom guardrail logic implementation
- Error handling and user feedback
