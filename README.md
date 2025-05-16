# 🦭 Walrus - AI-Powered Onchain Actions, Simplified

This is a Python chatbot project bootstrapped with `create-onchain-agent`.  
It integrates [AgentKit](https://github.com/coinbase/agentkit) to provide AI-driven interactions with on-chain capabilities.

## 🌟 Features

- **Intuitive Chat Interface** - Talk to your wallet like you'd talk to a friend
- **Smart Wallet Integration** - Seamlessly interact with Coinbase's Smart Wallet API
- **Token Management** - Check balances and transfer tokens with simple commands
- **Real-time Updates** - Stream responses as they're generated
- **Base Sepolia Compatible** - Built specifically for the Base ecosystem

## Prerequisites

Before using `create-onchain-agent`, ensure you have the following installed:

- **Python** (3.10 - 3.12) – [Download here](https://www.python.org/downloads/)
- **Poetry** (latest version) – [Installation guide](https://python-poetry.org/docs/#installation)

## Getting Started

First, install dependencies:

`poetry install`

Then, configure your environment variables:

```sh
mv .env.local .env
```

Finally, run the chatbot:

`poetry run python chatbot.py`


## Configuring Your Agent

You can [modify your agent configuration](https://github.com/coinbase/agentkit/tree/main/typescript/agentkit#usage) in the `chatbot.py` file.

### 1. Select Your LLM  
Modify the `ChatOpenAI` instantiation to use the model of your choice.

### 2. Select Your Wallet Provider  
AgentKit requires a **Wallet Provider** to interact with blockchain networks.

### 3. Select Your Action Providers  
Action Providers define what your agent can do. You can use built-in providers or create your own.

## Demo Usage
The `demo.py` script walks the agent through key Wallet API operations:

1. Retrieve the smart wallet address
2. Check the wallet's EVM balance
3. Generate a new smart wallet account
4. Request testnet ETH from the faucet
5. (Optional) Send ETH to a destination address

### Environment Variables
Create a `.env` file in this directory with the following keys:
```properties
OPENAI_API_KEY=your_openai_api_key
CDP_API_KEY_NAME=your_cdp_api_key_name
CDP_API_KEY_PRIVATE_KEY=your_cdp_api_private_key
PRIVATE_KEY=your_ethereum_private_key
NETWORK=base-sepolia
DEMO_DEST_ADDRESS=optional_destination_address
```

### Running the Demo
Install dependencies and run:
```pwsh
poetry install
poetry run python demo.py
```

### Starting the Chat Agent
Use the provided script to launch the interactive chatbot:
```pwsh
poetry run start-agent
```

---

## Next Steps

- Explore the AgentKit README: [AgentKit Documentation](https://github.com/coinbase/agentkit)
- Learn more about available Wallet Providers & Action Providers.
- Experiment with custom Action Providers for your specific use case.

## Learn More

- [Learn more about CDP](https://docs.cdp.coinbase.com/)
- [Learn more about AgentKit](https://docs.cdp.coinbase.com/agentkit/docs/welcome)

## Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed instructions on deploying Walrus to production.

## Base Batches Submission

Walrus is our submission for Base Batches in the AI category. It demonstrates how AI agents can simplify blockchain interactions using AgentKit and other Coinbase developer platform tools.

**Key innovations:**
- Conversational interface for wallet management
- Streaming responses for real-time feedback
- Elegant, intuitive UI for both technical and non-technical users
- Full integration with Base Sepolia for all onchain actions


## Contributing

Interested in contributing to AgentKit? Follow the contribution guide:

- [Contribution Guide](https://github.com/coinbase/agentkit/blob/main/CONTRIBUTING.md)
- Join the discussion on [Discord](https://discord.gg/CDP)
