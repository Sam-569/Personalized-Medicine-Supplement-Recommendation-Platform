import React from 'react';
import { Link } from 'react-router-dom';
import { ShieldCheck, Filter, Calculator, FileText, Database, ArrowRight, CheckCircle2, AlertOctagon } from 'lucide-react';
import { MedicalDisclaimer } from '../components/MedicalDisclaimer';
import { getToken } from '../api';

export const LandingPage: React.FC = () => {
  const token = getToken();

  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <section className="rounded-2xl border border-[#E5E5DD] bg-white p-8 sm:p-12 text-center shadow-2xs">
        <div className="inline-flex items-center gap-2 rounded-md border border-[#CBE3D4] bg-[#F0F7F3] px-3 py-1 text-xs font-semibold text-[#235E3F] mb-6">
          <ShieldCheck className="h-4 w-4 text-[#235E3F]" aria-hidden="true" />
          <span>B.Tech Capstone Project · Group 101 · SRS v1.0</span>
        </div>

        <h1 className="text-2xl sm:text-4xl font-extrabold tracking-tight text-[#252923] max-w-3xl mx-auto leading-tight">
          Personalized, Safety-First <span className="text-[#244B38]">Supplement Guidance</span>
        </h1>

        <p className="mt-4 text-sm sm:text-base text-[#73796F] max-w-2xl mx-auto leading-relaxed">
          An open-source platform helping you explore supplement types based on your health goals, dietary compatibility, and lifestyle — powered by a transparent, deterministic algorithm and curated scientific monographs.
        </p>

        <div className="mt-8 flex flex-wrap items-center justify-center gap-4">
          <Link
            to={token ? "/dashboard" : "/login"}
            className="inline-flex items-center gap-2 rounded-xl bg-teal-700 px-6 py-3.5 text-base font-semibold text-white shadow-sm hover:bg-teal-800 transition cursor-pointer"
          >
            <span>{token ? "Go to Dashboard" : "Get Started"}</span>
            <ArrowRight className="h-4 w-4" />
          </Link>
          <Link
            to="/catalogue"
            className="inline-flex items-center gap-2 rounded-xl border border-slate-300 bg-white px-6 py-3.5 text-base font-semibold text-slate-700 shadow-2xs hover:bg-slate-50 transition cursor-pointer"
          >
            <span>Explore Catalogue</span>
          </Link>
        </div>

        <div className="mt-8 flex flex-wrap justify-center items-center gap-6 text-xs text-slate-500 font-medium">
          <span className="flex items-center gap-1.5"><CheckCircle2 className="h-4 w-4 text-teal-600" /> Deterministic WSM Scoring</span>
          <span className="flex items-center gap-1.5"><CheckCircle2 className="h-4 w-4 text-teal-600" /> Safety Filtering Before Scoring</span>
          <span className="flex items-center gap-1.5"><CheckCircle2 className="h-4 w-4 text-teal-600" /> 100% Explainable Decisions</span>
          <span className="flex items-center gap-1.5"><CheckCircle2 className="h-4 w-4 text-teal-600" /> No Black-Box AI/ML</span>
        </div>
      </section>

      {/* How it Works Section */}
      <section className="space-y-6">
        <div className="text-center max-w-2xl mx-auto">
          <h2 className="text-2xl sm:text-3xl font-bold text-slate-900">How the Recommendation Engine Works</h2>
          <p className="mt-2 text-sm text-slate-600">
            Our recommendation pipeline strictly adheres to deterministic multi-criteria decision analysis (MCDA) in 6 well-defined stages:
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-2xs space-y-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-teal-50 text-teal-700 font-bold">1</div>
            <h3 className="font-semibold text-slate-900 text-base">Profile Validation</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Validates your health goals, dietary preferences, and safety answers. If essential safety information is unconfirmed or missing, recommendations are withheld pending completion.
            </p>
          </div>

          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-2xs space-y-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-rose-50 text-rose-700 font-bold">2</div>
            <h3 className="font-semibold text-slate-900 text-base">Safety Filtering (First!)</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Evaluates allergies, dietary incompatibilities, condition contraindications, and medication interactions. Incompatible items are permanently excluded and never reach scoring.
            </p>
          </div>

          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-2xs space-y-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-indigo-50 text-indigo-700 font-bold">3</div>
            <h3 className="font-semibold text-slate-900 text-base">Weighted Sum Model (WSM)</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Only eligible items are evaluated via the transparent formula:
              <br /><code className="mt-1 inline-block rounded bg-slate-100 px-2 py-0.5 text-[11px] font-mono text-slate-800">0.40G + 0.20D + 0.15A + 0.15L + 0.10H</code>
            </p>
          </div>

          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-2xs space-y-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-amber-50 text-amber-700 font-bold">4</div>
            <h3 className="font-semibold text-slate-900 text-base">Threshold Filtering</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Only candidates meeting or exceeding the configurable threshold (default <code className="bg-slate-100 px-1 py-0.5 rounded text-[11px]">0.60</code>) are retained. The threshold is never lowered automatically when results are sparse.
            </p>
          </div>

          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-2xs space-y-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-teal-50 text-teal-700 font-bold">5</div>
            <h3 className="font-semibold text-slate-900 text-base">Deterministic Ranking</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Candidates are ranked strictly by descending score. Ties are broken deterministically by Goal Match score, then Supplement ID, ensuring identical inputs always produce identical outputs.
            </p>
          </div>

          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-2xs space-y-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-purple-50 text-purple-700 font-bold">6</div>
            <h3 className="font-semibold text-slate-900 text-base">Rule-Based Explanations</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Every ranked supplement receives human-readable explanations based on verified criterion mappings, accompanied by a complete frozen snapshot of your profile for immutable history tracking.
            </p>
          </div>
        </div>
      </section>

      {/* Philosophy / Mentor Constraint Section */}
      <section className="rounded-2xl border border-slate-200 bg-white p-6 sm:p-8 space-y-4 shadow-xs">
        <h3 className="text-xl font-bold text-slate-900 flex items-center gap-2">
          <AlertOctagon className="h-5 w-5 text-teal-700" />
          <span>Core Engineering Principle: No Generative AI or Black-Box ML</span>
        </h3>
        <p className="text-sm text-slate-600 leading-relaxed">
          In healthcare informatics, explainability and reproducibility are paramount. This application adheres to the academic constraint that <strong>no machine learning models or large language models generate recommendations</strong>. Recommendations are derived solely from verified rules, controlled vocabularies, and scientific monographs published by the National Institutes of Health (NIH) Office of Dietary Supplements.
        </p>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
          <div className="rounded-xl bg-slate-50 border border-slate-200 p-4">
            <h4 className="font-semibold text-xs text-slate-900 uppercase tracking-wide">Global Safety Axiom (Rule R000)</h4>
            <p className="text-xs text-slate-600 mt-1 leading-relaxed">
              Unknown is never treated as safe. Any candidate supplement lacking a verified safety record is automatically routed to <em>Requires Review</em> and cannot be recommended as eligible.
            </p>
          </div>
          <div className="rounded-xl bg-slate-50 border border-slate-200 p-4">
            <h4 className="font-semibold text-xs text-slate-900 uppercase tracking-wide">Historical Snapshot Guarantee</h4>
            <p className="text-xs text-slate-600 mt-1 leading-relaxed">
              Each recommendation run stores a frozen JSON snapshot of your health profile along with exact dataset, rule, and scoring versions. Your historical results remain immutable over time.
            </p>
          </div>
        </div>
      </section>

      {/* Prominent Medical Disclaimer */}
      <MedicalDisclaimer />
    </div>
  );
};

