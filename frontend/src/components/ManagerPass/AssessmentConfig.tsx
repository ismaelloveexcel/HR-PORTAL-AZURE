/**
 * Assessment Configuration Component
 * 
 * LOCKED DESIGN DECISION:
 * - Assessments are NOT stages - they are action-triggered events inside Screening/Interview
 * - They are optional, role-driven, and selectable
 * - They create temporary blocking actions
 * 
 * WHO CAN SELECT WHAT (LOCKED):
 * - Technical Assessment: Triggered by Manager (owns role competence)
 * - Soft Skill Assessment: Triggered by HR (owns culture & behavior)
 * - Combined Assessment: HR + Manager (senior/critical roles)
 * 
 * No candidate self-selection. Ever.
 * 
 * FLOW:
 * 1. Manager selects "Technical Assessment Required" → System triggers assessment
 * 2. HR assigns/reviews assessment → Sends to candidate
 * 3. Candidate completes → Manager (Technical) or HR (Soft) reviews results
 * 4. Pass/Fail decision → Proceed to interview or reject
 */

import { useState, useEffect } from 'react'

interface AssessmentConfigProps {
  recruitmentRequestId: number
  candidateId?: number  // If configuring for specific candidate
  positionTitle: string
  jobDescription?: string
  token: string
  entityColor?: string
  viewMode: 'manager' | 'hr'  // WHO is configuring
  currentStage?: 'screening' | 'interview'  // WHERE in the flow
  onConfigSaved?: (config: AssessmentConfigData) => void
  onClose?: () => void
  readonly?: boolean
}

interface AssessmentConfigData {
  // Type and Trigger
  assessment_type: 'technical' | 'soft_skill' | 'combined' | null
  triggered_by: 'manager' | 'hr' | null
  linked_stage: 'screening' | 'interview'
  // Status (LOCKED: required, sent, completed, failed, waived)
  status: 'not_required' | 'required' | 'sent' | 'completed' | 'failed' | 'waived'
  // Details
  assessment_link?: string
  notes?: string
  // Results (after completion)
  score?: number
  result?: 'pass' | 'fail'
}

interface AssessmentTemplate {
  id: number
  name: string
  type: 'soft_skill' | 'technical'
  description: string
  duration_minutes: number
  is_default: boolean
}

// Assessment status labels - LOCKED
const STATUS_LABELS = {
  not_required: 'Not Required',
  required: 'Assessment Required',
  sent: 'Sent to Candidate',
  completed: 'Completed',
  failed: 'Failed',
  waived: 'Waived'
}

export function AssessmentConfig({
  recruitmentRequestId,
  candidateId,
  positionTitle,
  jobDescription,
  token,
  entityColor = '#1800ad',
  viewMode,
  currentStage = 'screening',
  onConfigSaved,
  onClose,
  readonly = false
}: AssessmentConfigProps) {
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [config, setConfig] = useState<AssessmentConfigData>({
    assessment_type: null,
    triggered_by: null,
    linked_stage: currentStage,
    status: 'not_required',
    notes: ''
  })
  const [templates, setTemplates] = useState<AssessmentTemplate[]>([])
  const [generatingAssessment, setGeneratingAssessment] = useState(false)

  const API_URL = '/api'
  
  // Manager can only trigger technical, HR can trigger soft_skill or combined
  const canTriggerTechnical = viewMode === 'manager'
  const canTriggerSoftSkill = viewMode === 'hr'
  const canTriggerCombined = viewMode === 'hr'  // HR initiates combined, manager confirms

  useEffect(() => {
    fetchConfig()
    fetchTemplates()
  }, [recruitmentRequestId])

  const fetchConfig = async () => {
    try {
      setLoading(true)
      const response = await fetch(`${API_URL}/recruitment/requests/${recruitmentRequestId}/assessment-config`, {
        headers: { 'Authorization': `Bearer ${token}` }
      })
      if (response.ok) {
        const data = await response.json()
        setConfig(data)
      }
    } catch (err) {
      console.error('Failed to fetch assessment config:', err)
    } finally {
      setLoading(false)
    }
  }

  const fetchTemplates = async () => {
    try {
      const response = await fetch(`${API_URL}/recruitment/assessment-templates`, {
        headers: { 'Authorization': `Bearer ${token}` }
      })
      if (response.ok) {
        const data = await response.json()
        setTemplates(data)
      }
    } catch (err) {
      console.error('Failed to fetch templates:', err)
    }
  }

  const handleTechnicalToggle = async (required: boolean) => {
    const newConfig = {
      ...config,
      technical_required: required,
      technical_status: required ? 'pending_generation' as const : 'not_required' as const
    }
    setConfig(newConfig)

    if (required && jobDescription) {
      // Trigger assessment generation
      setGeneratingAssessment(true)
      try {
        const response = await fetch(`${API_URL}/recruitment/requests/${recruitmentRequestId}/generate-assessment`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({
            type: 'technical',
            job_description: jobDescription,
            position_title: positionTitle
          })
        })
        if (response.ok) {
          const data = await response.json()
          setConfig(prev => ({
            ...prev,
            technical_status: 'pending_hr_review',
            technical_assessment_link: data.assessment_link
          }))
        }
      } catch (err) {
        console.error('Failed to generate assessment:', err)
      } finally {
        setGeneratingAssessment(false)
      }
    }
  }

  const handleSoftSkillsToggle = (required: boolean) => {
    setConfig(prev => ({
      ...prev,
      soft_skills_required: required,
      soft_skills_status: required ? 'pending_hr_review' : 'not_required'
    }))
  }

  const handleTemplateSelect = (templateId: number) => {
    setConfig(prev => ({
      ...prev,
      soft_skills_template_id: templateId
    }))
  }

  const saveConfig = async () => {
    try {
      setSaving(true)
      const response = await fetch(`${API_URL}/recruitment/requests/${recruitmentRequestId}/assessment-config`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(config)
      })
      if (response.ok) {
        onConfigSaved?.(config)
        onClose?.()
      }
    } catch (err) {
      console.error('Failed to save config:', err)
    } finally {
      setSaving(false)
    }
  }

  const getStatusBadge = (status: keyof typeof STATUS_LABELS) => {
    const statusStyles = {
      not_required: 'bg-slate-100 text-slate-500',
      pending_generation: 'bg-amber-100 text-amber-700',
      pending_hr_review: 'bg-purple-100 text-purple-700',
      approved: 'bg-emerald-100 text-emerald-700',
      sent_to_candidate: 'bg-blue-100 text-blue-700'
    }
    return (
      <span className={`text-[9px] px-2 py-0.5 rounded-full font-semibold ${statusStyles[status]}`}>
        {STATUS_LABELS[status]}
      </span>
    )
  }

  if (loading) {
    return (
      <div className="p-6 text-center">
        <div className="w-8 h-8 border-2 border-slate-200 border-t-[#1800ad] rounded-full animate-spin mx-auto mb-2" />
        <p className="text-sm text-slate-500">Loading assessment configuration...</p>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-2xl shadow-lg overflow-hidden max-w-md w-full">
      {/* Header */}
      <div className="px-5 py-4 border-b border-slate-100">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-base font-bold text-slate-800">Assessment Configuration</h3>
            <p className="text-xs text-slate-500 mt-0.5">{positionTitle}</p>
          </div>
          {onClose && (
            <button onClick={onClose} className="p-1.5 hover:bg-slate-100 rounded-lg transition-colors">
              <svg className="w-5 h-5 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          )}
        </div>
      </div>

      <div className="p-5 space-y-5">
        {/* Technical Assessment */}
        <div className="rounded-xl border border-slate-200 p-4">
          <div className="flex items-start justify-between mb-3">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg flex items-center justify-center" style={{ backgroundColor: `${entityColor}15` }}>
                <svg className="w-4 h-4" style={{ color: entityColor }} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                </svg>
              </div>
              <div>
                <p className="text-sm font-semibold text-slate-800">Technical Assessment</p>
                <p className="text-[10px] text-slate-400">Auto-generated from Job Description</p>
              </div>
            </div>
            {getStatusBadge(config.technical_status)}
          </div>

          {/* Toggle */}
          <div className="flex items-center justify-between py-2 px-3 bg-slate-50 rounded-lg">
            <span className="text-xs text-slate-600">Required?</span>
            <button
              onClick={() => !readonly && handleTechnicalToggle(!config.technical_required)}
              disabled={readonly || generatingAssessment}
              className={`relative w-10 h-5 rounded-full transition-colors ${
                config.technical_required ? '' : 'bg-slate-300'
              } ${readonly ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
              style={config.technical_required ? { backgroundColor: entityColor } : {}}
            >
              <div className={`absolute top-0.5 left-0.5 w-4 h-4 bg-white rounded-full shadow transition-transform ${
                config.technical_required ? 'translate-x-5' : ''
              }`} />
            </button>
          </div>

          {generatingAssessment && (
            <div className="mt-3 flex items-center gap-2 p-2 bg-amber-50 rounded-lg">
              <div className="w-4 h-4 border-2 border-amber-200 border-t-amber-600 rounded-full animate-spin" />
              <span className="text-xs text-amber-700">Generating assessment from JD...</span>
            </div>
          )}

          {config.technical_required && config.technical_status === 'pending_hr_review' && (
            <div className="mt-3 p-2 bg-purple-50 rounded-lg">
              <p className="text-[10px] text-purple-700">
                <strong>Next:</strong> HR will review the generated assessment before it's sent to candidates.
              </p>
            </div>
          )}

          {config.technical_assessment_link && (
            <div className="mt-3">
              <a 
                href={config.technical_assessment_link}
                target="_blank"
                rel="noopener noreferrer"
                className="text-xs font-medium hover:underline"
                style={{ color: entityColor }}
              >
                Preview Assessment →
              </a>
            </div>
          )}
        </div>

        {/* Soft Skills Assessment */}
        <div className="rounded-xl border border-slate-200 p-4">
          <div className="flex items-start justify-between mb-3">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg flex items-center justify-center bg-emerald-50">
                <svg className="w-4 h-4 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
              <div>
                <p className="text-sm font-semibold text-slate-800">Soft Skills Assessment</p>
                <p className="text-[10px] text-slate-400">Uses HR-defined template</p>
              </div>
            </div>
            {getStatusBadge(config.soft_skills_status)}
          </div>

          {/* Toggle */}
          <div className="flex items-center justify-between py-2 px-3 bg-slate-50 rounded-lg">
            <span className="text-xs text-slate-600">Required?</span>
            <button
              onClick={() => !readonly && handleSoftSkillsToggle(!config.soft_skills_required)}
              disabled={readonly}
              className={`relative w-10 h-5 rounded-full transition-colors ${
                config.soft_skills_required ? 'bg-emerald-500' : 'bg-slate-300'
              } ${readonly ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
            >
              <div className={`absolute top-0.5 left-0.5 w-4 h-4 bg-white rounded-full shadow transition-transform ${
                config.soft_skills_required ? 'translate-x-5' : ''
              }`} />
            </button>
          </div>

          {/* Template Selection */}
          {config.soft_skills_required && templates.length > 0 && (
            <div className="mt-3">
              <p className="text-[10px] text-slate-500 mb-2">Select Template:</p>
              <div className="space-y-1.5">
                {templates.filter(t => t.type === 'soft_skills').map(template => (
                  <button
                    key={template.id}
                    onClick={() => !readonly && handleTemplateSelect(template.id)}
                    disabled={readonly}
                    className={`w-full p-2 rounded-lg text-left transition-colors ${
                      config.soft_skills_template_id === template.id
                        ? 'bg-emerald-50 border-2 border-emerald-500'
                        : 'bg-white border border-slate-200 hover:border-slate-300'
                    } ${readonly ? 'opacity-50' : ''}`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-medium text-slate-700">{template.name}</span>
                      <span className="text-[9px] text-slate-400">{template.duration_minutes} min</span>
                    </div>
                    <p className="text-[10px] text-slate-500 mt-0.5">{template.description}</p>
                    {template.is_default && (
                      <span className="inline-block mt-1 text-[8px] px-1.5 py-0.5 bg-emerald-100 text-emerald-600 rounded font-medium">
                        Default
                      </span>
                    )}
                  </button>
                ))}
              </div>
            </div>
          )}

          {config.soft_skills_required && templates.filter(t => t.type === 'soft_skills').length === 0 && (
            <div className="mt-3 p-2 bg-amber-50 rounded-lg">
              <p className="text-[10px] text-amber-700">
                No soft skills templates available. HR will create templates in the portal.
              </p>
            </div>
          )}
        </div>

        {/* Notes */}
        <div>
          <label className="block text-xs font-medium text-slate-600 mb-1.5">Notes for HR</label>
          <textarea
            value={config.notes || ''}
            onChange={(e) => !readonly && setConfig(prev => ({ ...prev, notes: e.target.value }))}
            disabled={readonly}
            placeholder="Any specific requirements or notes..."
            className={`w-full p-3 text-xs bg-slate-50 border border-slate-200 rounded-xl resize-none focus:outline-none focus:ring-2 focus:ring-[#1800ad]/20 ${
              readonly ? 'opacity-50' : ''
            }`}
            rows={2}
          />
        </div>

        {/* Info Notice */}
        <div className="p-3 bg-slate-50 rounded-xl">
          <div className="flex gap-2">
            <svg className="w-4 h-4 text-slate-400 flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p className="text-[10px] text-slate-500 leading-relaxed">
              <strong>How it works:</strong> Once you enable assessments, HR will review and approve them 
              before sending to candidates. Candidates will see "Assessment Pending" in their next actions.
            </p>
          </div>
        </div>
      </div>

      {/* Footer */}
      {!readonly && (
        <div className="px-5 py-4 border-t border-slate-100 flex gap-3">
          {onClose && (
            <button
              onClick={onClose}
              className="flex-1 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-600 rounded-xl text-xs font-medium transition-colors"
            >
              Cancel
            </button>
          )}
          <button
            onClick={saveConfig}
            disabled={saving}
            className="flex-1 py-2.5 text-white rounded-xl text-xs font-medium transition-colors disabled:opacity-50"
            style={{ backgroundColor: entityColor }}
          >
            {saving ? 'Saving...' : 'Save Configuration'}
          </button>
        </div>
      )}
    </div>
  )
}
