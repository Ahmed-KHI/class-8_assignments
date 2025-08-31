# Assignment 4: Advanced Customer Support Bot

This assignment demonstrates building a comprehensive customer support system using the OpenAI Agents SDK with advanced features including bot/human agent handoffs, function tools with error handling, guardrails, and sophisticated conversation management.

## 🎯 Learning Objectives

By completing this assignment, you will learn:
- **BotAgent and HumanAgent Implementation**: Create specialized agents for different roles
- **Agent Handoffs**: Seamlessly transfer conversations between agents
- **Function Tools with Error Handling**: Implement tools with `is_enabled` and `error_function` parameters
- **Comprehensive Guardrails**: Apply input/output filtering and validation
- **ModelSettings Usage**: Configure different models for different agent types
- **Structured Logging**: Implement detailed conversation logging
- **Context Management**: Maintain context across agent handoffs
- **Escalation Logic**: Implement intelligent escalation rules

## 🏗️ Architecture Overview

```
📁 assignment-4/
├── 📄 README.md (This file)
├── 📁 config/
│   └── model_config.py      # Model configurations for different agents
├── 📁 data/
│   ├── customer_data.py     # Customer information and ticket system
│   └── knowledge_base.py    # FAQ and knowledge base data
├── 📁 tools/
│   ├── support_tools.py     # Customer support function tools
│   ├── ticket_tools.py      # Ticket management tools
│   └── knowledge_tools.py   # Knowledge base search tools
├── 📁 agents/
│   ├── bot_agent.py         # Automated support bot agent
│   ├── human_agent.py       # Human support agent
│   └── supervisor_agent.py  # Escalation and routing agent
├── 📁 guardrails/
│   └── support_guardrails.py # Input/output content filtering
├── 📁 utils/
│   ├── conversation_logger.py # Detailed logging system
│   ├── handoff_manager.py     # Agent handoff logic
│   └── escalation_engine.py   # Escalation decision engine
└── main.py                   # Main demo application
```

## 🔧 Key Features

### 1. Multi-Agent Architecture
- **BotAgent**: Handles routine inquiries, FAQs, and simple issues
- **HumanAgent**: Manages complex issues, complaints, and escalated cases
- **SupervisorAgent**: Routes conversations and manages escalations

### 2. Advanced Function Tools
```python
@function_tool(
    name_override="search_orders",
    description_override="Search customer orders with error handling",
    is_enabled=lambda ctx: ctx.user.is_authenticated,
    error_function=lambda ctx, error: handle_search_error(ctx, error)
)
def search_orders_tool(ctx, customer_id: str, order_date: str = None):
    # Tool implementation with comprehensive error handling
```

### 3. Intelligent Handoffs
- Seamless conversation transfer between agents
- Context preservation across handoffs
- Automatic escalation based on conversation analysis
- Human agent availability checking

### 4. Comprehensive Guardrails
- Content filtering for inappropriate language
- Privacy protection for sensitive information
- Compliance checking for industry regulations
- Input validation and sanitization

### 5. Advanced Logging
- Detailed conversation tracking
- Performance metrics
- Issue resolution tracking
- Agent handoff auditing

## 🚀 Getting Started

### Prerequisites
1. **Environment Setup**:
   ```bash
   pip install openai-agents-sdk python-decouple
   ```

2. **API Configuration**:
   Create `.env` file:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

3. **Run the Demo**:
   ```bash
   python main.py
   ```

## 📚 Implementation Details

### Agent Configuration
Each agent type uses different model settings optimized for their role:

- **BotAgent**: Fast responses, lower temperature for consistency
- **HumanAgent**: Higher creativity, longer context for complex issues  
- **SupervisorAgent**: Balanced settings for decision-making

### Function Tools with Error Handling
All tools implement:
- **is_enabled**: Dynamic tool availability based on context
- **error_function**: Graceful error handling and user feedback
- **Input validation**: Comprehensive parameter checking
- **Rate limiting**: Prevent API abuse

### Guardrails Implementation  
Multi-layered protection:
- **Input Guardrails**: Filter inappropriate requests
- **Output Guardrails**: Ensure appropriate responses
- **Privacy Guardrails**: Protect sensitive information
- **Compliance Guardrails**: Meet industry standards

### Conversation Flow
1. **Initial Contact**: Customer connects to BotAgent
2. **Issue Analysis**: Bot attempts to resolve using knowledge base
3. **Escalation Decision**: Complex issues trigger human handoff
4. **Human Support**: Specialized agent handles escalated cases
5. **Resolution Tracking**: Full conversation logging and metrics

## 🔍 Key Learning Points

### Advanced SDK Features
- **Context Variables**: Pass data between agents and tools
- **Message History**: Maintain conversation continuity
- **Agent Coordination**: Multiple agents working together
- **Error Recovery**: Graceful handling of failures

### Best Practices
- **Modular Design**: Separate concerns into focused components
- **Error Handling**: Comprehensive error management
- **Logging**: Detailed tracking for debugging and analytics
- **Testing**: Validate all components thoroughly

### Real-World Applications
- **Customer Service**: Automated first-line support
- **Help Desks**: Technical support systems
- **E-commerce**: Order and shipping support
- **Healthcare**: Patient inquiry management

## 🎮 Demo Scenarios

The main.py includes several demonstration scenarios:

1. **Simple FAQ Query**: Bot handles basic questions
2. **Order Status Inquiry**: Tool usage with authentication
3. **Complaint Escalation**: Automatic handoff to human agent
4. **Complex Technical Issue**: Multi-agent collaboration
5. **Error Handling**: Demonstrating graceful failure recovery

## 🏆 Success Metrics

After completing this assignment, you should be able to:
- ✅ Build multi-agent systems with seamless handoffs
- ✅ Implement function tools with comprehensive error handling
- ✅ Apply guardrails for content safety and compliance
- ✅ Create sophisticated conversation management systems
- ✅ Design real-world customer support solutions

## 📖 Additional Resources

- [OpenAI Agents SDK Documentation](https://github.com/openai/agents-sdk)
- [Function Tools Advanced Guide](https://docs.openai.com/agents/function-tools)
- [Agent Handoffs Best Practices](https://docs.openai.com/agents/handoffs)
- [Guardrails Implementation Patterns](https://docs.openai.com/agents/guardrails)

---

**Note**: This assignment represents advanced usage of the OpenAI Agents SDK and showcases enterprise-level features for production customer support systems.
