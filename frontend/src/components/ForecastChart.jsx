import React from 'react';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ReferenceLine } from 'recharts';
import { TrendingDown } from 'lucide-react';

export default function ForecastChart() {
  const forecastData = [
    { step: 'T-6', frequency: 3.85, type: 'Historical' },
    { step: 'T-4', frequency: 3.82, type: 'Historical' },
    { step: 'T-2', frequency: 3.78, type: 'Historical' },
    { step: 'T-0', frequency: 3.71, type: 'Historical' },
    { step: 'T+2', forecast: 3.65, type: 'Forecast' },
    { step: 'T+4', forecast: 3.58, type: 'Forecast' },
    { step: 'T+6', forecast: 3.52, type: 'Forecast' },
    { step: 'T+8', forecast: 3.46, type: 'Forecast' },
    { step: 'T+10', forecast: 3.41, type: 'Forecast' },
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <TrendingDown className="h-5 w-5 text-amber-400" />
          <h2 className="text-lg font-semibold text-slate-200">ARIMA Stiffness Degradation Forecast</h2>
        </div>
        <span className="text-xs px-2.5 py-1 bg-amber-950 text-amber-400 border border-amber-800 rounded font-medium">
          Warning: Threshold breach predicted at T+7
        </span>
      </div>

      <div className="h-60 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={forecastData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
            <XAxis dataKey="step" stroke="#64748b" tick={{ fontSize: 11 }} />
            <YAxis stroke="#64748b" domain={[3.3, 4.0]} tick={{ fontSize: 11 }} unit=" Hz" />
            <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', color: '#f8fafc' }} />
            <ReferenceLine y={3.50} stroke="#ef4444" strokeDasharray="4 4" label={{ value: 'Critical Safety Threshold (3.50 Hz)', fill: '#ef4444', fontSize: 11, position: 'insideTopLeft' }} />
            <Line type="monotone" dataKey="frequency" stroke="#38bdf8" strokeWidth={2} dot={{ r: 3 }} />
            <Line type="monotone" dataKey="forecast" stroke="#f59e0b" strokeWidth={2} strokeDasharray="5 5" dot={{ r: 3 }} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
