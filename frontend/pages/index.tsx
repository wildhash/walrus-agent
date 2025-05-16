import { useState } from 'react'
import { useAccount } from 'wagmi'
import { ConnectButton } from '@rainbow-me/rainbowkit'

export default function Home() {
  const { address } = useAccount()
  const [messages, setMessages] = useState<{ from: 'user'|'agent'; text: string }[]>([])
  const [input, setInput] = useState('')

  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')

  const send = async () => {
    if (!input.trim()) return
    
    setMessages([...messages, { from: 'user', text: input }])
    setError('')
    setIsLoading(true)
    setInput('')
    
    try {
      // Fetch using POST with body data and get response as stream
      const response = await fetch('http://localhost:8001/chat/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: input })
      });

      // Create a new response message
      const agentIdx = messages.length;
      setMessages(msgs => [...msgs, { from: 'agent', text: '' }]);
      
      // Read the stream
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let responseText = '';
      
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        // Decode the chunk and process it
        const chunk = decoder.decode(value);
        const lines = chunk.split('\n\n');
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.substring(6);
            responseText += data;
            
            // Update the message
            setMessages(msgs => {
              const newMsgs = [...msgs];
              if (newMsgs[agentIdx]) {
                newMsgs[agentIdx] = { ...newMsgs[agentIdx], text: responseText };
              }
              return newMsgs;
            });
          }
        }
      }
      
      setIsLoading(false);
    } catch (err) {
      fallbackRequest()
    }
  }
  
  const fallbackRequest = async () => {
    try {
      const res = await fetch('http://localhost:8001/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: input }),
      }).then(r => r.json())
      setMessages(msgs => [...msgs, { from: 'agent', text: res.response }])
    } catch (err) {
      setError('Failed to connect to agent. Please check if the backend is running.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="h-screen flex flex-col">
      <header className="p-4 bg-gradient-to-r from-blue-700 to-blue-900 text-white flex justify-between items-center shadow-md">
        <h1 className="text-xl font-bold flex items-center">
          <span className="text-3xl mr-2">🦭</span> 
          Walrus on Base
        </h1>
        <ConnectButton />
      </header>
      <main className="flex-1 p-4 overflow-auto bg-gray-50">
        {messages.map((m, i) => (
          <div key={i} className={`my-3 ${m.from==='user'?'text-right':'text-left'}`}>
            <span className={`inline-block p-3 rounded-lg shadow-sm max-w-[80%] ${
              m.from==='user'
                ? 'bg-blue-600 text-white rounded-br-none'
                : 'bg-white border border-gray-200 rounded-bl-none'
            }`}>
              {m.text}
            </span>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-center my-4">
            <div className="animate-pulse flex space-x-2">
              <div className="w-2 h-2 bg-blue-600 rounded-full"></div>
              <div className="w-2 h-2 bg-blue-600 rounded-full"></div>
              <div className="w-2 h-2 bg-blue-600 rounded-full"></div>
            </div>
          </div>
        )}
        {error && (
          <div className="p-3 bg-red-100 text-red-800 rounded-lg my-3">
            {error}
          </div>
        )}
      </main>
      <footer className="p-4 flex border-t border-gray-200 bg-white shadow-inner">
        <input
          className="flex-1 border-2 border-gray-300 rounded-l-lg p-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          value={input}
          onChange={e=>setInput(e.target.value)}
          disabled={!address}
          placeholder={address ? 'Ask Walrus to perform onchain actions...' : 'Connect wallet to start chatting'}
          onKeyPress={e => e.key === 'Enter' && send()}
        />
        <button
          className={`px-6 py-3 rounded-r-lg font-medium flex items-center justify-center min-w-[100px] ${
            address 
              ? 'bg-blue-600 hover:bg-blue-700 text-white'
              : 'bg-gray-300 text-gray-500 cursor-not-allowed'
          }`}
          onClick={send}
          disabled={!address || isLoading}
        >
          {isLoading ? 'Sending...' : 'Send'}
        </button>
      </footer>
    </div>
  )
}
