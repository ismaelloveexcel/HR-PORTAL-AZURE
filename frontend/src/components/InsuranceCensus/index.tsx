import React, { useState, useEffect, useCallback } from 'react'

interface CensusRecord {
  id: number
  entity: string
  insurance_type: string
  employee_id: number | null
  sr_no: string | null
  first_name: string | null
  second_name: string | null
  family_name: string | null
  full_name: string | null
  dob: string | null
  gender: string | null
  marital_status: string | null
  maternity_coverage: string | null
  relation: string | null
  staff_id: string | null
  employee_card_number: string | null
  category: string | null
  sub_group_name: string | null
  billing_entity: string | null
  department: string | null
  nationality: string | null
  effective_date: string | null
  emirates_id_number: string | null
  emirates_id_application_number: string | null
  uid_number: string | null
  gdrfa_file_number: string | null
  passport_number: string | null
  emirate_of_residency: string | null
  work_location: string | null
  mobile_no: string | null
  personal_email: string | null
  missing_fields: string[]
  completeness_pct: number
  import_batch_id: string | null
  // New fields for DHA/DOH validation and renewal tracking
  dha_doh_missing_fields: string[]
  dha_doh_valid: boolean
  renewal_status: 'existing' | 'addition' | 'deletion'
  renewal_effective_date: string | null
  amended_fields: string[]
}

interface CensusSummary {
  total: number
  linked: number
  by_entity: Record<string, number>
  by_insurance_type: Record<string, number>
  avg_completeness: number
}

const API_BASE = '/api'

// DHA/DOH Validation Required Fields (for UAE-based policy)
// If any of these are incorrect/pending, validation will fail
const DHA_DOH_VALIDATION_FIELDS = [
  'passport_number',       // Passport-No
  'gdrfa_file_number',     // Visa File No
  'emirates_id_number',    // EID No
  'uid_number',            // UID No
  'nationality',           // Nationality
  'dob',                   // DOB
  'gender',                // Gender
]

const MANDATORY_FIELDS = [
  'full_name', 'dob', 'gender', 'relation', 'staff_id', 'category',
  'effective_date', 'nationality', 'uid_number',
]
const MANDATORY_FIELDS_FOR_RENEWAL = [
  'emirates_id_number', 'gdrfa_file_number', 'passport_number',
]
const ALL_MANDATORY = [...MANDATORY_FIELDS, ...MANDATORY_FIELDS_FOR_RENEWAL]

// Fields tracked for amendments (purple highlighting)
const AMENDMENT_TRACKED_FIELDS = [
  'full_name', 'first_name', 'second_name', 'family_name',
  'marital_status', 'passport_number', 'gdrfa_file_number',
  'emirates_id_number', 'nationality', 'dob', 'gender',
]

const DISPLAY_COLUMNS = [
  { key: 'sr_no', label: 'SR No', width: '60px' },
  { key: 'full_name', label: 'Full Name', width: '180px' },
  { key: 'staff_id', label: 'Staff ID', width: '90px' },
  { key: 'relation', label: 'Relation', width: '90px' },
  { key: 'dob', label: 'DOB', width: '100px' },
  { key: 'gender', label: 'Gender', width: '70px' },
  { key: 'nationality', label: 'Nationality', width: '110px' },
  { key: 'category', label: 'Category', width: '100px' },
  { key: 'emirates_id_number', label: 'Emirates ID', width: '160px' },
  { key: 'uid_number', label: 'UID', width: '140px' },
  { key: 'gdrfa_file_number', label: 'GDRFA/Visa File', width: '120px' },
  { key: 'passport_number', label: 'Passport', width: '120px' },
  { key: 'effective_date', label: 'Effective Date', width: '110px' },
  { key: 'mobile_no', label: 'Mobile', width: '120px' },
  { key: 'completeness_pct', label: 'Complete %', width: '90px' },
  { key: 'renewal_status', label: 'Status', width: '80px' },
]

interface InsuranceCensusProps {
  token: string
  onBack: () => void
}

export function InsuranceCensus({ token, onBack }: InsuranceCensusProps) {
  const [records, setRecords] = useState<CensusRecord[]>([])
  const [summary, setSummary] = useState<CensusSummary | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [entityFilter, setEntityFilter] = useState<string>('all')
  const [insuranceTypeFilter, setInsuranceTypeFilter] = useState<string>('all')
  const [renewalStatusFilter, setRenewalStatusFilter] = useState<string>('all')
  const [searchTerm, setSearchTerm] = useState('')
  const [editingCell, setEditingCell] = useState<{id: number, field: string} | null>(null)
  const [editValue, setEditValue] = useState('')
  const [pendingChanges, setPendingChanges] = useState<Record<number, Record<string, string>>>({})
  const [saving, setSaving] = useState(false)
  const [saveMessage, setSaveMessage] = useState<string | null>(null)
  
  // Verification email state
  const [showVerificationModal, setShowVerificationModal] = useState(false)
  const [sendingEmails, setSendingEmails] = useState(false)
  const [verificationStats, setVerificationStats] = useState<{
    total_tokens: number
    emails_sent: number
    verified: number
    pending: number
    expired: number
  } | null>(null)
  const [verificationResult, setVerificationResult] = useState<{
    tokens_created?: number
    emails_prepared?: number
    emails?: Array<{ to: string; subject: string; verification_url: string }>
  } | null>(null)

  const fetchData = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const params = new URLSearchParams()
      if (entityFilter !== 'all') params.append('entity', entityFilter)
      if (insuranceTypeFilter !== 'all') params.append('insurance_type', insuranceTypeFilter)
      if (searchTerm) params.append('search', searchTerm)

      const [recordsRes, summaryRes] = await Promise.all([
        fetch(`${API_BASE}/insurance-census?${params}`, {
          headers: { Authorization: `Bearer ${token}` }
        }),
        fetch(`${API_BASE}/insurance-census/summary`, {
          headers: { Authorization: `Bearer ${token}` }
        })
      ])

      if (!recordsRes.ok) throw new Error('Failed to fetch records')
      if (!summaryRes.ok) throw new Error('Failed to fetch summary')

      const recordsData = await recordsRes.json()
      const summaryData = await summaryRes.json()

      setRecords(recordsData.records || recordsData)
      setSummary(summaryData)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load data')
    } finally {
      setLoading(false)
    }
  }, [token, entityFilter, insuranceTypeFilter, searchTerm])

  useEffect(() => {
    fetchData()
  }, [fetchData])

  const handleCellClick = (id: number, field: string, currentValue: string | null) => {
    if (field === 'completeness_pct') return
    setEditingCell({ id, field })
    const pendingValue = pendingChanges[id]?.[field]
    setEditValue(pendingValue ?? currentValue ?? '')
  }

  const handleCellChange = (value: string) => {
    setEditValue(value)
  }

  const handleCellBlur = () => {
    if (editingCell) {
      const { id, field } = editingCell
      const originalRecord = records.find(r => r.id === id)
      const originalValue = originalRecord ? (originalRecord[field as keyof CensusRecord] as string | null) ?? '' : ''
      
      if (editValue !== originalValue) {
        setPendingChanges(prev => ({
          ...prev,
          [id]: {
            ...prev[id],
            [field]: editValue
          }
        }))
      }
    }
    setEditingCell(null)
    setEditValue('')
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleCellBlur()
    } else if (e.key === 'Escape') {
      setEditingCell(null)
      setEditValue('')
    }
  }

  const hasPendingChanges = Object.keys(pendingChanges).length > 0

  const handleSaveChanges = async () => {
    if (!hasPendingChanges) return
    setSaving(true)
    setSaveMessage(null)
    setError(null)

    try {
      const updates = Object.entries(pendingChanges).map(([id, changes]: [string, Record<string, string>]) => {
        return { id: parseInt(id), ...changes }
      })

      const res = await fetch(`${API_BASE}/insurance-census/batch-update`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({ updates })
      })

      if (!res.ok) {
        const data = await res.json()
        throw new Error(data.detail || 'Failed to save changes')
      }

      const result = await res.json()
      setSaveMessage(`Saved ${result.updated} records successfully`)
      setPendingChanges({})
      await fetchData()

      setTimeout(() => setSaveMessage(null), 3000)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to save changes')
    } finally {
      setSaving(false)
    }
  }

  const handleDiscardChanges = () => {
    setPendingChanges({})
  }

  // Verification email functions
  const fetchVerificationStats = async () => {
    try {
      const res = await fetch(`${API_BASE}/census-verification/stats`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      if (res.ok) {
        setVerificationStats(await res.json())
      }
    } catch (err) {
      console.error('Failed to fetch verification stats:', err)
    }
  }

  const handleGenerateTokens = async () => {
    setSendingEmails(true)
    setError(null)
    try {
      const res = await fetch(`${API_BASE}/census-verification/generate-tokens`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({
          entity: entityFilter !== 'all' ? entityFilter : null,
          insurance_type: insuranceTypeFilter !== 'all' ? insuranceTypeFilter : null,
          missing_fields_only: true,
          expires_in_days: 14
        })
      })
      if (!res.ok) {
        const data = await res.json()
        throw new Error(data.detail || 'Failed to generate tokens')
      }
      const result = await res.json()
      setVerificationResult(result)
      await fetchVerificationStats()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate tokens')
    } finally {
      setSendingEmails(false)
    }
  }

  const handleSendEmails = async () => {
    setSendingEmails(true)
    setError(null)
    try {
      const res = await fetch(`${API_BASE}/census-verification/send-emails`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` }
      })
      if (!res.ok) {
        const data = await res.json()
        throw new Error(data.detail || 'Failed to send emails')
      }
      const result = await res.json()
      setVerificationResult(result)
      await fetchVerificationStats()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to send emails')
    } finally {
      setSendingEmails(false)
    }
  }

  const openVerificationModal = () => {
    setShowVerificationModal(true)
    setVerificationResult(null)
    fetchVerificationStats()
  }

  const getCellValue = (record: CensusRecord, field: string): string => {
    const pending = pendingChanges[record.id]?.[field]
    if (pending !== undefined) return pending
    const val = record[field as keyof CensusRecord]
    if (val === null || val === undefined) return ''
    if (typeof val === 'number') return val.toString()
    if (typeof val === 'boolean') return val ? 'Yes' : 'No'
    if (Array.isArray(val)) return val.join(', ')
    return val as string
  }

  const isMandatoryField = (field: string) => ALL_MANDATORY.includes(field)
  const isDhaDohField = (field: string) => DHA_DOH_VALIDATION_FIELDS.includes(field)

  const isMissingMandatory = (record: CensusRecord, field: string): boolean => {
    if (!isMandatoryField(field)) return false
    const val = getCellValue(record, field)
    return !val || val.trim() === ''
  }

  // Check if field is missing for DHA/DOH validation
  const isMissingDhaDoh = (record: CensusRecord, field: string): boolean => {
    if (!isDhaDohField(field)) return false
    return record.dha_doh_missing_fields?.includes(field) || false
  }

  // Check if field has been amended (for purple highlighting)
  const isAmendedField = (record: CensusRecord, field: string): boolean => {
    return record.amended_fields?.includes(field) || false
  }

  // Get row background style based on renewal status
  const getRowStyle = (record: CensusRecord): React.CSSProperties => {
    switch (record.renewal_status) {
      case 'deletion':
        return { backgroundColor: 'rgba(239, 68, 68, 0.15)' }  // Red - members to be deleted
      case 'addition':
        return { backgroundColor: 'rgba(34, 197, 94, 0.15)' }  // Green - new members to add
      default:
        return {}
    }
  }

  // Get row class based on renewal status
  const getRowClass = (record: CensusRecord): string => {
    switch (record.renewal_status) {
      case 'deletion':
        return 'border-l-4 border-l-red-500'
      case 'addition':
        return 'border-l-4 border-l-green-500'
      default:
        return ''
    }
  }

  const getEntityColor = (entity: string) => {
    return entity === 'watergeneration' ? '#00B0F0' : '#00bf63'
  }

  // Filter records based on renewal status
  const filteredRecords = renewalStatusFilter === 'all' 
    ? records 
    : records.filter(r => r.renewal_status === renewalStatusFilter)

  if (loading && records.length === 0) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-white">Loading census data...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <div className="max-w-full mx-auto p-4">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-4">
            <button
              onClick={onBack}
              className="px-4 py-2 bg-slate-800 hover:bg-slate-700 rounded-lg text-sm font-medium transition-colors"
            >
              ← Back
            </button>
            <h1 className="text-2xl font-bold">Medical Insurance Census</h1>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={openVerificationModal}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-500 rounded-lg text-sm font-medium transition-colors flex items-center gap-2"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              Send Verification Emails
            </button>
            {hasPendingChanges && (
              <>
                <span className="text-amber-400 text-sm">
                  {Object.keys(pendingChanges).length} records modified
                </span>
                <button
                  onClick={handleDiscardChanges}
                  className="px-4 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg text-sm font-medium transition-colors"
                >
                  Discard
                </button>
                <button
                  onClick={handleSaveChanges}
                  disabled={saving}
                  className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 rounded-lg text-sm font-medium transition-colors disabled:opacity-50"
                >
                  {saving ? 'Saving...' : 'Save Changes'}
                </button>
              </>
            )}
          </div>
        </div>

        {saveMessage && (
          <div className="mb-4 p-3 bg-emerald-900/50 border border-emerald-500 rounded-lg text-emerald-400">
            {saveMessage}
          </div>
        )}

        {error && (
          <div className="mb-4 p-3 bg-red-900/50 border border-red-500 rounded-lg text-red-400">
            {error}
          </div>
        )}

        {summary && (
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6">
            <div className="bg-slate-800 rounded-xl p-4">
              <div className="text-3xl font-bold">{summary.total}</div>
              <div className="text-slate-400 text-sm">Total Records</div>
            </div>
            <div className="bg-slate-800 rounded-xl p-4">
              <div className="text-3xl font-bold text-emerald-400">{summary.linked}</div>
              <div className="text-slate-400 text-sm">Linked to Employees</div>
            </div>
            <div className="bg-slate-800 rounded-xl p-4">
              <div className="text-3xl font-bold" style={{ color: '#00B0F0' }}>
                {summary.by_entity?.watergeneration || 0}
              </div>
              <div className="text-slate-400 text-sm">Watergeneration</div>
            </div>
            <div className="bg-slate-800 rounded-xl p-4">
              <div className="text-3xl font-bold" style={{ color: '#00bf63' }}>
                {summary.by_entity?.agriculture || 0}
              </div>
              <div className="text-slate-400 text-sm">Agriculture</div>
            </div>
            <div className="bg-slate-800 rounded-xl p-4">
              <div className="text-3xl font-bold">{Math.round(summary.avg_completeness)}%</div>
              <div className="text-slate-400 text-sm">Avg Completeness</div>
            </div>
          </div>
        )}

        <div className="flex flex-wrap items-center gap-4 mb-4">
          <div className="flex items-center gap-2">
            <label className="text-sm text-slate-400">Entity:</label>
            <select
              value={entityFilter}
              onChange={(e) => setEntityFilter(e.target.value)}
              className="bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-sm"
            >
              <option value="all">All Entities</option>
              <option value="watergeneration">Watergeneration</option>
              <option value="agriculture">Agriculture</option>
            </select>
          </div>
          <div className="flex items-center gap-2">
            <label className="text-sm text-slate-400">Type:</label>
            <select
              value={insuranceTypeFilter}
              onChange={(e) => setInsuranceTypeFilter(e.target.value)}
              className="bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-sm"
            >
              <option value="all">All Types</option>
              <option value="thiqa">Thiqa</option>
              <option value="expats">Expats</option>
            </select>
          </div>
          <div className="flex items-center gap-2">
            <label className="text-sm text-slate-400">Status:</label>
            <select
              value={renewalStatusFilter}
              onChange={(e) => setRenewalStatusFilter(e.target.value)}
              className="bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-sm"
            >
              <option value="all">All Status</option>
              <option value="existing">Existing</option>
              <option value="addition">🟢 Additions</option>
              <option value="deletion">🔴 Deletions</option>
            </select>
          </div>
          <div className="flex-1 min-w-[200px]">
            <input
              type="text"
              placeholder="Search by name, staff ID, Emirates ID..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 text-sm placeholder-slate-500"
            />
          </div>
          <div className="text-sm text-slate-400">
            Showing {filteredRecords.length} of {records.length} records
          </div>
        </div>

        <div className="bg-slate-900 rounded-xl border border-slate-700 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="bg-slate-800 border-b border-slate-700">
                  <th className="sticky left-0 bg-slate-800 px-2 py-3 text-left font-medium text-slate-300 z-10" style={{ width: '100px' }}>
                    Entity / Type
                  </th>
                  {DISPLAY_COLUMNS.map(col => (
                    <th
                      key={col.key}
                      className={`px-2 py-3 text-left font-medium ${isDhaDohField(col.key) ? 'text-cyan-400' : isMandatoryField(col.key) ? 'text-amber-400' : 'text-slate-300'}`}
                      style={{ minWidth: col.width }}
                    >
                      {col.label}
                      {isDhaDohField(col.key) && <span className="text-cyan-400 ml-1">◆</span>}
                      {isMandatoryField(col.key) && !isDhaDohField(col.key) && <span className="text-red-400 ml-1">*</span>}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {filteredRecords.map(record => (
                  <tr 
                    key={record.id} 
                    className={`border-b border-slate-800 hover:bg-slate-800/50 ${getRowClass(record)}`}
                    style={getRowStyle(record)}
                  >
                    <td className="sticky left-0 px-2 py-2 z-10" style={{
                      ...getRowStyle(record),
                      backgroundColor: record.renewal_status === 'deletion' ? 'rgba(239, 68, 68, 0.15)' : 
                                       record.renewal_status === 'addition' ? 'rgba(34, 197, 94, 0.15)' : 
                                       'rgb(15, 23, 42)'
                    }}>
                      <div className="flex flex-col gap-1">
                        <span
                          className="px-2 py-0.5 rounded text-xs font-medium text-white"
                          style={{ backgroundColor: getEntityColor(record.entity) }}
                        >
                          {record.entity === 'watergeneration' ? 'Water' : 'Agri'}
                        </span>
                        <span className="text-xs text-slate-400 capitalize">
                          {record.insurance_type}
                        </span>
                      </div>
                    </td>
                    {DISPLAY_COLUMNS.map(col => {
                      const isEditing = editingCell?.id === record.id && editingCell?.field === col.key
                      const cellValue = getCellValue(record, col.key)
                      const isMissing = isMissingMandatory(record, col.key)
                      const isMissingDha = isMissingDhaDoh(record, col.key)
                      const isAmended = isAmendedField(record, col.key)
                      const isPending = pendingChanges[record.id]?.[col.key] !== undefined

                      // Renewal status column
                      if (col.key === 'renewal_status') {
                        return (
                          <td key={col.key} className="px-2 py-2">
                            <span className={`px-2 py-1 rounded text-xs font-medium ${
                              record.renewal_status === 'deletion' ? 'bg-red-500/30 text-red-400' :
                              record.renewal_status === 'addition' ? 'bg-green-500/30 text-green-400' :
                              'bg-slate-700 text-slate-400'
                            }`}>
                              {record.renewal_status === 'deletion' ? '🔴 Delete' :
                               record.renewal_status === 'addition' ? '🟢 Add' : 'Existing'}
                            </span>
                          </td>
                        )
                      }

                      if (col.key === 'completeness_pct') {
                        const pct = record.completeness_pct
                        const dhaDohValid = record.dha_doh_valid
                        return (
                          <td key={col.key} className="px-2 py-2">
                            <div className="flex flex-col gap-1">
                              <div className="flex items-center gap-2">
                                <div className="w-16 h-2 bg-slate-700 rounded-full overflow-hidden">
                                  <div
                                    className={`h-full rounded-full ${pct >= 80 ? 'bg-emerald-500' : pct >= 50 ? 'bg-amber-500' : 'bg-red-500'}`}
                                    style={{ width: `${pct}%` }}
                                  />
                                </div>
                                <span className="text-xs">{pct}%</span>
                              </div>
                              {!dhaDohValid && (
                                <span className="text-xs text-red-400" title="DHA/DOH validation failed">⚠ DHA</span>
                              )}
                            </div>
                          </td>
                        )
                      }

                      // Determine cell background based on priority: amended (purple) > missing DHA (cyan warning) > missing mandatory (red) > pending (amber)
                      let cellBgClass = ''
                      if (isAmended) {
                        cellBgClass = 'bg-purple-900/40'  // Purple for amendments
                      } else if (isMissingDha) {
                        cellBgClass = 'bg-cyan-900/30'    // Cyan for missing DHA/DOH fields
                      } else if (isMissing) {
                        cellBgClass = 'bg-red-900/30'     // Red for missing mandatory
                      } else if (isPending) {
                        cellBgClass = 'bg-amber-900/30'   // Amber for pending changes
                      }

                      return (
                        <td
                          key={col.key}
                          className={`px-2 py-2 cursor-pointer ${cellBgClass}`}
                          onClick={() => handleCellClick(record.id, col.key, record[col.key as keyof CensusRecord] as string | null)}
                        >
                          {isEditing ? (
                            <input
                              type="text"
                              value={editValue}
                              onChange={(e) => handleCellChange(e.target.value)}
                              onBlur={handleCellBlur}
                              onKeyDown={handleKeyDown}
                              autoFocus
                              className="w-full bg-slate-700 border border-blue-500 rounded px-2 py-1 text-sm focus:outline-none"
                            />
                          ) : (
                            <span className={`${!cellValue ? 'text-slate-500 italic' : ''} ${isAmended ? 'font-semibold' : ''}`}>
                              {cellValue || (isMissing || isMissingDha ? 'Required' : '-')}
                            </span>
                          )}
                        </td>
                      )
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Legend */}
        <div className="mt-4 space-y-2 text-sm text-slate-400">
          <div className="flex flex-wrap gap-4">
            <span><span className="text-cyan-400">◆</span> = DHA/DOH Validation Required</span>
            <span><span className="text-red-400">*</span> = Other Mandatory Field</span>
          </div>
          <div className="flex flex-wrap gap-4">
            <span><span className="inline-block w-4 h-3 bg-red-500/30 rounded mr-1"></span>Deletion (Red row)</span>
            <span><span className="inline-block w-4 h-3 bg-green-500/30 rounded mr-1"></span>Addition (Green row)</span>
            <span><span className="bg-purple-900/40 px-2 py-0.5 rounded">Purple cells</span> = Amended fields</span>
          </div>
          <div className="flex flex-wrap gap-4">
            <span><span className="bg-red-900/30 px-2 py-0.5 rounded">Red cells</span> = Missing required data</span>
            <span><span className="bg-cyan-900/30 px-2 py-0.5 rounded">Cyan cells</span> = Missing DHA/DOH fields</span>
            <span><span className="bg-amber-900/30 px-2 py-0.5 rounded">Amber cells</span> = Pending changes</span>
          </div>
          <p className="text-xs mt-2 text-slate-500">
            <strong>DHA/DOH Validation:</strong> Passport-No, Visa File No (GDRFA), EID No, UID No, Nationality, DOB, Gender - required for UAE-based policy renewal
          </p>
        </div>
      </div>

      {/* Verification Email Modal */}
      {showVerificationModal && (
        <div 
          className="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4"
          onClick={() => setShowVerificationModal(false)}
        >
          <div 
            className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg max-h-[90vh] overflow-hidden"
            onClick={e => e.stopPropagation()}
          >
            {/* Header */}
            <div className="px-6 py-4 border-b border-slate-700 flex items-center justify-between">
              <div>
                <h2 className="text-lg font-semibold text-white">Send Verification Emails</h2>
                <p className="text-sm text-slate-400">Request employees to verify their insurance details</p>
              </div>
              <button
                onClick={() => setShowVerificationModal(false)}
                className="text-slate-400 hover:text-white transition-colors"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            {/* Stats */}
            {verificationStats && (
              <div className="px-6 py-4 border-b border-slate-700">
                <div className="grid grid-cols-4 gap-3">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-white">{verificationStats.total_tokens}</div>
                    <div className="text-xs text-slate-400">Total</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-blue-400">{verificationStats.emails_sent}</div>
                    <div className="text-xs text-slate-400">Sent</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-emerald-400">{verificationStats.verified}</div>
                    <div className="text-xs text-slate-400">Verified</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-amber-400">{verificationStats.pending}</div>
                    <div className="text-xs text-slate-400">Pending</div>
                  </div>
                </div>
              </div>
            )}

            {/* Content */}
            <div className="px-6 py-4 max-h-[50vh] overflow-y-auto">
              {!verificationResult ? (
                <div className="space-y-4">
                  <div className="p-4 bg-blue-900/30 border border-blue-700 rounded-lg">
                    <h4 className="font-medium text-blue-400 mb-2">How it works:</h4>
                    <ol className="text-sm text-slate-300 space-y-2 list-decimal list-inside">
                      <li>Generate unique verification links for each employee</li>
                      <li>Each employee receives an email with their personal link</li>
                      <li>They click the link to review and update their details</li>
                      <li>Changes are automatically tracked (purple highlighting)</li>
                    </ol>
                  </div>

                  <div className="p-4 bg-slate-800 rounded-lg">
                    <h4 className="font-medium text-white mb-2">Current Filter:</h4>
                    <div className="text-sm text-slate-300">
                      <p>Entity: <span className="text-cyan-400">{entityFilter === 'all' ? 'All' : entityFilter}</span></p>
                      <p>Type: <span className="text-cyan-400">{insuranceTypeFilter === 'all' ? 'All' : insuranceTypeFilter}</span></p>
                      <p className="text-xs text-slate-400 mt-2">Only employees with missing DHA/DOH fields will receive emails</p>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="space-y-4">
                  <div className="p-4 bg-emerald-900/30 border border-emerald-700 rounded-lg">
                    <h4 className="font-medium text-emerald-400 mb-2">✓ Success</h4>
                    {verificationResult.tokens_created !== undefined && (
                      <p className="text-sm text-slate-300">{verificationResult.tokens_created} verification tokens generated</p>
                    )}
                    {verificationResult.emails_prepared !== undefined && (
                      <p className="text-sm text-slate-300">{verificationResult.emails_prepared} emails prepared</p>
                    )}
                  </div>

                  {verificationResult.emails && verificationResult.emails.length > 0 && (
                    <div className="p-4 bg-slate-800 rounded-lg">
                      <h4 className="font-medium text-white mb-2">Email Preview ({verificationResult.emails.length})</h4>
                      <div className="space-y-2 max-h-40 overflow-y-auto">
                        {verificationResult.emails.slice(0, 5).map((email, idx) => (
                          <div key={idx} className="text-xs p-2 bg-slate-700 rounded">
                            <p className="text-slate-300">To: {email.to}</p>
                            <p className="text-slate-400 truncate">Link: {email.verification_url}</p>
                          </div>
                        ))}
                        {verificationResult.emails.length > 5 && (
                          <p className="text-xs text-slate-400">... and {verificationResult.emails.length - 5} more</p>
                        )}
                      </div>
                      <p className="text-xs text-amber-400 mt-2">Note: SMTP integration pending - emails shown for preview</p>
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* Actions */}
            <div className="px-6 py-4 border-t border-slate-700 flex justify-end gap-3">
              <button
                onClick={() => setShowVerificationModal(false)}
                className="px-4 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg text-sm font-medium transition-colors"
              >
                Close
              </button>
              {!verificationResult ? (
                <>
                  <button
                    onClick={handleGenerateTokens}
                    disabled={sendingEmails}
                    className="px-4 py-2 bg-blue-600 hover:bg-blue-500 rounded-lg text-sm font-medium transition-colors disabled:opacity-50"
                  >
                    {sendingEmails ? 'Generating...' : '1. Generate Tokens'}
                  </button>
                  <button
                    onClick={handleSendEmails}
                    disabled={sendingEmails}
                    className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 rounded-lg text-sm font-medium transition-colors disabled:opacity-50"
                  >
                    {sendingEmails ? 'Sending...' : '2. Send Emails'}
                  </button>
                </>
              ) : (
                <button
                  onClick={() => setVerificationResult(null)}
                  className="px-4 py-2 bg-blue-600 hover:bg-blue-500 rounded-lg text-sm font-medium transition-colors"
                >
                  Done
                </button>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
