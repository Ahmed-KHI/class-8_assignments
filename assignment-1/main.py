"""
Assignment 1: Custom Web Search Tool with Native Gemini
Using Google's official Generative AI SDK + Tavily API

This implementation provides:
- Native Gemini integration (no OpenAI compatibility issues)
- Tavily web search functionality
- Real-time information retrieval
- Clean, direct API calls
"""

import google.generativeai as genai
from tavily import TavilyClient
from decouple import config
import asyncio
import json


class WebSearchAgent:
    def __init__(self):
        """Initialize the web search agent with native Gemini and Tavily"""
        try:
            self.gemini_api_key = str(config("GEMINI_API_KEY"))
            genai.configure(api_key=self.gemini_api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            
            self.tavily_api_key = str(config("TAVILY_API_KEY"))
            self.tavily_client = TavilyClient(api_key=self.tavily_api_key)
            
            print("✅ Web Search Agent initialized successfully!")
            print(f"🤖 Gemini Model: gemini-1.5-flash")
            print(f"🔍 Tavily API: Ready")
            
        except Exception as e:
            raise Exception(f"Failed to initialize agent: {str(e)}")
    
    async def search_and_respond(self, user_query: str) -> str:
        """Main method: Search web and generate response"""
        try:
            print(f"🔍 Searching for: {user_query}")
            
            search_results = await self._web_search(user_query)
            
            response = await self._generate_response(user_query, search_results)
            
            return response
            
        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}"
    
    async def _web_search(self, query: str) -> dict:
        """Perform web search using Tavily API"""
        try:
            response = self.tavily_client.search(
                query=query,
                search_depth="basic",
                max_results=5,
                include_answer=True
            )
            
            return {
                "success": True,
                "query": query,
                "answer": response.get("answer", ""),
                "results": response.get("results", [])
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "query": query
            }
    
    async def _generate_response(self, user_query: str, search_data: dict) -> str:
        """Generate response using Gemini with search context"""
        try:
            if search_data["success"]:
                
                context = f"User Query: {user_query}\n\n"
                
                if search_data.get("answer"):
                    context += f"Summary: {search_data['answer']}\n\n"
                
                context += "Detailed Results:\n"
                for i, result in enumerate(search_data.get("results", [])[:3], 1):
                    context += f"{i}. {result.get('title', 'No title')}\n"
                    context += f"   Source: {result.get('url', 'No URL')}\n"
                    content = result.get('content', '')[:300]
                    context += f"   Content: {content}{'...' if len(content) >= 300 else ''}\n\n"
                
                prompt = f"""Based on the web search results below, provide a comprehensive and helpful response to the user's question.

{context}

Instructions:
- Use the search results to provide accurate, up-to-date information
- Synthesize information from multiple sources when relevant
- Be conversational and helpful
- Include key facts and details from the search results
- If appropriate, mention sources or provide context about the information

Provide a detailed response to: {user_query}"""
                
            else:
                prompt = f"""I encountered an issue with the web search: {search_data.get('error', 'Unknown error')}

However, I can still try to help with your question: {user_query}

Please provide what information you can based on your general knowledge, and mention that the web search was not available for the most current information."""
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"I was able to search the web for '{user_query}' but encountered an issue generating the response: {str(e)}"


async def main():
    """Main application loop"""
    print("🌐 Assignment 1: Custom Web Search Tool")
    print("=" * 60)
    print("This tool combines Gemini AI with Tavily web search for real-time information!")
    print()
    print("Try queries like:")
    print("  - 'What's the latest news about AI?'")
    print("  - 'Current weather in New York'")
    print("  - 'Recent developments in quantum computing'")
    print("  - 'Latest cryptocurrency prices'")
    print("=" * 60)
    
    try:
        agent = WebSearchAgent()
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        print("Please check your API keys in the .env file")
        return
    
    while True:
        try:
            user_query = input("\n💬 Enter your search query (or 'quit' to exit): ")
            
            if user_query.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not user_query.strip():
                print("❌ Please enter a valid query.")
                continue
            
            print("\n⏳ Processing...")
            response = await agent.search_and_respond(user_query)
            
            print("\n📝 Response:")
            print("-" * 50)
            print(response)
            print("-" * 50)
            
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {str(e)}")
            print("Please try again with a different query.")


def demo_mode():
    """Run demo scenarios automatically"""
    async def run_demos():
        print("🎯 Running Demo Mode...")
        print("=" * 50)
        
        demo_queries = [
            "What are the latest developments in AI?",
            "Current stock market trends today",
            "Recent news about climate change"
        ]
        
        try:
            agent = WebSearchAgent()
            
            for i, query in enumerate(demo_queries, 1):
                print(f"\n📍 Demo {i}: {query}")
                print("⏳ Processing...")
                
                response = await agent.search_and_respond(query)
                
                print(f"\n📝 Response:")
                print("-" * 40)
                print(response[:500] + "..." if len(response) > 500 else response)
                print("-" * 40)
                
                if i < len(demo_queries):
                    await asyncio.sleep(2)  # Pause between demos
                    
        except Exception as e:
            print(f"❌ Demo failed: {e}")
    
    return run_demos()


if __name__ == "__main__":
    print("🚀 Starting Assignment 1: Custom Web Search Tool")
    
    mode = input("Choose mode: [1] Interactive [2] Demo scenarios (1/2): ").strip()
    
    if mode == "2":
        asyncio.run(demo_mode())
    else:
        asyncio.run(main())
