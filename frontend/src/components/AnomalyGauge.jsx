import React from 'react';
import { ShieldAlert, AlertTriangle, CheckCircle } from 'lucide-react';

export default function AnomalyGauge({ segmentId }) {
  const isAnomaly = segmentId > 400;
  const score = isAnomaly ? -0.42 : 0.38;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-slate-200">Isolation Forest Status</h2>
        {isAnomaly ? (
          <span className="flex items-center gap-1 text-xs px-2.5 py-1 bg-red-950 text-red-400 border border-red-800 rounded-full font-semibold">
            <AlertTriangle className="h-3.5 w-3.5" /> ANOMALY DETECTED
          </span>
        ) : (
          <span className="flex items-center gap-1 text-xs px-2.5 py-1 bg-emerald-950 text-emerald-400 border border-emerald-800 rounded-full font-semibold">
            <CheckCircle className="h-3.5 w-3.5" /> NORMAL
          </span>
        )}
      </div>

      <div className="flex flex-col items-center justify-center py-4">
        <div className={`text-4xl font-extrabold ${isAnomaly ? 'text-red-400' : 'text-emerald-400'}`}>
          {score.toFixed(2)}
        </div>
        <p className="text-xs text-slate-400 mt-1">Decision Score (Threshold: 0.00)</p>
      </div>

      <div className="text-xs text-slate-400 border-t border-slate-800 pt-3 mt-2 flex justify-between">
        <span>Model: Isolation Forest</span>
        <span>Evaluated: Segment #{segmentId}</span>
      </div>
    </div>
  );
}
