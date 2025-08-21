import os
import sys
import time

from langchain_core.messages import HumanMessage

from dotenv import load_dotenv

from create_agent import create_agent

"""
AgentKit Chatbot Interface

This file provides a command-line interface for interacting with your AgentKit-powered AI agent.
It supports two modes of operation:

1. Chat Mode:
   - Interactive conversations with the agent
   - Direct user input and agent responses

2. Autonomous Mode:
   - Agent operates independently
   - Performs periodic blockchain interactions
   - Useful for automated tasks or monitoring

Use this as a starting point for building your own agent interface or integrate
the agent into your existing applications.

# Want to contribute?
Join us in shaping AgentKit! Check out the contribution guide:  
- https://github.com/coinbase/agentkit/blob/main/CONTRIBUTING.md
- https://discord.gg/CDP
"""

load_dotenv()


# Autonomous Mode
def run_autonomous_mode(agent_executor, config, interval=10):
    """Run the agent autonomously with specified intervals."""
    print("Starting autonomous mode...")
    while True:
        try:
            # Provide instructions autonomously
            thought = (
                "Be creative and do something interesting on the blockchain. "
                "Choose an action or set of actions and execute it that highlights your abilities."
            )

            # Run agent in autonomous mode
            for chunk in agent_executor.stream(
                {"messages": [HumanMessage(content=thought)]}, config
            ):
                msg = chunk.get("agent") or chunk.get("tools")
                if msg and msg.get("messages"):
                    print(msg["messages"][0].content)
                print("-------------------")

            # Wait before the next action
            time.sleep(interval)

        except KeyboardInterrupt:
            print("Goodbye Agent!")
            sys.exit(0)


# Chat Mode
def run_chat_mode(agent_executor, config):
    """Run the agent interactively based on user input."""
    print("Starting chat mode... Type 'exit' to end.")
    while True:
        try:
            user_input = input("\nPrompt: ")
            if user_input.lower() == "exit":
                break

            # Run agent with the user's input in chat mode
            for chunk in agent_executor.stream(
                {"messages": [HumanMessage(content=user_input)]}, config
            ):
                msg = chunk.get("agent") or chunk.get("tools")
                if msg and msg.get("messages"):
                    print(msg["messages"][0].content)
                print("-------------------")

        except KeyboardInterrupt:
            print("Goodbye Agent!")
            sys.exit(0)


# Mode Selection
def choose_mode():
    """Choose whether to run in autonomous or chat mode based on user input."""
    while True:
        print("\nAvailable modes:")
        print("1. chat    - Interactive chat mode")
        print("2. auto    - Autonomous action mode")

        choice = input("\nChoose a mode (enter number or name): ").lower().strip()
        if choice in ["1", "chat"]:
            return "chat"
        elif choice in ["2", "auto"]:
            return "auto"
        print("Invalid choice. Please try again.")


def main():

    """Start the chatbot agent."""
    agent_executor, config = create_agent()

    # Allow non-interactive mode selection via env or CLI
    mode = None
    if len(sys.argv) > 1:
        mode = sys.argv[1].strip().lower()
    if mode not in ("chat", "auto"):
        mode = os.getenv("AGENT_MODE")
    if mode not in ("chat", "auto"):
        mode = choose_mode()
    if mode == "chat":
        run_chat_mode(agent_executor=agent_executor, config=config)
    elif mode == "auto":
        interval = int(os.getenv("AUTO_INTERVAL_SECONDS", "10"))
        run_autonomous_mode(agent_executor=agent_executor, config=config, interval=interval)

if __name__ == "__main__":
    print("Starting Agent...")
    
    main()
    
