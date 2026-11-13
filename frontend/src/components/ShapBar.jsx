import React, { useState, useEffect } from 'react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';
import { fetchShapExplanation } from '../api';

export default function ShapBar({ segmentId, onShapSummary }) {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetchShapExplanation(segmentId)
      .then(res => {
        setData(res);
        if (onShapSummary) onShapSummary(res.summary_text);
      })
      .catch(err => console.error('Failed to fetch SHAP:', err));
  }, [segmentId]);

  const shapFeatures = data?.shap_features || [];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg">
      <div className="flex items-center justify-between mb-1">
        <h2 className="text-base font-semibold text-slate-200">SHAP Attribution Diagnostics</h2>
        <span className="text-[10px] text-slate-400 bg-slate-800 px-2 py-0.5 rounded">TreeExplainer</span>
      </div>
      <p className="text-xs text-slate-400 mb-3">Vibration features pushing anomaly score toward critical threshold</p>

      <div className="h-44 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={shapFeatures} layout="vertical" margin={{ left: 15, right: 15, top: 5, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
            <XAxis type="number" stroke="#64748b" tick={{ fontSize: 10 }} />
            <YAxis dataKey="feature" type="category" stroke="#94a3b8" tick={{ fontSize: 10 }} width={90} />
            <Tooltip 
              contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', color: '#f8fafc', fontSize: '11px' }} 
            />
            <Bar dataKey="attribution" fill="#3b82f6" radius={[0, 4, 4, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
