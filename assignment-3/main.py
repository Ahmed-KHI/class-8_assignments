"""
Assignment 3: Dynamic Instructions - Hotel Booking Agent
========================================================

This assignment demonstrates dynamic instruction generation based on user context.
The agent adapts its behavior, language, and priorities based on:
- User loyalty status (standard, silver, gold, platinum)
- Budget preferences (budget, mid-range, luxury)
- Previous booking history
- Personal preferences

Key Concepts Demonstrated:
✅ Dynamic instruction generation based on user context
✅ Context-aware agent behavior
✅ Personalized service levels
✅ Adaptive communication styles
✅ Hotel booking and search functionality

To run: uv run python main.py
"""

import google.generativeai as genai
from decouple import config
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json
import asyncio


@dataclass
class Hotel:
    """Hotel information model"""
    id: str
    name: str
    location: str
    description: str
    price_per_night: float
    available_rooms: int
    amenities: List[str]
    rating: float
    contact_email: str
    contact_phone: str


@dataclass
class UserContext:
    """User context for dynamic instruction generation"""
    name: str
    user_id: str
    preferred_location: Optional[str] = None
    budget_range: Optional[str] = "mid-range"  # "budget", "mid-range", "luxury"
    loyalty_status: str = "standard"  # "standard", "silver", "gold", "platinum"
    previous_bookings: List[str] = field(default_factory=list)
    preferences: List[str] = field(default_factory=list)


class DynamicInstructionsGenerator:
    """Generates dynamic instructions based on user context"""
    
    @staticmethod
    def generate_instructions(user_context: UserContext) -> str:
        """Generate personalized instructions based on user context"""
        
        base_instructions = f"""You are a professional hotel booking assistant helping {user_context.name}.

CORE RESPONSIBILITIES:
- Help search and book hotels
- Provide personalized recommendations
- Handle booking requests professionally
- Offer relevant amenities and services
"""
        
        loyalty_instructions = DynamicInstructionsGenerator._get_loyalty_instructions(user_context)
          
        budget_instructions = DynamicInstructionsGenerator._get_budget_instructions(user_context)
        
        preference_instructions = DynamicInstructionsGenerator._get_preference_instructions(user_context)
        
        communication_style = DynamicInstructionsGenerator._get_communication_style(user_context)
        
        full_instructions = f"""{base_instructions}

{loyalty_instructions}

{budget_instructions}

{preference_instructions}

{communication_style}

PERSONALIZATION CONTEXT:
- User: {user_context.name} ({user_context.loyalty_status.title()} member)
- Budget preference: {user_context.budget_range}
- Preferred location: {user_context.preferred_location or "Not specified"}
- Previous bookings: {len(user_context.previous_bookings)} hotels
- Special preferences: {', '.join(user_context.preferences) if user_context.preferences else "None"}

Always maintain a professional yet personalized approach based on this context."""

        return full_instructions
    
    @staticmethod
    def _get_loyalty_instructions(user_context: UserContext) -> str:
        """Generate loyalty-specific instructions"""
        loyalty_status = user_context.loyalty_status.lower()
        
        if loyalty_status == "platinum":
            return """PLATINUM MEMBER TREATMENT:
- Prioritize premium suites and luxury accommodations
- Offer complimentary upgrades and exclusive amenities
- Provide concierge-level service with detailed attention
- Mention exclusive platinum benefits and VIP services
- Use formal, respectful language acknowledging their status"""
            
        elif loyalty_status == "gold":
            return """GOLD MEMBER TREATMENT:
- Recommend higher-tier rooms with enhanced amenities
- Offer room upgrades when available
- Highlight gold member benefits and discounts
- Provide priority booking assistance
- Use professional, appreciative tone"""
            
        elif loyalty_status == "silver":
            return """SILVER MEMBER TREATMENT:
- Acknowledge silver status and available benefits
- Suggest mid-range to upper-mid-range options
- Mention member discounts and perks
- Provide attentive, helpful service"""
            
        else:  # standard
            return """STANDARD MEMBER TREATMENT:
- Provide excellent basic service to all guests
- Focus on value and meeting their specific needs
- Suggest ways to earn loyalty points
- Maintain friendly, professional assistance"""
    
    @staticmethod
    def _get_budget_instructions(user_context: UserContext) -> str:
        """Generate budget-specific instructions"""
        budget = user_context.budget_range.lower()
        
        if budget == "luxury":
            return """LUXURY BUDGET APPROACH:
- Prioritize 4-5 star hotels and premium properties
- Emphasize exclusive amenities and exceptional service
- Don't hesitate to recommend high-end options
- Focus on unique experiences and luxury features"""
            
        elif budget == "mid-range":
            return """MID-RANGE BUDGET APPROACH:
- Balance quality and value in recommendations
- Suggest 3-4 star hotels with good amenities
- Highlight value-for-money options
- Consider both comfort and reasonable pricing"""
            
        else:  # budget
            return """BUDGET-CONSCIOUS APPROACH:
- Focus on affordable options without compromising safety
- Highlight budget-friendly hotels with essential amenities
- Emphasize value, deals, and cost savings
- Suggest money-saving tips and alternatives"""
    
    @staticmethod
    def _get_preference_instructions(user_context: UserContext) -> str:
        """Generate preference-based instructions"""
        if not user_context.preferences:
            return "PREFERENCES: No specific preferences noted. Ask about preferences to personalize service."
        
        prefs_text = ", ".join(user_context.preferences)
        return f"""PREFERENCE-BASED SERVICE:
- User preferences: {prefs_text}
- Prioritize hotels that match these specific preferences
- Mention relevant amenities that align with their interests
- Actively filter recommendations based on these preferences"""
    
    @staticmethod
    def _get_communication_style(user_context: UserContext) -> str:
        """Generate communication style based on context"""
        loyalty = user_context.loyalty_status.lower()
        
        if loyalty == "platinum":
            return """COMMUNICATION STYLE:
- Use formal, respectful language ("Mr./Ms. [Name]")
- Demonstrate expertise and exclusivity
- Be concise but comprehensive
- Show appreciation for their valued membership"""
            
        elif loyalty in ["gold", "silver"]:
            return """COMMUNICATION STYLE:
- Professional yet warm and personable
- Acknowledge their membership benefits
- Be helpful and informative
- Show appreciation for their loyalty"""
            
        else:
            return """COMMUNICATION STYLE:
- Friendly, helpful, and approachable
- Focus on being informative and supportive
- Encourage engagement and questions
- Build rapport to encourage future loyalty"""


class HotelDatabase:
    """Hotel database with sample data"""
    
    @staticmethod
    def get_hotels() -> Dict[str, Hotel]:
        """Get sample hotel data"""
        return {
            "hotel_001": Hotel(
                id="hotel_001",
                name="Grand Palace Hotel",
                location="New York City",
                description="Luxury hotel in Manhattan with world-class amenities",
                price_per_night=350.00,
                available_rooms=25,
                amenities=["spa", "pool", "gym", "restaurant", "room_service", "wifi", "parking"],
                rating=4.8,
                contact_email="reservations@grandpalace.com",
                contact_phone="+1-555-0101"
            ),
            "hotel_002": Hotel(
                id="hotel_002",
                name="Budget Inn Downtown",
                location="New York City", 
                description="Clean, affordable accommodation in downtown area",
                price_per_night=89.00,
                available_rooms=40,
                amenities=["wifi", "parking", "24h-front-desk"],
                rating=3.9,
                contact_email="info@budgetinn.com",
                contact_phone="+1-555-0102"
            ),
            "hotel_003": Hotel(
                id="hotel_003",
                name="Seaside Resort & Spa",
                location="Miami Beach",
                description="Beachfront resort with spa and premium amenities",
                price_per_night=280.00,
                available_rooms=60,
                amenities=["beach-access", "spa", "pool", "restaurant", "wifi", "pet-friendly"],
                rating=4.6,
                contact_email="bookings@seasideresort.com",
                contact_phone="+1-555-0103"
            ),
            "hotel_004": Hotel(
                id="hotel_004",
                name="Business Center Hotel",
                location="Chicago",
                description="Modern hotel designed for business travelers",
                price_per_night=195.00,
                available_rooms=80,
                amenities=["business-center", "gym", "wifi", "restaurant", "parking"],
                rating=4.2,
                contact_email="corporate@businesscenter.com",
                contact_phone="+1-555-0104"
            )
        }


class HotelBookingTools:
    """Hotel booking and search tools"""
    
    def __init__(self, hotels_db: Dict[str, Hotel]):
        self.hotels_db = hotels_db
    
    def search_hotels(self, user_context: UserContext, location: str = "", max_price: float = 1000.0, 
                     min_rating: float = 0.0, required_amenities: List[str] = None) -> List[Dict]:
        """Search hotels based on criteria and user context"""
        required_amenities = required_amenities or []
        
        print(f"🔍 Searching hotels for {user_context.name} ({user_context.loyalty_status})")
        
        if not location and user_context.preferred_location:
            location = user_context.preferred_location
        
        if user_context.budget_range == "budget" and max_price > 150:
            max_price = 150
        elif user_context.budget_range == "mid-range" and max_price > 300:
            max_price = 300
        
        results = []
        for hotel in self.hotels_db.values():
            
            if location and location.lower() not in hotel.location.lower():
                continue
            
            if hotel.price_per_night > max_price:
                continue
            
            if hotel.rating < min_rating:
                continue
            
            if required_amenities:
                hotel_amenities = [a.lower() for a in hotel.amenities]
                if not all(req.lower() in hotel_amenities for req in required_amenities):
                    continue
            
            preference_score = 0
            for pref in user_context.preferences:
                if pref.lower() in [a.lower() for a in hotel.amenities]:
                    preference_score += 1
            
            results.append({
                "hotel": hotel,
                "preference_score": preference_score
            })
        
        results.sort(key=lambda x: (x["preference_score"], x["hotel"].rating), reverse=True)
        
        return [r["hotel"] for r in results]
    
    def get_hotel_details(self, hotel_id: str) -> Optional[Hotel]:
        """Get detailed hotel information"""
        return self.hotels_db.get(hotel_id)
    
    def make_reservation(self, user_context: UserContext, hotel_id: str, 
                        check_in: str, check_out: str, guests: int) -> Dict:
        """Make a hotel reservation"""
        hotel = self.hotels_db.get(hotel_id)
        if not hotel:
            return {"success": False, "message": "Hotel not found"}
        
        if hotel.available_rooms < 1:
            return {"success": False, "message": "No rooms available"}
        
        discount = 0
        if user_context.loyalty_status == "platinum":
            discount = 0.20  # 20% discount
        elif user_context.loyalty_status == "gold":
            discount = 0.15  # 15% discount
        elif user_context.loyalty_status == "silver":
            discount = 0.10  # 10% discount
        
        final_price = hotel.price_per_night * (1 - discount)
        
        reservation_id = f"RES-{user_context.user_id}-{hotel_id}-{datetime.now().strftime('%Y%m%d')}"
        
        return {
            "success": True,
            "reservation_id": reservation_id,
            "hotel_name": hotel.name,
            "check_in": check_in,
            "check_out": check_out,
            "guests": guests,
            "original_price": hotel.price_per_night,
            "discount": discount,
            "final_price": final_price,
            "loyalty_savings": hotel.price_per_night * discount
        }


class DynamicInstructionHotelAgent:
    """Hotel booking agent with dynamic instructions"""
    
    def __init__(self):
        """Initialize the agent"""
        try:
            gemini_api_key = str(config("GEMINI_API_KEY"))
            genai.configure(api_key=gemini_api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            
            self.instructions_generator = DynamicInstructionsGenerator()
            self.hotels_db = HotelDatabase.get_hotels()
            self.booking_tools = HotelBookingTools(self.hotels_db)
            
            print("✅ Dynamic Instruction Hotel Agent initialized!")
            self.initialized = True
            
        except Exception as e:
            print(f"❌ Initialization error: {e}")
            self.initialized = False
    
    async def process_user_request(self, user_context: UserContext, user_message: str) -> str:
        """Process user request with dynamic instructions"""
        
        if not self.initialized:
            return "❌ Agent not properly initialized"
        
        print(f"\n🔄 Processing request for {user_context.name} ({user_context.loyalty_status})")
        print(f"💬 Request: {user_message}")
        
        dynamic_instructions = self.instructions_generator.generate_instructions(user_context)
        
        print(f"🎯 Generated dynamic instructions for {user_context.loyalty_status} member")
        
        tools_used = []
        
        if any(keyword in user_message.lower() for keyword in ['search', 'find', 'look for', 'hotels']):
            search_results = self.booking_tools.search_hotels(user_context)
            tools_used.append(f"Hotel search results: {len(search_results)} hotels found")
            
            hotel_info = "\n".join([
                f"- {hotel.name} in {hotel.location}: ${hotel.price_per_night}/night, Rating: {hotel.rating}/5"
                for hotel in search_results[:5]  # Limit to top 5
            ])
        else:
            hotel_info = "Use search functionality to find specific hotels"
        
        try:
            prompt = f"""{dynamic_instructions}

CURRENT USER REQUEST: "{user_message}"

AVAILABLE HOTEL INFORMATION:
{hotel_info}

TOOLS USED: {', '.join(tools_used) if tools_used else 'None'}

Provide a helpful, personalized response that:
1. Addresses their specific request
2. Uses the appropriate communication style for their loyalty status
3. Considers their budget and preferences
4. Offers relevant hotel recommendations if applicable
5. Maintains the personalized service level appropriate for their context

Response:"""

            response = self.model.generate_content(prompt)
            generated_response = response.text
            
            print(f"✅ Response generated using {user_context.loyalty_status}-tier instructions")
            return generated_response
            
        except Exception as e:
            return f"Error generating personalized response: {str(e)}"


async def demonstrate_dynamic_instructions():
    """Demonstrate how instructions change based on user context"""
    
    print("🎯 Assignment 3: Dynamic Instructions Demonstration")
    print("=" * 60)
    print("This demo shows how agent instructions adapt based on user context")
    print("=" * 60)
    
    agent = DynamicInstructionHotelAgent()
    
    if not agent.initialized:
        print("❌ Failed to initialize agent")
        return
    
    users = [
        UserContext(
            name="John Smith",
            user_id="user_001",
            loyalty_status="standard",
            budget_range="budget",
            preferred_location="New York City",
            preferences=["wifi", "parking"]
        ),
        UserContext(
            name="Sarah Johnson",
            user_id="user_002", 
            loyalty_status="gold",
            budget_range="mid-range",
            preferred_location="Miami Beach",
            preferences=["spa", "pool", "beach-access"]
        ),
        UserContext(
            name="Robert Williams",
            user_id="user_003",
            loyalty_status="platinum",
            budget_range="luxury",
            preferred_location="New York City",
            preferences=["spa", "restaurant", "room_service"]
        )
    ]
    
    test_message = "I'm looking for a hotel for my upcoming business trip. Can you help me find something suitable?"
    
    for i, user in enumerate(users, 1):
        print(f"\n{'='*70}")
        print(f"🧪 TEST CASE {i}: {user.loyalty_status.title()} Member")
        print(f"User: {user.name}")
        print(f"Loyalty Status: {user.loyalty_status}")
        print(f"Budget Range: {user.budget_range}")
        print(f"Preferred Location: {user.preferred_location}")
        print(f"Preferences: {', '.join(user.preferences)}")
        print("="*70)
        
        instructions = agent.instructions_generator.generate_instructions(user)
        print(f"\n🎯 DYNAMIC INSTRUCTIONS PREVIEW:")
        print("-" * 50)
        print(instructions[:200] + "..." if len(instructions) > 200 else instructions)
        print("-" * 50)
        
        response = await agent.process_user_request(user, test_message)
        
        print(f"\n📝 PERSONALIZED RESPONSE:")
        print("─" * 50)
        print(response)
        print("─" * 50)
        
        if i < len(users):
            print(f"\n⏳ Moving to next user context...")
            await asyncio.sleep(2)


async def interactive_mode():
    """Interactive mode for testing with custom user context"""
    print("🏨 Assignment 3: Interactive Hotel Booking Agent")
    print("=" * 55)
    print("Experience dynamic instructions based on your profile!")
    print("=" * 55)
    
    agent = DynamicInstructionHotelAgent()
    
    if not agent.initialized:
        print("❌ Failed to initialize agent")
        return
    
    print("\n👤 Let's set up your profile for personalized service:")
    name = input("Enter your name: ").strip()
    
    print("\nLoyalty Status:")
    print("1. Standard")
    print("2. Silver")
    print("3. Gold") 
    print("4. Platinum")
    loyalty_choice = input("Select your loyalty status (1-4): ").strip()
    loyalty_map = {"1": "standard", "2": "silver", "3": "gold", "4": "platinum"}
    loyalty_status = loyalty_map.get(loyalty_choice, "standard")
    
    print("\nBudget Preference:")
    print("1. Budget-conscious")
    print("2. Mid-range")
    print("3. Luxury")
    budget_choice = input("Select your budget preference (1-3): ").strip()
    budget_map = {"1": "budget", "2": "mid-range", "3": "luxury"}
    budget_range = budget_map.get(budget_choice, "mid-range")
    
    preferred_location = input("Preferred location (optional): ").strip() or None
    
    user_context = UserContext(
        name=name,
        user_id=f"user_{hash(name) % 10000}",
        loyalty_status=loyalty_status,
        budget_range=budget_range,
        preferred_location=preferred_location,
        preferences=["wifi", "pool"] if loyalty_status in ["gold", "platinum"] else ["wifi"]
    )
    
    print(f"\n✅ Profile created! You are a {loyalty_status.title()} member with {budget_range} preferences.")
    print(f"🎯 The agent will now personalize its service based on your profile.")
    print("\nType 'quit' to exit")
    
    while True:
        try:
            user_input = input(f"\n💬 {name}, what can I help you with? ")
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Thank you for using our hotel booking service!")
                break
            
            if not user_input.strip():
                print("❌ Please enter a valid request.")
                continue
            
            print("\n⏳ Generating personalized response...")
            response = await agent.process_user_request(user_context, user_input)
            
            print(f"\n🏨 Hotel Assistant:")
            print("─" * 50)
            print(response)
            print("─" * 50)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


async def main():
    """Main application entry point"""
    print("🚀 Assignment 3: Dynamic Instructions - Hotel Booking Agent")
    print("This demonstrates how agent instructions adapt based on user context")
    print("including loyalty status, budget preferences, and personal preferences.")
    print()
    
    try:
        print("Select mode:")
        print("1. Interactive mode (personalized hotel assistant)")
        print("2. Demo mode (show dynamic instruction examples)")
        choice = input("Enter choice (1 or 2): ").strip()
        
        if choice == "2":
            await demonstrate_dynamic_instructions()
        else:
            await interactive_mode()
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Application error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
