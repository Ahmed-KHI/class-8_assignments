"""
Assignment 2: Math Agent with Guardrails (Native Gemini Implementation)

This implementation demonstrates:
- Input guardrails (filtering non-math queries)
- Output guardrails (filtering inappropriate responses)
- Math tools integration
- Clean native Gemini approach
"""

import google.generativeai as genai
from decouple import config
import asyncio
import math
import re
from typing import Dict, Any, List


class GuardrailViolation(Exception):
    """Exception raised when a guardrail is violated"""
    pass


class MathGuardrails:
    """Guardrails for input and output filtering"""
    
    @staticmethod
    def input_math_only_guardrail(user_input: str) -> bool:
        """
        Input guardrail that only allows math-related queries.
        Returns True if input passes, False if blocked.
        """
        user_input_lower = user_input.lower()
        
        math_keywords = [
            'calculate', 'compute', 'solve', 'equation', 'formula', 'math', 'mathematics',
            'algebra', 'geometry', 'calculus', 'statistics', 'arithmetic', 'derivative',
            'integral', 'fraction', 'percentage', 'ratio', 'proportion', 'graph', 'plot',
            'function', 'variable', 'coefficient', 'polynomial', 'linear', 'quadratic',
            'exponential', 'logarithm', 'trigonometry', 'sine', 'cosine', 'tangent',
            'sum', 'product', 'difference', 'quotient', 'square', 'root', 'power',
            'angle', 'triangle', 'circle', 'rectangle', 'area', 'volume', 'perimeter'
        ]
        
        math_symbols = ['+', '-', '*', '/', '=', '(', ')', '^', '²', '³', '√', '∑', '∫', 'π', 'x', 'y']
        
        has_math_keywords = any(keyword in user_input_lower for keyword in math_keywords)
        
        has_math_symbols = any(symbol in user_input for symbol in math_symbols)
        
        has_numbers = bool(re.search(r'\d', user_input))
        
        return has_math_keywords or has_math_symbols or has_numbers
    
    @staticmethod
    def input_inappropriate_content_guardrail(user_input: str) -> bool:
        """
        Input guardrail that blocks inappropriate content.
        Returns True if input passes, False if blocked.
        """
        user_input_lower = user_input.lower()
        
        inappropriate_keywords = [
            'violence', 'hate', 'harm', 'illegal', 'drugs', 'explicit', 'offensive'
        ]
        
        return not any(keyword in user_input_lower for keyword in inappropriate_keywords)
    
    @staticmethod
    def output_political_content_guardrail(response: str) -> bool:
        """
        Output guardrail that filters political content.
        Returns True if output passes, False if blocked.
        """
        response_lower = response.lower()
        
        political_keywords = [
            'president', 'election', 'vote', 'political', 'politics', 'democrat', 'republican',
            'government', 'congress', 'senate', 'politician', 'campaign', 'policy', 'law'
        ]
        
        return not any(keyword in response_lower for keyword in political_keywords)
    
    @staticmethod
    def output_length_guardrail(response: str, max_length: int = 500) -> bool:
        """
        Output guardrail that limits response length.
        Returns True if output passes, False if blocked.
        """
        return len(response) <= max_length


class MathTools:
    """Math calculation tools"""
    
    @staticmethod
    def calculate(expression: str) -> str:
        """Perform mathematical calculations safely"""
        try:
            print(f"🔢 Calculating: {expression}")
            
            expression = expression.replace("^", "**")  # Replace ^ with ** for power
            expression = re.sub(r'[^0-9+\-*/().\s]', '', expression)  # Remove non-math characters
            
            allowed_names = {
                "__builtins__": {},
                "abs": abs, "round": round, "min": min, "max": max,
                "sum": sum, "pow": pow, "sqrt": math.sqrt, "sin": math.sin,
                "cos": math.cos, "tan": math.tan, "log": math.log, "pi": math.pi
            }
            
            result = eval(expression, allowed_names)
            return f"Result: {result}"
            
        except Exception as e:
            return f"Calculation error: {str(e)}"
    
    @staticmethod
    def solve_equation(equation: str) -> str:
        """Provide help with solving equations"""
        try:
            print(f"📐 Solving equation: {equation}")
            
            if "x" in equation.lower():
                return f"To solve '{equation}', isolate x by performing inverse operations on both sides."
            else:
                return f"For equation '{equation}', identify the unknown variable and use algebraic principles."
                
        except Exception as e:
            return f"Equation solving error: {str(e)}"


class MathAgentWithGuardrails:
    """Math agent with comprehensive guardrails"""
    
    def __init__(self):
        """Initialize the math agent with Gemini"""
        try:
            self.gemini_api_key = str(config("GEMINI_API_KEY"))
            genai.configure(api_key=self.gemini_api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            
            self.math_tools = MathTools()
            self.guardrails = MathGuardrails()
            
            print("✅ Math Agent with Guardrails initialized successfully!")
            print("🛡️ Guardrails: Input filtering + Output filtering")
            print("🔢 Math Tools: Ready")
            
        except Exception as e:
            raise Exception(f"Failed to initialize math agent: {str(e)}")
    
    async def process_query(self, user_input: str) -> str:
        """Process user query with guardrails"""
        try:
            print(f"\n🔍 Processing: {user_input}")
            
            print("🛡️ Checking input guardrails...")
            
            if not self.guardrails.input_math_only_guardrail(user_input):
                return "🚫 Input blocked: This assistant only responds to mathematics-related queries. Please ask a math question!"
            
            if not self.guardrails.input_inappropriate_content_guardrail(user_input):
                return "🚫 Input blocked: Inappropriate content detected. Please ask a respectful math question!"
            
            print("✅ Input guardrails passed")
            
            response = await self._generate_math_response(user_input)
            
            print("🛡️ Checking output guardrails...")
            
            if not self.guardrails.output_political_content_guardrail(response):
                return "🚫 Output blocked: Response contained political content. Let me focus on the mathematical aspects of your question."
            
            if not self.guardrails.output_length_guardrail(response):
                response = response[:450] + "... [Response truncated for brevity]"
            
            print("✅ Output guardrails passed")
            
            return response
            
        except Exception as e:
            return f"Error processing query: {str(e)}"
    
    async def _generate_math_response(self, user_input: str) -> str:
        """Generate math response using Gemini and tools"""
        try:
            if any(op in user_input for op in ['+', '-', '*', '/', '=', 'calculate']):
                
                calculation_result = self.math_tools.calculate(user_input)
                
                prompt = f"""You are a mathematics assistant. The user asked: "{user_input}"

I performed this calculation: {calculation_result}

Provide a helpful mathematical response that:
1. Explains the calculation if relevant
2. Shows the result clearly
3. Provides any additional mathematical context
4. Stays focused only on mathematics
5. Avoids any political or inappropriate topics

Keep the response concise and educational."""
                
            elif "solve" in user_input.lower() and any(var in user_input.lower() for var in ['x', 'y', 'equation']):
                
                equation_help = self.math_tools.solve_equation(user_input)
                
                prompt = f"""You are a mathematics assistant. The user asked: "{user_input}"

I provided this equation solving guidance: {equation_help}

Provide a helpful mathematical response that:
1. Explains the equation solving process
2. Shows step-by-step approach if possible
3. Provides mathematical principles involved
4. Stays focused only on mathematics
5. Avoids any political or inappropriate topics

Keep the response educational and clear."""
                
            else:
                prompt = f"""You are a mathematics assistant. The user asked: "{user_input}"

Provide a helpful mathematical response that:
1. Answers their math question directly
2. Explains relevant mathematical concepts
3. Shows examples or steps if helpful
4. Stays focused only on mathematics
5. Avoids any political or inappropriate topics

Keep the response educational and concise."""
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"I encountered an issue generating the math response: {str(e)}"


async def main():
    """Main application loop"""
    print("🧮 Assignment 2: Math Agent with Guardrails")
    print("=" * 60)
    print("This agent demonstrates input and output guardrails for a math assistant.")
    print()
    print("Features:")
    print("  🛡️ Input Guardrails: Only accepts math-related queries")
    print("  🚫 Content Filtering: Blocks inappropriate content")
    print("  🔒 Output Guardrails: Filters political content and length")
    print("  🔢 Math Tools: Calculations and equation solving")
    print("=" * 60)
    
    try:
        agent = MathAgentWithGuardrails()
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        return
    
    while True:
        try:
            user_input = input("\n💬 Enter your math question (or 'quit' to exit): ")
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not user_input.strip():
                print("❌ Please enter a valid question.")
                continue
            
            print("\n⏳ Processing with guardrails...")
            response = await agent.process_query(user_input)
            
            print("\n📝 Response:")
            print("-" * 50)
            print(response)
            print("-" * 50)
            
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {str(e)}")


async def demo_guardrails():
    """Demonstrate guardrails with test cases"""
    print("🎯 Guardrails Demo Mode")
    print("=" * 50)
    
    test_cases = [
        ("What is 2 + 2?", "✅ Valid math query"),
        ("How do I solve x + 5 = 10?", "✅ Valid math query"),  
        ("What's the weather today?", "❌ Should be blocked (not math)"),
        ("Tell me about politics", "❌ Should be blocked (not math)"),
        ("Calculate the area of a circle with radius 5", "✅ Valid math query"),
    ]
    
    try:
        agent = MathAgentWithGuardrails()
        
        for i, (query, expected) in enumerate(test_cases, 1):
            print(f"\n📍 Test {i}: {query}")
            print(f"Expected: {expected}")
            print("⏳ Processing...")
            
            response = await agent.process_query(query)
            print(f"📝 Response: {response[:100]}...")
            
            await asyncio.sleep(1)  # Pause between tests
            
    except Exception as e:
        print(f"❌ Demo failed: {e}")


if __name__ == "__main__":
    print("🚀 Starting Assignment 2: Math Agent with Guardrails")
    
    mode = input("Choose mode: [1] Interactive [2] Demo guardrails (1/2): ").strip()
    
    if mode == "2":
        asyncio.run(demo_guardrails())
    else:
        asyncio.run(main())
