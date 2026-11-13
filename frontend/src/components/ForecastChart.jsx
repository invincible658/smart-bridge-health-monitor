import React, { useState, useEffect } from 'react';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ReferenceLine } from 'recharts';
import { TrendingDown, AlertCircle } from 'lucide-react';
import { fetchForecast } from '../api';

export default function ForecastChart({ degrading = true }) {
  const [forecast, setForecast] = useState(null);

  useEffect(() => {
    fetchForecast(10, degrading)
      .then(res => setForecast(res))
      .catch(err => console.error('Failed to fetch forecast:', err));
  }, [degrading]);

  const chartData = forecast?.chart_data || [];
  const willBreach = forecast?.breach_predicted || false;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg">
      <div className="flex flex-wrap items-center justify-between gap-2 mb-4">
        <div className="flex items-center gap-2">
          <TrendingDown className={`h-5 w-5 ${willBreach ? 'text-amber-400' : 'text-blue-400'}`} />
          <h2 className="text-base font-semibold text-slate-200">ARIMA Stiffness Degradation Forecast</h2>
        </div>
        
        {willBreach ? (
          <span className="flex items-center gap-1 text-[11px] px-2.5 py-1 bg-amber-950/80 text-amber-300 border border-amber-800 rounded font-medium">
            <AlertCircle className="h-3.5 w-3.5 text-amber-400" />
            Breach predicted at T+{forecast?.steps_to_breach}
          </span>
        ) : (
          <span className="text-[11px] px-2.5 py-1 bg-slate-800 text-slate-300 border border-slate-700 rounded font-medium">
            Trajectory Stable (> 3.50 Hz)
          </span>
        )}
      </div>

      <div className="h-56 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
            <XAxis dataKey="step" stroke="#64748b" tick={{ fontSize: 10 }} />
            <YAxis stroke="#64748b" domain={[3.3, 4.0]} tick={{ fontSize: 10 }} unit=" Hz" />
            <Tooltip 
              contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', color: '#f8fafc', fontSize: '11px' }} 
            />
            <ReferenceLine 
              y={3.50} 
              stroke="#ef4444" 
              strokeDasharray="4 4" 
              label={{ value: 'Safety Limit (3.50 Hz)', fill: '#ef4444', fontSize: 10, position: 'insideTopLeft' }} 
            />
            {/* Historical Sequence Line */}
            <Line 
              type="monotone" 
              dataKey="historical" 
              stroke="#38bdf8" 
              strokeWidth={2} 
              dot={{ r: 3, fill: '#38bdf8' }} 
              connectNulls={false}
            />
            {/* Projected Forecast Horizon Line */}
            <Line 
              type="monotone" 
              dataKey="forecast" 
              stroke="#f59e0b" 
              strokeWidth={2} 
              strokeDasharray="5 5" 
              dot={{ r: 3, fill: '#f59e0b' }} 
              connectNulls={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <p className="text-[11px] text-slate-400 mt-2 border-t border-slate-800/80 pt-2">
        {forecast?.summary || 'Fitting ARIMA(1,1,0) model to sequential fundamental bending frequencies.'}
      </p>
    </div>
  );
}
