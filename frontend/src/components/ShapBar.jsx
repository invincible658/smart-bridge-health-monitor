import React from 'react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';

export default function ShapBar({ segmentId }) {
  const shapData = [
    { feature: 'ch14_dom_freq', contribution: 0.48 },
    { feature: 'ch15_kurtosis', contribution: 0.26 },
    { feature: 'ch14_entropy', contribution: 0.18 },
    { feature: 'ch7_ptp', contribution: 0.11 },
    { feature: 'ch3_rms', contribution: -0.04 },
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg">
      <h2 className="text-lg font-semibold text-slate-200 mb-1">SHAP Attribution Diagnostics</h2>
      <p className="text-xs text-slate-400 mb-4">Top vibration features driving the anomaly score</p>

      <div className="h-48 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={shapData} layout="vertical">
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
            <XAxis type="number" stroke="#64748b" tick={{ fontSize: 10 }} />
            <YAxis dataKey="feature" type="category" stroke="#94a3b8" tick={{ fontSize: 10 }} width={90} />
            <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', color: '#f8fafc' }} />
            <Bar dataKey="contribution" fill="#3b82f6" radius={[0, 4, 4, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
