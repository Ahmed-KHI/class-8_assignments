# Assignment 1: Custom Web Search Tool

A web search tool that combines Google's Gemini AI with Tavily web search API to provide real-time information retrieval and intelligent responses.

## Features

- 🤖 **Native Gemini Integration**: Uses Google's official Generative AI SDK
- 🔍 **Web Search**: Real-time information retrieval via Tavily API
- 📰 **News Search**: Specialized news search functionality
- 🎯 **Interactive Mode**: Command-line interface for queries
- 🎪 **Demo Mode**: Pre-configured scenarios for testing

## Setup

1. **Install Dependencies**:
   ```bash
   uv add google-generativeai tavily-python python-decouple
   ```

2. **Configure API Keys**:
   The `.env` file is already configured with working API keys.

3. **Run the Application**:
   ```bash
   uv run python main.py
   ```

## Usage

### Interactive Mode
```bash
python main.py
# Choose option [1] for interactive mode
```

### Demo Mode
```bash
python main.py
# Choose option [2] for demo scenarios
```

## Architecture

```
assignment-1/
├── main.py                 # Main application with native Gemini
├── tools/
│   └── web_search_tools.py # Tavily API integration
├── .env                    # API keys configuration
└── README.md              # This file
```

## Assignment Objectives ✅

- ✅ **Explore Tavily API**: Implemented web search and news search
- ✅ **Simple search tool**: Clean, functional implementation
- ✅ **AI agent integration**: Gemini AI processes and responds with search context
- ✅ **Real-time information**: Live web search results

## Example Queries

- "What's the latest news about AI?"
- "Current weather in New York"
- "Recent developments in quantum computing"
- "Latest cryptocurrency prices"
- "Stock market trends today"

## Technical Implementation

### Web Search Flow
1. User enters query
2. Tavily API searches the web for relevant information
3. Gemini AI processes search results and generates response
4. Formatted response displayed to user

### Key Components
- **WebSearchAgent**: Main class orchestrating search and response generation
- **WebSearchTools**: Tavily API wrapper for web and news searches
- **Native Integration**: Direct Google SDK usage (no compatibility issues)

This is a clean, working implementation that eliminates all API compatibility issues by using native SDKs.
