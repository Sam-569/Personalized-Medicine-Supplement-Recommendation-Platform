import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  ArrowRight,
  BookOpen,
  Clock,
  Sliders,
  Sparkles,
  RefreshCw,
  ShieldAlert,
  Check,
  X,
  ChevronDown,
  Info,
} from 'lucide-react';
import { http, errMsg } from '../api';
import { MedicalDisclaimer } from '../components/MedicalDisclaimer';
import { Button } from '../components/ui/Button';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import { Alert } from '../components/ui/Alert';

interface ProfileSummary {
  isComplete: boolean;
  hasSafetyConfirmed: boolean;
  missingFields: string[];
  goalsCount: number;
  diet: string;
  activity: string;
  sleep: string;
  age: number | null;
  allergiesCount: number;
  conditionsCount: number;
  medicationsCount: number;
}

function evaluateProfile(profile: any): ProfileSummary {
  if (!profile) {
    return {
      isComplete: false,
      hasSafetyConfirmed: false,
      missingFields: ['Health goals', 'Age', 'Dietary preference', 'Activity level', 'Sleep quality', 'Safety confirmation'],
      goalsCount: 0,
      diet: '',
      activity: '',
      sleep: '',
      age: null,
      allergiesCount: 0,
      conditionsCount: 0,
      medicationsCount: 0,
    };
  }

  const missing: string[] = [];
  if (!profile.goals || profile.goals.length === 0) missing.push('Health goals');
  if (typeof profile.age !== 'number' || profile.age < 13 || profile.age > 120) missing.push('Age');
  if (!profile.dietary_preference) missing.push('Dietary preference');
  if (!profile.activity_level) missing.push('Activity level');
  if (!profile.sleep_quality) missing.push('Sleep quality');
  if (!profile.safety_confirmed) missing.push('Safety confirmation');

  return {
    isComplete: missing.length === 0,
    hasSafetyConfirmed: Boolean(profile.safety_confirmed),
    missingFields: missing,
    goalsCount: Array.isArray(profile.goals) ? profile.goals.length : 0,
    diet: profile.dietary_preference || '',
    activity: profile.activity_level || '',
    sleep: profile.sleep_quality || '',
    age: typeof profile.age === 'number' ? profile.age : null,
    allergiesCount: Array.isArray(profile.allergies) ? profile.allergies.length : 0,
    conditionsCount: Array.isArray(profile.existing_conditions) ? profile.existing_conditions.length : 0,
    medicationsCount: Array.isArray(profile.current_medication_classes) ? profile.current_medication_classes.length : 0,
  };
}

function formatDate(dateStr: string): string {
  if (!dateStr) return 'None';
  try {
    const d = new Date(dateStr);
    return new Intl.DateTimeFormat('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: 'numeric',
      minute: '2-digit',
    }).format(d);
  } catch {
    return dateStr;
  }
}

export const DashboardPage: React.FC = () => {
  const [profile, setProfile] = useState<any>(null);
  const [history, setHistory] = useState<any[]>([]);
  const [options, setOptions] = useState<any>(null);
  const [currentUser, setCurrentUser] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isGenerating, setIsGenerating] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');
  const navigate = useNavigate();

  const loadData = async () => {
    setIsLoading(true);
    setErrorMsg('');
    try {
      const [uRes, pRes, hRes, oRes] = await Promise.all([
        http.get('/auth/me').catch(() => ({ data: null })),
        http.get('/profile').catch(() => ({ data: null })),
        http.get('/recommendations').catch(() => ({ data: [] })),
        http.get('/options').catch(() => ({ data: null })),
      ]);
      setCurrentUser(uRes.data);
      setProfile(pRes.data);
      setHistory(hRes.data || []);
      setOptions(oRes.data);
    } catch (err: any) {
      setErrorMsg(errMsg(err));
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleGenerate = async () => {
    if (!profile) {
      setErrorMsg('Please complete your health profile before generating recommendations.');
      return;
    }
    setErrorMsg('');
    setIsGenerating(true);
    try {
      const res = await http.post('/recommendations?limit=5');
      if (res.data?.run_id) {
        navigate(`/runs/${res.data.run_id}`);
      }
    } catch (err: any) {
      setErrorMsg(errMsg(err));
    } finally {
      setIsGenerating(false);
    }
  };

  const goalNameMap: Record<string, string> = {};
  if (options?.goals) {
    options.goals.forEach(([gid, gname]: [string, string]) => {
      goalNameMap[gid] = gname;
    });
  }

  const profileSummary = evaluateProfile(profile);
  const latestRun = history.length > 0 ? history[0] : null;

  // Loading skeleton
  if (isLoading) {
    return (
      <div className="space-y-5 animate-pulse" role="status" aria-label="Loading dashboard">
        <div className="h-10 bg-white rounded-lg border border-[#E5E5DD]" />
        <div className="h-28 bg-white rounded-xl border border-[#E5E5DD]" />
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
          <div className="lg:col-span-2 h-72 bg-white rounded-xl border border-[#E5E5DD]" />
          <div className="h-72 bg-white rounded-xl border border-[#E5E5DD]" />
        </div>
        <div className="h-48 bg-white rounded-xl border border-[#E5E5DD]" />
      </div>
    );
  }

  return (
    <div className="space-y-5">
      {/* 1. Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 pb-3 border-b border-[#E5E5DD]">
        <div>
          <h1 className="text-xl sm:text-2xl font-bold tracking-tight text-[#252923]">
            Dashboard
          </h1>
          <p className="text-xs text-[#73796F] mt-0.5">
            Your supplement profile and recommendations.
          </p>
        </div>

        {currentUser?.email && (
          <div className="text-xs text-[#73796F] self-start sm:self-auto">
            Signed in as <span className="font-medium text-[#252923]">{currentUser.email}</span>
          </div>
        )}
      </div>

      {/* Actionable Error Banner */}
      {errorMsg && (
        <Alert variant="danger" title="Operation Failed">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <span>{errorMsg}</span>
            <Button
              variant="outline"
              size="sm"
              onClick={loadData}
              leftIcon={<RefreshCw className="h-3 w-3" />}
            >
              Retry
            </Button>
          </div>
        </Alert>
      )}

      {/* Actionable Notice: Incomplete Profile */}
      {!profile && (
        <Alert variant="warning" title="Action Required: Incomplete Profile">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <p>
              Your health profile has not been completed. Recommendations require recorded goals, dietary fit, and safety confirmation.
            </p>
            <Link to="/profile" className="shrink-0">
              <Button variant="primary" size="sm" rightIcon={<ArrowRight className="h-3.5 w-3.5" />}>
                Complete Profile
              </Button>
            </Link>
          </div>
        </Alert>
      )}

      {/* Actionable Notice: Safety Affirmation Unconfirmed */}
      {profile && !profileSummary.hasSafetyConfirmed && (
        <Alert variant="warning" title="Safety Notice: Confirmation Required">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <p>
              Your wellness profile is recorded, but safety confirmation is currently unconfirmed. Under Rule R000, recommendation runs withhold unconfirmed evaluations.
            </p>
            <Link to="/profile" className="shrink-0">
              <Button variant="secondary" size="sm" rightIcon={<ArrowRight className="h-3.5 w-3.5" />}>
                Confirm Safety Declaration
              </Button>
            </Link>
          </div>
        </Alert>
      )}

      {/* 2. Refined Recommendation Action Banner */}
      <Card className="border-[#E5E5DD]">
        <div className="p-5 sm:p-6 space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div className="space-y-1">
              <h2 className="text-base font-bold text-[#252923]">
                Supplement Recommendations
              </h2>
              <p className="text-xs text-[#73796F]">
                Evaluate candidates against your health criteria using verified NIH ODS monographs and deterministic safety rules.
              </p>
            </div>

            <div className="flex flex-wrap items-center gap-2.5 shrink-0">
              {latestRun && (
                <Link to={`/runs/${latestRun.run_id}`}>
                  <Button variant="secondary" size="md">
                    View Latest Results (#{latestRun.run_id})
                  </Button>
                </Link>
              )}

              <Button
                variant="primary"
                size="md"
                onClick={handleGenerate}
                disabled={!profile || isGenerating}
                isLoading={isGenerating}
                leftIcon={!isGenerating ? <Sparkles className="h-4 w-4" /> : undefined}
              >
                {isGenerating ? 'Evaluating Candidates...' : 'Generate Recommendations'}
              </Button>
            </div>
          </div>

          {/* Expandable Technical Details */}
          <details className="group border-t border-[#E5E5DD] pt-3 text-xs text-[#73796F]">
            <summary className="flex items-center gap-1.5 font-medium text-[#244B38] hover:text-[#1B382A] select-none cursor-pointer list-none">
              <ChevronDown className="h-3.5 w-3.5 transition-transform group-open:rotate-180" />
              <span>How recommendations work</span>
            </summary>
            <div className="mt-2.5 p-3 rounded-lg bg-[#F7F7F2] border border-[#E5E5DD] space-y-2 text-xs leading-relaxed text-[#5A6056]">
              <p>
                <strong>Scoring Methodology:</strong> Evaluated candidates are ranked deterministically using a Weighted Sum Model (WSM) across five criteria:
                <code className="block mt-1 font-mono text-[11px] bg-white border border-[#E5E5DD] px-2 py-1 rounded text-[#252923]">
                  Score = 0.40(Goal) + 0.20(Diet) + 0.15(Activity) + 0.15(Lifestyle) + 0.10(Usage)
                </code>
              </p>
              <p>
                <strong>Cutoff Threshold & Top 5 Focus:</strong> Only candidates achieving a relevance score &ge; 0.60 proceed to ranking. Rather than returning an unbounded list of supplements, the system always selects and presents the <strong>Top 5</strong> highest-scoring candidates to keep guidance focused, practical, and safe.
              </p>
              <p>
                <strong>Rule R000 Safety Axiom:</strong> Any supplement lacking a verified safety monograph or missing compatibility data is routed to review and disqualified from automatic recommendation.
              </p>
            </div>
          </details>
        </div>
      </Card>

      {/* 3. Main Grid: Health Profile & Evaluation Audit */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
        {/* Health Profile Summary (2 Columns on Desktop) */}
        <Card className="lg:col-span-2 border-[#E5E5DD] flex flex-col justify-between">
          <div>
            <div className="p-5 pb-4 border-b border-[#E5E5DD] flex items-center justify-between gap-3">
              <div className="flex items-center gap-2.5">
                <Sliders className="h-4 w-4 text-[#244B38]" />
                <h3 className="text-base font-bold text-[#252923]">Health Profile</h3>
              </div>

              {profileSummary.isComplete ? (
                <Badge variant="safe" size="sm" icon={true}>
                  Profile Complete
                </Badge>
              ) : profile ? (
                <Badge variant="review" size="sm" icon={true}>
                  Action Required
                </Badge>
              ) : (
                <Badge variant="excluded" size="sm" icon={true}>
                  Incomplete Profile
                </Badge>
              )}
            </div>

            <div className="p-5 space-y-5">
              {profile ? (
                <>
                  {/* Subsection A: Health Goals */}
                  <div className="space-y-2">
                    <span className="text-[11px] font-bold uppercase tracking-wider text-[#73796F] block">
                      Target Health Goals ({profileSummary.goalsCount})
                    </span>

                    {profile.goals && profile.goals.length > 0 ? (
                      <div className="flex flex-wrap gap-1.5">
                        {profile.goals.map((g: string) => (
                          <span
                            key={g}
                            className="inline-flex items-center rounded-md bg-[#EEF3EE] border border-[#CBE3D4] px-2.5 py-1 text-xs font-medium text-[#244B38]"
                          >
                            {goalNameMap[g] || g}
                          </span>
                        ))}
                      </div>
                    ) : (
                      <p className="text-xs text-[#9E2A2B]">No health goals selected.</p>
                    )}
                  </div>

                  <hr className="border-[#E5E5DD]" />

                  {/* Subsection B: Lifestyle & Demographics Grid */}
                  <div className="space-y-2">
                    <span className="text-[11px] font-bold uppercase tracking-wider text-[#73796F] block">
                      Lifestyle and Demographics
                    </span>

                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
                      <div className="p-2.5 rounded-lg bg-[#F7F7F2] border border-[#E5E5DD]/80">
                        <span className="text-[#73796F] text-[11px] block">Age</span>
                        <span className="font-semibold text-[#252923] text-sm mt-0.5 block">
                          {profileSummary.age !== null ? `${profileSummary.age} yrs` : 'Not provided'}
                        </span>
                      </div>

                      <div className="p-2.5 rounded-lg bg-[#F7F7F2] border border-[#E5E5DD]/80">
                        <span className="text-[#73796F] text-[11px] block">Dietary Preference</span>
                        <span className="font-semibold text-[#252923] text-sm capitalize mt-0.5 block">
                          {profileSummary.diet || 'Not set'}
                        </span>
                      </div>

                      <div className="p-2.5 rounded-lg bg-[#F7F7F2] border border-[#E5E5DD]/80">
                        <span className="text-[#73796F] text-[11px] block">Activity Level</span>
                        <span className="font-semibold text-[#252923] text-sm capitalize mt-0.5 block">
                          {profileSummary.activity || 'Not set'}
                        </span>
                      </div>

                      <div className="p-2.5 rounded-lg bg-[#F7F7F2] border border-[#E5E5DD]/80">
                        <span className="text-[#73796F] text-[11px] block">Sleep Quality</span>
                        <span className="font-semibold text-[#252923] text-sm capitalize mt-0.5 block">
                          {profileSummary.sleep || 'Not set'}
                        </span>
                      </div>
                    </div>
                  </div>

                  <hr className="border-[#E5E5DD]" />

                  {/* Subsection C: Clinical Safety Declaration */}
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="text-[11px] font-bold uppercase tracking-wider text-[#73796F] flex items-center gap-1.5">
                        <ShieldAlert className="h-3.5 w-3.5" />
                        <span>Contraindications and Safety Declaration</span>
                      </span>

                      <span className={`inline-flex items-center gap-1 text-[11px] font-semibold ${
                        profileSummary.hasSafetyConfirmed ? 'text-[#235E3F]' : 'text-[#8A5C00]'
                      }`}>
                        {profileSummary.hasSafetyConfirmed ? (
                          <>
                            <Check className="h-3 w-3" />
                            <span>Confirmed</span>
                          </>
                        ) : (
                          <>
                            <X className="h-3 w-3" />
                            <span>Unconfirmed</span>
                          </>
                        )}
                      </span>
                    </div>

                    <div className="text-xs text-[#5A6056] space-y-1 bg-[#F7F7F2]/60 p-3 rounded-lg border border-[#E5E5DD]/80">
                      <div>
                        <strong className="text-[#252923]">Allergens:</strong>{' '}
                        {profile.allergies?.length ? profile.allergies.join(', ') : 'None declared'}
                      </div>
                      <div>
                        <strong className="text-[#252923]">Conditions:</strong>{' '}
                        {profile.existing_conditions?.length ? profile.existing_conditions.join(', ') : 'None declared'}
                      </div>
                      <div>
                        <strong className="text-[#252923]">Prescription Classes:</strong>{' '}
                        {profile.current_medication_classes?.length ? profile.current_medication_classes.join(', ') : 'None declared'}
                      </div>
                    </div>
                  </div>
                </>
              ) : (
                <div className="py-8 text-center space-y-3">
                  <p className="text-xs text-[#73796F] max-w-sm mx-auto">
                    You have not configured your health profile yet. Setting your goals, lifestyle factors, and safety details is required for recommendations.
                  </p>
                  <Link to="/profile">
                    <Button variant="primary" size="sm" rightIcon={<ArrowRight className="h-3.5 w-3.5" />}>
                      Complete Health Profile Questionnaire
                    </Button>
                  </Link>
                </div>
              )}
            </div>
          </div>

          {/* Footer Action */}
          <div className="p-4 px-5 bg-[#F7F7F2]/40 border-t border-[#E5E5DD] flex items-center justify-between text-xs">
            <span className="text-[#73796F]">
              {profileSummary.isComplete
                ? 'All required safety and lifestyle parameters are verified.'
                : `Pending: ${profileSummary.missingFields.join(', ')}`}
            </span>

            <Link to="/profile">
              <Button variant="secondary" size="sm" rightIcon={<ArrowRight className="h-3.5 w-3.5" />}>
                Edit Profile
              </Button>
            </Link>
          </div>
        </Card>

        {/* Evaluation Audit Panel (1 Column on Desktop) */}
        <Card className="border-[#E5E5DD] flex flex-col justify-between">
          <div>
            <div className="p-5 pb-4 border-b border-[#E5E5DD] flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Clock className="h-4 w-4 text-[#244B38]" />
                <h3 className="text-base font-bold text-[#252923]">Evaluation Audit</h3>
              </div>
              <span className="text-xs font-mono font-semibold text-[#252923] bg-[#F7F7F2] border border-[#E5E5DD] px-2 py-0.5 rounded">
                {history.length} {history.length === 1 ? 'run' : 'runs'}
              </span>
            </div>

            <div className="p-5 space-y-4">
              <p className="text-xs text-[#73796F] leading-relaxed">
                Evaluations produce immutable records pairing frozen profile states with active rule and scoring versions.
              </p>

              <div className="space-y-2.5 text-xs">
                <div className="flex items-center justify-between py-1.5 border-b border-[#E5E5DD]/70">
                  <span className="text-[#73796F]">Dataset Version</span>
                  <span className="font-mono font-medium text-[#252923]">NIH ODS v1.0</span>
                </div>
                <div className="flex items-center justify-between py-1.5 border-b border-[#E5E5DD]/70">
                  <span className="text-[#73796F]">Scoring Model</span>
                  <span className="font-mono font-medium text-[#252923]">WSM-v1.0 (Linear)</span>
                </div>
                <div className="flex items-center justify-between py-1.5 border-b border-[#E5E5DD]/70">
                  <span className="text-[#73796F]">Cutoff Threshold</span>
                  <span className="font-mono font-medium text-[#252923]">&ge; 0.60 Score</span>
                </div>
                <div className="flex items-center justify-between py-1.5">
                  <span className="text-[#73796F]">Last Evaluated</span>
                  <span className="font-medium text-[#252923]">{latestRun ? formatDate(latestRun.created_at) : 'None'}</span>
                </div>
              </div>
            </div>
          </div>

          <div className="p-4 px-5 bg-[#F7F7F2]/40 border-t border-[#E5E5DD]">
            <Link to="/history" className="w-full block">
              <Button variant="secondary" size="sm" className="w-full" rightIcon={<ArrowRight className="h-3.5 w-3.5" />}>
                View Run History
              </Button>
            </Link>
          </div>
        </Card>
      </div>

      {/* 4. Recent Recommendations Table */}
      <Card className="border-[#E5E5DD]">
        <div className="p-5 pb-3 border-b border-[#E5E5DD] flex items-center justify-between">
          <div>
            <h3 className="text-base font-bold text-[#252923]">Recent Evaluations</h3>
            <p className="text-xs text-[#73796F] mt-0.5">
              Chronological records of safety-filtered recommendation runs.
            </p>
          </div>

          {history.length > 0 && (
            <Link to="/history" className="text-xs font-semibold text-[#244B38] hover:underline">
              View All ({history.length})
            </Link>
          )}
        </div>

        <div className="overflow-x-auto">
          {history.length === 0 ? (
            <div className="py-10 px-4 text-center space-y-2.5">
              <Clock className="h-6 w-6 text-[#73796F] mx-auto opacity-60" aria-hidden="true" />
              <div className="space-y-0.5">
                <h4 className="text-xs font-semibold text-[#252923]">No evaluations recorded yet</h4>
                <p className="text-xs text-[#73796F]">
                  Run the recommendation engine to generate your first audit record.
                </p>
              </div>
            </div>
          ) : (
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-[#E5E5DD] bg-[#F7F7F2]/60 text-[#73796F] text-[11px] font-semibold">
                  <th className="py-2.5 px-4">Run ID</th>
                  <th className="py-2.5 px-4">Date</th>
                  <th className="py-2.5 px-4">Status</th>
                  <th className="py-2.5 px-4 text-center">Results</th>
                  <th className="py-2.5 px-4">Algorithm</th>
                  <th className="py-2.5 px-4 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#E5E5DD] text-[#252923]">
                {history.slice(0, 5).map((r) => {
                  let badgeVariant: 'safe' | 'review' | 'excluded' | 'neutral' = 'neutral';
                  let statusLabel = r.status.replaceAll('_', ' ');

                  if (r.status === 'completed') {
                    badgeVariant = 'safe';
                    statusLabel = 'Completed';
                  } else if (r.status === 'no_eligible_results') {
                    badgeVariant = 'review';
                    statusLabel = 'No Matches >= Threshold';
                  } else if (r.status === 'withheld_incomplete_profile') {
                    badgeVariant = 'excluded';
                    statusLabel = 'Withheld Incomplete';
                  }

                  return (
                    <tr key={r.run_id} className="hover:bg-[#F7F7F2]/60 transition-colors">
                      <td className="py-2.5 px-4 font-mono font-semibold text-[#252923]">
                        #{r.run_id}
                      </td>
                      <td className="py-2.5 px-4 text-[#73796F]">
                        {formatDate(r.created_at)}
                      </td>
                      <td className="py-2.5 px-4">
                        <Badge variant={badgeVariant} size="sm">
                          {statusLabel}
                        </Badge>
                      </td>
                      <td className="py-2.5 px-4 text-center font-semibold text-[#252923]">
                        {r.n_results}
                      </td>
                      <td className="py-2.5 px-4 text-[#73796F] font-mono text-[11px]">
                        {r.scoring_version || 'WSM-v1.0'}
                      </td>
                      <td className="py-2.5 px-4 text-right">
                        <Link
                          to={`/runs/${r.run_id}`}
                          className="inline-flex items-center gap-1 font-semibold text-[#244B38] hover:underline"
                        >
                          <span>View</span>
                          <ArrowRight className="h-3 w-3" />
                        </Link>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          )}
        </div>
      </Card>

      {/* 5. Quick Workflow Navigation */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3.5">
        <Link to="/profile" className="block group">
          <Card className="border-[#E5E5DD] p-3.5 h-full hover:border-[#D0D0C5] transition-colors">
            <div className="flex items-start gap-3">
              <div className="p-2 rounded-lg bg-[#EEF3EE] text-[#244B38] group-hover:bg-[#244B38] group-hover:text-white transition-colors shrink-0">
                <Sliders className="h-4 w-4" />
              </div>
              <div className="space-y-0.5 min-w-0">
                <h4 className="text-xs font-bold text-[#252923] group-hover:text-[#244B38] transition-colors">
                  Health Profile
                </h4>
                <p className="text-[11px] text-[#73796F] leading-snug">
                  Manage wellness goals, dietary restrictions, and safety factors.
                </p>
              </div>
            </div>
          </Card>
        </Link>

        <Link to="/catalogue" className="block group">
          <Card className="border-[#E5E5DD] p-3.5 h-full hover:border-[#D0D0C5] transition-colors">
            <div className="flex items-start gap-3">
              <div className="p-2 rounded-lg bg-[#EEF3EE] text-[#244B38] group-hover:bg-[#244B38] group-hover:text-white transition-colors shrink-0">
                <BookOpen className="h-4 w-4" />
              </div>
              <div className="space-y-0.5 min-w-0">
                <h4 className="text-xs font-bold text-[#252923] group-hover:text-[#244B38] transition-colors">
                  Supplement Catalogue
                </h4>
                <p className="text-[11px] text-[#73796F] leading-snug">
                  Browse 130 supplement monographs with NIH ODS references.
                </p>
              </div>
            </div>
          </Card>
        </Link>

        <Link to="/history" className="block group">
          <Card className="border-[#E5E5DD] p-3.5 h-full hover:border-[#D0D0C5] transition-colors">
            <div className="flex items-start gap-3">
              <div className="p-2 rounded-lg bg-[#EEF3EE] text-[#244B38] group-hover:bg-[#244B38] group-hover:text-white transition-colors shrink-0">
                <Clock className="h-4 w-4" />
              </div>
              <div className="space-y-0.5 min-w-0">
                <h4 className="text-xs font-bold text-[#252923] group-hover:text-[#244B38] transition-colors">
                  Recommendation History
                </h4>
                <p className="text-[11px] text-[#73796F] leading-snug">
                  Inspect immutable historical run snapshots and audit trails.
                </p>
              </div>
            </div>
          </Card>
        </Link>
      </div>

      {/* 6. Medical Disclaimer */}
      <MedicalDisclaimer compact />
    </div>
  );
};
