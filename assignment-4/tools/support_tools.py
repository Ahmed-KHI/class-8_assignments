from agents import function_tool, RunContextWrapper, HandoffToAgent
from data.customer_data import (
    Customer, SupportTicket, Order, TicketStatus, TicketPriority,
    get_customer_by_id, get_customer_by_email, get_tickets_by_customer, 
    get_orders_by_customer, create_new_ticket, TICKETS_DATABASE
)
from data.knowledge_base import search_faq, search_knowledge_base, FAQ_CATEGORIES
from typing import List, Dict, Any, Optional
import json
from datetime import datetime


def handle_authentication_error(ctx: RunContextWrapper, error: Exception) -> str:
    """Handle authentication errors gracefully"""
    return "I need to verify your identity first. Could you please provide your email address or customer ID?"


def handle_search_error(ctx: RunContextWrapper, error: Exception) -> str:
    """Handle search errors gracefully"""
    return f"I encountered an issue while searching. Please try again or contact support if the problem persists. Error: {str(error)[:100]}"


def handle_ticket_error(ctx: RunContextWrapper, error: Exception) -> str:
    """Handle ticket operation errors"""
    return f"I couldn't complete that ticket operation. Please verify your information and try again. If you continue having issues, I'll connect you with a human agent."


@function_tool(
    name_override="authenticate_customer",
    description_override="Authenticate customer using email or customer ID",
    is_enabled=lambda ctx: True,  # Always enabled for authentication
    error_function=handle_authentication_error
)
def authenticate_customer_tool(
    ctx: RunContextWrapper,
    identifier: str,
    identifier_type: str = "email"
) -> str:
    """
    Authenticate customer and set session context.
    
    Args:
        ctx: Context wrapper
        identifier: Email address or customer ID
        identifier_type: Type of identifier ('email' or 'customer_id')
        
    Returns:
        JSON string with authentication result
    """
    print(f"🔐 Authenticating customer: {identifier}")
    
    try:
        customer = None
        if identifier_type == "email":
            customer = get_customer_by_email(identifier)
        elif identifier_type == "customer_id":
            customer = get_customer_by_id(identifier)
        
        if customer:
            # Set authenticated status
            customer.is_authenticated = True
            
            # Update context
            if hasattr(ctx, 'context_variables'):
                ctx.context_variables['customer'] = customer
            
            auth_result = {
                "authenticated": True,
                "customer": {
                    "id": customer.customer_id,
                    "name": customer.name,
                    "tier": customer.tier.value,
                    "account_since": customer.account_since
                },
                "message": f"Welcome back, {customer.name}! I have access to your account information."
            }
        else:
            auth_result = {
                "authenticated": False,
                "message": "I couldn't find an account with that information. Please double-check your email or customer ID."
            }
        
        return json.dumps(auth_result, indent=2)
        
    except Exception as e:
        print(f"❌ Authentication error: {str(e)}")
        raise e


@function_tool(
    name_override="search_orders",
    description_override="Search customer orders with detailed information",
    is_enabled=lambda ctx: getattr(ctx.context_variables.get('customer'), 'is_authenticated', False) if hasattr(ctx, 'context_variables') else False,
    error_function=handle_search_error
)
def search_orders_tool(
    ctx: RunContextWrapper,
    customer_id: str = "",
    order_id: str = "",
    status_filter: str = ""
) -> str:
    """
    Search customer orders with filtering options.
    
    Args:
        ctx: Context wrapper with customer info
        customer_id: Customer ID (optional if in context)
        order_id: Specific order ID to search for
        status_filter: Filter by order status
        
    Returns:
        JSON formatted order information
    """
    print(f"🔍 Searching orders for customer")
    
    try:
        # Get customer from context or parameter
        customer = ctx.context_variables.get('customer') if hasattr(ctx, 'context_variables') else None
        if not customer and customer_id:
            customer = get_customer_by_id(customer_id)
        
        if not customer:
            return json.dumps({"error": "Customer authentication required"})
        
        if not customer.is_authenticated:
            return json.dumps({"error": "Please authenticate first"})
        
        # Get orders
        orders = get_orders_by_customer(customer.customer_id)
        
        # Filter by specific order ID
        if order_id:
            orders = [order for order in orders if order.order_id == order_id]
        
        # Filter by status
        if status_filter:
            orders = [order for order in orders if order.status.lower() == status_filter.lower()]
        
        # Format response
        order_list = []
        for order in orders:
            order_info = {
                "order_id": order.order_id,
                "product_name": order.product_name,
                "order_date": order.order_date,
                "status": order.status,
                "amount": f"${order.amount:.2f}",
                "shipping_address": order.shipping_address,
                "tracking_number": order.tracking_number,
                "estimated_delivery": order.estimated_delivery
            }
            order_list.append(order_info)
        
        result = {
            "customer_name": customer.name,
            "total_orders": len(order_list),
            "orders": order_list
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        print(f"❌ Order search error: {str(e)}")
        raise e


@function_tool(
    name_override="search_support_tickets",
    description_override="Search customer support tickets and history",
    is_enabled=lambda ctx: getattr(ctx.context_variables.get('customer'), 'is_authenticated', False) if hasattr(ctx, 'context_variables') else False,
    error_function=handle_search_error
)
def search_support_tickets_tool(
    ctx: RunContextWrapper,
    customer_id: str = "",
    ticket_id: str = "",
    status_filter: str = "",
    include_history: bool = False
) -> str:
    """
    Search customer support tickets.
    
    Args:
        ctx: Context wrapper
        customer_id: Customer ID (optional if in context)
        ticket_id: Specific ticket ID
        status_filter: Filter by ticket status
        include_history: Include conversation history
        
    Returns:
        JSON formatted ticket information
    """
    print(f"🎫 Searching support tickets")
    
    try:
        # Get customer from context
        customer = ctx.context_variables.get('customer') if hasattr(ctx, 'context_variables') else None
        if not customer and customer_id:
            customer = get_customer_by_id(customer_id)
        
        if not customer or not customer.is_authenticated:
            return json.dumps({"error": "Customer authentication required"})
        
        # Get tickets
        tickets = get_tickets_by_customer(customer.customer_id)
        
        # Filter by specific ticket ID
        if ticket_id:
            tickets = [ticket for ticket in tickets if ticket.ticket_id == ticket_id]
        
        # Filter by status
        if status_filter:
            tickets = [ticket for ticket in tickets if ticket.status.value == status_filter]
        
        # Format response
        ticket_list = []
        for ticket in tickets:
            ticket_info = {
                "ticket_id": ticket.ticket_id,
                "title": ticket.title,
                "description": ticket.description,
                "status": ticket.status.value,
                "priority": ticket.priority.value,
                "category": ticket.category,
                "created_at": ticket.created_at,
                "updated_at": ticket.updated_at,
                "assigned_agent": ticket.assigned_agent,
                "resolution": ticket.resolution
            }
            
            if include_history and ticket.conversation_history:
                ticket_info["conversation_history"] = ticket.conversation_history
            
            ticket_list.append(ticket_info)
        
        result = {
            "customer_name": customer.name,
            "total_tickets": len(ticket_list),
            "tickets": ticket_list
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        print(f"❌ Ticket search error: {str(e)}")
        raise e


@function_tool(
    name_override="create_support_ticket",
    description_override="Create a new support ticket for the customer",
    is_enabled=lambda ctx: getattr(ctx.context_variables.get('customer'), 'is_authenticated', False) if hasattr(ctx, 'context_variables') else False,
    error_function=handle_ticket_error
)
def create_support_ticket_tool(
    ctx: RunContextWrapper,
    title: str,
    description: str,
    category: str,
    priority: str = "medium"
) -> str:
    """
    Create a new support ticket.
    
    Args:
        ctx: Context wrapper with customer info
        title: Ticket title
        description: Detailed description
        category: Ticket category
        priority: Priority level (low, medium, high, urgent, critical)
        
    Returns:
        JSON formatted ticket creation result
    """
    print(f"🎫 Creating new support ticket: {title}")
    
    try:
        customer = ctx.context_variables.get('customer') if hasattr(ctx, 'context_variables') else None
        
        if not customer or not customer.is_authenticated:
            return json.dumps({"error": "Customer authentication required"})
        
        # Convert priority string to enum
        try:
            priority_enum = TicketPriority(priority.lower())
        except ValueError:
            priority_enum = TicketPriority.MEDIUM
        
        # Create ticket
        new_ticket = create_new_ticket(
            customer_id=customer.customer_id,
            title=title,
            description=description,
            category=category,
            priority=priority_enum
        )
        
        # Determine if escalation is needed
        escalation_keywords = ["urgent", "critical", "emergency", "outage", "down", "not working"]
        needs_escalation = (
            priority_enum in [TicketPriority.URGENT, TicketPriority.CRITICAL] or
            any(keyword in description.lower() for keyword in escalation_keywords) or
            customer.tier.value in ["enterprise", "vip"]
        )
        
        result = {
            "ticket_created": True,
            "ticket": {
                "ticket_id": new_ticket.ticket_id,
                "title": new_ticket.title,
                "status": new_ticket.status.value,
                "priority": new_ticket.priority.value,
                "category": new_ticket.category,
                "created_at": new_ticket.created_at
            },
            "customer_tier": customer.tier.value,
            "escalation_recommended": needs_escalation,
            "next_steps": "Your ticket has been created and assigned a unique ID. You'll receive updates via email."
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        print(f"❌ Ticket creation error: {str(e)}")
        raise e


@function_tool(
    name_override="search_faq_knowledge",
    description_override="Search FAQ and knowledge base for answers",
    is_enabled=lambda ctx: True,  # Always available
    error_function=handle_search_error
)
def search_faq_knowledge_tool(
    ctx: RunContextWrapper,
    query: str,
    search_type: str = "both",
    category: str = ""
) -> str:
    """
    Search FAQ and knowledge base.
    
    Args:
        ctx: Context wrapper
        query: Search query
        search_type: Type of search ('faq', 'knowledge', 'both')
        category: Optional category filter
        
    Returns:
        JSON formatted search results
    """
    print(f"📚 Searching knowledge base: {query}")
    
    try:
        results = {
            "query": query,
            "search_type": search_type,
            "faq_results": [],
            "knowledge_results": []
        }
        
        # Search FAQ
        if search_type in ["faq", "both"]:
            faq_results = search_faq(query, category if category else None)
            for faq in faq_results[:3]:  # Limit to top 3 results
                results["faq_results"].append({
                    "question": faq.question,
                    "answer": faq.answer,
                    "category": FAQ_CATEGORIES.get(faq.category, faq.category),
                    "confidence": faq.confidence_threshold
                })
        
        # Search Knowledge Base
        if search_type in ["knowledge", "both"]:
            kb_results = search_knowledge_base(query, category if category else None)
            for article in kb_results[:2]:  # Limit to top 2 results
                results["knowledge_results"].append({
                    "title": article.title,
                    "content": article.content[:500] + "..." if len(article.content) > 500 else article.content,
                    "category": article.category,
                    "article_id": article.article_id
                })
        
        results["total_results"] = len(results["faq_results"]) + len(results["knowledge_results"])
        
        return json.dumps(results, indent=2)
        
    except Exception as e:
        print(f"❌ Knowledge search error: {str(e)}")
        raise e


@function_tool(
    name_override="escalate_to_human",
    description_override="Escalate conversation to human agent",
    is_enabled=lambda ctx: True,  # Always enabled for escalations
    error_function=lambda ctx, error: "I'm having trouble with the escalation process. Let me try again."
)
def escalate_to_human_tool(
    ctx: RunContextWrapper,
    reason: str,
    urgency: str = "normal",
    customer_context: str = ""
) -> HandoffToAgent:
    """
    Escalate conversation to human agent.
    
    Args:
        ctx: Context wrapper
        reason: Reason for escalation
        urgency: Urgency level (low, normal, high, critical)
        customer_context: Additional context for human agent
        
    Returns:
        HandoffToAgent object
    """
    print(f"🚨 Escalating to human agent: {reason}")
    
    try:
        customer = ctx.context_variables.get('customer') if hasattr(ctx, 'context_variables') else None
        
        escalation_message = f"""
ESCALATION FROM BOT AGENT

Reason: {reason}
Urgency: {urgency.upper()}
Timestamp: {datetime.now().isoformat()}

Customer Information:
- Name: {customer.name if customer else 'Not authenticated'}
- Tier: {customer.tier.value if customer else 'Unknown'}
- Customer ID: {customer.customer_id if customer else 'Unknown'}

Additional Context: {customer_context}

Please take over this conversation and assist the customer.
        """
        
        return HandoffToAgent(
            agent_name="human_support_agent",
            message=escalation_message.strip(),
            context_variables={
                "escalation_reason": reason,
                "urgency": urgency,
                "customer": customer,
                "escalated_at": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        print(f"❌ Escalation error: {str(e)}")
        # Fallback - still try to escalate
        return HandoffToAgent(
            agent_name="human_support_agent", 
            message=f"Bot escalation: {reason}",
            context_variables={"escalation_reason": reason}
        )
