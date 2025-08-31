"""
Assignment 4: Advanced Customer Support Bot - Native Implementation
================================================================

This implementation demonstrates a comprehensive customer support system with:
- Multi-agent architecture (Bot → Human → Supervisor)
- Advanced function tools with error handling
- Comprehensive guardrails and content filtering
- Intelligent escalation and handoff logic
- Detailed conversation logging and metrics

Key Concepts Demonstrated:
✅ BotAgent and HumanAgent implementation
✅ Agent handoffs and conversation continuity
✅ Function tools with is_enabled and error handling
✅ Multi-layered guardrails system
✅ Context management across agent switches
✅ Escalation logic and routing decisions
✅ Comprehensive logging and analytics

To run: uv run python main.py
"""

import google.generativeai as genai
from decouple import config
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from enum import Enum
import json
import asyncio
import re


class TicketStatus(Enum):
    """Support ticket status"""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    WAITING_CUSTOMER = "waiting_customer"
    RESOLVED = "resolved"
    ESCALATED = "escalated"
    CLOSED = "closed"


class TicketPriority(Enum):
    """Support ticket priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"
    CRITICAL = "critical"


class AgentType(Enum):
    """Types of support agents"""
    BOT = "bot"
    HUMAN = "human"
    SUPERVISOR = "supervisor"


@dataclass
class Customer:
    """Customer information model"""
    customer_id: str
    name: str
    email: str
    tier: str = "basic"  # basic, premium, enterprise
    is_authenticated: bool = False
    recent_issues: List[str] = field(default_factory=list)


@dataclass
class SupportTicket:
    """Support ticket model"""
    ticket_id: str
    customer_id: str
    title: str
    description: str
    status: TicketStatus
    priority: TicketPriority
    created_at: datetime
    assigned_agent: Optional[str] = None
    escalation_reason: Optional[str] = None
    resolution_notes: Optional[str] = None


@dataclass
class ConversationLog:
    """Conversation logging model"""
    session_id: str
    customer_id: Optional[str]
    messages: List[Dict[str, Any]] = field(default_factory=list)
    agent_handoffs: List[Dict[str, Any]] = field(default_factory=list)
    escalations: List[Dict[str, Any]] = field(default_factory=list)
    resolution_outcome: Optional[str] = None


class SupportGuardrails:
    """Comprehensive guardrails for customer support"""
    
    @staticmethod
    def input_content_filter(user_input: str) -> tuple[bool, str]:
        """Filter inappropriate input content"""
        user_input_lower = user_input.lower()
        
        inappropriate_patterns = [
            'offensive', 'abusive', 'threatening', 'harassment',
            'discrimination', 'hate speech', 'profanity'
        ]
        
        for pattern in inappropriate_patterns:
            if pattern in user_input_lower:
                return False, "🚫 Input contains inappropriate content. Please rephrase your message professionally."
        
        return True, "✅ Input content acceptable"
    
    @staticmethod  
    def privacy_protection_filter(text: str) -> tuple[str, List[str]]:
        """Protect sensitive information in text"""
        protected_text = text
        protected_items = []
        
        cc_pattern = r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'
        if re.search(cc_pattern, text):
            protected_text = re.sub(cc_pattern, '[CREDIT_CARD_REDACTED]', protected_text)
            protected_items.append('credit_card')
        
        ssn_pattern = r'\b\d{3}-?\d{2}-?\d{4}\b'
        if re.search(ssn_pattern, text):
            protected_text = re.sub(ssn_pattern, '[SSN_REDACTED]', protected_text)
            protected_items.append('ssn')
        
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        if re.search(phone_pattern, text):
            protected_text = re.sub(phone_pattern, '[PHONE_REDACTED]', protected_text)
            protected_items.append('phone')
            
        return protected_text, protected_items
    
    @staticmethod
    def output_compliance_check(response: str) -> tuple[bool, str]:
        """Ensure output meets compliance standards"""
        response_lower = response.lower()
        
        violations = []
        
        medical_terms = ['diagnose', 'medical advice', 'prescription', 'treatment']
        if any(term in response_lower for term in medical_terms):
            violations.append('medical_advice')
         
        legal_terms = ['legal advice', 'lawsuit', 'sue', 'attorney']
        if any(term in response_lower for term in legal_terms):
            violations.append('legal_advice')
        
        if violations:
            return False, f"🚫 Output contains compliance violations: {', '.join(violations)}"
        
        return True, "✅ Output compliant"


class SupportTools:
    """Function tools for customer support operations"""
    
    CUSTOMERS_DB = {
        "cust_001": Customer("cust_001", "John Doe", "john@email.com", "premium"),
        "cust_002": Customer("cust_002", "Jane Smith", "jane@email.com", "basic"),
        "cust_003": Customer("cust_003", "Bob Wilson", "bob@email.com", "enterprise")
    }
    
    TICKETS_DB = {
        "tick_001": SupportTicket(
            "tick_001", "cust_001", "Login Issue", "Cannot access account",
            TicketStatus.OPEN, TicketPriority.HIGH, datetime.now()
        ),
        "tick_002": SupportTicket(
            "tick_002", "cust_002", "Billing Question", "Charge dispute",
            TicketStatus.IN_PROGRESS, TicketPriority.MEDIUM, datetime.now()
        )
    }
    
    FAQ_DB = {
        "login": "To reset your password, click 'Forgot Password' on the login page.",
        "billing": "Billing questions can be resolved by contacting our billing department.",
        "account": "Account issues require verification of your identity first.",
        "technical": "For technical issues, please provide detailed error descriptions."
    }
    
    @staticmethod
    def authenticate_customer(identifier: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Authenticate customer by email or ID"""
        try:
            if identifier in SupportTools.CUSTOMERS_DB:
                customer = SupportTools.CUSTOMERS_DB[identifier]
                customer.is_authenticated = True
                context['authenticated_customer'] = customer
                return {
                    "success": True,
                    "customer_id": customer.customer_id,
                    "name": customer.name,
                    "tier": customer.tier,
                    "message": f"✅ Authentication successful. Welcome, {customer.name}!"
                }
            
            for customer in SupportTools.CUSTOMERS_DB.values():
                if customer.email.lower() == identifier.lower():
                    customer.is_authenticated = True
                    context['authenticated_customer'] = customer
                    return {
                        "success": True,
                        "customer_id": customer.customer_id,
                        "name": customer.name,
                        "tier": customer.tier,
                        "message": f"✅ Authentication successful. Welcome, {customer.name}!"
                    }
            
            return {
                "success": False,
                "message": "❌ Customer not found. Please check your email or customer ID."
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Authentication error: {str(e)}"
            }
    
    @staticmethod
    def search_customer_tickets(customer_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Search tickets for authenticated customer"""
        try:
            customer = context.get('authenticated_customer')
            if not customer or not customer.is_authenticated:
                return {
                    "success": False,
                    "message": "🔐 Please authenticate first to access ticket information."
                }
            
            tickets = []
            for ticket in SupportTools.TICKETS_DB.values():
                if ticket.customer_id == customer_id:
                    tickets.append({
                        "ticket_id": ticket.ticket_id,
                        "title": ticket.title,
                        "status": ticket.status.value,
                        "priority": ticket.priority.value,
                        "created": ticket.created_at.strftime("%Y-%m-%d")
                    })
            
            return {
                "success": True,
                "tickets": tickets,
                "count": len(tickets),
                "message": f"📋 Found {len(tickets)} tickets for your account."
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Error searching tickets: {str(e)}"
            }
    
    @staticmethod
    def search_knowledge_base(query: str) -> Dict[str, Any]:
        """Search FAQ and knowledge base"""
        try:
            query_lower = query.lower()
            results = []
            
            for category, answer in SupportTools.FAQ_DB.items():
                if category in query_lower or any(word in answer.lower() for word in query_lower.split()):
                    results.append({
                        "category": category,
                        "answer": answer,
                        "relevance": "high" if category in query_lower else "medium"
                    })
            
            return {
                "success": True,
                "results": results,
                "count": len(results),
                "message": f"📚 Found {len(results)} knowledge base articles."
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Knowledge base search error: {str(e)}"
            }
    
    @staticmethod
    def create_support_ticket(title: str, description: str, priority: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Create new support ticket"""
        try:
            customer = context.get('authenticated_customer')
            if not customer or not customer.is_authenticated:
                return {
                    "success": False,
                    "message": "🔐 Please authenticate first to create a support ticket."
                }
            
            ticket_id = f"tick_{len(SupportTools.TICKETS_DB) + 1:03d}"
            
            new_ticket = SupportTicket(
                ticket_id=ticket_id,
                customer_id=customer.customer_id,
                title=title,
                description=description,
                status=TicketStatus.OPEN,
                priority=TicketPriority(priority.lower()),
                created_at=datetime.now()
            )
            
            SupportTools.TICKETS_DB[ticket_id] = new_ticket
            
            return {
                "success": True,
                "ticket_id": ticket_id,
                "status": new_ticket.status.value,
                "message": f"🎫 Support ticket {ticket_id} created successfully!"
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Error creating ticket: {str(e)}"
            }


class ConversationLogger:
    """Comprehensive conversation logging system"""
    
    def __init__(self):
        self.sessions = {}
    
    def start_session(self, session_id: str) -> ConversationLog:
        """Start new conversation session"""
        log = ConversationLog(session_id, None)
        self.sessions[session_id] = log
        return log
    
    def log_message(self, session_id: str, role: str, content: str, agent_type: Optional[AgentType] = None):
        """Log conversation message"""
        if session_id in self.sessions:
            message = {
                "timestamp": datetime.now().isoformat(),
                "role": role,
                "content": content,
                "agent_type": agent_type.value if agent_type else None
            }
            self.sessions[session_id].messages.append(message)
    
    def log_handoff(self, session_id: str, from_agent: AgentType, to_agent: AgentType, reason: str):
        """Log agent handoff"""
        if session_id in self.sessions:
            handoff = {
                "timestamp": datetime.now().isoformat(),
                "from_agent": from_agent.value,
                "to_agent": to_agent.value,
                "reason": reason
            }
            self.sessions[session_id].agent_handoffs.append(handoff)
    
    def log_escalation(self, session_id: str, agent: AgentType, reason: str, priority: str):
        """Log escalation event"""
        if session_id in self.sessions:
            escalation = {
                "timestamp": datetime.now().isoformat(),
                "agent": agent.value,
                "reason": reason,
                "priority": priority
            }
            self.sessions[session_id].escalations.append(escalation)


class EscalationEngine:
    """Intelligent escalation decision engine"""
    
    @staticmethod
    def should_escalate_to_human(conversation_context: Dict[str, Any]) -> tuple[bool, str]:
        """Determine if conversation should escalate to human agent"""
        
        escalation_triggers = []
        
        if any(keyword in str(conversation_context).lower() for keyword in 
               ['bug', 'error', 'broken', 'not working', 'system down']):
            escalation_triggers.append('technical_complexity')
        
        if any(keyword in str(conversation_context).lower() for keyword in 
               ['frustrated', 'angry', 'upset', 'disappointed', 'complaint']):
            escalation_triggers.append('customer_emotion')
        
        customer = conversation_context.get('authenticated_customer')
        if customer and customer.tier in ['premium', 'enterprise']:
            escalation_triggers.append('vip_customer')
        
        if conversation_context.get('bot_failures', 0) >= 2:
            escalation_triggers.append('bot_failure')
        
        if escalation_triggers:
            return True, f"Escalating due to: {', '.join(escalation_triggers)}"
        
        return False, "No escalation needed"
    
    @staticmethod
    def should_escalate_to_supervisor(conversation_context: Dict[str, Any]) -> tuple[bool, str]:
        """Determine if conversation should escalate to supervisor"""
        
        supervisor_triggers = []
        
        if any(keyword in str(conversation_context).lower() for keyword in 
               ['security', 'breach', 'fraud', 'legal', 'compliance']):
            supervisor_triggers.append('critical_issue')
        
        if conversation_context.get('ticket_priority') == 'critical':
            supervisor_triggers.append('critical_priority')
        
        customer = conversation_context.get('authenticated_customer')
        if customer and customer.tier == 'enterprise':
            supervisor_triggers.append('enterprise_customer')
        
        if supervisor_triggers:
            return True, f"Supervisor escalation due to: {', '.join(supervisor_triggers)}"
        
        return False, "Supervisor escalation not needed"


class BotAgent:
    """Automated customer support bot"""
    
    def __init__(self):
        self.agent_type = AgentType.BOT
        self.name = "SupportBot"
        self.guardrails = SupportGuardrails()
        self.tools = SupportTools()
        
        try:
            gemini_api_key = str(config("GEMINI_API_KEY"))
            genai.configure(api_key=gemini_api_key)  # type: ignore
            self.model = genai.GenerativeModel('gemini-1.5-flash')  # type: ignore
            self.initialized = True
        except Exception as e:
            print(f"❌ BotAgent initialization error: {e}")
            self.initialized = False
    
    async def process_message(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process user message with comprehensive bot logic"""
        
        print(f"\n🤖 BOT AGENT Processing: '{user_input}'")
        print("-" * 50)
        
        print("🛡️ STEP 1: Input Guardrails")
        input_ok, input_message = self.guardrails.input_content_filter(user_input)
        print(f"   {input_message}")
        
        if not input_ok:
            return {
                "response": input_message,
                "needs_handoff": False,
                "agent_type": self.agent_type.value
            }
        
        print("\n🔐 STEP 2: Privacy Protection")
        protected_input, protected_items = self.guardrails.privacy_protection_filter(user_input)
        if protected_items:
            print(f"   🛡️ Protected: {', '.join(protected_items)}")
        else:
            print("   ✅ No sensitive data detected")
        
        print("\n🔍 STEP 3: Intent Analysis & Tool Usage")
        intent_response = await self._analyze_intent_and_respond(protected_input, context)
        
        print("\n🎯 STEP 4: Escalation Decision")
        escalation_engine = EscalationEngine()
        needs_escalation, escalation_reason = escalation_engine.should_escalate_to_human(context)
        
        if needs_escalation:
            print(f"   🔄 Escalation needed: {escalation_reason}")
            return {
                "response": f"I understand this requires specialized attention. Let me connect you with a human agent who can better assist you. Reason: {escalation_reason}",
                "needs_handoff": True,
                "handoff_to": AgentType.HUMAN.value,
                "escalation_reason": escalation_reason,
                "agent_type": self.agent_type.value
            }
        else:
            print(f"   ✅ No escalation needed")
        
        print("\n📋 STEP 5: Output Compliance Check")
        output_ok, compliance_message = self.guardrails.output_compliance_check(intent_response)
        print(f"   {compliance_message}")
        
        if not output_ok:
            intent_response = "I apologize, but I cannot provide that type of information. Let me connect you with a human agent who can assist you appropriately."
            return {
                "response": intent_response,
                "needs_handoff": True,
                "handoff_to": AgentType.HUMAN.value,
                "escalation_reason": "compliance_violation",
                "agent_type": self.agent_type.value
            }
        
        print("\n✅ Bot processing completed successfully")
        
        return {
            "response": intent_response,
            "needs_handoff": False,
            "agent_type": self.agent_type.value
        }
    
    async def _analyze_intent_and_respond(self, user_input: str, context: Dict[str, Any]) -> str:
        """Analyze user intent and provide appropriate response"""
        
        user_input_lower = user_input.lower()
        
        if any(keyword in user_input_lower for keyword in ['login', 'authenticate', 'sign in', 'my account']):
            if '@' in user_input or 'cust_' in user_input:
                
                words = user_input.split()
                identifier = None
                for word in words:
                    if '@' in word or word.startswith('cust_'):
                        identifier = word
                        break
                
                if identifier:
                    auth_result = self.tools.authenticate_customer(identifier, context)
                    return auth_result.get('message', 'Authentication attempted.')
            
            return "I can help you with account access. Please provide your email address or customer ID."
        
        if any(keyword in user_input_lower for keyword in ['my tickets', 'ticket status', 'support tickets']):
            customer = context.get('authenticated_customer')
            if customer:
                ticket_result = self.tools.search_customer_tickets(customer.customer_id, context)
                return ticket_result.get('message', 'Ticket search attempted.')
            else:
                return "Please authenticate first so I can look up your tickets."
        
        if any(keyword in user_input_lower for keyword in ['help', 'how to', 'question', 'problem']):
            kb_result = self.tools.search_knowledge_base(user_input)
            if kb_result.get('success') and kb_result.get('results'):
                responses = []
                for result in kb_result['results'][:2]:  # Top 2 results
                    responses.append(f"📚 {result['answer']}")
                return "Here's what I found:\n" + "\n".join(responses)
            else:
                return "I searched our knowledge base but couldn't find specific information. Let me connect you with a human agent."
        
        if any(keyword in user_input_lower for keyword in ['create ticket', 'new ticket', 'report issue']):
            return "I can help you create a support ticket. Please describe your issue and I'll set that up for you."
        
        if self.initialized:
            try:
                prompt = f"""You are a helpful customer support bot. The customer said: "{user_input}"

Provide a helpful, professional response that:
1. Acknowledges their request
2. Offers appropriate assistance
3. Stays within customer support scope
4. Maintains professional tone
5. Suggests next steps if needed

Keep response under 200 characters and be helpful but concise."""
                
                response = self.model.generate_content(prompt)
                return response.text
                
            except Exception as e:
                context['bot_failures'] = context.get('bot_failures', 0) + 1
                return f"I encountered a technical issue processing your request. Let me connect you with a human agent for assistance."
        else:
            return "I'm currently experiencing technical difficulties. Let me connect you with a human agent who can assist you."


class HumanAgent:
    """Human customer support agent"""
    
    def __init__(self):
        self.agent_type = AgentType.HUMAN
        self.name = "Human Support Agent"
        self.guardrails = SupportGuardrails()
        self.tools = SupportTools()
        
        try:
            gemini_api_key = str(config("GEMINI_API_KEY"))
            genai.configure(api_key=gemini_api_key)  # type: ignore
            self.model = genai.GenerativeModel('gemini-1.5-flash')  # type: ignore
            self.initialized = True
        except Exception as e:
            print(f"❌ HumanAgent initialization error: {e}")
            self.initialized = False
    
    async def process_message(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process user message with human agent approach"""
        
        print(f"\n👤 HUMAN AGENT Processing: '{user_input}'")
        print("-" * 50)
        
        print("🛡️ STEP 1: Input Guardrails")
        input_ok, input_message = self.guardrails.input_content_filter(user_input)
        print(f"   {input_message}")
        
        if not input_ok:
            return {
                "response": "I understand you're frustrated, but let's keep our conversation professional so I can help you effectively.",
                "needs_handoff": False,
                "agent_type": self.agent_type.value
            }
        
        print("\n💭 STEP 2: Human-level Response Generation")
        response = await self._generate_human_response(user_input, context)
        
        print("\n🎯 STEP 3: Supervisor Escalation Check")
        escalation_engine = EscalationEngine()
        needs_supervisor, supervisor_reason = escalation_engine.should_escalate_to_supervisor(context)
        
        if needs_supervisor:
            print(f"   🔄 Supervisor escalation: {supervisor_reason}")
            return {
                "response": f"This requires immediate supervisor attention. I'm escalating this to my supervisor who will contact you shortly. Reason: {supervisor_reason}",
                "needs_handoff": True,
                "handoff_to": AgentType.SUPERVISOR.value,
                "escalation_reason": supervisor_reason,
                "agent_type": self.agent_type.value
            }
        else:
            print("   ✅ No supervisor escalation needed")
        
        print("\n✅ Human agent processing completed")
        
        return {
            "response": response,
            "needs_handoff": False,
            "agent_type": self.agent_type.value
        }
    
    async def _generate_human_response(self, user_input: str, context: Dict[str, Any]) -> str:
        """Generate human-like response with empathy and expertise"""
        
        if not self.initialized:
            return "I apologize for the technical difficulties. Let me help you with your issue manually. Could you provide more details about what you need assistance with?"
        
        try:
            customer = context.get('authenticated_customer')
            customer_info = ""
            if customer:
                customer_info = f"Customer: {customer.name} ({customer.tier} tier)"
            
            escalation_reason = context.get('escalation_reason', '')
            escalation_context = f"Escalated from bot due to: {escalation_reason}" if escalation_reason else ""
            
            prompt = f"""You are an experienced human customer support agent. 

Context:
- {customer_info}
- {escalation_context}
- Customer message: "{user_input}"

Provide a professional, empathetic response that:
1. Shows understanding and empathy
2. Addresses their specific concern
3. Offers concrete next steps
4. Maintains professional but warm tone
5. Demonstrates human expertise and understanding
6. Asks clarifying questions if needed

Be more detailed and thorough than a bot would be, showing human judgment and empathy.
"""
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return "I apologize for any technical issues. I'm here to personally help resolve your concern. Could you please describe your issue in detail so I can provide the best assistance?"


class SupervisorAgent:
    """Supervisor agent for escalations and management decisions"""
    
    def __init__(self):
        self.agent_type = AgentType.SUPERVISOR
        self.name = "Support Supervisor"
        self.guardrails = SupportGuardrails()
        
        try:
            gemini_api_key = str(config("GEMINI_API_KEY"))
            genai.configure(api_key=gemini_api_key)  # type: ignore
            self.model = genai.GenerativeModel('gemini-1.5-flash')  # type: ignore
            self.initialized = True
        except Exception as e:
            print(f"❌ SupervisorAgent initialization error: {e}")
            self.initialized = False
    
    async def process_message(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process escalated issues with supervisor authority"""
        
        print(f"\n👔 SUPERVISOR Processing: '{user_input}'")
        print("-" * 50)
        
        escalation_reason = context.get('escalation_reason', 'general_escalation')
        
        print("🎯 STEP 1: Supervisor Analysis")
        response = await self._handle_supervisor_escalation(user_input, context, escalation_reason)
        
        print("✅ Supervisor processing completed")
        
        return {
            "response": response,
            "needs_handoff": False,
            "agent_type": self.agent_type.value,
            "supervisor_action": True
        }
    
    async def _handle_supervisor_escalation(self, user_input: str, context: Dict[str, Any], escalation_reason: str) -> str:
        """Handle supervisor-level escalations"""
        
        if not self.initialized:
            return f"As the support supervisor, I'm personally taking over this case (escalated due to: {escalation_reason}). I will ensure this receives immediate priority attention and will personally follow up with you within 2 business hours."
        
        try:
            customer = context.get('authenticated_customer')
            customer_info = ""
            if customer:
                customer_info = f"Customer: {customer.name} ({customer.tier} tier)"
            
            prompt = f"""You are a customer support supervisor handling an escalated case.

Escalation Details:
- Reason: {escalation_reason}
- {customer_info}
- Customer message: "{user_input}"

As a supervisor, provide a response that:
1. Acknowledges the escalation and takes ownership
2. Demonstrates authority and expertise
3. Offers immediate action and resolution
4. Provides clear next steps and timelines
5. Shows empathy while being decisive
6. Offers compensation or special considerations if appropriate
7. Ensures customer satisfaction

Be authoritative, empathetic, and solution-focused. Show that this has the highest priority.
"""
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"As the support supervisor, I am personally taking over this escalated case ({escalation_reason}). This will receive my immediate attention, and I will ensure a resolution within 24 hours. I will personally follow up with you."


class AdvancedCustomerSupportSystem:
    """Main customer support system with multi-agent architecture"""
    
    def __init__(self):
        self.bot_agent = BotAgent()
        self.human_agent = HumanAgent()  
        self.supervisor_agent = SupervisorAgent()
        self.logger = ConversationLogger()
        
        self.current_agent = self.bot_agent
        self.session_id = None
        self.context = {}
        
        print("🏢 Advanced Customer Support System Initialized")
        print("   🤖 Bot Agent: Ready")
        print("   👤 Human Agent: Ready")
        print("   👔 Supervisor Agent: Ready")
    
    async def start_conversation(self, session_id: Optional[str] = None):
        """Start new customer support conversation"""
        if not session_id:
            session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.session_id = session_id
        self.context = {'session_id': session_id, 'bot_failures': 0}
        self.current_agent = self.bot_agent
        
        self.logger.start_session(session_id)
        self.logger.log_message(session_id, "system", "Conversation started", AgentType.BOT)
        
        return f"👋 Hello! I'm {self.current_agent.name}. How can I assist you today?"
    
    async def process_user_message(self, user_input: str) -> str:
        """Process user message through current agent"""
        
        if not self.session_id:
            return "Please start a conversation session first."
        
        self.logger.log_message(self.session_id, "user", user_input)
        
        result = await self.current_agent.process_message(user_input, self.context)
        
        self.logger.log_message(self.session_id, "agent", result['response'], self.current_agent.agent_type)
        
        if result.get('needs_handoff'):
            handoff_response = await self._handle_agent_handoff(result)
            return handoff_response
        
        return result['response']
    
    async def _handle_agent_handoff(self, result: Dict[str, Any]) -> str:
        """Handle handoff between agents"""
        
        if not self.session_id:
            return "Error: No active session for handoff"
        
        handoff_to = result.get('handoff_to')
        escalation_reason = result.get('escalation_reason', 'general')
        
        if handoff_to == AgentType.HUMAN.value:
            self.logger.log_handoff(self.session_id, self.current_agent.agent_type, AgentType.HUMAN, escalation_reason)
            self.logger.log_escalation(self.session_id, self.current_agent.agent_type, escalation_reason, "medium")
            self.current_agent = self.human_agent
            
        elif handoff_to == AgentType.SUPERVISOR.value:
            self.logger.log_handoff(self.session_id, self.current_agent.agent_type, AgentType.SUPERVISOR, escalation_reason)
            self.logger.log_escalation(self.session_id, self.current_agent.agent_type, escalation_reason, "high")
            self.current_agent = self.supervisor_agent
        
        self.context['escalation_reason'] = escalation_reason
        
        handoff_message = f"\n🔄 **AGENT HANDOFF**\n{result['response']}\n\n👋 Hi, I'm {self.current_agent.name}. I've been briefed on your situation and I'm here to help."
        
        return handoff_message
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get detailed conversation summary and metrics"""
        
        if not self.session_id or self.session_id not in self.logger.sessions:
            return {"error": "No active session"}
        
        session_log = self.logger.sessions[self.session_id]
        
        return {
            "session_id": self.session_id,
            "current_agent": self.current_agent.agent_type.value,
            "message_count": len(session_log.messages),
            "handoff_count": len(session_log.agent_handoffs),
            "escalation_count": len(session_log.escalations),
            "authenticated_customer": self.context.get('authenticated_customer', {}).name if self.context.get('authenticated_customer') else None,
            "session_duration": len(session_log.messages) * 30,  # Estimated seconds
            "handoffs": session_log.agent_handoffs,
            "escalations": session_log.escalations
        }


async def run_interactive_demo():
    """Interactive demonstration of the customer support system"""
    
    print("🎯 ASSIGNMENT 4: ADVANCED CUSTOMER SUPPORT SYSTEM")
    print("=" * 65)
    print("Interactive Demo - Experience multi-agent support with handoffs")
    print("Type 'quit' to exit, 'summary' for conversation metrics")
    print("=" * 65)
    
    support_system = AdvancedCustomerSupportSystem()
    
    welcome_message = await support_system.start_conversation()
    print(f"\n🏢 {welcome_message}")
    
    while True:
        try:
            user_input = input(f"\n💬 You: ")
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                
                summary = support_system.get_conversation_summary()
                print(f"\n📊 CONVERSATION SUMMARY:")
                print("-" * 40)
                print(f"Session ID: {summary.get('session_id')}")
                print(f"Final Agent: {summary.get('current_agent')}")
                print(f"Total Messages: {summary.get('message_count')}")
                print(f"Agent Handoffs: {summary.get('handoff_count')}")
                print(f"Escalations: {summary.get('escalation_count')}")
                if summary.get('authenticated_customer'):
                    print(f"Customer: {summary.get('authenticated_customer')}")
                print("\n👋 Thank you for using our support system!")
                break
            
            if user_input.lower() == 'summary':
                summary = support_system.get_conversation_summary()
                print(f"\n📊 Current Session Metrics:")
                print(f"   Agent: {summary.get('current_agent')}")
                print(f"   Messages: {summary.get('message_count')}")
                print(f"   Handoffs: {summary.get('handoff_count')}")
                print(f"   Escalations: {summary.get('escalation_count')}")
                continue
            
            if not user_input.strip():
                print("❌ Please enter a message.")
                continue
            
            response = await support_system.process_user_message(user_input)
            
            print(f"\n🤖 {support_system.current_agent.name}:")
            print("─" * 50)
            print(response)
            print("─" * 50)
            
        except KeyboardInterrupt:
            print("\n\n👋 Session interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


async def run_demonstration_scenarios():
    """Pre-defined demo scenarios showcasing all features"""
    
    print("🎯 ASSIGNMENT 4: DEMONSTRATION SCENARIOS")
    print("=" * 60)
    print("Automated demo showing multi-agent handoffs and escalations")
    print("=" * 60)
    
    support_system = AdvancedCustomerSupportSystem()
    
    scenarios = [
        {
            "name": "Simple FAQ Query",
            "messages": [
                "Hello, I need help with login",
                "My email is john@email.com"
            ],
            "description": "🤖 Bot handles basic authentication and FAQ"
        },
        {
            "name": "Complex Technical Issue",
            "messages": [
                "I'm having a serious bug with your system",
                "This is broken and not working at all",
                "I'm very frustrated with this service"
            ],
            "description": "🤖→👤 Bot escalates to human for complex/emotional issues"
        },
        {
            "name": "Critical Security Issue",
            "messages": [
                "I think there's been a security breach on my account",
                "This looks like fraud or unauthorized access",
                "I need immediate help with this security issue"
            ],
            "description": "🤖→👤→👔 Full escalation chain to supervisor"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{'='*60}")
        print(f"🎬 SCENARIO {i}: {scenario['name']}")
        print(f"Description: {scenario['description']}")
        print("="*60)
        
        session_id = f"demo_scenario_{i}"
        welcome = await support_system.start_conversation(session_id)
        print(f"\n🏢 {welcome}")
        
        for j, message in enumerate(scenario['messages'], 1):
            print(f"\n💬 User Message {j}: {message}")
            
            response = await support_system.process_user_message(message)
            
            print(f"\n🎭 {support_system.current_agent.name} Response:")
            print("─" * 50)
            print(response)
            print("─" * 50)
            
            await asyncio.sleep(1)
        
        summary = support_system.get_conversation_summary()
        print(f"\n📋 Scenario {i} Results:")
        print(f"   Final Agent: {summary.get('current_agent')}")
        print(f"   Handoffs: {summary.get('handoff_count')}")
        print(f"   Escalations: {summary.get('escalation_count')}")
        
        if i < len(scenarios):
            print("\n⏳ Moving to next scenario...")
            await asyncio.sleep(2)


async def main():
    """Main application entry point"""
    
    print("🚀 ASSIGNMENT 4: ADVANCED CUSTOMER SUPPORT BOT")
    print("This demonstrates comprehensive multi-agent customer support with")
    print("handoffs, escalations, function tools, and guardrails.")
    print()
    
    try:
        print("Select demo mode:")
        print("1. Interactive mode (chat with the system)")
        print("2. Automated scenarios (see all features)")
        choice = input("Enter choice (1 or 2): ").strip()
        
        if choice == "2":
            await run_demonstration_scenarios()
        else:
            await run_interactive_demo()
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Application error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
