import React, { useState, useEffect } from 'react';
import { AlertTriangle, CheckCircle, ShieldAlert } from 'lucide-react';
import { fetchDetection } from '../api';

export default function AnomalyGauge({ segmentId, onDetectionResult }) {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetchDetection(segmentId)
      .then(res => {
        setData(res);
        if (onDetectionResult) onDetectionResult(res);
      })
      .catch(err => console.error('Failed to fetch detection:', err));
  }, [segmentId]);

  const isAnomaly = data?.is_anomaly ?? false;
  const riskScore = data?.anomaly_risk_score ?? 0.0;
  const decisionScore = data?.decision_score ?? 0.0;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg">
      <div className="flex items-center justify-between mb-3">
        <h2 className="text-base font-semibold text-slate-200">Isolation Forest Status</h2>
        {isAnomaly ? (
          <span className="flex items-center gap-1.5 text-xs px-2.5 py-1 bg-red-950 text-red-400 border border-red-800 rounded-full font-semibold animate-pulse">
            <AlertTriangle className="h-3.5 w-3.5" /> CRITICAL ANOMALY
          </span>
        ) : (
          <span className="flex items-center gap-1.5 text-xs px-2.5 py-1 bg-emerald-950 text-emerald-400 border border-emerald-800 rounded-full font-semibold">
            <CheckCircle className="h-3.5 w-3.5" /> NORMAL BASELINE
          </span>
        )}
      </div>

      <div className="flex flex-col items-center justify-center py-3">
        {/* Risk Percentage Display */}
        <div className={`text-4xl font-extrabold tracking-tight ${isAnomaly ? 'text-red-400' : 'text-emerald-400'}`}>
          {(riskScore * 100).toFixed(1)}%
        </div>
        <p className="text-xs text-slate-400 mt-1">Structural Risk Probability</p>

        {/* Linear Progress Meter */}
        <div className="w-full bg-slate-800 h-2.5 rounded-full mt-4 overflow-hidden border border-slate-700">
          <div 
            className={`h-full transition-all duration-500 rounded-full ${isAnomaly ? 'bg-red-500' : 'bg-emerald-500'}`}
            style={{ width: `${Math.min(100, Math.max(5, riskScore * 100))}%` }}
          />
        </div>
      </div>

      <div className="text-[11px] text-slate-400 border-t border-slate-800 pt-3 mt-1 flex justify-between">
        <span>Raw Score: <code className="text-slate-300">{decisionScore.toFixed(3)}</code></span>
        <span>Threshold: <code className="text-slate-300">0.000</code></span>
      </div>
    </div>
  );
}
