import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import {
  Sparkles, ShieldAlert, AlertTriangle, CheckCircle2,
  RefreshCw, ArrowLeft, Info, ExternalLink, HelpCircle
} from 'lucide-react';
import { http, errMsg } from '../api';
import { MedicalDisclaimer } from '../components/MedicalDisclaimer';

export const ResultsPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [run, setRun] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState('');

  useEffect(() => {
    const fetchRun = async () => {
      setIsLoading(true);
      setErrorMsg('');
      try {
        const res = await http.get(`/recommendations/${id}`);
        setRun(res.data);
      } catch (err: any) {
        setErrorMsg(errMsg(err));
      } finally {
        setIsLoading(false);
      }
    };
    if (id) {
      fetchRun();
    }
  }, [id]);

  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center py-20 space-y-3">
        <RefreshCw className="h-8 w-8 text-teal-600 animate-spin" />
        <p className="text-sm text-slate-500">Retrieving recommendation run #{id}...</p>
      </div>
    );
  }

  if (errorMsg || !run) {
    return (
      <div className="mx-auto max-w-xl py-12 text-center space-y-4">
        <div className="rounded-3xl border border-rose-200 bg-rose-50 p-6 text-rose-800">
          <AlertTriangle className="h-8 w-8 mx-auto text-rose-600 mb-2" />
          <h2 className="text-base font-bold">Failed to load recommendation run</h2>
          <p className="text-xs mt-1">{errorMsg || 'Run not found or unauthorized.'}</p>
        </div>
        <Link
          to="/dashboard"
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-teal-700 hover:underline"
        >
          <ArrowLeft className="h-4 w-4" />
          <span>Return to Dashboard</span>
        </Link>
      </div>
    );
  }

  const eligibleResults = run.results || [];
  const excludedItems = run.excluded || [];
  const reviewItems = run.needs_review || [];

  const displayedResults = eligibleResults.slice(0, 5);

  return (
    <div className="space-y-8 py-4">
      {/* Header card with run metadata */}
      <div className="rounded-3xl border border-slate-200 bg-white p-6 sm:p-8 shadow-xs">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-100 pb-4 mb-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="font-mono text-xs font-bold text-teal-700 bg-teal-50 px-2.5 py-1 rounded-md">
                Run #{run.run_id}
              </span>
              <span
                className={`rounded-full px-2.5 py-0.5 text-xs font-semibold ${
                  run.status === 'completed'
                    ? 'bg-emerald-50 text-emerald-800'
                    : run.status === 'no_eligible_results'
                    ? 'bg-amber-50 text-amber-800'
                    : 'bg-rose-50 text-rose-800'
                }`}
              >
                {run.status.replaceAll('_', ' ')}
              </span>
              <span className="rounded-full bg-teal-50 border border-teal-200 text-teal-800 px-2.5 py-0.5 text-xs font-semibold">
                Top 5 Recommendations
              </span>
            </div>
            <h1 className="text-2xl font-extrabold text-slate-900 mt-2">
              Recommendation Evaluation Results
            </h1>
            <p className="text-xs text-slate-400 mt-0.5">
              Evaluated on {run.created_at ? new Date(run.created_at).toLocaleString() : 'N/A'} · Dataset {run.dataset_version} · Scoring {run.scoring_version} · Cutoff Threshold {run.threshold}
            </p>
          </div>

          <Link
            to="/history"
            className="inline-flex items-center gap-1 text-xs font-semibold text-slate-600 hover:text-slate-900"
          >
            <ArrowLeft className="h-4 w-4" />
            <span>History</span>
          </Link>
        </div>

        {/* Explainability explanation banner */}
        <div className="rounded-xl bg-slate-50 border border-slate-200/80 p-3.5 text-xs text-slate-600 space-y-1">
          <div className="flex items-center gap-1.5 font-semibold text-slate-800">
            <Info className="h-4 w-4 text-teal-600" />
            <span>Transparent Weighted Sum Model (WSM) Scoring & Top 5 Focus</span>
          </div>
          <p className="leading-relaxed">
            Relevance Score = <code className="bg-white px-1.5 py-0.5 rounded border border-slate-200 font-mono text-[11px]">0.40G + 0.20D + 0.15A + 0.15L + 0.10H</code>. Only candidate supplements that satisfy all safety checks and achieve a score &ge; {run.threshold} proceed to ranking. The system strictly selects the <strong>Top 5</strong> highest-scoring supplements to maintain a focused, clinically viable regimen.
          </p>
        </div>
      </div>

      {/* When profile was incomplete */}
      {run.status === 'withheld_incomplete_profile' && (
        <div className="rounded-3xl border border-rose-200 bg-rose-50 p-6 sm:p-8 space-y-3">
          <div className="flex items-center gap-2 text-rose-800 font-bold">
            <AlertTriangle className="h-5 w-5 text-rose-600" />
            <h2 className="text-base">Recommendations Withheld Pending Complete Safety Information</h2>
          </div>
          <p className="text-xs text-rose-700 leading-relaxed">
            Our safety-first architecture requires explicit responses to all allergy, condition, and medication questions before candidates can be scored. Missing attributes: <strong>{run.missing_fields?.join(', ')}</strong>.
          </p>
          <Link
            to="/profile"
            className="inline-flex items-center gap-2 rounded-xl bg-rose-700 px-4 py-2 text-xs font-semibold text-white shadow-xs hover:bg-rose-800 transition"
          >
            <span>Update Profile Questionnaire</span>
          </Link>
        </div>
      )}

      {/* Eligible Recommendations */}
      {displayedResults.length > 0 ? (
        <div className="space-y-4">
          <div>
            <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
              <CheckCircle2 className="h-5 w-5 text-emerald-600" />
              <span>
                Top {displayedResults.length} Eligible Recommendations
                {run.total_eligible && run.total_eligible > displayedResults.length && (
                  <span className="text-xs font-normal text-slate-500 ml-1.5">
                    (Selected from {run.total_eligible} qualifying candidates)
                  </span>
                )}
              </span>
            </h2>
            <p className="text-xs text-slate-500 mt-0.5">
              Top 5 ranked supplements satisfying all safety rules and achieving WSM relevance score &ge; {run.threshold}.
            </p>
          </div>

          <div className="space-y-4">
            {displayedResults.map((item: any) => (

              <div
                key={item.supplement_id}
                className="rounded-3xl border border-slate-200 bg-white p-6 shadow-xs space-y-5"
              >
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 pb-4">
                  <div className="flex items-center gap-3">
                    <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-teal-700 font-extrabold text-white text-sm">
                      #{item.rank}
                    </span>
                    <div>
                      <h3 className="text-xl font-bold text-slate-900">{item.name}</h3>
                      <span className="font-mono text-xs text-slate-400">ID: {item.supplement_id}</span>
                    </div>
                  </div>

                  <div className="text-right">
                    <span className="text-xs text-slate-500 block">Relevance Score</span>
                    <span className="text-2xl font-extrabold text-teal-800">
                      {(item.score * 100).toFixed(1)}%{' '}
                      <span className="text-sm font-semibold text-slate-400">({item.score.toFixed(3)})</span>
                    </span>
                  </div>
                </div>

                {/* Score bar */}
                <div className="space-y-1">
                  <div className="h-2.5 w-full rounded-full bg-slate-100 overflow-hidden">
                    <div
                      className="h-full rounded-full bg-teal-700 transition-all duration-500"
                      style={{ width: `${Math.min(100, item.score * 100)}%` }}
                    />
                  </div>
                </div>

                {/* Criteria breakdown */}
                <div>
                  <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">
                    Multi-Criteria WSM Breakdown
                  </h4>
                  <div className="grid grid-cols-2 sm:grid-cols-5 gap-2 text-xs">
                    <div className="rounded-xl bg-slate-50 border border-slate-200/80 p-2 text-center">
                      <span className="text-slate-400 block text-[10px]">Goal Match (40%)</span>
                      <span className="font-mono font-bold text-slate-900 block mt-0.5">
                        {item.values?.G?.toFixed(2)}
                      </span>
                      <span className="text-[10px] text-teal-700">+{item.contributions?.G?.toFixed(3)}</span>
                    </div>
                    <div className="rounded-xl bg-slate-50 border border-slate-200/80 p-2 text-center">
                      <span className="text-slate-400 block text-[10px]">Dietary Fit (20%)</span>
                      <span className="font-mono font-bold text-slate-900 block mt-0.5">
                        {item.values?.D?.toFixed(2)}
                      </span>
                      <span className="text-[10px] text-teal-700">+{item.contributions?.D?.toFixed(3)}</span>
                    </div>
                    <div className="rounded-xl bg-slate-50 border border-slate-200/80 p-2 text-center">
                      <span className="text-slate-400 block text-[10px]">Activity Fit (15%)</span>
                      <span className="font-mono font-bold text-slate-900 block mt-0.5">
                        {item.values?.A?.toFixed(2)}
                      </span>
                      <span className="text-[10px] text-teal-700">+{item.contributions?.A?.toFixed(3)}</span>
                    </div>
                    <div className="rounded-xl bg-slate-50 border border-slate-200/80 p-2 text-center">
                      <span className="text-slate-400 block text-[10px]">Sleep / Lifestyle (15%)</span>
                      <span className="font-mono font-bold text-slate-900 block mt-0.5">
                        {item.values?.L?.toFixed(2)}
                      </span>
                      <span className="text-[10px] text-teal-700">+{item.contributions?.L?.toFixed(3)}</span>
                    </div>
                    <div className="rounded-xl bg-slate-50 border border-slate-200/80 p-2 text-center">
                      <span className="text-slate-400 block text-[10px]">Prior Usage (10%)</span>
                      <span className="font-mono font-bold text-slate-900 block mt-0.5">
                        {item.values?.H?.toFixed(2)}
                      </span>
                      <span className="text-[10px] text-teal-700">+{item.contributions?.H?.toFixed(3)}</span>
                    </div>
                  </div>
                </div>

                {/* Predefined Rule-based Explanations */}
                <div className="rounded-2xl bg-teal-50/50 border border-teal-100 p-4 space-y-2">
                  <h4 className="text-xs font-bold text-teal-900 uppercase tracking-wider flex items-center gap-1.5">
                    <Info className="h-3.5 w-3.5 text-teal-700" />
                    <span>Deterministic Explanation</span>
                  </h4>
                  <ul className="space-y-1.5 text-xs text-slate-700 list-disc pl-4">
                    {item.explanation?.map((exp: string, idx: number) => (
                      <li key={idx} className="leading-relaxed">
                        {exp}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            ))}
          </div>
        </div>
      ) : (
        run.status !== 'withheld_incomplete_profile' && (
          <div className="rounded-3xl border border-slate-200 bg-white p-8 text-center space-y-3">
            <HelpCircle className="h-10 w-10 text-slate-400 mx-auto" />
            <h3 className="text-lg font-bold text-slate-900">No Eligible Recommendations Found</h3>
            <p className="text-xs text-slate-600 max-w-xl mx-auto leading-relaxed">
              No supplement in the knowledge base passed all safety filters and achieved a WSM score &ge; {run.threshold}. 
              In accordance with safety requirements, <strong>the threshold is never lowered automatically</strong> when candidate rows are unverified or non-matching.
            </p>
          </div>
        )
      )}

      {/* Needs Review Section */}
      {reviewItems.length > 0 && (
        <div className="rounded-3xl border border-amber-200 bg-white p-6 shadow-xs space-y-4">
          <div className="flex items-center gap-2 text-amber-900 font-bold border-b border-amber-100 pb-3">
            <AlertTriangle className="h-5 w-5 text-amber-600" />
            <h2 className="text-base">Requires Professional Review (Not Recommended) — {reviewItems.length} items</h2>
          </div>
          <p className="text-xs text-slate-600">
            Under Global Rule R000 and clinical caution rules, items with unverified candidate records or uncertain drug interactions cannot be suggested as eligible.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {reviewItems.map((r: any) => (
              <div
                key={r.supplement_id}
                className="rounded-xl border border-amber-100 bg-amber-50/50 p-3 text-xs space-y-1"
              >
                <div className="flex items-center justify-between font-bold text-amber-950">
                  <span>{r.name || r.supplement_id}</span>
                  <span className="font-mono text-[10px] text-amber-700">{r.supplement_id}</span>
                </div>
                <div className="space-y-0.5 text-amber-900">
                  {r.reasons?.map((reason: any, idx: number) => (
                    <p key={idx} className="text-[11px] leading-tight">
                      &bull; <strong>{reason[0]}:</strong> {reason[1]}
                    </p>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Safety Excluded Section */}
      {excludedItems.length > 0 && (
        <div className="rounded-3xl border border-rose-200 bg-white p-6 shadow-xs space-y-4">
          <div className="flex items-center gap-2 text-rose-900 font-bold border-b border-rose-100 pb-3">
            <ShieldAlert className="h-5 w-5 text-rose-600" />
            <h2 className="text-base">Excluded by Safety Contraindication Rules — {excludedItems.length} items</h2>
          </div>
          <p className="text-xs text-slate-600">
            Permanently disqualified during Stage 2 safety filtering due to verified conflicts with your allergies, dietary preferences, or medical conditions.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {excludedItems.map((ex: any) => (
              <div
                key={ex.supplement_id}
                className="rounded-xl border border-rose-100 bg-rose-50/50 p-3 text-xs space-y-1"
              >
                <div className="flex items-center justify-between font-bold text-rose-950">
                  <span>{ex.name || ex.supplement_id}</span>
                  <span className="font-mono text-[10px] text-rose-700">{ex.supplement_id}</span>
                </div>
                <div className="space-y-0.5 text-rose-900">
                  {ex.reasons?.map((reason: any, idx: number) => (
                    <p key={idx} className="text-[11px] leading-tight">
                      &bull; <strong>{reason[0]}:</strong> {reason[1]}
                    </p>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      <MedicalDisclaimer />
    </div>
  );
};

