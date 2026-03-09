'use client'
import { useState } from 'react'
import { matchSchemes } from '../../lib/api'




export default function SchemesPage() {
  const [step, setStep] = useState(1)
  const [showResults, setShowResults] = useState(false)
  const [loading, setLoading] = useState(false)
  const [profile, setProfile] = useState({
    age: '',
    gender: '',
    state: '',
    district: '',
    occupation: [] as string[],
    income: '',
    familySize: '',
    bplCard: null as boolean | null,
    casteCategory: '',
    needs: [] as string[],
    hasAadhaar: false,
    hasBankAccount: false,
    hasLandRecords: false,
    hasRationCard: false
  })
  const [matchedSchemes, setMatchedSchemes] = useState<any[]>([])

  const states = ['Gujarat', 'Maharashtra', 'Karnataka', 'Tamil Nadu', 'Uttar Pradesh', 'Bihar', 'West Bengal', 'Rajasthan', 'Madhya Pradesh', 'Punjab']
  const occupations = ['Farmer', 'Agricultural Laborer', 'Daily Wage Worker', 'Small Business Owner', 'Salaried Employee', 'Unemployed', 'Student', 'Homemaker', 'Self-Employed']
  const needs = ['Housing Support', 'Education/Scholarship', 'Healthcare', 'Women & Child Welfare', 'Agricultural Support', 'Employment/Skill Training', 'Senior Citizen Benefits', 'Financial Assistance']

  const toggleOccupation = (occ: string) => {
    setProfile(prev => ({
      ...prev,
      occupation: prev.occupation.includes(occ)
        ? prev.occupation.filter(o => o !== occ)
        : [...prev.occupation, occ]
    }))
  }

  const toggleNeed = (need: string) => {
    setProfile(prev => ({
      ...prev,
      needs: prev.needs.includes(need)
        ? prev.needs.filter(n => n !== need)
        : [...prev.needs, need]
    }))
  }

  const incomeMap: Record<string, string> = {
    '<₹1L': 'BPL',
    '₹1-3L': '0-2.5L',
    '₹3-5L': '2.5-5L',
    '₹5-10L': '5-10L',
    '>₹10L': '10L+',
  }

  const handleSubmit = async () => {
    setLoading(true)
    try {
      const result = await matchSchemes({
        age: parseInt(profile.age) || 25,
        incomeBracket: incomeMap[profile.income] || '0-2.5L',
        occupation: profile.occupation[0]?.toLowerCase() || 'unemployed',
        state: profile.state || 'Maharashtra',
        category: profile.casteCategory || 'General',
        disability: false,
        gender: profile.gender?.toLowerCase() || undefined,
      })

      const mapped = (result.recommendations || []).map((rec: any) => ({
        id: rec.scheme.schemeId,
        name: rec.scheme.name,
        fullName: rec.scheme.description,
        benefit: rec.scheme.benefitAmount || 'Benefits available',
        description: rec.scheme.simpleDescription || rec.scheme.description,
        matchPercentage: rec.eligibilityScore,
        confidence: (rec.eligibilityScore / 100).toFixed(2),
        helpline: rec.scheme.helplineNumber || 'N/A',
        website: rec.scheme.officialLink || '#',
        ministry: rec.scheme.category,
        reasoning: rec.reasoning,
        matchedCriteria: rec.matchedCriteria || [],
        missingCriteria: rec.missingCriteria || [],
        requiredDocuments: rec.requiredDocuments || [],
      }))

      setMatchedSchemes(mapped)
      setShowResults(true)
    } catch (err) {
      console.error('API Error:', err)
      alert('Could not connect to the backend. Please ensure the AWS Lambda service is active.')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-slate-200 border-t-slate-900 rounded-full animate-spin mx-auto mb-6"></div>
          <h2 className="text-2xl font-light text-slate-900 mb-4">Analyzing your profile...</h2>
          <div className="space-y-2 text-sm text-slate-600">
            <p>Filtering 2,000+ schemes</p>
            <p>Checking eligibility rules</p>
            <p>Ranking by relevance</p>
          </div>
        </div>
      </div>
    )
  }

  if (showResults) {
    return (
      <div className="min-h-screen bg-slate-50 py-12 px-4">
        <div className="max-w-5xl mx-auto">
          <button
            onClick={() => { setShowResults(false); setStep(1); }}
            className="mb-8 text-slate-900 hover:text-slate-700 font-light flex items-center gap-2 transition-colors"
          >
            ← Start New Search
          </button>

          <div className="mb-12">
            <h1 className="text-5xl font-light text-slate-900 mb-4">
              {matchedSchemes.length} Schemes Found
            </h1>
            <p className="text-xl text-slate-600 font-light">Based on your profile, here are the schemes you're eligible for</p>
          </div>

          <div className="space-y-6">
            {matchedSchemes.map((scheme: any, idx: number) => (
              <div key={scheme.id} className="card">
                <div className="flex justify-between items-start mb-6">
                  <div>
                    <h2 className="text-3xl font-light text-slate-900 mb-2">{scheme.name}</h2>
                    <p className="text-slate-600 text-sm mb-2">{scheme.fullName}</p>
                    <span className="badge">
                      {scheme.ministry}
                    </span>
                  </div>
                  <div className="text-right">
                    <div className="text-sm text-slate-600 mb-1">Match Score</div>
                    <div className="text-3xl font-light text-slate-900">{scheme.matchPercentage}%</div>
                  </div>
                </div>

                <div className="bg-slate-50 rounded-xl p-6 mb-6">
                  <div className="text-3xl font-light text-slate-900 mb-2">{scheme.benefit}</div>
                  <p className="text-slate-700">{scheme.description}</p>
                </div>

                {/* AI Reasoning */}
                {scheme.reasoning && (
                  <div className="bg-blue-50 border border-blue-200 rounded-xl p-4 mb-6">
                    <p className="text-sm text-blue-800 font-medium mb-1">🤖 AI Analysis</p>
                    <p className="text-blue-900 text-sm">{scheme.reasoning}</p>
                  </div>
                )}

                {/* Matched Criteria */}
                {scheme.matchedCriteria?.length > 0 && (
                  <div className="mb-4">
                    <p className="text-sm font-medium text-slate-700 mb-2">✅ Matched Criteria</p>
                    <div className="space-y-1">
                      {scheme.matchedCriteria.map((c: string, i: number) => (
                        <p key={i} className="text-sm text-green-700">✓ {c}</p>
                      ))}
                    </div>
                  </div>
                )}

                {/* Required Documents */}
                {scheme.requiredDocuments?.length > 0 && (
                  <div className="mb-6 border border-slate-200 rounded-xl p-4">
                    <p className="text-sm font-medium text-slate-700 mb-2">📄 Required Documents</p>
                    <div className="flex flex-wrap gap-2">
                      {scheme.requiredDocuments.map((d: string, i: number) => (
                        <span key={i} className="text-xs bg-slate-100 text-slate-700 px-3 py-1 rounded-full">{d}</span>
                      ))}
                    </div>
                  </div>
                )}

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                  <div className="border border-slate-200 rounded-xl p-4">
                    <p className="text-sm text-slate-600 mb-1">Eligibility Score</p>
                    <div className="flex items-center gap-2">
                      <div className="flex-1 bg-slate-200 rounded-full h-2">
                        <div className="bg-slate-900 h-2 rounded-full transition-all duration-1000" style={{ width: `${scheme.matchPercentage}%` }}></div>
                      </div>
                      <span className="font-medium text-slate-900">{scheme.matchPercentage}%</span>
                    </div>
                  </div>
                  <div className="border border-slate-200 rounded-xl p-4">
                    <p className="text-sm text-slate-600 mb-1">Helpline</p>
                    <p className="font-medium text-slate-900 text-xl">{scheme.helpline}</p>
                  </div>
                </div>

                <div className="flex flex-wrap gap-3">
                  <a
                    href={scheme.website}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="btn-primary flex-1 text-center"
                  >
                    Apply Now →
                  </a>
                  <button className="btn-secondary">
                    View Details
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-slate-50 py-12 px-4">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-5xl md:text-6xl font-light text-slate-900 mb-4">
            Find Your Schemes
          </h1>
          <p className="text-xl text-slate-600 font-light">Answer a few questions to discover schemes tailored for you</p>
        </div>

        {/* Progress */}
        <div className="mb-12">
          <div className="flex justify-between mb-3">
            {[1, 2, 3, 4].map(s => (
              <div key={s} className="flex-1 mx-1">
                <div className={`h-1 rounded-full transition-all duration-500 ${s <= step ? 'bg-slate-900' : 'bg-slate-200'}`} />
              </div>
            ))}
          </div>
          <p className="text-center text-sm text-slate-600">
            Step {step} of 4 • {['Basic Info', 'Economic Info', 'Social Category', 'Your Needs'][step - 1]}
          </p>
        </div>

        {/* Step 1 */}
        {step === 1 && (
          <div className="card space-y-8">
            <h2 className="text-3xl font-light text-slate-900">Basic Information</h2>

            <div>
              <label className="block text-sm font-medium mb-3 text-slate-700">Age</label>
              <input
                type="number"
                value={profile.age}
                onChange={e => setProfile({ ...profile, age: e.target.value })}
                className="input"
                placeholder="Enter your age"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-3 text-slate-700">Gender</label>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                {['Male', 'Female', 'Other', 'Prefer not to say'].map(g => (
                  <button
                    key={g}
                    onClick={() => setProfile({ ...profile, gender: g })}
                    className={`btn-select ${profile.gender === g ? 'btn-select-active' : 'btn-select-inactive'
                      }`}
                  >
                    {g}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium mb-3 text-slate-700">State</label>
              <select
                value={profile.state}
                onChange={e => setProfile({ ...profile, state: e.target.value })}
                className="input"
              >
                <option value="">Select your state</option>
                {states.map(s => (
                  <option key={s} value={s}>{s}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-3 text-slate-700">District</label>
              <input
                type="text"
                value={profile.district}
                onChange={e => setProfile({ ...profile, district: e.target.value })}
                className="input"
                placeholder="Enter your district"
              />
            </div>
          </div>
        )}

        {/* Step 2 */}
        {step === 2 && (
          <div className="card space-y-8">
            <h2 className="text-3xl font-light text-slate-900">Economic Information</h2>

            <div>
              <label className="block text-sm font-medium mb-3 text-slate-700">Occupation (select all that apply)</label>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                {occupations.map(occ => (
                  <button
                    key={occ}
                    onClick={() => toggleOccupation(occ)}
                    className={`btn-select text-sm ${profile.occupation.includes(occ) ? 'btn-select-active' : 'btn-select-inactive'
                      }`}
                  >
                    {occ}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium mb-3 text-slate-700">Annual Household Income</label>
              <select
                value={profile.income}
                onChange={e => setProfile({ ...profile, income: e.target.value })}
                className="input"
              >
                <option value="">Select income range</option>
                <option value="<₹1L">&lt;₹1 Lakh</option>
                <option value="₹1-3L">₹1-3 Lakh</option>
                <option value="₹3-5L">₹3-5 Lakh</option>
                <option value="₹5-10L">₹5-10 Lakh</option>
                <option value=">₹10L">&gt;₹10 Lakh</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-3 text-slate-700">Family Size</label>
              <input
                type="number"
                value={profile.familySize}
                onChange={e => setProfile({ ...profile, familySize: e.target.value })}
                className="input"
                placeholder="Number of family members"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-3 text-slate-700">Do you have a BPL Card?</label>
              <div className="flex gap-3">
                {[{ label: 'Yes', value: true }, { label: 'No', value: false }, { label: "Don't Know", value: null }].map(opt => (
                  <button
                    key={opt.label}
                    onClick={() => setProfile({ ...profile, bplCard: opt.value })}
                    className={`flex-1 btn-select ${profile.bplCard === opt.value ? 'btn-select-active' : 'btn-select-inactive'
                      }`}
                  >
                    {opt.label}
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Step 3 */}
        {step === 3 && (
          <div className="card space-y-8">
            <h2 className="text-3xl font-light text-slate-900">Social Category</h2>

            <div>
              <label className="block text-sm font-medium mb-3 text-slate-700">Caste Category</label>
              <select
                value={profile.casteCategory}
                onChange={e => setProfile({ ...profile, casteCategory: e.target.value })}
                className="input"
              >
                <option value="">Select category</option>
                <option value="General">General</option>
                <option value="OBC">OBC</option>
                <option value="SC">SC</option>
                <option value="ST">ST</option>
                <option value="EWS">EWS</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-3 text-slate-700">Documents You Have</label>
              <div className="space-y-3">
                {[
                  { key: 'hasAadhaar', label: 'Aadhaar Card' },
                  { key: 'hasBankAccount', label: 'Bank Account' },
                  { key: 'hasLandRecords', label: 'Land Records' },
                  { key: 'hasRationCard', label: 'Ration Card' },
                ].map(doc => (
                  <label key={doc.key} className="flex items-center space-x-3 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={profile[doc.key as keyof typeof profile] as boolean}
                      onChange={e => setProfile({ ...profile, [doc.key]: e.target.checked })}
                      className="w-5 h-5 text-slate-900 focus:ring-slate-900 rounded border-slate-300"
                    />
                    <span className="text-slate-700">{doc.label}</span>
                  </label>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Step 4 */}
        {step === 4 && (
          <div className="card-clean space-y-8">
            <h2 className="text-3xl font-light text-navy">What do you need help with?</h2>
            <p className="text-gray-600">Select all that apply</p>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {needs.map(need => (
                <button
                  key={need}
                  onClick={() => toggleNeed(need)}
                  className={`py-4 px-6 rounded-xl border-2 font-medium transition-all text-left ${profile.needs.includes(need)
                      ? 'border-navy bg-navy text-white'
                      : 'border-gray-300 hover:border-gray-400 bg-white'
                    }`}
                >
                  {need}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Navigation */}
        <div className="flex justify-between mt-10">
          <button
            onClick={() => setStep(Math.max(1, step - 1))}
            disabled={step === 1}
            className="btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            ← Back
          </button>

          {step < 4 ? (
            <button
              onClick={() => setStep(step + 1)}
              className="btn-primary"
            >
              Next Step →
            </button>
          ) : (
            <button
              onClick={handleSubmit}
              className="btn-primary"
            >
              Find My Schemes
            </button>
          )}
        </div>
      </div>
    </div>
  )
}
