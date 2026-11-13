import React, { useState } from 'react';
import { Activity, ShieldCheck, AlertCircle, RefreshCw, Sliders } from 'lucide-react';
import TelemetryChart from './components/TelemetryChart';
import AnomalyGauge from './components/AnomalyGauge';
import ForecastChart from './components/ForecastChart';
import ShapBar from './components/ShapBar';
import AiChat from './components/AiChat';

export default function App() {
  // Segment 50 = Normal Baseline; Segment 450 = Progressive Pier Settlement Damage
  const [segmentId, setSegmentId] = useState(450);
  const [shapSummary, setShapSummary] = useState('');
  const [detectionResult, setDetectionResult] = useState(null);

  const isDamageScenario = segmentId > 400;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 selection:bg-blue-600 selection:text-white">
      {/* Top Header */}
      <header className="flex flex-wrap items-center justify-between border-b border-slate-800 pb-4 mb-6 gap-4">
        <div>
          <div className="flex items-center gap-2.5">
            <Activity className="h-7 w-7 text-blue-500" />
            <h1 className="text-xl md:text-2xl font-bold tracking-tight text-white">
              Smart Bridge Structural Health Monitoring System
            </h1>
          </div>
          <p className="text-xs text-slate-400 mt-0.5">
            Real-Time Vibration Telemetry • Isolation Forest Detection • ARIMA Stiffness Forecasting • SHAP XAI • RAG Advisory
          </p>
        </div>

        {/* Global Status Badges */}
        <div className="flex items-center gap-3">
          <span className="flex items-center gap-1.5 text-xs px-3 py-1 bg-slate-900 border border-slate-700 text-slate-300 rounded-full font-medium shadow-sm">
            <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse"></span>
            FastAPI REST Server (Port 8000)
          </span>
          <span className="text-xs px-3 py-1 bg-blue-950/80 text-blue-300 border border-blue-800 rounded-full font-medium">
            Z24 Benchmark (27 Channels @ 100 Hz)
          </span>
        </div>
      </header>

      {/* Control Bar: Interactive Scenario / Segment Selector */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-4 mb-6 shadow-md flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-2">
          <Sliders className="h-4 w-4 text-blue-400" />
          <span className="text-xs font-semibold text-slate-300 uppercase tracking-wider">Test Scenario Selector:</span>
        </div>

        <div className="flex items-center gap-3 flex-1 max-w-xl">
          <button
            onClick={() => setSegmentId(50)}
            className={`px-3 py-1.5 text-xs rounded-lg font-medium transition-all ${
              !isDamageScenario 
                ? 'bg-emerald-600 text-white shadow-sm' 
                : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
            }`}
          >
            Scenario 0: Healthy Baseline (Seg #50)
          </button>
          
          <button
            onClick={() => setSegmentId(450)}
            className={`px-3 py-1.5 text-xs rounded-lg font-medium transition-all ${
              isDamageScenario 
                ? 'bg-red-600 text-white shadow-sm' 
                : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
            }`}
          >
            Scenario 6: Pier Settlement (Seg #450)
          </button>

          <div className="flex items-center gap-2 flex-1 ml-2">
            <input 
              type="range" 
              min="0" 
              max="1529" 
              value={segmentId} 
              onChange={(e) => setSegmentId(Number(e.target.value))}
              className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-blue-500"
            />
            <span className="text-xs font-mono text-slate-400 w-16 text-right">#{segmentId}</span>
          </div>
        </div>

        <div className="text-xs text-slate-400 flex items-center gap-1.5">
          {isDamageScenario ? (
            <span className="text-red-400 font-semibold flex items-center gap-1">
              <AlertCircle className="h-3.5 w-3.5" /> Physical Damage Introduced (Settlement)
            </span>
          ) : (
            <span className="text-emerald-400 font-semibold flex items-center gap-1">
              <ShieldCheck className="h-3.5 w-3.5" /> Undamaged Reference Geometry
            </span>
          )}
        </div>
      </div>

      {/* Main Grid Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left 2 Columns: Telemetry Waveforms & ARIMA Degradation Forecasting */}
        <div className="lg:col-span-2 space-y-6">
          <TelemetryChart segmentId={segmentId} />
          <ForecastChart degrading={isDamageScenario} />
        </div>

        {/* Right Column: Isolation Forest Gauge, SHAP Bar, & AI Inspector Chat */}
        <div className="space-y-6">
          <AnomalyGauge 
            segmentId={segmentId} 
            onDetectionResult={setDetectionResult} 
          />
          <ShapBar 
            segmentId={segmentId} 
            onShapSummary={setShapSummary} 
          />
          <AiChat 
            segmentId={segmentId} 
            anomalyScore={detectionResult?.decision_score ?? -0.42}
            shapSummary={shapSummary}
            topChannels={detectionResult?.top_affected_channels ?? [14, 15]}
          />
        </div>
      </div>
    </div>
  );
}
