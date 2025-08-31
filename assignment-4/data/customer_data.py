from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class TicketStatus(Enum):
    """Ticket status enumeration"""
    OPEN = "open"
    IN_PROGRESS = "in_progress" 
    WAITING_CUSTOMER = "waiting_customer"
    RESOLVED = "resolved"
    CLOSED = "closed"
    ESCALATED = "escalated"


class TicketPriority(Enum):
    """Ticket priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"
    CRITICAL = "critical"


class CustomerTier(Enum):
    """Customer tier levels"""
    BASIC = "basic"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"
    VIP = "vip"


@dataclass
class Customer:
    """Customer information model"""
    customer_id: str
    name: str
    email: str
    phone: str
    tier: CustomerTier
    account_since: str
    is_authenticated: bool = False
    previous_tickets: List[str] = None
    preferences: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.previous_tickets is None:
            self.previous_tickets = []
        if self.preferences is None:
            self.preferences = {}


@dataclass
class SupportTicket:
    """Support ticket model"""
    ticket_id: str
    customer_id: str
    title: str
    description: str
    status: TicketStatus
    priority: TicketPriority
    category: str
    created_at: str
    updated_at: str
    assigned_agent: Optional[str] = None
    resolution: Optional[str] = None
    tags: List[str] = None
    conversation_history: List[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.conversation_history is None:
            self.conversation_history = []


@dataclass
class Order:
    """Order information model"""
    order_id: str
    customer_id: str
    product_name: str
    order_date: str
    status: str
    amount: float
    shipping_address: str
    tracking_number: Optional[str] = None
    estimated_delivery: Optional[str] = None

CUSTOMERS_DATABASE = {
    "CUST_001": Customer(
        customer_id="CUST_001",
        name="Alice Johnson",
        email="alice.johnson@email.com",
        phone="+1-555-0101",
        tier=CustomerTier.VIP,
        account_since="2022-01-15",
        is_authenticated=True,
        previous_tickets=["TICK_001", "TICK_005"],
        preferences={"communication": "email", "language": "en", "timezone": "EST"}
    ),
    "CUST_002": Customer(
        customer_id="CUST_002", 
        name="Bob Chen",
        email="bob.chen@company.com",
        phone="+1-555-0202",
        tier=CustomerTier.ENTERPRISE,
        account_since="2021-06-20",
        is_authenticated=True,
        previous_tickets=["TICK_002", "TICK_007", "TICK_012"],
        preferences={"communication": "phone", "language": "en", "timezone": "PST"}
    ),
    "CUST_003": Customer(
        customer_id="CUST_003",
        name="Carol Smith",
        email="carol.smith@email.com", 
        phone="+1-555-0303",
        tier=CustomerTier.PREMIUM,
        account_since="2023-03-10",
        is_authenticated=True,
        previous_tickets=["TICK_003"],
        preferences={"communication": "chat", "language": "en", "timezone": "CST"}
    ),
    "CUST_004": Customer(
        customer_id="CUST_004",
        name="David Wilson",
        email="david.wilson@email.com",
        phone="+1-555-0404", 
        tier=CustomerTier.BASIC,
        account_since="2023-08-05",
        is_authenticated=False,
        previous_tickets=[],
        preferences={"communication": "email", "language": "en", "timezone": "EST"}
    )
}

TICKETS_DATABASE = {
    "TICK_001": SupportTicket(
        ticket_id="TICK_001",
        customer_id="CUST_001",
        title="Cannot access premium features",
        description="I'm unable to access the premium features I paid for. Getting error 'Access Denied'.",
        status=TicketStatus.RESOLVED,
        priority=TicketPriority.HIGH,
        category="account_access",
        created_at="2024-01-15T10:30:00Z",
        updated_at="2024-01-15T14:45:00Z",
        assigned_agent="AGENT_HUMAN_001",
        resolution="Account permissions updated. Premium features restored.",
        tags=["premium", "access", "billing"],
        conversation_history=[
            {"timestamp": "2024-01-15T10:30:00Z", "agent": "bot", "message": "I understand you're having trouble accessing premium features. Let me check your account."},
            {"timestamp": "2024-01-15T10:35:00Z", "agent": "human", "message": "I see the issue. Your premium subscription is active but permissions weren't properly set. Let me fix this now."}
        ]
    ),
    "TICK_002": SupportTicket(
        ticket_id="TICK_002",
        customer_id="CUST_002",
        title="Integration API returning 500 errors",
        description="Our integration with your API has been returning 500 Internal Server Error since yesterday. This is affecting our production systems.",
        status=TicketStatus.IN_PROGRESS,
        priority=TicketPriority.CRITICAL,
        category="technical_integration",
        created_at="2024-01-20T09:15:00Z", 
        updated_at="2024-01-20T11:30:00Z",
        assigned_agent="AGENT_HUMAN_002",
        tags=["api", "integration", "500_error", "production"],
        conversation_history=[
            {"timestamp": "2024-01-20T09:15:00Z", "agent": "bot", "message": "I see you're experiencing API errors. This requires immediate technical assistance."},
            {"timestamp": "2024-01-20T09:20:00Z", "agent": "human", "message": "I'm escalating this to our API engineering team. We're investigating the 500 errors affecting your integration."}
        ]
    ),
    "TICK_003": SupportTicket(
        ticket_id="TICK_003", 
        customer_id="CUST_003",
        title="How to upgrade my plan?",
        description="I'd like to upgrade from Premium to Enterprise. What are the steps and pricing?",
        status=TicketStatus.CLOSED,
        priority=TicketPriority.MEDIUM,
        category="billing_upgrades",
        created_at="2024-01-18T16:20:00Z",
        updated_at="2024-01-18T16:45:00Z",
        assigned_agent="AGENT_BOT_001", 
        resolution="Provided upgrade information and initiated plan change process.",
        tags=["upgrade", "premium_to_enterprise", "billing"],
        conversation_history=[
            {"timestamp": "2024-01-18T16:20:00Z", "agent": "bot", "message": "I can help you upgrade to Enterprise! Let me explain the benefits and pricing."},
            {"timestamp": "2024-01-18T16:25:00Z", "agent": "bot", "message": "Enterprise plan includes unlimited API calls, priority support, and dedicated account manager for $299/month."}
        ]
    )
}

ORDERS_DATABASE = {
    "ORD_001": Order(
        order_id="ORD_001",
        customer_id="CUST_001", 
        product_name="Premium Software License (1 Year)",
        order_date="2024-01-10",
        status="delivered",
        amount=599.99,
        shipping_address="123 Main St, Boston, MA 02101",
        tracking_number="TRACK123456789",
        estimated_delivery="2024-01-12"
    ),
    "ORD_002": Order(
        order_id="ORD_002",
        customer_id="CUST_002",
        product_name="Enterprise API Package", 
        order_date="2024-01-18",
        status="processing",
        amount=2999.99,
        shipping_address="456 Corporate Blvd, San Francisco, CA 94102",
        tracking_number=None,
        estimated_delivery="2024-01-25"
    ),
    "ORD_003": Order(
        order_id="ORD_003",
        customer_id="CUST_003",
        product_name="Premium Upgrade Package",
        order_date="2024-01-19",
        status="shipped", 
        amount=199.99,
        shipping_address="789 Oak Ave, Chicago, IL 60601",
        tracking_number="TRACK987654321",
        estimated_delivery="2024-01-22"
    )
}


def get_customer_by_id(customer_id: str) -> Optional[Customer]:
    """Get customer by ID"""
    return CUSTOMERS_DATABASE.get(customer_id)


def get_customer_by_email(email: str) -> Optional[Customer]:
    """Get customer by email"""
    for customer in CUSTOMERS_DATABASE.values():
        if customer.email.lower() == email.lower():
            return customer
    return None


def get_tickets_by_customer(customer_id: str) -> List[SupportTicket]:
    """Get all tickets for a customer"""
    return [ticket for ticket in TICKETS_DATABASE.values() 
            if ticket.customer_id == customer_id]


def get_orders_by_customer(customer_id: str) -> List[Order]:
    """Get all orders for a customer"""
    return [order for order in ORDERS_DATABASE.values() 
            if order.customer_id == customer_id]


def create_new_ticket(customer_id: str, title: str, description: str, 
                     category: str, priority: TicketPriority = TicketPriority.MEDIUM) -> SupportTicket:
    """Create a new support ticket"""
    ticket_id = f"TICK_{len(TICKETS_DATABASE) + 1:03d}"
    timestamp = datetime.now().isoformat() + "Z"
    
    new_ticket = SupportTicket(
        ticket_id=ticket_id,
        customer_id=customer_id,
        title=title,
        description=description,
        status=TicketStatus.OPEN,
        priority=priority,
        category=category,
        created_at=timestamp,
        updated_at=timestamp
    )
    
    TICKETS_DATABASE[ticket_id] = new_ticket
    return new_ticket
