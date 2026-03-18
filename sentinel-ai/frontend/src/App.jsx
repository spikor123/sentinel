import { useState, useEffect } from 'react';
import { Shield, CheckCircle, Zap, Clock, Activity, Code } from 'lucide-react';

function App() {
  const [logs, setLogs] = useState([]);
  const [stats, setStats] = useState({ fixes: 12, hours: 4.5, success: 100 });

  // Fetch logs from backend
  const fetchLogs = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/logs');
      const data = await response.json();
      setLogs(data.reverse()); // Show newest first
    } catch (err) {
      console.error('Failed to fetch logs', err);
    }
  };

  useEffect(() => {
    fetchLogs();
    const interval = setInterval(fetchLogs, 3000); // Poll every 3 seconds
    return () => clearInterval(interval);
  }, []);

  const triggerSimulation = async () => {
    await fetch('http://localhost:5000/api/simulate-scan', { method: 'POST' });
    fetchLogs();
  };

  return (
    <div className="app-container">
      {/* Header */}
      <header style={{ marginBottom: '4rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <img src="/logo.png" alt="Sentinel Logo" style={{ width: 40, height: 40, borderRadius: '8px' }} />
          <div>
            <h1 style={{ fontSize: '1.25rem' }}>SENTINEL AI</h1>
            <p className="text-small">Autonomous Security Engineer for GitLab</p>
          </div>
        </div>
        <div style={{ display: 'flex', gap: '1.5rem', alignItems: 'center' }}>
           <button onClick={triggerSimulation} className="button-minimal" style={{ fontSize: '0.75rem', padding: '0.5rem 1rem' }}>TRIGGER SIMULATION</button>
           <div style={{ textAlign: 'right' }}>
             <span style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: '#10b981', fontSize: '0.75rem', fontWeight: 600 }}> 
               <div style={{ width: 6, height: 6, background: '#10b981', borderRadius: '50%' }}></div>
               MONITORING ACTIVE
             </span>
             <span style={{ fontSize: '0.7rem', color: '#94a3b8', display: 'block' }}>BRAIN: CLAUDE 3.5 SONNET CONNECTED</span>
           </div>
        </div>
      </header>

      {/* Hero Stats */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1.5rem', marginBottom: '3rem' }}>
        <div className="minimal-card">
          <Zap size={20} color="#2563eb" style={{ marginBottom: '1rem' }} />
          <h3 style={{ fontSize: '2rem' }}>128</h3>
          <p className="text-small">Autonomous Fixes</p>
        </div>
        <div className="minimal-card">
          <Clock size={20} color="#10b981" style={{ marginBottom: '1rem' }} />
          <h3 style={{ fontSize: '2rem' }}>42.5h</h3>
          <p className="text-small">Manual Toil Saved</p>
        </div>
        <div className="minimal-card">
          <CheckCircle size={20} color="#6366f1" style={{ marginBottom: '1rem' }} />
          <h3 style={{ fontSize: '2rem' }}>99.2%</h3>
          <p className="text-small">Success Rate</p>
        </div>
      </div>

      {/* Main Content: Logs & Logic */}
      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '2rem' }}>
        <section>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
            <h2 style={{ fontSize: '1rem' }}>Active Remediation Log</h2>
            <Activity size={16} className="text-small" />
          </div>
          <div className="minimal-card" style={{ padding: '0' }}>
            {logs.map((log) => (
              <div key={log.id} style={{ padding: '1.25rem 2rem', borderBottom: '1px solid var(--border)', display: 'grid', gridTemplateColumns: '80px 1fr' }}>
                <span className="text-mono" style={{ color: '#94a3b8' }}>{log.time}</span>
                <div>
                   <span style={{ fontWeight: 600, fontSize: '0.9rem', color: log.status === 'success' ? '#10b981' : '#111827' }}>{log.action}</span>
                   <p style={{ color: '#475569', fontSize: '0.875rem', marginTop: '0.2rem' }}>{log.detail}</p>
                </div>
              </div>
            ))}
          </div>
        </section>

        <section>
          <h2 style={{ fontSize: '1rem', marginBottom: '1.5rem' }}>Recent Patches</h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div className="minimal-card" style={{ padding: '1.25rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                <Code size={16} color="#64748b" />
                <span className="text-small" style={{ fontWeight: 600 }}>Merge Request #42</span>
              </div>
              <p className="text-small">Migration of hardcoded secrets to vault.</p>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}

export default App;
