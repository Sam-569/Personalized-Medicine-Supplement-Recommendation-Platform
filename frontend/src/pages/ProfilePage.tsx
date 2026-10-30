import React, { useEffect, useState, useMemo } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import {
  Sliders,
  ShieldAlert,
  Heart,
  Activity,
  Check,
  ArrowRight,
  AlertCircle,
  CheckCircle2,
  RefreshCw,
  History,
  Info,
  ChevronDown,
} from 'lucide-react';
import { http, errMsg } from '../api';
import { MedicalDisclaimer } from '../components/MedicalDisclaimer';
import { Button } from '../components/ui/Button';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import { Alert } from '../components/ui/Alert';

interface FormState {
  age: string | number;
  goals: string[];
  dietary_preference: string;
  activity_level: string;
  sleep_quality: string;
  allergies: string[];
  existing_conditions: string[];
  current_medication_classes: string[];
  previous_usage: Record<string, { used: boolean; reaction: boolean }>;
  safety_confirmed: boolean;
}

const defaultForm: FormState = {
  age: '',
  goals: [],
  dietary_preference: 'omnivore',
  activity_level: 'light',
  sleep_quality: 'good',
  allergies: [],
  existing_conditions: [],
  current_medication_classes: [],
  previous_usage: {},
  safety_confirmed: false,
};

export const ProfilePage: React.FC = () => {
  const navigate = useNavigate();
  const [options, setOptions] = useState<any>(null);
  const [initialData, setInitialData] = useState<FormState | null>(null);
  const [form, setForm] = useState<FormState>(defaultForm);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');
  const [successMsg, setSuccessMsg] = useState('');
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});
  const [usageFilter, setUsageFilter] = useState('');

  // Fetch options and active user profile
  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      setErrorMsg('');
      try {
        const [optRes, profRes] = await Promise.all([
          http.get('/options'),
          http.get('/profile').catch(() => ({ data: null })),
        ]);
        setOptions(optRes.data);

        if (profRes.data) {
          const loaded: FormState = {
            age: profRes.data.age !== undefined && profRes.data.age !== null ? profRes.data.age : '',
            goals: Array.isArray(profRes.data.goals) ? profRes.data.goals : [],
            dietary_preference: profRes.data.dietary_preference || 'omnivore',
            activity_level: profRes.data.activity_level || 'light',
            sleep_quality: profRes.data.sleep_quality || 'good',
            allergies: Array.isArray(profRes.data.allergies) ? profRes.data.allergies : [],
            existing_conditions: Array.isArray(profRes.data.existing_conditions) ? profRes.data.existing_conditions : [],
            current_medication_classes: Array.isArray(profRes.data.current_medication_classes)
              ? profRes.data.current_medication_classes
              : [],
            previous_usage: profRes.data.previous_usage || {},
            safety_confirmed: Boolean(profRes.data.safety_confirmed),
          };
          setForm(loaded);
          setInitialData(loaded);
        } else {
          setInitialData(defaultForm);
        }
      } catch (err: any) {
        setErrorMsg(errMsg(err));
      } finally {
        setIsLoading(false);
      }
    };
    fetchData();
  }, []);

  // Determine if form has unsaved modifications
  const isDirty = useMemo(() => {
    if (!initialData) return false;
    return JSON.stringify(form) !== JSON.stringify(initialData);
  }, [form, initialData]);

  const toggleArrayItem = (field: 'goals' | 'allergies' | 'existing_conditions' | 'current_medication_classes', item: string) => {
    setFieldErrors((prev) => {
      const copy = { ...prev };
      delete copy[field];
      return copy;
    });

    const current = form[field];
    const next = current.includes(item)
      ? current.filter((x) => x !== item)
      : [...current, item];
    setForm({ ...form, [field]: next });
  };

  const handlePreviousUsageChange = (suppId: string, used: boolean, reaction: boolean) => {
    const updated = { ...form.previous_usage };
    if (!used && !reaction) {
      delete updated[suppId];
    } else {
      updated[suppId] = { used, reaction };
    }
    setForm({ ...form, previous_usage: updated });
  };

  const validateForm = (): boolean => {
    const errors: Record<string, string> = {};

    // Validate Age
    const ageNum = typeof form.age === 'number' ? form.age : parseInt(String(form.age), 10);
    if (isNaN(ageNum) || ageNum < 13 || ageNum > 120) {
      errors.age = 'Please enter a valid age between 13 and 120.';
    }

    // Validate Health Goals
    if (!form.goals || form.goals.length === 0) {
      errors.goals = 'Please select at least one health and wellness goal.';
    }

    // Validate Safety Confirmation
    if (!form.safety_confirmed) {
      errors.safety_confirmed = 'Mandatory safety declaration confirmation is required.';
    }

    setFieldErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg('');
    setSuccessMsg('');

    if (!validateForm()) {
      setErrorMsg('Please review the highlighted fields before saving your profile.');
      // Scroll to top of form smoothly
      window.scrollTo({ top: 0, behavior: 'smooth' });
      return;
    }

    setIsSaving(true);
    try {
      const ageNum = typeof form.age === 'number' ? form.age : parseInt(String(form.age), 10);
      const payload = {
        ...form,
        age: ageNum,
      };
      await http.put('/profile', payload);
      setInitialData(payload);
      setSuccessMsg('Your health profile has been saved successfully.');
      setTimeout(() => {
        navigate('/dashboard');
      }, 900);
    } catch (err: any) {
      setErrorMsg(errMsg(err));
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } finally {
      setIsSaving(false);
    }
  };

  // Filtered supplement list for Previous Usage section
  const filteredSupplements = useMemo(() => {
    if (!options?.supplements) return [];
    if (!usageFilter.trim()) return options.supplements;
    const q = usageFilter.toLowerCase();
    return options.supplements.filter(
      ([sid, sname]: [string, string]) =>
        sname.toLowerCase().includes(q) || sid.toLowerCase().includes(q)
    );
  }, [options?.supplements, usageFilter]);

  if (isLoading || !options) {
    return (
      <div className="space-y-5 animate-pulse max-w-4xl mx-auto" role="status" aria-label="Loading profile form">
        <div className="h-10 bg-white rounded-lg border border-[#E5E5DD]" />
        <div className="h-44 bg-white rounded-xl border border-[#E5E5DD]" />
        <div className="h-64 bg-white rounded-xl border border-[#E5E5DD]" />
        <div className="h-56 bg-white rounded-xl border border-[#E5E5DD]" />
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 pb-3 border-b border-[#E5E5DD]">
        <div>
          <h1 className="text-xl sm:text-2xl font-bold tracking-tight text-[#252923]">
            Health Profile Questionnaire
          </h1>
          <p className="text-xs text-[#73796F] mt-0.5">
            Configure your wellness goals, lifestyle parameters, and safety restrictions.
          </p>
        </div>

        <div className="flex items-center gap-2 self-start sm:self-auto">
          {isDirty && (
            <Badge variant="review" size="sm">
              Unsaved Changes
            </Badge>
          )}
          <Link to="/dashboard">
            <Button variant="ghost" size="sm">
              Back to Dashboard
            </Button>
          </Link>
        </div>
      </div>

      {/* Global Form Alerts */}
      {errorMsg && (
        <Alert variant="danger" title="Validation Error">
          <p>{errorMsg}</p>
        </Alert>
      )}

      {successMsg && (
        <Alert variant="success" title="Profile Saved">
          <p>{successMsg}</p>
        </Alert>
      )}

      {/* Main Profile Form */}
      <form onSubmit={handleSubmit} className="space-y-6" noValidate>
        {/* Section A: Basic Information */}
        <Card className="border-[#E5E5DD]">
          <CardHeader className="pb-3 border-b border-[#E5E5DD]">
            <CardTitle>Section 1: Basic Information</CardTitle>
            <CardDescription>
              Used for demographic eligibility ranges in accordance with NIH dietary guidelines.
            </CardDescription>
          </CardHeader>

          <CardContent className="p-5 sm:p-6 space-y-4">
            <div className="max-w-xs space-y-1.5">
              <label htmlFor="age" className="block text-xs font-semibold text-[#252923]">
                Your Age (years) <span className="text-[#9E2A2B]">*</span>
              </label>
              <input
                id="age"
                type="number"
                min={13}
                max={120}
                required
                value={form.age}
                onChange={(e) => {
                  setFieldErrors((prev) => {
                    const copy = { ...prev };
                    delete copy.age;
                    return copy;
                  });
                  setForm({ ...form, age: e.target.value });
                }}
                placeholder="e.g. 28"
                aria-invalid={Boolean(fieldErrors.age)}
                aria-describedby={fieldErrors.age ? 'age-error' : 'age-helper'}
                className={`w-full rounded-lg border bg-white py-2 px-3 text-sm text-[#252923] placeholder:text-[#9A9F96] transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#244B38] focus-visible:ring-offset-1 ${
                  fieldErrors.age ? 'border-[#9E2A2B] focus-visible:ring-[#9E2A2B]' : 'border-[#E5E5DD] hover:border-[#D0D0C5]'
                }`}
              />
              {fieldErrors.age ? (
                <p id="age-error" className="text-xs text-[#9E2A2B] font-medium">
                  {fieldErrors.age}
                </p>
              ) : (
                <p id="age-helper" className="text-xs text-[#73796F]">
                  Eligible adult range: 13 to 120 years.
                </p>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Section B: Health Goals */}
        <Card className="border-[#E5E5DD]">
          <CardHeader className="pb-3 border-b border-[#E5E5DD]">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-1">
              <div>
                <CardTitle>Section 2: Health and Wellness Goals</CardTitle>
                <CardDescription>
                  Select all health areas you wish to prioritize. Feeds Criterion G (0.40 weight).
                </CardDescription>
              </div>
              <span className="text-xs font-medium text-[#73796F]">
                {form.goals.length} selected <span className="text-[#9E2A2B]">*</span>
              </span>
            </div>
          </CardHeader>

          <CardContent className="p-5 sm:p-6 space-y-3">
            {fieldErrors.goals && (
              <p className="text-xs text-[#9E2A2B] font-medium" role="alert">
                {fieldErrors.goals}
              </p>
            )}

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2.5">
              {options.goals?.map(([gid, gname]: [string, string]) => {
                const isSelected = form.goals.includes(gid);
                return (
                  <button
                    type="button"
                    key={gid}
                    role="checkbox"
                    aria-checked={isSelected}
                    onClick={() => toggleArrayItem('goals', gid)}
                    className={`flex items-start justify-between gap-2.5 p-3 rounded-lg border text-left text-xs transition-colors cursor-pointer select-none ${
                      isSelected
                        ? 'border-[#244B38] bg-[#EEF3EE] text-[#244B38] font-semibold'
                        : 'border-[#E5E5DD] bg-white text-[#252923] hover:border-[#D0D0C5] hover:bg-[#F7F7F2]'
                    }`}
                  >
                    <div className="space-y-0.5 min-w-0">
                      <span className="block leading-snug">{gname}</span>
                      <span className="font-mono text-[10px] text-[#73796F] block">{gid}</span>
                    </div>

                    <div
                      className={`h-4 w-4 rounded shrink-0 flex items-center justify-center border transition-colors mt-0.5 ${
                        isSelected
                          ? 'border-[#244B38] bg-[#244B38] text-white'
                          : 'border-[#D0D0C5] bg-white'
                      }`}
                      aria-hidden="true"
                    >
                      {isSelected && <Check className="h-3 w-3" />}
                    </div>
                  </button>
                );
              })}
            </div>
          </CardContent>
        </Card>

        {/* Section C: Dietary Preferences and Lifestyle */}
        <Card className="border-[#E5E5DD]">
          <CardHeader className="pb-3 border-b border-[#E5E5DD]">
            <CardTitle>Section 3: Dietary Preference and Lifestyle</CardTitle>
            <CardDescription>
              Feeds Criterion D (Diet, 0.20), Criterion A (Activity, 0.15), and Criterion L (Sleep, 0.15).
            </CardDescription>
          </CardHeader>

          <CardContent className="p-5 sm:p-6 space-y-4">
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              {/* Dietary Preference */}
              <div className="space-y-1.5">
                <label htmlFor="diet" className="block text-xs font-semibold text-[#252923]">
                  Dietary Preference <span className="text-[#9E2A2B]">*</span>
                </label>
                <select
                  id="diet"
                  value={form.dietary_preference}
                  onChange={(e) => setForm({ ...form, dietary_preference: e.target.value })}
                  className="w-full rounded-lg border border-[#E5E5DD] bg-white py-2 px-3 text-xs text-[#252923] capitalize hover:border-[#D0D0C5] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#244B38] focus-visible:ring-offset-1"
                >
                  {options.diets?.map((d: string) => (
                    <option key={d} value={d}>
                      {d}
                    </option>
                  ))}
                </select>
                <p className="text-[11px] text-[#73796F]">
                  Incompatible formulations are excluded.
                </p>
              </div>

              {/* Activity Level */}
              <div className="space-y-1.5">
                <label htmlFor="activity" className="block text-xs font-semibold text-[#252923]">
                  Physical Activity Level <span className="text-[#9E2A2B]">*</span>
                </label>
                <select
                  id="activity"
                  value={form.activity_level}
                  onChange={(e) => setForm({ ...form, activity_level: e.target.value })}
                  className="w-full rounded-lg border border-[#E5E5DD] bg-white py-2 px-3 text-xs text-[#252923] capitalize hover:border-[#D0D0C5] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#244B38] focus-visible:ring-offset-1"
                >
                  {options.activity?.map((a: string) => (
                    <option key={a} value={a}>
                      {a}
                    </option>
                  ))}
                </select>
                <p className="text-[11px] text-[#73796F]">
                  Criterion A scoring match.
                </p>
              </div>

              {/* Sleep Quality */}
              <div className="space-y-1.5">
                <label htmlFor="sleep" className="block text-xs font-semibold text-[#252923]">
                  Sleep Quality <span className="text-[#9E2A2B]">*</span>
                </label>
                <select
                  id="sleep"
                  value={form.sleep_quality}
                  onChange={(e) => setForm({ ...form, sleep_quality: e.target.value })}
                  className="w-full rounded-lg border border-[#E5E5DD] bg-white py-2 px-3 text-xs text-[#252923] capitalize hover:border-[#D0D0C5] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#244B38] focus-visible:ring-offset-1"
                >
                  {options.sleep?.map((s: string) => (
                    <option key={s} value={s}>
                      {s}
                    </option>
                  ))}
                </select>
                <p className="text-[11px] text-[#73796F]">
                  Criterion L scoring match.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Section D: Safety Information and Contraindications */}
        <Card className="border-[#E5E5DD]">
          <CardHeader className="pb-3 border-b border-[#E5E5DD]">
            <CardTitle>Section 4: Safety Information and Contraindications</CardTitle>
            <CardDescription>
              Requested strictly to eliminate contraindicated candidates in Stage 2 before scoring.
            </CardDescription>
          </CardHeader>

          <CardContent className="p-5 sm:p-6 space-y-6">
            <div className="p-3 rounded-lg bg-[#F7F7F2] border border-[#E5E5DD] flex items-start gap-2.5 text-xs text-[#73796F]">
              <Info className="h-4 w-4 shrink-0 text-[#244B38] mt-0.5" />
              <p className="leading-relaxed">
                If none apply to you, leave the items unselected. Any selected allergen, medical condition, or medication class triggers verified safety exclusion rules.
              </p>
            </div>

            {/* Allergens */}
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="block text-xs font-semibold text-[#252923]">
                  Known Food and Formulation Allergens
                </span>
                <span className="text-[11px] text-[#73796F]">
                  {form.allergies.length === 0 ? 'None selected' : `${form.allergies.length} selected`}
                </span>
              </div>

              <div className="flex flex-wrap gap-2">
                {options.allergens?.map((a: string) => {
                  const isChecked = form.allergies.includes(a);
                  return (
                    <button
                      type="button"
                      key={a}
                      role="checkbox"
                      aria-checked={isChecked}
                      onClick={() => toggleArrayItem('allergies', a)}
                      className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border text-xs font-medium transition-colors capitalize cursor-pointer ${
                        isChecked
                          ? 'border-[#9E2A2B] bg-[#FDF2F2] text-[#9E2A2B] font-semibold'
                          : 'border-[#E5E5DD] bg-white text-[#252923] hover:bg-[#F7F7F2]'
                      }`}
                    >
                      {isChecked && <Check className="h-3 w-3" />}
                      <span>{a.replaceAll('_', ' ')}</span>
                    </button>
                  );
                })}
              </div>
            </div>

            <hr className="border-[#E5E5DD]" />

            {/* Pre-existing Conditions */}
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="block text-xs font-semibold text-[#252923]">
                  Pre-existing Clinical Conditions
                </span>
                <span className="text-[11px] text-[#73796F]">
                  {form.existing_conditions.length === 0 ? 'None selected' : `${form.existing_conditions.length} selected`}
                </span>
              </div>

              <div className="flex flex-wrap gap-2">
                {options.conditions?.map((c: string) => {
                  const isChecked = form.existing_conditions.includes(c);
                  return (
                    <button
                      type="button"
                      key={c}
                      role="checkbox"
                      aria-checked={isChecked}
                      onClick={() => toggleArrayItem('existing_conditions', c)}
                      className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border text-xs font-medium transition-colors capitalize cursor-pointer ${
                        isChecked
                          ? 'border-[#8A5C00] bg-[#FEF9EE] text-[#8A5C00] font-semibold'
                          : 'border-[#E5E5DD] bg-white text-[#252923] hover:bg-[#F7F7F2]'
                      }`}
                    >
                      {isChecked && <Check className="h-3 w-3" />}
                      <span>{c.replaceAll('_', ' ')}</span>
                    </button>
                  );
                })}
              </div>
            </div>

            <hr className="border-[#E5E5DD]" />

            {/* Current Medication Classes */}
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="block text-xs font-semibold text-[#252923]">
                  Current Prescription Medication Classes
                </span>
                <span className="text-[11px] text-[#73796F]">
                  {form.current_medication_classes.length === 0 ? 'None selected' : `${form.current_medication_classes.length} selected`}
                </span>
              </div>

              <div className="flex flex-wrap gap-2">
                {options.medication_classes?.map((m: string) => {
                  const isChecked = form.current_medication_classes.includes(m);
                  return (
                    <button
                      type="button"
                      key={m}
                      role="checkbox"
                      aria-checked={isChecked}
                      onClick={() => toggleArrayItem('current_medication_classes', m)}
                      className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border text-xs font-medium transition-colors capitalize cursor-pointer ${
                        isChecked
                          ? 'border-[#2B5876] bg-[#F1F6F9] text-[#2B5876] font-semibold'
                          : 'border-[#E5E5DD] bg-white text-[#252923] hover:bg-[#F7F7F2]'
                      }`}
                    >
                      {isChecked && <Check className="h-3 w-3" />}
                      <span>{m.replaceAll('_', ' ')}</span>
                    </button>
                  );
                })}
              </div>
            </div>

            <hr className="border-[#E5E5DD]" />

            {/* Previous Supplement Usage (Criterion H) */}
            <div className="space-y-3">
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
                <div>
                  <span className="block text-xs font-semibold text-[#252923]">
                    Previous Supplement Experience (Criterion H)
                  </span>
                  <p className="text-[11px] text-[#73796F]">
                    Items previously used with no reaction receive full weight (1.0). Reported adverse reactions flag the candidate for review.
                  </p>
                </div>

                <input
                  type="text"
                  placeholder="Filter supplements..."
                  value={usageFilter}
                  onChange={(e) => setUsageFilter(e.target.value)}
                  className="w-full sm:w-44 rounded-lg border border-[#E5E5DD] bg-white py-1.5 px-2.5 text-xs text-[#252923] placeholder:text-[#9A9F96] focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-[#244B38]"
                />
              </div>

              <div className="rounded-lg border border-[#E5E5DD] bg-[#F7F7F2]/40 divide-y divide-[#E5E5DD] max-h-56 overflow-y-auto">
                {filteredSupplements.length === 0 ? (
                  <p className="p-3 text-xs text-[#73796F] text-center">No matching supplements found.</p>
                ) : (
                  filteredSupplements.map(([sid, sname]: [string, string]) => {
                    const entry = form.previous_usage[sid] || { used: false, reaction: false };
                    return (
                      <div key={sid} className="p-2.5 sm:px-3 flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-xs">
                        <span className="font-medium text-[#252923] truncate" title={sname}>
                          {sname}
                        </span>

                        <div className="flex items-center gap-4 shrink-0">
                          <label className="flex items-center gap-1.5 text-[#5A6056] cursor-pointer">
                            <input
                              type="checkbox"
                              checked={entry.used}
                              onChange={(e) =>
                                handlePreviousUsageChange(sid, e.target.checked, entry.reaction)
                              }
                              className="rounded border-[#E5E5DD] text-[#244B38] focus:ring-[#244B38]"
                            />
                            <span>Used previously</span>
                          </label>

                          {entry.used && (
                            <label className="flex items-center gap-1.5 text-[#9E2A2B] font-medium cursor-pointer">
                              <input
                                type="checkbox"
                                checked={entry.reaction}
                                onChange={(e) =>
                                  handlePreviousUsageChange(sid, true, e.target.checked)
                                }
                                className="rounded border-[#E5E5DD] text-[#9E2A2B] focus:ring-[#9E2A2B]"
                              />
                              <span>Had adverse reaction</span>
                            </label>
                          )}
                        </div>
                      </div>
                    );
                  })
                )}
              </div>
            </div>

            <hr className="border-[#E5E5DD]" />

            {/* Mandatory Safety Confirmation Checkbox */}
            <div className={`p-4 rounded-xl border transition-colors ${
              fieldErrors.safety_confirmed ? 'border-[#9E2A2B] bg-[#FDF2F2]' : 'border-[#E5E5DD] bg-[#F7F7F2]'
            }`}>
              <label className="flex items-start gap-3 cursor-pointer select-none">
                <input
                  type="checkbox"
                  required
                  checked={form.safety_confirmed}
                  onChange={(e) => {
                    setFieldErrors((prev) => {
                      const copy = { ...prev };
                      delete copy.safety_confirmed;
                      return copy;
                    });
                    setForm({ ...form, safety_confirmed: e.target.checked });
                  }}
                  className="mt-0.5 h-4 w-4 rounded border-[#E5E5DD] text-[#244B38] focus:ring-[#244B38] shrink-0"
                />
                <div className="space-y-1">
                  <span className="text-xs font-bold text-[#252923] block leading-snug">
                    Mandatory Safety Review Confirmation <span className="text-[#9E2A2B]">*</span>
                  </span>
                  <p className="text-xs text-[#5A6056] leading-relaxed">
                    I confirm that I have reviewed the three safety categories above (allergies, health conditions, and medication types). I understand that this information is used strictly to filter contraindicated supplements and does not constitute clinical clearance or personalized prescription.
                  </p>
                  {!form.safety_confirmed && (
                    <p className="text-[11px] text-[#8A5C00] font-medium pt-0.5">
                      Note: Recommendation runs are automatically withheld by the engine if safety confirmation is unconfirmed (Rule R000).
                    </p>
                  )}
                </div>
              </label>

              {fieldErrors.safety_confirmed && (
                <p className="text-xs text-[#9E2A2B] font-medium mt-2 pl-7" role="alert">
                  {fieldErrors.safety_confirmed}
                </p>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Form Submission Actions */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 pt-2 pb-4">
          <div className="text-xs text-[#73796F]">
            {isDirty ? (
              <span className="text-[#8A5C00] font-medium">You have unsaved changes. Remember to click Save Profile.</span>
            ) : (
              <span>All changes are saved.</span>
            )}
          </div>

          <div className="flex items-center gap-3 justify-end">
            <Link to="/dashboard">
              <Button type="button" variant="secondary" size="md">
                Cancel
              </Button>
            </Link>

            <Button
              type="submit"
              variant="primary"
              size="md"
              disabled={isSaving}
              isLoading={isSaving}
              rightIcon={!isSaving ? <ArrowRight className="h-4 w-4" /> : undefined}
            >
              {isSaving ? 'Saving Profile...' : 'Save Profile'}
            </Button>
          </div>
        </div>
      </form>

      {/* Regulatory Notice */}
      <MedicalDisclaimer compact />
    </div>
  );
};
