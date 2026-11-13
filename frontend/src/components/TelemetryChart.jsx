import React, { useState, useEffect } from 'react';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';
import { Activity, Radio } from 'lucide-react';
import { fetchTelemetry } from '../api';

export default function TelemetryChart({ segmentId }) {
  const [channel, setChannel] = useState(14);
  const [telemetry, setTelemetry] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;
    setLoading(true);
    fetchTelemetry(segmentId, channel, 80)
      .then(data => {
        if (isMounted) {
          setTelemetry(data);
          setLoading(false);
        }
      })
      .catch(err => {
        console.error('Failed to fetch telemetry:', err);
        if (isMounted) setLoading(false);
      });
    return () => { isMounted = false; };
  }, [segmentId, channel]);

  const waveformData = telemetry?.waveform || [];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg">
      <div className="flex flex-wrap items-center justify-between gap-3 mb-4">
        <div className="flex items-center gap-2">
          <Activity className="h-5 w-5 text-blue-400" />
          <h2 className="text-base font-semibold text-slate-100">Live Vibration Telemetry Waveform</h2>
        </div>

        <div className="flex items-center gap-3">
          <div className="flex items-center gap-1.5 text-xs text-slate-400">
            <Radio className="h-3.5 w-3.5 text-emerald-400 animate-pulse" />
            <span>Mode: {telemetry?.fundamental_frequency_hz || 3.85} Hz</span>
          </div>

          <div className="flex items-center gap-2 text-xs">
            <span className="text-slate-400">Sensor:</span>
            <select 
              value={channel} 
              onChange={(e) => setChannel(Number(e.target.value))}
              className="bg-slate-800 border border-slate-700 text-slate-200 rounded px-2.5 py-1 outline-none focus:border-blue-500 font-medium"
            >
              {[1, 2, 3, 5, 7, 10, 14, 15, 18, 20, 24, 27].map(ch => (
                <option key={ch} value={ch}>Channel {ch} {ch === 14 ? '(Pier P1 Deck)' : ''}</option>
              ))}
            </select>
          </div>
        </div>
      </div>

      <div className="h-64 w-full">
        {loading ? (
          <div className="h-full flex items-center justify-center text-xs text-slate-500">
            Streaming segment #{segmentId} channel #{channel}...
          </div>
        ) : (
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={waveformData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="time" stroke="#64748b" tick={{ fontSize: 10 }} />
              <YAxis stroke="#64748b" tick={{ fontSize: 10 }} unit=" m/s²" domain={[-0.4, 0.4]} />
              <Tooltip 
                contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', color: '#f8fafc', fontSize: '11px' }} 
              />
              <Line 
                type="monotone" 
                dataKey="amplitude" 
                stroke={telemetry?.is_damaged_state ? "#ef4444" : "#38bdf8"} 
                strokeWidth={1.8} 
                dot={false} 
                isAnimationActive={false}
              />
            </LineChart>
          </ResponsiveContainer>
        )}
      </div>

      <div className="flex justify-between items-center text-[11px] text-slate-500 mt-2 border-t border-slate-800/80 pt-2">
        <span>Sampling: 100 Hz (Z24 Highway Bridge Benchmark)</span>
        <span>Digital Filter: 30 Hz Low-Pass (Butterworth 4th-Order)</span>
      </div>
    </div>
  );
}
