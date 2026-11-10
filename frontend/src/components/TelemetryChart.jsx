import React, { useState } from 'react';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';
import { Activity } from 'lucide-react';

export default function TelemetryChart({ segmentId }) {
  const [channel, setChannel] = useState(14);

  // Sample vibration data for waveform rendering
  const data = Array.from({ length: 60 }, (_, i) => ({
    time: `${(i * 0.05).toFixed(2)}s`,
    amplitude: Math.sin(i * 0.3) * 0.4 + (Math.random() - 0.5) * 0.1
  }));

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Activity className="h-5 w-5 text-blue-400" />
          <h2 className="text-lg font-semibold text-slate-200">Bridge Telemetry Waveform</h2>
        </div>
        <div className="flex items-center gap-2 text-sm">
          <span className="text-slate-400">Channel:</span>
          <select 
            value={channel} 
            onChange={(e) => setChannel(Number(e.target.value))}
            className="bg-slate-800 border border-slate-700 text-slate-200 rounded px-2 py-1 outline-none text-xs"
          >
            {[1, 3, 7, 14, 15, 20, 27].map(ch => (
              <option key={ch} value={ch}>Channel {ch}</option>
            ))}
          </select>
        </div>
      </div>

      <div className="h-64 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
            <XAxis dataKey="time" stroke="#64748b" tick={{ fontSize: 11 }} />
            <YAxis stroke="#64748b" tick={{ fontSize: 11 }} unit=" m/s²" domain={[-1, 1]} />
            <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', color: '#f8fafc' }} />
            <Line type="monotone" dataKey="amplitude" stroke="#38bdf8" strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
