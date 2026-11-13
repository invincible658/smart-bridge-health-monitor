import React, { useState, useEffect } from 'react';
import { Bot, Send, FileText, Sparkles } from 'lucide-react';
import { fetchAdvisory, sendChatMessage } from '../api';

export default function AiChat({ segmentId, anomalyScore = -0.42, shapSummary = '', topChannels = [14, 15] }) {
  const [advisory, setAdvisory] = useState(null);
  const [messages, setMessages] = useState([
    {
      sender: 'ai',
      text: 'Advisory Engine online. ChromaDB knowledge base loaded with 11 Z24 progressive damage ground-truth records and IRC-SP-35 / FHWA maintenance guidelines.'
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  // Fetch synthesized advisory when segment changes
  useEffect(() => {
    fetchAdvisory(segmentId, anomalyScore, shapSummary, topChannels, 'Threshold breach predicted in 5 steps')
      .then(res => setAdvisory(res))
      .catch(err => console.error('Failed to fetch advisory:', err));
  }, [segmentId, anomalyScore, shapSummary]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userText = input;
    setInput('');
    setMessages(prev => [...prev, { sender: 'user', text: userText }]);
    setLoading(true);

    try {
      const res = await sendChatMessage(userText);
      setMessages(prev => [...prev, { sender: 'ai', text: res.reply }]);
    } catch (err) {
      setMessages(prev => [...prev, { sender: 'ai', text: 'Error connecting to RAG advisory service.' }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col h-[400px]">
      <div className="flex items-center justify-between mb-3 border-b border-slate-800 pb-2">
        <div className="flex items-center gap-2">
          <Bot className="h-5 w-5 text-indigo-400" />
          <h2 className="text-base font-semibold text-slate-100">AI Inspector & RAG Advisory</h2>
        </div>
        <span className="text-[10px] text-indigo-300 bg-indigo-950/80 border border-indigo-800 px-2 py-0.5 rounded flex items-center gap-1">
          <Sparkles className="h-3 w-3" /> ChromaDB + LLM
        </span>
      </div>

      {/* RAG Generated Advisory Memo Preview */}
      {advisory && (
        <div className="bg-slate-950/80 border border-slate-800 rounded-lg p-3 mb-3 text-[11px] text-slate-300 max-h-32 overflow-y-auto">
          <div className="flex items-center gap-1.5 font-semibold text-indigo-300 mb-1">
            <FileText className="h-3.5 w-3.5" />
            <span>Inspection Advisory Memo (Segment #{segmentId})</span>
          </div>
          <p className="leading-relaxed whitespace-pre-line text-slate-300">{advisory.advisory_text}</p>
        </div>
      )}

      {/* Interactive Chat Stream */}
      <div className="flex-1 overflow-y-auto space-y-2.5 pr-1 text-xs">
        {messages.map((m, i) => (
          <div 
            key={i} 
            className={`p-2.5 rounded-lg leading-relaxed ${
              m.sender === 'user' 
                ? 'bg-blue-600/20 text-blue-100 ml-6 border border-blue-500/30' 
                : 'bg-slate-800/70 text-slate-200 mr-4 border border-slate-700/60'
            }`}
          >
            <p className="font-semibold text-[10px] text-slate-400 mb-0.5">
              {m.sender === 'user' ? 'Civil Engineer' : 'AI Assistant'}
            </p>
            {m.text}
          </div>
        ))}
        {loading && (
          <div className="text-[11px] text-slate-400 italic">Consulting ChromaDB knowledge base...</div>
        )}
      </div>

      {/* Chat Input */}
      <form onSubmit={handleSend} className="flex gap-2 mt-3 pt-2 border-t border-slate-800">
        <input 
          type="text" 
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask: 'What protocol applies to pier settlement?'"
          className="flex-1 bg-slate-950 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 outline-none focus:border-indigo-500 transition-colors"
        />
        <button 
          type="submit" 
          disabled={loading}
          className="bg-indigo-600 hover:bg-indigo-500 text-white px-3 py-1.5 rounded-lg text-xs font-medium flex items-center gap-1 transition-colors disabled:opacity-50"
        >
          <Send className="h-3.5 w-3.5" />
        </button>
      </form>
    </div>
  );
}
