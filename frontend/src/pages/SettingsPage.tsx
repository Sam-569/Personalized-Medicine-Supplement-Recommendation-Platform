import React, { useEffect, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { User, Shield, Lock, LogOut, CheckCircle2, Sliders, RefreshCw, FileText } from 'lucide-react';
import { http, setToken, errMsg } from '../api';
import { MedicalDisclaimer } from '../components/MedicalDisclaimer';

export const SettingsPage: React.FC = () => {
  const [currentUser, setCurrentUser] = useState<any>(null);
  const [profile, setProfile] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [uRes, pRes] = await Promise.all([
          http.get('/auth/me'),
          http.get('/profile').catch(() => ({ data: null }))
        ]);
        setCurrentUser(uRes.data);
        setProfile(pRes.data);
      } catch (err: any) {
        setErrorMsg(errMsg(err));
      } finally {
        setIsLoading(false);
      }
    };
    fetchData();
  }, []);

  const handleLogout = async () => {
    try {
      await http.post('/auth/logout').catch(() => {});
    } finally {
      setToken(null);
      navigate('/');
    }
  };

  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center py-16 space-y-3">
        <RefreshCw className="h-8 w-8 text-teal-600 animate-spin" />
        <p className="text-sm text-slate-500">Loading account settings...</p>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-2xl space-y-8 py-4">
      {/* Account Details Card */}
      <div className="rounded-3xl border border-slate-200 bg-white p-6 sm:p-8 shadow-xs space-y-6">
        <div className="flex items-center gap-3 border-b border-slate-100 pb-4">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-teal-50 text-teal-700">
            <User className="h-5 w-5" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-slate-900">Account &amp; Privacy Settings</h1>
            <p className="text-xs text-slate-500">
              Manage your credentials, active session, and personal health data.
            </p>
          </div>
        </div>

        {/* Account Info */}
        <div className="space-y-4">
          <h2 className="text-xs font-bold text-slate-400 uppercase tracking-wider">
            User Account Details
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
            <div className="rounded-xl bg-slate-50 border border-slate-200/80 p-3">
              <span className="text-slate-400 block text-[11px]">Registered Email</span>
              <span className="font-semibold text-slate-900 text-sm mt-0.5 block">{currentUser?.email}</span>
            </div>
            <div className="rounded-xl bg-slate-50 border border-slate-200/80 p-3">
              <span className="text-slate-400 block text-[11px]">System Account ID</span>
              <span className="font-mono font-semibold text-slate-900 text-sm mt-0.5 block">USR-{currentUser?.id}</span>
            </div>
          </div>
        </div>

        {/* Health Profile Status */}
        <div className="space-y-3 border-t border-slate-100 pt-6">
          <h2 className="text-xs font-bold text-slate-400 uppercase tracking-wider">
            Profile Status
          </h2>
          <div className="flex items-center justify-between rounded-xl bg-slate-50 border border-slate-200/80 p-4">
            <div>
              <span className="font-semibold text-xs text-slate-900 block">
                {profile ? 'Health & Lifestyle Questionnaire Saved' : 'No Profile Saved'}
              </span>
              <p className="text-[11px] text-slate-500 mt-0.5">
                {profile
                  ? `Configured with ${profile.goals?.length || 0} goals and ${profile.dietary_preference} diet.`
                  : 'Complete your profile to enable personalized evaluations.'}
              </p>
            </div>
            <Link
              to="/profile"
              className="inline-flex items-center gap-1 rounded-lg bg-teal-700 px-3 py-1.5 text-xs font-semibold text-white hover:bg-teal-800 transition"
            >
              <Sliders className="h-3.5 w-3.5" />
              <span>{profile ? 'Edit' : 'Create'}</span>
            </Link>
          </div>
        </div>

        {/* Privacy & Data Protection Statement */}
        <div className="space-y-3 border-t border-slate-100 pt-6">
          <h2 className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
            <Shield className="h-4 w-4 text-teal-700" />
            <span>Health Privacy &amp; Data Ethics Policy</span>
          </h2>
          <div className="rounded-2xl border border-teal-100 bg-teal-50/40 p-4 text-xs text-slate-700 space-y-2 leading-relaxed">
            <p>
              In compliance with academic engineering standards (Group 101 SRS v1.0), this application treats user health criteria with the highest confidentiality:
            </p>
            <ul className="list-disc pl-4 space-y-1 text-slate-600">
              <li>
                <strong>No Generative Model Training:</strong> Your health goals, conditions, and allergies are never used to train or fine-tune AI models.
              </li>
              <li>
                <strong>Deterministic Processing:</strong> All recommendations are executed via transparent, rule-based backend algorithms without third-party API exposure.
              </li>
              <li>
                <strong>Strict Backend Authorization:</strong> Every profile snapshot and recommendation run is owned strictly by your account ID and inaccessible to other users.
              </li>
              <li>
                <strong>Password Security:</strong> Passwords are cryptographically salted and hashed using bcrypt. No plain text secrets are ever logged or transmitted.
              </li>
            </ul>
          </div>
        </div>

        {/* Logout action */}
        <div className="border-t border-slate-100 pt-6 flex justify-between items-center">
          <Link
            to="/dashboard"
            className="text-xs font-semibold text-slate-600 hover:text-slate-800"
          >
            &larr; Back to Dashboard
          </Link>
          <button
            type="button"
            onClick={handleLogout}
            className="inline-flex items-center gap-1.5 rounded-xl border border-rose-200 bg-rose-50 px-4 py-2 text-xs font-semibold text-rose-700 hover:bg-rose-100 transition cursor-pointer"
          >
            <LogOut className="h-4 w-4" />
            <span>Sign Out</span>
          </button>
        </div>
      </div>

      <MedicalDisclaimer compact />
    </div>
  );
};

