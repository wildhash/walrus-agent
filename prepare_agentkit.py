import os
import json
import secrets
from dotenv import load_dotenv

from coinbase_agentkit import (
    AgentKit,
    AgentKitConfig,
    
    SmartWalletProvider,
    SmartWalletProviderConfig,
    
    cdp_api_action_provider,
    erc20_action_provider,
    pyth_action_provider,
    wallet_action_provider,
    weth_action_provider,
)

from eth_account import Account


"""
AgentKit Configuration

This file serves as the entry point for configuring AgentKit tools and wallet providers.
It handles wallet setup, persistence, and initializes AgentKit with the appropriate providers.

# Key Steps to Configure AgentKit:

1. Set up your WalletProvider:
   - Learn more: https://github.com/coinbase/agentkit/tree/main/python/agentkit#evm-wallet-providers

2. Set up your Action Providers:
   - Action Providers define what your agent can do.  
   - Choose from built-in providers or create your own:
     - Built-in: https://github.com/coinbase/agentkit/tree/main/python/coinbase-agentkit#create-an-agentkit-instance-with-specified-action-providers
     - Custom: https://github.com/coinbase/agentkit/tree/main/python/coinbase-agentkit#creating-an-action-provider

# Next Steps:

- Explore the AgentKit README: https://github.com/coinbase/agentkit
- Learn more about available WalletProviders & Action Providers.
- Experiment with custom Action Providers for your unique use case.

## Want to contribute?
Join us in shaping AgentKit! Check out the contribution guide:  
- https://github.com/coinbase/agentkit/blob/main/CONTRIBUTING.md
- https://discord.gg/CDP
"""

# Configure a file to persist wallet data
wallet_data_file = os.getenv("WALLET_DATA_FILE", "wallet_data.txt")

def prepare_agentkit():
    """Initialize Smart Wallet Provider and return tools."""

    # Ensure environment variables are loaded when used as a library
    load_dotenv()

    
    # Load wallet data from JSON file
    wallet_data = {
        "private_key": None,
        "smart_wallet_address": None
    }
    if os.path.exists(wallet_data_file):
        try:
            with open(wallet_data_file) as f:
                wallet_data = json.load(f)
        except json.JSONDecodeError:
            print("Warning: Invalid wallet data file format. Creating new wallet.")
    
    # Use private key from env if not in wallet data
    private_key = wallet_data.get("private_key") or os.getenv("PRIVATE_KEY")
    
    if not private_key:
        # Generate new private key if none exists
        private_key = "0x" + secrets.token_hex(32)
        print("Created new private key and saved to wallet_data.txt")
        print("We recommend you save this private key to your .env file and delete wallet_data.txt afterwards.")

    signer = Account.from_key(private_key)

    # Initialize Smart Wallet Provider
    network_id = os.getenv("NETWORK", "base-sepolia")
    paymaster_url = os.getenv("PAYMASTER_URL") or None

    wallet_provider = SmartWalletProvider(SmartWalletProviderConfig(
        network_id=network_id,
        signer=signer,
        smart_wallet_address=wallet_data.get("smart_wallet_address"),
        paymaster_url=paymaster_url,
    ))
    
    # Save both private key and smart wallet address
    wallet_data = {
        "private_key": private_key,
        "smart_wallet_address": wallet_provider.get_address()
    }
    with open(wallet_data_file, "w") as f:
        json.dump(wallet_data, f, indent=2)

    

    # Initialize AgentKit
    # Only include core CDP Wallet API and wallet actions
    # Allow optional provider toggles via env
    enable_erc20 = os.getenv("ENABLE_ERC20", "1") not in ("0", "false", "False")
    enable_pyth = os.getenv("ENABLE_PYTH", "1") not in ("0", "false", "False")

    action_providers = [
        cdp_api_action_provider(),
        wallet_action_provider(),
    ]
    if enable_erc20:
        action_providers.append(erc20_action_provider())
    if enable_pyth:
        action_providers.append(pyth_action_provider())

    agentkit = AgentKit(AgentKitConfig(
        wallet_provider=wallet_provider,
        action_providers=action_providers,
    ))

    

    return agentkit