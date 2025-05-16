#!/usr/bin/env python
import os
import time
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from create_agent import create_agent

"""
Demo script for the Coinbase Smart Wallet API Agent.
This will guide the agent through a series of wallet API operations:
 1. Retrieve the smart wallet address
 2. Check the wallet's EVM balance
 3. Create a new account via the wallet API
"""

def run_demo(agent_executor, config):
    print("=== Coinbase Smart Wallet API Agent Demo ===")
    # Load demo destination address from environment (optional)
    dest_address = os.getenv("DEMO_DEST_ADDRESS")
    steps = [
        "Retrieve smart wallet address",
        "Check the wallet's EVM balance",
        "Generate a new smart wallet account",
        "Request testnet ETH from faucet",
    ]
    # Add transfer step only if destination is provided
    if dest_address:
        steps.append(f"Send 0.001 ETH to {dest_address}")
    else:
        print("Warning: DEMO_DEST_ADDRESS not set; skipping transfer step.")
    for step in steps:
        print(f"\n>> Step: {step}")
        for chunk in agent_executor.stream({"messages": [HumanMessage(content=step)]}, config):
            if "tools" in chunk:
                print(chunk["tools"]["messages"][0].content)
            elif "agent" in chunk:
                print(chunk["agent"]["messages"][0].content)
            print("---")
        time.sleep(1)


def main():
    load_dotenv()
    agent_executor, config = create_agent()
    run_demo(agent_executor, config)


if __name__ == "__main__":
    main()
