import React, { useState } from 'react';
import { Bot, Send, ShieldCheck } from 'lucide-react';

export default function AiChat() {
  const [messages, setMessages] = useState([
    {
      sender: 'ai',
      text: 'Advisory Engine Ready. Ground-truth benchmark logs (Z24 SIMCES) & IRC-SP-35 inspection standards loaded. Ask any question about structural safety.'
    }
  ]);
  const [input, setInput] = useState('');

  const handleSend = (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMsg = input;
    setMessages(prev => [...prev, { sender: 'user', text: userMsg }]);
    setInput('');

    // Simulate RAG Assistant response
    setTimeout(() => {
      setMessages(prev => [
        ...prev,
        {
          sender: 'ai',
          text: `Retrieved Protocol [IRC-SP-35]: When fundamental bending frequency drops > 8%, schedule visual bearing inspection within 24h and enforce axle-load restrictions.`
        }
      ]);
    }, 600);
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col h-80">
      <div className="flex items-center gap-2 mb-3 border-b border-slate-800 pb-2">
        <Bot className="h-5 w-5 text-indigo-400" />
        <h2 className="text-base font-semibold text-slate-200">AI Structural Inspector (RAG)</h2>
      </div>

      <div className="flex-1 overflow-y-auto space-y-2.5 pr-1 text-xs">
        {messages.map((m, i) => (
          <div key={i} className={`p-2.5 rounded-lg ${m.sender === 'user' ? 'bg-blue-600/20 text-blue-200 ml-6 border border-blue-500/30' : 'bg-slate-800/60 text-slate-300 mr-4 border border-slate-700/50'}`}>
            <p className="font-semibold text-[10px] text-slate-400 mb-0.5">{m.sender === 'user' ? 'Engineer' : 'AI Assistant'}</p>
            {m.text}
          </div>
        ))}
      </div>

      <form onSubmit={handleSend} className="flex gap-2 mt-3 pt-2 border-t border-slate-800">
        <input 
          type="text" 
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about pier settlement or protocols..."
          className="flex-1 bg-slate-950 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 outline-none focus:border-blue-500"
        />
        <button type="submit" className="bg-blue-600 hover:bg-blue-500 text-white px-3 py-1.5 rounded-lg text-xs font-medium flex items-center gap-1 transition-colors">
          <Send className="h-3.5 w-3.5" />
        </button>
      </form>
    </div>
  );
}
