import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Clock, ArrowRight, RefreshCw, AlertCircle, FileCheck, ShieldCheck } from 'lucide-react';
import { http, errMsg } from '../api';
import { MedicalDisclaimer } from '../components/MedicalDisclaimer';

export const HistoryPage: React.FC = () => {
  const [history, setHistory] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState('');

  const fetchHistory = async () => {
    setIsLoading(true);
    try {
      const res = await http.get('/recommendations');
      setHistory(res.data || []);
    } catch (err: any) {
      setErrorMsg(errMsg(err));
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  return (
    <div className="space-y-8 py-4">
      <div className="rounded-3xl border border-slate-200 bg-white p-6 sm:p-8 shadow-xs">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-100 pb-4 mb-6">
          <div>
            <div className="inline-flex items-center gap-1.5 rounded-full bg-teal-50 px-2.5 py-0.5 text-xs font-semibold text-teal-800 mb-2">
              <Clock className="h-3.5 w-3.5" />
              <span>Audit Trail &amp; Reproducibility</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900">
              Recommendation Evaluation History
            </h1>
            <p className="mt-1 text-xs sm:text-sm text-slate-500 max-w-2xl">
              All previous recommendation runs are preserved as immutable, frozen profile snapshots alongside their exact dataset and rule versions.
            </p>
          </div>
          <span className="text-xs font-semibold text-slate-400">
            {history.length} runs recorded
          </span>
        </div>

        {errorMsg && (
          <div className="mb-6 flex items-start gap-2.5 rounded-xl border border-rose-200 bg-rose-50 p-3.5 text-xs text-rose-800">
            <AlertCircle className="h-4 w-4 shrink-0 text-rose-600 mt-0.5" />
            <span>{errorMsg}</span>
          </div>
        )}

        {isLoading ? (
          <div className="flex flex-col items-center justify-center py-16 space-y-3">
            <RefreshCw className="h-8 w-8 text-teal-600 animate-spin" />
            <p className="text-sm text-slate-500">Loading historical evaluations...</p>
          </div>
        ) : history.length === 0 ? (
          <div className="py-12 text-center space-y-3">
            <FileCheck className="h-10 w-10 text-slate-300 mx-auto" />
            <h3 className="text-base font-semibold text-slate-800">No recommendation evaluations yet</h3>
            <p className="text-xs text-slate-500 max-w-sm mx-auto">
              Once you complete your health profile and generate recommendations, each run will be archived here.
            </p>
            <div className="pt-2">
              <Link
                to="/dashboard"
                className="inline-flex items-center gap-1.5 rounded-xl bg-teal-700 px-4 py-2 text-xs font-semibold text-white hover:bg-teal-800 transition"
              >
                <span>Go to Dashboard</span>
                <ArrowRight className="h-3.5 w-3.5" />
              </Link>
            </div>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-slate-100 text-slate-400 uppercase tracking-wider text-[10px]">
                  <th className="py-3 px-3">Run ID</th>
                  <th className="py-3 px-3">Evaluation Timestamp</th>
                  <th className="py-3 px-3">Engine Status</th>
                  <th className="py-3 px-3 text-center">Results Count</th>
                  <th className="py-3 px-3">Rule Version</th>
                  <th className="py-3 px-3">Scoring Config</th>
                  <th className="py-3 px-3 text-right">View Report</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-slate-700">
                {history.map((r) => (
                  <tr key={r.run_id} className="hover:bg-slate-50/80 transition">
                    <td className="py-3.5 px-3 font-mono font-bold text-slate-900">#{r.run_id}</td>
                    <td className="py-3.5 px-3 text-slate-500">
                      {r.created_at ? new Date(r.created_at).toLocaleString() : 'N/A'}
                    </td>
                    <td className="py-3.5 px-3">
                      <span
                        className={`inline-block rounded-full px-2.5 py-0.5 text-[11px] font-medium ${
                          r.status === 'completed'
                            ? 'bg-emerald-50 text-emerald-800'
                            : r.status === 'no_eligible_results'
                            ? 'bg-amber-50 text-amber-800'
                            : 'bg-rose-50 text-rose-800'
                        }`}
                      >
                        {r.status.replaceAll('_', ' ')}
                      </span>
                    </td>
                    <td className="py-3.5 px-3 text-center font-bold text-slate-900">
                      {r.n_results}
                    </td>
                    <td className="py-3.5 px-3 font-mono text-[11px] text-slate-500">
                      {r.rule_version || 'v0.1-draft'}
                    </td>
                    <td className="py-3.5 px-3 font-mono text-[11px] text-slate-500">
                      {r.scoring_version || 'wsm-1'}
                    </td>
                    <td className="py-3.5 px-3 text-right">
                      <Link
                        to={`/runs/${r.run_id}`}
                        className="inline-flex items-center gap-1 font-semibold text-teal-700 hover:text-teal-800 hover:underline"
                      >
                        <span>Inspect Run</span>
                        <ArrowRight className="h-3.5 w-3.5" />
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <MedicalDisclaimer compact />
    </div>
  );
};

