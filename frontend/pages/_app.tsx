import '../styles/globals.css'
import { WagmiConfig, createClient, configureChains, Chain } from 'wagmi'
import { mainnet } from 'wagmi/chains'
import { publicProvider } from 'wagmi/providers/public'
import { RainbowKitProvider, getDefaultWallets } from '@rainbow-me/rainbowkit'
import '@rainbow-me/rainbowkit/styles.css'

// Base testnet config
const baseSepolia: Chain = {
  id: 84531,
  name: 'Base Sepolia',
  network: 'base-sepolia',
  rpcUrls: { default: 'https://rpc.sepolia.base.org' },
  nativeCurrency: { name: 'ETH', symbol: 'ETH', decimals: 18 },
  blockExplorers: { default: { name: 'BaseScan', url: 'https://sepolia.basescan.org' } },
}

const { chains, provider } = configureChains([baseSepolia, mainnet], [publicProvider()])
const { connectors } = getDefaultWallets({ appName: 'Walrus', chains })
const wagmiClient = createClient({ autoConnect: true, connectors, provider })

function MyApp({ Component, pageProps }) {
  return (
    <WagmiConfig client={wagmiClient}>
      <RainbowKitProvider chains={chains}>
        <Component {...pageProps} />
      </RainbowKitProvider>
    </WagmiConfig>
  )
}

export default MyApp
