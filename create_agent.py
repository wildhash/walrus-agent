from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from coinbase_agentkit_langchain import get_langchain_tools

from prepare_agentkit import prepare_agentkit

"""
Agent Framework Integration

This file bridges your AgentKit configuration with your chosen AI framework 
(Langchain or OpenAI Assistants). It handles:

1. LLM Configuration:
   - Select and configure your Language Model

2. Tool Integration:
   - Convert AgentKit tools to framework-compatible format
   - Configure tool availability and permissions

3. Agent Creation:
   - Initialize the agent with tools and instructions
   - Set up memory and conversation management

The create_agent() function returns a configured agent ready for use in your application.
"""

# Shared agent instructions specialized for wallet API
AGENT_INSTRUCTIONS = (
    "You are Walrus, an AI assistant that helps users perform onchain actions using Coinbase's AgentKit. "
    "You can help users manage their smart wallets, check balances, request testnet funds, make transfers, "
    "and interact with Base Sepolia. Be concise, helpful, and focus on onchain actions. "
    "Always explain what you're doing and why. When users ask you to perform actions, execute them confidently "
    "and explain the results in simple terms. Remember you're assisting non-technical users with blockchain interactions."
)

def create_agent():
    """Initialize the agent with tools from AgentKit."""
    # Get AgentKit instance
    agentkit = prepare_agentkit()

    
    # Initialize LLM
    llm = ChatOpenAI(model="gpt-4o-mini")

    # Get Langchain tools
    tools = get_langchain_tools(agentkit)
    
    # Store buffered conversation history in memory
    memory = MemorySaver()
    
    config = {"configurable": {"thread_id": "Smart Wallet Chatbot"}}
    

    # Create ReAct Agent using the LLM and CDP Agentkit tools
    return create_react_agent(
        llm,
        tools=tools,
        checkpointer=memory,
        state_modifier=AGENT_INSTRUCTIONS,
    ), config

     