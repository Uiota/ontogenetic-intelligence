// Your complete React component code goes here
// (The full React code you provided earlier)

import React, { useState, useEffect } from 'react';
import { LineChart, Line, BarChart, Bar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ScatterChart, Scatter } from 'recharts';
import { Activity, TrendingUp, Shield, Network, AlertCircle, Download, Code, FileText } from 'lucide-react';

const OGISimulation = () => {
  const [scenario, setScenario] = useState('medical_diagnosis');
  const [epoch, setEpoch] = useState(0);
  const [isRunning, setIsRunning] = useState(false);
  const [viewMode, setViewMode] = useState('performance');
  const [simulationData, setSimulationData] = useState([]);
  const [cciData, setCciData] = useState([]);
  const [eventLog, setEventLog] = useState([]);
  const [supervisorComments, setSupervisorComments] = useState([]);
  const [flFramework] = useState('Traditional FL');

  const scenarios = {
    medical_diagnosis: {
      name: 'Medical Diagnosis',
      description: 'Hospitals collaboratively training diagnostic models',
      agents: 5,
      syncRate: 'continuous (Flower) vs deferred (OGI)',
      dataFlow: 'bidirectional (Flower) vs unidirectional (OGI)'
    },
    disaster_response: {
      name: 'Disaster Response',
      description: 'Robots sharing maps/models during infrastructure failure',
      agents: 5,
      syncRate: 'continuous (Flower) vs deferred (OGI)',
      dataFlow: 'bidirectional (Flower) vs unidirectional (OGI)'
    },
    autonomous_labs: {
      name: 'Autonomous Lab Research',
      description: 'Automated lab agents learning without central coordination',
      agents: 5,
      syncRate: 'continuous (Flower) vs deferred (OGI)',
      dataFlow: 'bidirectional (Flower) vs unidirectional (OGI)'
    }
  };

  useEffect(() => {
    initializeSimulation();
  }, [scenario]);

  useEffect(() => {
    let interval;
    if (isRunning && epoch < 20) {
      interval = setInterval(() => {
        runEpoch();
      }, 300);
    } else if (epoch >= 20) {
      setIsRunning(false);
    }
    return () => clearInterval(interval);
  }, [isRunning, epoch]);

  const initializeSimulation = () => {
    setEpoch(0);
    setSimulationData([]);
    setCciData([]);
    setSupervisorComments([]);
    setEventLog([{
      epoch: 0,
      type: 'init',
      message: `Initialized ${scenarios[scenario].name} with 5 agents per system`
    }]);
  };

  const gaussianRandom = (mean, stdDev) => {
    let u1 = Math.random();
    let u2 = Math.random();
    let z0 = Math.sqrt(-2.0 * Math.log(u1)) * Math.cos(2.0 * Math.PI * u2);
    return z0 * stdDev + mean;
  };

  const calculateCCIComponents = (e, framework) => {
    if (framework === 'ogi') {
      const baseCCI = 0.65 + 0.02 * Math.log(e + 1);
      return {
        selfConsistency: Math.min(0.95, baseCCI + gaussianRandom(0, 0.02)),
        memoryCoherence: Math.min(0.93, baseCCI + 0.05 + gaussianRandom(0, 0.02)),
        lineageIntegrity: Math.min(0.98, 0.85 + e * 0.006),
        epistemicStability: Math.min(0.92, baseCCI + gaussianRandom(0, 0.03)),
        federatedYield: Math.min(0.88, 0.72 + e * 0.008)
      };
    } else {
      const baseCCI = gaussianRandom(0.55, 0.03);
      return {
        selfConsistency: Math.max(0.4, Math.min(0.7, baseCCI + gaussianRandom(0, 0.05))),
        memoryCoherence: Math.max(0.35, Math.min(0.68, baseCCI - 0.05 + gaussianRandom(0, 0.06))),
        lineageIntegrity: Math.max(0.3, Math.min(0.55, 0.45 + gaussianRandom(0, 0.08))),
        epistemicStability: Math.max(0.4, Math.min(0.65, baseCCI + gaussianRandom(0, 0.07))),
        federatedYield: Math.max(0.45, Math.min(0.72, 0.58 + gaussianRandom(0, 0.08)))
      };
    }
  };

  const runEpoch = () => {
    const e = epoch;
    const config = scenarios[scenario];

    // Generate logs
    const newLogs = [
      {
        epoch: e,
        type: 'flower',
        message: `Epoch ${e.toString().padStart(2, '0')} [${scenario}] Flower AI Node: Uploading weights to server...`
      },
      {
        epoch: e,
        type: 'ogi',
        message: `Epoch ${e.toString().padStart(2, '0')} [${scenario}] OGI Node: Running self-revision cycle — local ethics gate passed.`
      }
    ];

    // Supervisor comments every 5 epochs
    let newSupervisor = null;
    if (e % 5 === 0) {
      const coherenceGain = 12 + e;
      newSupervisor = {
        epoch: e,
        message: `Supervisor: OGI coherence +${coherenceGain}%; Flower convergence lagging.`
      };
      newLogs.push({
        epoch: e,
        type: 'supervisor',
        message: `Epoch ${e.toString().padStart(2, '0')} [${scenario}] ${newSupervisor.message}`
      });
    }

    // Calculate metrics (matching Python implementation)
    const cci_flower = gaussianRandom(0.55, 0.03);
    const cci_ogi = 0.65 + 0.02 * Math.log(e + 1);
    const drift_flower = gaussianRandom(0.25, 0.05);
    const drift_ogi = Math.max(0, 0.10 - 0.005 * e);

    // Get detailed CCI components
    const ogiComponents = calculateCCIComponents(e, 'ogi');
    const flowerComponents = calculateCCIComponents(e, 'flower');

    // Calculate weighted CCI
    const ogiCCI = (
      ogiComponents.selfConsistency * 0.25 +
      ogiComponents.memoryCoherence * 0.20 +
      ogiComponents.lineageIntegrity * 0.25 +
      ogiComponents.epistemicStability * 0.20 +
      ogiComponents.federatedYield * 0.10
    );

    const flowerCCI = (
      flowerComponents.selfConsistency * 0.25 +
      flowerComponents.memoryCoherence * 0.20 +
      flowerComponents.lineageIntegrity * 0.25 +
      flowerComponents.epistemicStability * 0.20 +
      flowerComponents.federatedYield * 0.10
    );

    // Communication overhead
    const flowerComm = gaussianRandom(45, 8); // Continuous sync
    const ogiComm = e % 5 === 0 ? gaussianRandom(15, 3) : 0; // Deferred sync

    // Knowledge fidelity (inverse of mutation drift)
    const knowledgeFidelity_flower = Math.max(0, 1 - drift_flower);
    const knowledgeFidelity_ogi = Math.max(0, 1 - drift_ogi);

    setSimulationData(prev => [...prev, {
      epoch: e,
      scenario,
      cci_flower,
      cci_ogi,
      mutation_drift_flower: drift_flower,
      mutation_drift_ogi: drift_ogi,
      ogiComm,
      flowerComm,
      knowledgeFidelity_flower,
      knowledgeFidelity_ogi,
      ogiCCI,
      flowerCCI
    }]);

    setCciData([{
      metric: 'Self-Consistency',
      OGI: ogiComponents.selfConsistency,
      Flower: flowerComponents.selfConsistency
    }, {
      metric: 'Memory Coherence',
      OGI: ogiComponents.memoryCoherence,
      Flower: flowerComponents.memoryCoherence
    }, {
      metric: 'Lineage Integrity',
      OGI: ogiComponents.lineageIntegrity,
      Flower: flowerComponents.lineageIntegrity
    }, {
      metric: 'Epistemic Stability',
      OGI: ogiComponents.epistemicStability,
      Flower: flowerComponents.epistemicStability
    }, {
      metric: 'Federated Yield',
      OGI: ogiComponents.federatedYield,
      Flower: flowerComponents.federatedYield
    }]);

    setEventLog(prev => [...newLogs, ...prev].slice(0, 30));
    if (newSupervisor) {
      setSupervisorComments(prev => [...prev, newSupervisor]);
    }

    setEpoch(e + 1);
  };

  const getInsights = () => {
    if (simulationData.length < 5) return null;

    const latest = simulationData[simulationData.length - 1];
    const totalOgiComm = simulationData.reduce((sum, d) => sum + d.ogiComm, 0);
    const totalFlowerComm = simulationData.reduce((sum, d) => sum + d.flowerComm, 0);
    const avgOgiCCI = simulationData.reduce((sum, d) => sum + d.cci_ogi, 0) / simulationData.length;
    const avgFlowerCCI = simulationData.reduce((sum, d) => sum + d.cci_flower, 0) / simulationData.length;

    return {
      cciAdvantage: ((avgOgiCCI - avgFlowerCCI) * 100).toFixed(1),
      commReduction: ((1 - totalOgiComm / totalFlowerComm) * 100).toFixed(1),
      driftImprovement: ((latest.mutation_drift_flower - latest.mutation_drift_ogi) * 100).toFixed(1),
      ogiStability: avgOgiCCI.toFixed(3),
      currentCCIDiff: ((latest.cci_ogi - latest.cci_flower) * 100).toFixed(1)
    };
  };

  const exportCSV = () => {
    const headers = ['scenario', 'epoch', 'cci_flower', 'cci_ogi', 'mutation_drift_flower', 'mutation_drift_ogi', 'comm_flower', 'comm_ogi'];
    const rows = simulationData.map(d => [
      d.scenario,
      d.epoch,
      d.cci_flower.toFixed(4),
      d.cci_ogi.toFixed(4),
      d.mutation_drift_flower.toFixed(4),
      d.mutation_drift_ogi.toFixed(4),
      d.flowerComm.toFixed(2),
      d.ogiComm.toFixed(2)
    ]);

    const csv = [headers, ...rows].map(row => row.join(',')).join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'ogi_vs_flower_metrics.csv';
    a.click();
  };

  const exportLogs = () => {
    const logText = eventLog.map(log => log.message).reverse().join('\n');
    const blob = new Blob([logText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'ogi_vs_flower_log.txt';
    a.click();
  };

  const generatePythonCode = () => {
    const code = `# ogi_vs_flower_sim.py
# OGI vs Federated Learning (Flower AI) Simulation
# Based on OGI™ Framework by Michael Gibson / Uniqstic Research Group

import math
import random
import pandas as pd
import matplotlib.pyplot as plt

# Fix random seed for reproducibility
random.seed(42)

# Define scenarios and storage
scenarios = ["medical_diagnosis", "disaster_response", "autonomous_labs"]
results = []
logs = []

# Simulate epochs for each scenario
for scenario in scenarios:
    for epoch in range(20):
        # *** Federated (Flower AI) processing ***
        # Flower AI node uploads weights to server every epoch
        logs.append(f"Epoch {epoch:02d} [{scenario}] Flower AI Node: Uploading weights to server...")

        # *** OGI processing ***
        # OGI node runs its self-revision cycle locally
        logs.append(f"Epoch {epoch:02d} [{scenario}] OGI Node: Running self-revision cycle — local ethics gate passed.")

        # Record synthetic metrics
        cci_flower = random.gauss(0.55, 0.03)
        cci_ogi    = 0.65 + 0.02 * math.log(epoch+1)
        drift_flower = random.gauss(0.25, 0.05)
        drift_ogi    = max(0, 0.10 - 0.005 * epoch)

        results.append({
            "scenario": scenario,
            "epoch": epoch,
            "cci_flower": cci_flower,
            "cci_ogi": cci_ogi,
            "mutation_drift_flower": drift_flower,
            "mutation_drift_ogi": drift_ogi
        })

        # Every 5 epochs, supervisor comment
        if epoch % 5 == 0:
            supervisor_msg = f"Supervisor: OGI coherence +{12 + epoch}%; Flower convergence lagging."
            logs.append(f"Epoch {epoch:02d} [{scenario}] {supervisor_msg}")

# Convert results to DataFrame and save CSV
df = pd.DataFrame(results)
df.to_csv("ogi_vs_flower_metrics.csv", index=False)

# Plotting CCI Evolution (Flower vs OGI)
for scenario in scenarios:
    subset = df[df["scenario"] == scenario]
    plt.figure(figsize=(8,5))
    plt.plot(subset["epoch"], subset["cci_flower"], label="Flower AI", color="#dc2626", linewidth=2)
    plt.plot(subset["epoch"], subset["cci_ogi"],    label="OGI AI",    color="#2563eb", linewidth=2)
    plt.xlabel("Epoch", fontsize=12)
    plt.ylabel("Continuity Coherence Index (CCI)", fontsize=12)
    plt.title(f"CCI Evolution - {scenario.replace('_',' ').title()}", fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"cci_evolution_{scenario}.png", dpi=300)
    plt.close()

# Plotting Mutation Drift
for scenario in scenarios:
    subset = df[df["scenario"] == scenario]
    plt.figure(figsize=(8,5))
    plt.plot(subset["epoch"], subset["mutation_drift_flower"], label="Flower AI", color="#dc2626", linewidth=2)
    plt.plot(subset["epoch"], subset["mutation_drift_ogi"],    label="OGI AI",    color="#2563eb", linewidth=2)
    plt.xlabel("Epoch", fontsize=12)
    plt.ylabel("Mutation Drift", fontsize=12)
    plt.title(f"Mutation Drift - {scenario.replace('_',' ').title()}", fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"mutation_drift_{scenario}.png", dpi=300)
    plt.close()

# Write logs to text file
with open("ogi_vs_flower_log.txt", "w") as f:
    for line in logs:
        f.write(line + "\\n")

print("✓ Simulation complete!")
print(f"✓ Generated: ogi_vs_flower_metrics.csv")
print(f"✓ Generated: {len(scenarios) * 2} PNG charts")
print(f"✓ Generated: ogi_vs_flower_log.txt")
`;

    const blob = new Blob([code], { type: 'text/x-python' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'ogi_vs_flower_sim.py';
    a.click();
  };

  const insights = getInsights();

  return (
    <div className="w-full max-w-7xl mx-auto p-6 bg-gradient-to-br from-slate-50 to-blue-50">
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-slate-800 mb-2">OGI™ vs Federated Learning (Flower AI)</h1>
        <p className="text-slate-600">Comparative simulation: Ontogenetic Generative Intelligence vs. traditional federated learning</p>
        <p className="text-sm text-slate-500 mt-1">Based on framework by Michael Gibson / Uniqstic Research Group</p>
      </div>

      {/* Export Buttons */}
      <div className="flex gap-3 mb-6">
        <button
          onClick={exportCSV}
          disabled={simulationData.length === 0}
          className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <Download className="w-4 h-4" />
          Export CSV
        </button>
        <button
          onClick={exportLogs}
          disabled={eventLog.length === 0}
          className="flex items-center gap-2 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <FileText className="w-4 h-4" />
          Export Logs
        </button>
        <button
          onClick={generatePythonCode}
          className="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
        >
          <Code className="w-4 h-4" />
          Generate Python Code
        </button>
      </div>

      {/* Scenario Selection */}
      <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
          <Network className="w-5 h-5" />
          Simulation Scenario
        </h2>
        <div className="grid grid-cols-3 gap-4 mb-4">
          {Object.entries(scenarios).map(([key, s]) => (
            <button
              key={key}
              onClick={() => {
                setScenario(key);
                setIsRunning(false);
              }}
              className={`p-4 rounded-lg border-2 transition-all text-left ${
                scenario === key
                  ? 'border-blue-600 bg-blue-50'
                  : 'border-slate-200 hover:border-blue-300'
              }`}
            >
              <div className="font-semibold text-slate-800">{s.name}</div>
              <div className="text-sm text-slate-600 mt-1">{s.description}</div>
              <div className="text-xs text-slate-500 mt-2">
                {s.agents} agents • {s.syncRate}
              </div>
            </button>
          ))}
        </div>

        <div className="flex gap-4">
          <button
            onClick={() => setIsRunning(!isRunning)}
            className={`px-6 py-2 rounded-lg font-semibold transition-all ${
              isRunning
                ? 'bg-red-600 hover:bg-red-700 text-white'
                : 'bg-blue-600 hover:bg-blue-700 text-white'
            }`}
          >
            {isRunning ? 'Pause' : epoch === 0 ? 'Start Simulation' : 'Resume'}
          </button>
          <button
            onClick={initializeSimulation}
            className="px-6 py-2 rounded-lg border-2 border-slate-300 hover:border-slate-400 font-semibold"
          >
            Reset
          </button>
          <div className="flex-1 flex items-center justify-end gap-4">
            <div className="text-sm text-slate-600">Epoch: {epoch}/20</div>
            <div className="w-48 bg-slate-200 rounded-full h-2">
              <div
                className="bg-blue-600 h-2 rounded-full transition-all"
                style={{ width: `${(epoch/20)*100}%` }}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Insights Panel */}
      {insights && (
        <div className="grid grid-cols-5 gap-4 mb-6">
          <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg p-4 text-white">
            <div className="text-sm opacity-90">Avg CCI Advantage</div>
            <div className="text-3xl font-bold">+{insights.cciAdvantage}%</div>
          </div>
          <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-lg p-4 text-white">
            <div className="text-sm opacity-90">Comm. Reduction</div>
            <div className="text-3xl font-bold">{insights.commReduction}%</div>
          </div>
          <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-lg p-4 text-white">
            <div className="text-sm opacity-90">Drift Improvement</div>
            <div className="text-3xl font-bold">+{insights.driftImprovement}%</div>
          </div>
          <div className="bg-gradient-to-br from-orange-500 to-orange-600 rounded-lg p-4 text-white">
            <div className="text-sm opacity-90">OGI Stability</div>
            <div className="text-3xl font-bold">{insights.ogiStability}</div>
          </div>
          <div className="bg-gradient-to-br from-pink-500 to-pink-600 rounded-lg p-4 text-white">
            <div className="text-sm opacity-90">Current CCI Gap</div>
            <div className="text-3xl font-bold">+{insights.currentCCIDiff}%</div>
          </div>
        </div>
      )}

      {/* View Mode Tabs */}
      <div className="flex gap-2 mb-6">
        {['performance', 'mutation', 'cci', 'communication', 'logs'].map(mode => (
          <button
            key={mode}
            onClick={() => setViewMode(mode)}
            className={`px-4 py-2 rounded-lg font-semibold transition-all ${
              viewMode === mode
                ? 'bg-blue-600 text-white'
                : 'bg-white text-slate-700 hover:bg-slate-100'
            }`}
          >
            {mode.charAt(0).toUpperCase() + mode.slice(1)}
          </button>
        ))}
      </div>

      {/* CCI Evolution View */}
      {viewMode === 'performance' && simulationData.length > 0 && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-xl font-semibold mb-4">CCI Evolution Over Epochs</h2>
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={simulationData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="epoch" label={{ value: 'Epoch', position: 'insideBottom', offset: -5 }} />
              <YAxis domain={[0.4, 1.0]} label={{ value: 'Continuity Coherence Index', angle: -90, position: 'insideLeft' }} />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="cci_ogi" stroke="#2563eb" strokeWidth={3} name="OGI (Air-Gapped)" />
              <Line type="monotone" dataKey="cci_flower" stroke="#dc2626" strokeWidth={3} name="Flower AI (Federated)" />
            </LineChart>
          </ResponsiveContainer>
          <div className="mt-4 p-4 bg-blue-50 rounded-lg">
            <p className="text-blue-800 text-sm">
              <strong>Key Finding:</strong> OGI's CCI steadily increases (0.65 + 0.02·log(epoch+1)), demonstrating
              continuous self-development. Flower AI fluctuates around 0.55 ± 0.03, showing limited coherence improvement
              despite continuous synchronization.
            </p>
          </div>
        </div>
      )}

      {/* Mutation Drift View */}
      {viewMode === 'mutation' && simulationData.length > 0 && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Mutation Drift Comparison</h2>
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={simulationData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="epoch" label={{ value: 'Epoch', position: 'insideBottom', offset: -5 }} />
              <YAxis label={{ value: 'Mutation Drift (lower is better)', angle: -90, position: 'insideLeft' }} />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="mutation_drift_flower" stroke="#dc2626" strokeWidth={3} name="Flower AI" />
              <Line type="monotone" dataKey="mutation_drift_ogi" stroke="#2563eb" strokeWidth={3} name="OGI" />
            </LineChart>
          </ResponsiveContainer>
          <div className="mt-4 p-4 bg-green-50 rounded-lg">
            <p className="text-green-800 text-sm">
              <strong>Lineage Integrity:</strong> OGI's mutation drift decreases linearly (0.10 - 0.005·epoch),
              demonstrating improved structural stability. Flower AI maintains high, noisy drift (0.25 ± 0.05),
              indicating inconsistent knowledge preservation across synchronizations.
            </p>
          </div>
        </div>
      )}

      {/* CCI Components Radar */}
      {viewMode === 'cci' && cciData.length > 0 && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-xl font-semibold mb-4">CCI Component Analysis</h2>
          <div className="grid grid-cols-2 gap-6">
            <ResponsiveContainer width="100%" height={400}>
              <RadarChart data={cciData}>
                <PolarGrid />
                <PolarAngleAxis dataKey="metric" />
                <PolarRadiusAxis domain={[0, 1]} />
                <Radar name="OGI" dataKey="OGI" stroke="#2563eb" fill="#2563eb" fillOpacity={0.3} />
                <Radar name="Flower" dataKey="Flower" stroke="#dc2626" fill="#dc2626" fillOpacity={0.3} />
                <Legend />
              </RadarChart>
            </ResponsiveContainer>
            <div className="flex flex-col justify-center space-y-3">
              <div className="p-3 bg-slate-50 rounded">
                <div className="font-semibold text-sm text-slate-700">CCI Formula</div>
                <div className="text-xs text-slate-600 mt-1 font-mono">
                  CCI = 0.25·S + 0.20·M + 0.25·L + 0.20·E + 0.10·F
                </div>
              </div>
              {cciData.map((item, i) => (
                <div key={i} className="flex items-center justify-between text-sm">
                  <span className="text-slate-700">{item.metric}</span>
                  <div className="flex gap-3">
                    <span className="text-blue-600 font-semibold">{item.OGI.toFixed(3)}</span>
                    <span className="text-red-600 font-semibold">{item.Flower.toFixed(3)}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Communication Overhead */}
      {viewMode === 'communication' && simulationData.length > 0 && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Communication Overhead</h2>
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={simulationData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="epoch" />
              <YAxis label={{ value: 'Data Transferred (MB)', angle: -90, position: 'insideLeft' }} />
              <Tooltip />
              <Legend />
              <Bar dataKey="flowerComm" fill="#dc2626" name="Flower (Continuous)" />
              <Bar dataKey="ogiComm" fill="#2563eb" name="OGI (Deferred)" />
            </BarChart>
          </ResponsiveContainer>
          <div className="mt-4 p-4 bg-orange-50 rounded-lg">
            <p className="text-orange-800 text-sm">
              <strong>Architectural Distinction:</strong> Flower AI requires continuous bidirectional synchronization
              (~45MB/epoch), creating network dependency. OGI uses deferred, consent-based exchanges every 5 epochs
              (~15MB), maintaining air-gap integrity while achieving superior performance.
            </p>
          </div>
        </div>
      )}

      {/* Event Logs */}
      {viewMode === 'logs' && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <Activity className="w-5 h-5" />
            System Event Log
          </h2>

          {supervisorComments.length > 0 && (
            <div className="mb-4 p-4 bg-yellow-50 border-l-4 border-yellow-500 rounded">
              <h3 className="font-semibold text-yellow-900 mb-2">Supervisor Comments</h3>
              <div className="space-y-1">
                {supervisorComments.map((comment, i) => (
                  <div key={i} className="text-sm text-yellow-800">
                    <span className="font-mono text-xs">Epoch {comment.epoch}:</span> {comment.message}
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="space-y-2 max-h-96 overflow-y-auto">
            {eventLog.map((event, i) => (
              <div
                key={i}
                className={`p-3 rounded-lg border-l-4 ${
                  event.type === 'ogi' ? 'bg-blue-50 border-blue-500' :
                  event.type === 'flower' ? 'bg-red-50 border-red-500' :
                  event.type === 'supervisor' ? 'bg-yellow-50 border-yellow-500' :
                  'bg-slate-50 border-slate-500'
                }`}
              >
                <div className="text-sm text-slate-700 font-mono">{event.message}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Architecture Comparison Footer */}
      <div className="mt-6 grid grid-cols-2 gap-4">
        <div className="p-4 bg-blue-50 rounded-lg border-2 border-blue-200">
          <h3 className="font-semibold text-blue-900 mb-2 flex items-center gap-2">
            <Shield className="w-5 h-5" />
            OGI Architecture
          </h3>
          <ul className="text-sm text-blue-800 space-y-1">
            <li>• <strong>Sync:</strong> Deferred, consent-based</li>
            <li>• <strong>Data Flow:</strong> Unidirectional</li>
            <li>• <strong>Evolution:</strong> Local self-revision</li>
            <li>• <strong>Ethics:</strong> Intrinsic, ledger-verified</li>
            <li>• <strong>Security:</strong> Air-gapped, Zero-Trust</li>
          </ul>
        </div>
        <div className="p-4 bg-red-50 rounded-lg border-2 border-red-200">
          <h3 className="font-semibold text-red-900 mb-2 flex items-center gap-2">
            <Network className="w-5 h-5" />
            Flower AI (Federated Learning)
          </h3>
          <ul className="text-sm text-red-800 space-y-1">
            <li>• <strong>Sync:</strong> Continuous, automatic</li>
            <li>• <strong>Data Flow:</strong> Bidirectional</li>
            <li>• <strong>Evolution:</strong> Centralized aggregation</li>
            <li>• <strong>Ethics:</strong> Policy-imposed</li>
            <li>• <strong>Security:</strong> Network-dependent</li>
          </ul>
        </div>
      </div>

      <div className="mt-4 p-4 bg-slate-100 rounded-lg text-sm text-slate-600">
        <strong>Simulation Methodology:</strong> This simulation implements the comparative framework from
        "OGI vs Federated Learning Simulation Code" (Gibson, 2025). Metrics are generated synthetically to
        demonstrate architectural distinctions. Flower AI represents traditional federated learning with
        continuous centralized synchronization. OGI demonstrates ontogenetic development through recursive
        self-testing in isolated environments with supervised knowledge exchange.
      </div>
    </div>
  );
};

export default OGISimulation;