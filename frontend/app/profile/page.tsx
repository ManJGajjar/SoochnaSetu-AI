'use client'
import { useState, useEffect } from 'react'
import { createProfile, getProfile } from '../../lib/api'

const STATES = [
  'Andhra Pradesh','Arunachal Pradesh','Assam','Bihar','Chhattisgarh','Goa','Gujarat',
  'Haryana','Himachal Pradesh','Jharkhand','Karnataka','Kerala','Madhya Pradesh',
  'Maharashtra','Manipur','Meghalaya','Mizoram','Nagaland','Odisha','Punjab','Rajasthan',
  'Sikkim','Tamil Nadu','Telangana','Tripura','Uttar Pradesh','Uttarakhand','West Bengal',
  'Andaman & Nicobar','Chandigarh','Dadra & Nagar Haveli','Daman & Diu','Delhi','Jammu & Kashmir','Ladakh','Lakshadweep','Puducherry'
]

export default function ProfilePage() {
  const [saved, setSaved] = useState(false)
  const [loading, setLoading] = useState(false)
  const [profile, setProfile] = useState({
    userId: '',
    name: '',
    phone: '',
    age: '',
    gender: '',
    state: '',
    occupation: '',
    incomeBracket: '',
    category: 'General',
    disability: false,
    familySize: '4',
    bplCard: false,
    hasAadhaar: true,
    hasBankAccount: true,
  })

  const update = (key: string, value: any) => setProfile(p => ({ ...p, [key]: value }))

  const handleSave = async () => {
    if (!profile.name || !profile.phone || !profile.age) {
      alert('Please fill in Name, Phone, and Age.')
      return
    }
    setLoading(true)
    try {
      const result = await createProfile({
        userId: profile.phone,
        name: profile.name,
        phone: profile.phone,
        age: parseInt(profile.age),
        gender: profile.gender || undefined,
        state: profile.state || undefined,
        occupation: profile.occupation || undefined,
        incomeBracket: profile.incomeBracket || undefined,
        category: profile.category,
        disability: profile.disability,
      })
      setSaved(true)
      update('userId', result.userId || profile.phone)
    } catch (err: any) {
      alert(err.message || 'Failed to save profile.')
    } finally {
      setLoading(false)
    }
  }

  if (saved) {
    return (
      <div className="min-h-screen bg-white py-12 px-4">
        <div className="max-w-3xl mx-auto text-center">
          <div className="text-7xl mb-6">✅</div>
          <h1 className="text-4xl font-light text-slate-900 mb-4">Profile Saved!</h1>
          <p className="text-lg text-slate-600 mb-8">
            Your profile has been stored securely. You can now get personalized scheme recommendations.
          </p>
          <div className="card text-left mb-8">
            <h2 className="text-xl font-medium text-slate-900 mb-4">Your Profile Summary</h2>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div><span className="text-slate-500">Name:</span> <span className="font-medium">{profile.name}</span></div>
              <div><span className="text-slate-500">Phone:</span> <span className="font-medium">{profile.phone}</span></div>
              <div><span className="text-slate-500">Age:</span> <span className="font-medium">{profile.age}</span></div>
              <div><span className="text-slate-500">Gender:</span> <span className="font-medium">{profile.gender || 'Not specified'}</span></div>
              <div><span className="text-slate-500">State:</span> <span className="font-medium">{profile.state || 'Not specified'}</span></div>
              <div><span className="text-slate-500">Occupation:</span> <span className="font-medium">{profile.occupation || 'Not specified'}</span></div>
              <div><span className="text-slate-500">Income:</span> <span className="font-medium">{profile.incomeBracket || 'Not specified'}</span></div>
              <div><span className="text-slate-500">Category:</span> <span className="font-medium">{profile.category}</span></div>
            </div>
          </div>
          <div className="flex flex-wrap gap-4 justify-center">
            <a href="/schemes" className="btn-primary">Find My Schemes →</a>
            <button onClick={() => setSaved(false)} className="btn-secondary">Edit Profile</button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-white py-12 px-4">
      <div className="max-w-3xl mx-auto">
        <div className="text-center mb-10">
          <h1 className="text-5xl md:text-6xl font-light text-slate-900 mb-4">My Profile</h1>
          <p className="text-xl text-slate-600 font-light">Save your details to get personalized scheme recommendations</p>
        </div>

        <div className="space-y-8">
          {/* Personal Information */}
          <div className="card">
            <h2 className="text-2xl font-light text-slate-900 mb-6">👤 Personal Information</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Full Name *</label>
                <input
                  type="text" value={profile.name} onChange={e => update('name', e.target.value)}
                  placeholder="Enter your full name"
                  className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-slate-900 focus:border-transparent outline-none"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Phone Number *</label>
                <input
                  type="tel" value={profile.phone} onChange={e => update('phone', e.target.value)}
                  placeholder="10-digit mobile number"
                  className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-slate-900 focus:border-transparent outline-none"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Age *</label>
                <input
                  type="number" value={profile.age} onChange={e => update('age', e.target.value)}
                  placeholder="Your age" min="0" max="120"
                  className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-slate-900 focus:border-transparent outline-none"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Gender</label>
                <select
                  value={profile.gender} onChange={e => update('gender', e.target.value)}
                  className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-slate-900 focus:border-transparent outline-none"
                >
                  <option value="">Select gender</option>
                  <option value="Male">Male</option>
                  <option value="Female">Female</option>
                  <option value="Other">Other</option>
                </select>
              </div>
            </div>
          </div>

          {/* Location & Occupation */}
          <div className="card">
            <h2 className="text-2xl font-light text-slate-900 mb-6">📍 Location & Occupation</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">State</label>
                <select
                  value={profile.state} onChange={e => update('state', e.target.value)}
                  className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-slate-900 focus:border-transparent outline-none"
                >
                  <option value="">Select state</option>
                  {STATES.map(s => <option key={s} value={s}>{s}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Occupation</label>
                <select
                  value={profile.occupation} onChange={e => update('occupation', e.target.value)}
                  className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-slate-900 focus:border-transparent outline-none"
                >
                  <option value="">Select occupation</option>
                  <option value="farmer">Farmer</option>
                  <option value="student">Student</option>
                  <option value="daily_wage">Daily Wage Worker</option>
                  <option value="self_employed">Self-Employed</option>
                  <option value="salaried">Salaried Employee</option>
                  <option value="business_owner">Business Owner</option>
                  <option value="homemaker">Homemaker</option>
                  <option value="unemployed">Unemployed</option>
                  <option value="senior_citizen">Senior Citizen</option>
                </select>
              </div>
            </div>
          </div>

          {/* Economic Details */}
          <div className="card">
            <h2 className="text-2xl font-light text-slate-900 mb-6">💰 Economic Details</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Annual Income</label>
                <select
                  value={profile.incomeBracket} onChange={e => update('incomeBracket', e.target.value)}
                  className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-slate-900 focus:border-transparent outline-none"
                >
                  <option value="">Select income bracket</option>
                  <option value="BPL">Below Poverty Line</option>
                  <option value="0-2.5L">₹0 - ₹2.5 Lakh</option>
                  <option value="2.5-5L">₹2.5 - ₹5 Lakh</option>
                  <option value="5-10L">₹5 - ₹10 Lakh</option>
                  <option value="10L+">Above ₹10 Lakh</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Social Category</label>
                <select
                  value={profile.category} onChange={e => update('category', e.target.value)}
                  className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-slate-900 focus:border-transparent outline-none"
                >
                  <option value="General">General</option>
                  <option value="OBC">OBC</option>
                  <option value="SC">SC</option>
                  <option value="ST">ST</option>
                  <option value="EWS">EWS</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Family Size</label>
                <input
                  type="number" value={profile.familySize} onChange={e => update('familySize', e.target.value)}
                  min="1" max="20"
                  className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-slate-900 focus:border-transparent outline-none"
                />
              </div>
              <div className="flex items-center gap-6 pt-8">
                <label className="flex items-center gap-2 cursor-pointer">
                  <input type="checkbox" checked={profile.bplCard} onChange={e => update('bplCard', e.target.checked)}
                    className="w-5 h-5 rounded border-slate-300"
                  />
                  <span className="text-sm text-slate-700">BPL Card</span>
                </label>
                <label className="flex items-center gap-2 cursor-pointer">
                  <input type="checkbox" checked={profile.disability} onChange={e => update('disability', e.target.checked)}
                    className="w-5 h-5 rounded border-slate-300"
                  />
                  <span className="text-sm text-slate-700">Person with Disability</span>
                </label>
              </div>
            </div>
          </div>

          {/* Documents Available */}
          <div className="card">
            <h2 className="text-2xl font-light text-slate-900 mb-6">📋 Documents Available</h2>
            <div className="flex flex-wrap gap-4">
              {[
                { key: 'hasAadhaar', label: 'Aadhaar Card', icon: '🪪' },
                { key: 'hasBankAccount', label: 'Bank Account', icon: '🏦' },
              ].map(doc => (
                <label key={doc.key} className="flex items-center gap-2 px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl cursor-pointer hover:bg-slate-100 transition-colors">
                  <input
                    type="checkbox"
                    checked={(profile as any)[doc.key]}
                    onChange={e => update(doc.key, e.target.checked)}
                    className="w-5 h-5 rounded border-slate-300"
                  />
                  <span className="text-lg mr-1">{doc.icon}</span>
                  <span className="text-sm text-slate-700">{doc.label}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Actions */}
          <div className="flex flex-wrap gap-4 justify-center pt-4">
            <button
              onClick={handleSave}
              disabled={loading}
              className="btn-primary text-lg px-12 disabled:opacity-50"
            >
              {loading ? 'Saving...' : '💾 Save Profile'}
            </button>
            <a href="/schemes" className="btn-secondary text-lg">
              Skip & Find Schemes →
            </a>
          </div>

          <p className="text-center text-sm text-slate-500 mt-4">
            🔒 Your data is stored securely and never shared with third parties.
          </p>
        </div>
      </div>
    </div>
  )
}
