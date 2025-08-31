from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass 
class FAQItem:
    """FAQ item model"""
    question: str
    answer: str
    category: str
    tags: List[str]
    confidence_threshold: float = 0.7


@dataclass
class KnowledgeArticle:
    """Knowledge base article model"""
    article_id: str
    title: str
    content: str
    category: str
    subcategory: str
    tags: List[str]
    last_updated: str
    view_count: int = 0


# FAQ Database
FAQ_DATABASE = [
    FAQItem(
        question="How do I reset my password?",
        answer="To reset your password:\n1. Go to the login page\n2. Click 'Forgot Password'\n3. Enter your email address\n4. Check your email for reset instructions\n5. Follow the link and create a new password\n\nIf you don't receive the email within 10 minutes, check your spam folder or contact support.",
        category="account_management",
        tags=["password", "reset", "login", "account"],
        confidence_threshold=0.8
    ),
    FAQItem(
        question="What payment methods do you accept?",
        answer="We accept the following payment methods:\n- Credit Cards (Visa, MasterCard, American Express)\n- Debit Cards\n- PayPal\n- Bank Transfer (for Enterprise customers)\n- Apple Pay and Google Pay\n\nAll payments are processed securely and we don't store your payment information.",
        category="billing_payments",
        tags=["payment", "billing", "credit card", "paypal"],
        confidence_threshold=0.8
    ),
    FAQItem(
        question="How can I upgrade my plan?",
        answer="To upgrade your plan:\n1. Log into your account\n2. Go to 'Billing & Plans' in settings\n3. Select 'Upgrade Plan'\n4. Choose your desired plan\n5. Complete the payment process\n\nUpgrades take effect immediately. You'll be prorated for the current billing period.",
        category="billing_upgrades",
        tags=["upgrade", "plan", "billing", "subscription"],
        confidence_threshold=0.8
    ),
    FAQItem(
        question="How do I cancel my subscription?",
        answer="To cancel your subscription:\n1. Log into your account\n2. Go to 'Billing & Plans'\n3. Click 'Cancel Subscription'\n4. Confirm your cancellation\n\nYou'll retain access until your current billing period ends. No refunds for partial months.",
        category="billing_cancellation", 
        tags=["cancel", "subscription", "billing", "refund"],
        confidence_threshold=0.8
    ),
    FAQItem(
        question="What is your refund policy?",
        answer="Our refund policy:\n- 30-day money-back guarantee for new customers\n- No refunds for partial months on subscriptions\n- Enterprise customers: Custom refund terms in contract\n- Refunds processed within 5-10 business days\n\nTo request a refund, contact our billing team with your order details.",
        category="billing_refunds",
        tags=["refund", "money back", "billing", "policy"],
        confidence_threshold=0.9
    ),
    FAQItem(
        question="How do I contact technical support?",
        answer="You can reach technical support through:\n- Live Chat (available 24/7)\n- Email: support@company.com\n- Phone: 1-800-SUPPORT (Premium/Enterprise customers)\n- Support Portal: Submit detailed tickets\n\nResponse times:\n- VIP/Enterprise: 1 hour\n- Premium: 4 hours\n- Basic: 24 hours",
        category="support_contact",
        tags=["contact", "support", "help", "chat", "email", "phone"],
        confidence_threshold=0.8
    ),
    FAQItem(
        question="Is my data secure?",
        answer="Yes, your data security is our top priority:\n- End-to-end encryption for all data\n- SOC 2 Type II certified infrastructure\n- GDPR and CCPA compliant\n- Regular security audits\n- 99.9% uptime guarantee\n\nWe never sell or share your personal data with third parties.",
        category="security_privacy",
        tags=["security", "privacy", "data", "encryption", "compliance"],
        confidence_threshold=0.9
    ),
    FAQItem(
        question="What browsers are supported?",
        answer="We support all modern browsers:\n- Chrome 90+ (recommended)\n- Firefox 88+\n- Safari 14+\n- Edge 90+\n- Opera 76+\n\nFor the best experience, keep your browser updated. Some features may not work on older versions.",
        category="technical_requirements",
        tags=["browser", "compatibility", "technical", "requirements"],
        confidence_threshold=0.8
    ),
    FAQItem(
        question="How do I integrate with your API?",
        answer="To integrate with our API:\n1. Generate API key in your dashboard\n2. Read our API documentation\n3. Use our SDK (available for Python, Node.js, PHP)\n4. Test in our sandbox environment\n5. Deploy to production\n\nAPI documentation: https://docs.company.com/api\nRate limits apply based on your plan.",
        category="technical_integration",
        tags=["api", "integration", "sdk", "documentation", "developer"],
        confidence_threshold=0.8
    ),
    FAQItem(
        question="What are your service hours?",
        answer="Our service availability:\n- Platform: 24/7/365 with 99.9% uptime\n- Chat Support: 24/7 for all customers\n- Phone Support: Business hours (Premium/Enterprise)\n- Email Support: Responses within SLA timeframes\n\nMaintenance windows are scheduled during low-usage periods with advance notice.",
        category="service_hours",
        tags=["hours", "availability", "uptime", "maintenance", "support"],
        confidence_threshold=0.8
    )
]


# Knowledge Base Articles
KNOWLEDGE_BASE = {
    "KB_001": KnowledgeArticle(
        article_id="KB_001",
        title="Getting Started with Our Platform",
        content="""
# Getting Started Guide

Welcome to our platform! This comprehensive guide will help you get up and running quickly.

## Initial Setup
1. **Account Creation**: Sign up with your email and create a strong password
2. **Email Verification**: Check your email and verify your account
3. **Profile Setup**: Complete your profile with business information
4. **Plan Selection**: Choose the plan that best fits your needs

## First Steps
1. **Dashboard Overview**: Familiarize yourself with the main dashboard
2. **Settings Configuration**: Set up your preferences and notifications
3. **Team Invitation**: Add team members if applicable
4. **Integration Setup**: Connect with your existing tools

## Best Practices
- Use strong, unique passwords
- Enable two-factor authentication
- Regularly backup your data
- Keep your profile information updated

## Need Help?
- Check our FAQ section
- Contact support via chat or email
- Schedule a demo call for personalized onboarding
        """,
        category="onboarding",
        subcategory="getting_started", 
        tags=["setup", "onboarding", "getting started", "guide"],
        last_updated="2024-01-01",
        view_count=1250
    ),
    "KB_002": KnowledgeArticle(
        article_id="KB_002",
        title="API Authentication and Security",
        content="""
# API Authentication Guide

Our API uses secure authentication methods to protect your data and ensure authorized access.

## Authentication Methods
1. **API Keys**: Simple authentication for basic usage
2. **OAuth 2.0**: Secure delegated access for applications
3. **JWT Tokens**: Stateless authentication with expiration

## Getting Your API Key
1. Log into your dashboard
2. Navigate to 'API Settings'
3. Click 'Generate New Key'
4. Copy and securely store your key

## Making Authenticated Requests
```bash
curl -H "Authorization: Bearer YOUR_API_KEY" https://api.company.com/v1/data
```

## Security Best Practices
- Never expose API keys in client-side code
- Use environment variables for key storage
- Rotate keys regularly
- Monitor API usage for unusual activity

## Rate Limits
- Basic: 1,000 requests/hour
- Premium: 10,000 requests/hour
- Enterprise: Custom limits available

## Error Handling
- 401: Unauthorized (invalid key)
- 403: Forbidden (insufficient permissions)
- 429: Rate limit exceeded
        """,
        category="technical",
        subcategory="api_authentication",
        tags=["api", "authentication", "security", "oauth", "jwt"],
        last_updated="2024-01-15",
        view_count=856
    ),
    "KB_003": KnowledgeArticle(
        article_id="KB_003",
        title="Troubleshooting Common Issues",
        content="""
# Troubleshooting Guide

This guide covers the most common issues users encounter and their solutions.

## Login Issues
**Problem**: Can't log into account
**Solutions**:
- Check if Caps Lock is on
- Clear browser cache and cookies
- Try incognito/private browsing mode
- Reset password if needed

## Performance Issues
**Problem**: Platform running slowly
**Solutions**:
- Check your internet connection
- Close unused browser tabs
- Disable browser extensions temporarily
- Try a different browser

## Integration Problems
**Problem**: API calls failing
**Solutions**:
- Verify API key is correct
- Check rate limit status
- Ensure proper authentication headers
- Review API documentation for changes

## Data Sync Issues
**Problem**: Data not updating
**Solutions**:
- Refresh the page
- Check sync settings
- Verify permissions
- Contact support if persistent

## Browser Compatibility
**Problem**: Features not working
**Solutions**:
- Update to latest browser version
- Enable JavaScript
- Disable ad blockers temporarily
- Check our supported browsers list

## Need More Help?
If these solutions don't resolve your issue:
1. Check our FAQ section
2. Search the knowledge base
3. Contact our support team
4. Provide detailed error descriptions
        """,
        category="troubleshooting",
        subcategory="common_issues",
        tags=["troubleshooting", "issues", "problems", "solutions", "help"],
        last_updated="2024-01-20",
        view_count=2100
    )
}


def search_faq(query: str, category: Optional[str] = None) -> List[FAQItem]:
    """
    Search FAQ database for relevant items.
    
    Args:
        query: Search query
        category: Optional category filter
        
    Returns:
        List of matching FAQ items
    """
    query_lower = query.lower()
    matching_faqs = []
    
    for faq in FAQ_DATABASE:
        # Category filter
        if category and faq.category != category:
            continue
            
        # Search in question, answer, and tags
        if (query_lower in faq.question.lower() or 
            query_lower in faq.answer.lower() or
            any(query_lower in tag.lower() for tag in faq.tags)):
            matching_faqs.append(faq)
    
    return matching_faqs


def search_knowledge_base(query: str, category: Optional[str] = None) -> List[KnowledgeArticle]:
    """
    Search knowledge base for relevant articles.
    
    Args:
        query: Search query
        category: Optional category filter
        
    Returns:
        List of matching knowledge base articles
    """
    query_lower = query.lower()
    matching_articles = []
    
    for article in KNOWLEDGE_BASE.values():
        # Category filter
        if category and article.category != category:
            continue
            
        # Search in title, content, and tags
        if (query_lower in article.title.lower() or
            query_lower in article.content.lower() or
            any(query_lower in tag.lower() for tag in article.tags)):
            matching_articles.append(article)
    
    # Sort by view count (popularity)
    matching_articles.sort(key=lambda x: x.view_count, reverse=True)
    return matching_articles


def get_faq_by_category(category: str) -> List[FAQItem]:
    """Get all FAQs in a specific category"""
    return [faq for faq in FAQ_DATABASE if faq.category == category]


def get_knowledge_articles_by_category(category: str) -> List[KnowledgeArticle]:
    """Get all knowledge base articles in a specific category"""
    return [article for article in KNOWLEDGE_BASE.values() if article.category == category]


# Category mapping for better organization
FAQ_CATEGORIES = {
    "account_management": "Account & Profile Management",
    "billing_payments": "Billing & Payments", 
    "billing_upgrades": "Plan Upgrades",
    "billing_cancellation": "Subscription Cancellation",
    "billing_refunds": "Refunds & Returns",
    "support_contact": "Contact Information",
    "security_privacy": "Security & Privacy",
    "technical_requirements": "Technical Requirements",
    "technical_integration": "API & Integrations",
    "service_hours": "Service Availability"
}

KNOWLEDGE_BASE_CATEGORIES = {
    "onboarding": "Getting Started & Onboarding",
    "technical": "Technical Documentation", 
    "troubleshooting": "Troubleshooting & Support"
}
