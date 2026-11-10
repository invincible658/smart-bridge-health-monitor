import React, { useState } from 'react';
import { Activity, ShieldAlert, TrendingDown, FileText, Bot } from 'lucide-react';
import TelemetryChart from './components/TelemetryChart';
import AnomalyGauge from './components/AnomalyGauge';
import ForecastChart from './components/ForecastChart';
import ShapBar from './components/ShapBar';
import AiChat from './components/AiChat';

export default function App() {
  const [selectedSegment, setSelectedSegment] = useState(450);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      {/* Header */}
      <header className="flex items-center justify-between border-b border-slate-800 pb-4 mb-6">
        <div>
          <h1 className="text-2xl font-bold flex items-center gap-2 text-blue-400">
            <Activity className="h-7 w-7 text-blue-500" />
            Smart Bridge Health Monitoring System
          </h1>
          <p className="text-sm text-slate-400">
            Real-time Telemetry, ML Anomaly Detection, ARIMA Forecasting & RAG Advisory
          </p>
        </div>
        <div className="flex items-center gap-4">
          <span className="text-xs px-3 py-1 bg-emerald-950 text-emerald-400 border border-emerald-800 rounded-full font-medium">
            System Online (100 Hz Stream)
          </span>
        </div>
      </header>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left 2 Cols: Telemetry & Forecasting */}
        <div className="lg:col-span-2 space-y-6">
          <TelemetryChart segmentId={selectedSegment} />
          <ForecastChart />
        </div>

        {/* Right Col: Diagnostics & AI Assistant */}
        <div className="space-y-6">
          <AnomalyGauge segmentId={selectedSegment} />
          <ShapBar segmentId={selectedSegment} />
          <AiChat />
        </div>
      </div>
    </div>
  );
}
