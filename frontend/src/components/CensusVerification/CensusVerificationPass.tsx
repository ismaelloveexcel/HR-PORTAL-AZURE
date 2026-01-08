import { useState, useEffect } from 'react'
import { QRCodeSVG } from 'qrcode.react'

interface CensusData {
  token: string
  employee_name: string
  staff_id: string
  entity: string
  insurance_type: string
  full_name: string | null
  first_name: string | null
  second_name: string | null
  family_name: string | null
  dob: string | null
  gender: string | null
  nationality: string | null
  marital_status: string | null
  emirates_id_number: string | null
  uid_number: string | null
  gdrfa_file_number: string | null
  passport_number: string | null
  mobile_no: string | null
  personal_email: string | null
  dha_doh_missing_fields: string[]
  missing_fields: string[]
  already_verified: boolean
}

interface CensusVerificationPassProps {
  token: string
}

const NATIONALITIES = [
  'UAE', 'India', 'Pakistan', 'Philippines', 'Bangladesh', 'Egypt', 
  'Jordan', 'Sri Lanka', 'Nepal', 'Sudan', 'Syria', 'Lebanon', 
  'Palestine', 'Yemen', 'Morocco', 'Tunisia', 'Other'
]

const GENDERS = ['Male', 'Female']

const MARITAL_STATUSES = ['Single', 'Married', 'Divorced', 'Widowed']

export function CensusVerificationPass({ token }: CensusVerificationPassProps) {
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [data, setData] = useState<CensusData | null>(null)
  const [formData, setFormData] = useState<Record<string, string>>({})
  const [confirmed, setConfirmed] = useState(false)
  const [submitting, setSubmitting] = useState(false)
  const [success, setSuccess] = useState(false)
  const [submitError, setSubmitError] = useState<string | null>(null)

  const API_URL = '/api'

  const getEntityColor = () => {
    return data?.entity?.includes('agriculture') ? '#00bf63' : '#00B0F0'
  }

  useEffect(() => {
    fetchData()
  }, [token])

  const fetchData = async () => {
    try {
      setLoading(true)
      // Validate token first
      const validateRes = await fetch(`${API_URL}/census-verification/validate/${token}`)
      const validation = await validateRes.json()
      
      if (!validation.valid && !validation.already_verified) {
        setError(validation.message || 'Invalid verification link')
        return
      }

      // Get census data
      const dataRes = await fetch(`${API_URL}/census-verification/data/${token}`)
      if (!dataRes.ok) {
        throw new Error('Failed to load your data')
      }
      const censusData = await dataRes.json()
      setData(censusData)
      
      // Initialize form with current data
      setFormData({
        full_name: censusData.full_name || '',
        first_name: censusData.first_name || '',
        second_name: censusData.second_name || '',
        family_name: censusData.family_name || '',
        dob: censusData.dob || '',
        gender: censusData.gender || '',
        nationality: censusData.nationality || '',
        marital_status: censusData.marital_status || '',
        emirates_id_number: censusData.emirates_id_number || '',
        uid_number: censusData.uid_number || '',
        gdrfa_file_number: censusData.gdrfa_file_number || '',
        passport_number: censusData.passport_number || '',
        mobile_no: censusData.mobile_no || '',
        personal_email: censusData.personal_email || '',
      })
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load data')
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async () => {
    if (!confirmed) {
      setSubmitError('Please confirm that the information is correct')
      return
    }

    setSubmitting(true)
    setSubmitError(null)
    try {
      const res = await fetch(`${API_URL}/census-verification/submit/${token}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...formData, confirmed: true })
      })

      if (!res.ok) {
        const err = await res.json()
        throw new Error(err.detail || 'Failed to submit')
      }

      setSuccess(true)
    } catch (err) {
      setSubmitError(err instanceof Error ? err.message : 'Failed to submit')
    } finally {
      setSubmitting(false)
    }
  }

  const isMissing = (field: string) => {
    return data?.dha_doh_missing_fields?.includes(field) || !formData[field]
  }

  const entityColor = getEntityColor()

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-100 via-slate-50 to-slate-100">
        <div className="text-center">
          <div className="w-12 h-12 border-3 border-slate-200 border-t-slate-600 rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-slate-500 text-sm font-medium">Loading your details...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-100 via-slate-50 to-slate-100 p-4">
        <div className="bg-white border border-slate-200 shadow-xl rounded-3xl p-8 max-w-sm text-center">
          <div className="w-16 h-16 bg-red-50 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <svg className="w-8 h-8 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <h2 className="text-lg font-semibold text-slate-800 mb-2">Link Error</h2>
          <p className="text-sm text-slate-500">{error}</p>
        </div>
      </div>
    )
  }

  if (success || data?.already_verified) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-100 via-slate-50 to-slate-100 p-4">
        <div className="bg-white border border-slate-200 shadow-xl rounded-3xl p-8 max-w-sm text-center">
          <div 
            className="w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-4"
            style={{ backgroundColor: `${entityColor}15` }}
          >
            <svg className="w-8 h-8" style={{ color: entityColor }} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h2 className="text-lg font-semibold text-slate-800 mb-2">
            {success ? 'Verification Complete!' : 'Already Verified'}
          </h2>
          <p className="text-sm text-slate-500">
            {success 
              ? 'Your insurance details have been updated successfully. Thank you!'
              : 'You have already verified your insurance details. Thank you!'}
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-100 via-slate-50 to-slate-100 flex items-center justify-center p-2 sm:p-4">
      <div className="w-full max-w-md">
        {/* Premium Card Container */}
        <div 
          className="bg-gradient-to-br from-white via-white to-slate-50 border border-white/80 rounded-2xl sm:rounded-3xl overflow-hidden transition-all duration-500"
          style={{ 
            boxShadow: `0 25px 60px -15px rgba(0,0,0,0.15), 0 10px 30px -10px ${entityColor}20, 0 -2px 6px rgba(255,255,255,0.8) inset`
          }}
        >
          {/* Header */}
          <div className="px-5 pt-5 pb-4">
            <p className="text-xs font-semibold text-slate-500 mb-3">Insurance Verification Pass</p>
            
            {/* Info Card */}
            <div className="bg-gradient-to-br from-white via-white to-slate-50 rounded-2xl border border-slate-100 shadow-lg p-4 relative overflow-hidden">
              <div 
                className="absolute top-0 right-0 w-20 h-20 opacity-5 rounded-bl-full"
                style={{ backgroundColor: entityColor }}
              />
              
              <div className="flex items-start gap-3 relative z-10">
                <div className="flex-1 min-w-0">
                  <p 
                    className="text-[10px] font-bold uppercase tracking-wider mb-1"
                    style={{ color: entityColor }}
                  >
                    {data?.insurance_type?.toUpperCase()}
                  </p>
                  <p className="text-lg font-bold text-slate-900 leading-tight mb-1">{data?.employee_name}</p>
                  <p className="text-sm text-slate-600">{data?.staff_id}</p>
                  
                  <div 
                    className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full mt-2"
                    style={{ 
                      background: `linear-gradient(135deg, ${entityColor}12 0%, ${entityColor}08 100%)`,
                      border: `1px solid ${entityColor}20`
                    }}
                  >
                    <div 
                      className="w-1.5 h-1.5 rounded-full animate-pulse"
                      style={{ backgroundColor: entityColor }}
                    />
                    <span className="text-[10px] font-bold" style={{ color: entityColor }}>
                      {data?.entity === 'watergeneration' ? 'Watergeneration' : 'Agriculture'}
                    </span>
                  </div>
                </div>
                
                {/* QR Code */}
                <div 
                  className="flex-shrink-0 p-2 bg-gradient-to-br from-white to-slate-50 rounded-xl"
                  style={{ boxShadow: `0 4px 12px ${entityColor}10` }}
                >
                  <QRCodeSVG 
                    value={window.location.href} 
                    size={60}
                    level="H"
                    fgColor={entityColor}
                  />
                </div>
              </div>
            </div>
          </div>

          {/* DHA/DOH Warning Banner */}
          {data?.dha_doh_missing_fields && data.dha_doh_missing_fields.length > 0 && (
            <div className="mx-5 mb-4 p-3 bg-amber-50 border border-amber-200 rounded-xl">
              <div className="flex items-center gap-2 mb-1">
                <svg className="w-4 h-4 text-amber-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                <span className="text-xs font-bold text-amber-700">DHA/DOH Validation Required</span>
              </div>
              <p className="text-[10px] text-amber-600">
                Please fill in the missing fields below to ensure your insurance renewal is processed correctly.
              </p>
            </div>
          )}

          {/* Form */}
          <div className="px-5 pb-4 max-h-[50vh] overflow-y-auto">
            <div className="space-y-3">
              {/* Full Name */}
              <div>
                <label className="block text-[10px] font-semibold text-slate-500 uppercase tracking-wide mb-1">
                  Full Name {isMissing('full_name') && <span className="text-red-500">*</span>}
                </label>
                <input
                  type="text"
                  value={formData.full_name}
                  onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                  className={`w-full px-3 py-2.5 bg-slate-50 border rounded-xl text-sm focus:outline-none focus:ring-2 transition-all ${
                    isMissing('full_name') ? 'border-red-300 bg-red-50/50' : 'border-slate-200'
                  }`}
                  style={{ '--tw-ring-color': `${entityColor}40` } as React.CSSProperties}
                />
              </div>

              {/* DOB & Gender Row */}
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-[10px] font-semibold text-slate-500 uppercase tracking-wide mb-1">
                    Date of Birth {isMissing('dob') && <span className="text-red-500">*</span>}
                  </label>
                  <input
                    type="text"
                    value={formData.dob}
                    onChange={(e) => setFormData({ ...formData, dob: e.target.value })}
                    placeholder="DD/MM/YYYY"
                    className={`w-full px-3 py-2.5 bg-slate-50 border rounded-xl text-sm focus:outline-none focus:ring-2 transition-all ${
                      isMissing('dob') ? 'border-red-300 bg-red-50/50' : 'border-slate-200'
                    }`}
                  />
                </div>
                <div>
                  <label className="block text-[10px] font-semibold text-slate-500 uppercase tracking-wide mb-1">
                    Gender {isMissing('gender') && <span className="text-red-500">*</span>}
                  </label>
                  <select
                    value={formData.gender}
                    onChange={(e) => setFormData({ ...formData, gender: e.target.value })}
                    className={`w-full px-3 py-2.5 bg-slate-50 border rounded-xl text-sm focus:outline-none focus:ring-2 transition-all ${
                      isMissing('gender') ? 'border-red-300 bg-red-50/50' : 'border-slate-200'
                    }`}
                  >
                    <option value="">Select</option>
                    {GENDERS.map(g => <option key={g} value={g}>{g}</option>)}
                  </select>
                </div>
              </div>

              {/* Nationality */}
              <div>
                <label className="block text-[10px] font-semibold text-slate-500 uppercase tracking-wide mb-1">
                  Nationality {isMissing('nationality') && <span className="text-red-500">*</span>}
                </label>
                <select
                  value={formData.nationality}
                  onChange={(e) => setFormData({ ...formData, nationality: e.target.value })}
                  className={`w-full px-3 py-2.5 bg-slate-50 border rounded-xl text-sm focus:outline-none focus:ring-2 transition-all ${
                    isMissing('nationality') ? 'border-red-300 bg-red-50/50' : 'border-slate-200'
                  }`}
                >
                  <option value="">Select Nationality</option>
                  {NATIONALITIES.map(n => <option key={n} value={n}>{n}</option>)}
                </select>
              </div>

              {/* Emirates ID */}
              <div>
                <label className="block text-[10px] font-semibold text-slate-500 uppercase tracking-wide mb-1">
                  Emirates ID Number {isMissing('emirates_id_number') && <span className="text-red-500">*</span>}
                </label>
                <input
                  type="text"
                  value={formData.emirates_id_number}
                  onChange={(e) => setFormData({ ...formData, emirates_id_number: e.target.value })}
                  placeholder="784-XXXX-XXXXXXX-X"
                  className={`w-full px-3 py-2.5 bg-slate-50 border rounded-xl text-sm focus:outline-none focus:ring-2 transition-all ${
                    isMissing('emirates_id_number') ? 'border-red-300 bg-red-50/50' : 'border-slate-200'
                  }`}
                />
              </div>

              {/* UID Number */}
              <div>
                <label className="block text-[10px] font-semibold text-slate-500 uppercase tracking-wide mb-1">
                  UID Number {isMissing('uid_number') && <span className="text-red-500">*</span>}
                </label>
                <input
                  type="text"
                  value={formData.uid_number}
                  onChange={(e) => setFormData({ ...formData, uid_number: e.target.value })}
                  className={`w-full px-3 py-2.5 bg-slate-50 border rounded-xl text-sm focus:outline-none focus:ring-2 transition-all ${
                    isMissing('uid_number') ? 'border-red-300 bg-red-50/50' : 'border-slate-200'
                  }`}
                />
              </div>

              {/* Passport Number */}
              <div>
                <label className="block text-[10px] font-semibold text-slate-500 uppercase tracking-wide mb-1">
                  Passport Number {isMissing('passport_number') && <span className="text-red-500">*</span>}
                </label>
                <input
                  type="text"
                  value={formData.passport_number}
                  onChange={(e) => setFormData({ ...formData, passport_number: e.target.value })}
                  className={`w-full px-3 py-2.5 bg-slate-50 border rounded-xl text-sm focus:outline-none focus:ring-2 transition-all ${
                    isMissing('passport_number') ? 'border-red-300 bg-red-50/50' : 'border-slate-200'
                  }`}
                />
              </div>

              {/* GDRFA / Visa File */}
              <div>
                <label className="block text-[10px] font-semibold text-slate-500 uppercase tracking-wide mb-1">
                  Visa File No (GDRFA) {isMissing('gdrfa_file_number') && <span className="text-red-500">*</span>}
                </label>
                <input
                  type="text"
                  value={formData.gdrfa_file_number}
                  onChange={(e) => setFormData({ ...formData, gdrfa_file_number: e.target.value })}
                  className={`w-full px-3 py-2.5 bg-slate-50 border rounded-xl text-sm focus:outline-none focus:ring-2 transition-all ${
                    isMissing('gdrfa_file_number') ? 'border-red-300 bg-red-50/50' : 'border-slate-200'
                  }`}
                />
              </div>

              {/* Mobile */}
              <div>
                <label className="block text-[10px] font-semibold text-slate-500 uppercase tracking-wide mb-1">
                  Mobile Number
                </label>
                <input
                  type="tel"
                  value={formData.mobile_no}
                  onChange={(e) => setFormData({ ...formData, mobile_no: e.target.value })}
                  placeholder="+971 50 XXX XXXX"
                  className="w-full px-3 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 transition-all"
                />
              </div>

              {/* Confirmation Checkbox */}
              <div className="pt-2">
                <label className="flex items-start gap-3 cursor-pointer group">
                  <div className="relative mt-0.5">
                    <input
                      type="checkbox"
                      checked={confirmed}
                      onChange={(e) => setConfirmed(e.target.checked)}
                      className="sr-only"
                    />
                    <div 
                      className={`w-5 h-5 rounded-md border-2 flex items-center justify-center transition-all ${
                        confirmed ? '' : 'border-slate-300 group-hover:border-slate-400'
                      }`}
                      style={confirmed ? { backgroundColor: entityColor, borderColor: entityColor } : {}}
                    >
                      {confirmed && (
                        <svg className="w-3 h-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3}>
                          <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                        </svg>
                      )}
                    </div>
                  </div>
                  <span className="text-xs text-slate-600 leading-tight">
                    I confirm that the information provided above is correct and accurate.
                  </span>
                </label>
              </div>
            </div>
          </div>

          {/* Footer */}
          <div className="px-5 py-4 border-t border-slate-100 bg-white/50">
            {submitError && (
              <div className="mb-3 p-2 bg-red-50 border border-red-200 rounded-lg text-red-600 text-xs">
                {submitError}
              </div>
            )}
            <button
              onClick={handleSubmit}
              disabled={!confirmed || submitting}
              className={`w-full py-3 rounded-xl font-semibold text-sm transition-all flex items-center justify-center gap-2 ${
                confirmed && !submitting ? 'text-white shadow-lg' : 'bg-slate-100 text-slate-400 cursor-not-allowed'
              }`}
              style={confirmed && !submitting ? { 
                backgroundColor: entityColor,
                boxShadow: `0 4px 14px ${entityColor}40`
              } : {}}
            >
              {submitting ? (
                <>
                  <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                  Submitting...
                </>
              ) : (
                <>
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Confirm & Submit
                </>
              )}
            </button>
          </div>

          {/* Entity Footer */}
          <div 
            className="px-4 py-2.5 text-center border-t border-slate-100/50"
            style={{ backgroundColor: `${entityColor}06` }}
          >
            <span className="text-[10px] text-slate-500 font-medium">
              Medical Insurance Renewal: <span style={{ color: entityColor }} className="font-semibold">Baynunah Group</span>
            </span>
          </div>
        </div>
      </div>
    </div>
  )
}
