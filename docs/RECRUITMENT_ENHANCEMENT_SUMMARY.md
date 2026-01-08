# Recruitment Module Enhancement Summary

## Overview

This document summarizes the analysis, issues identified, and enhancements made to the recruitment module of the HR system.

---

## Task 1: Issues Identification & Fixes

### Issue 1: Missing `required_skills` Field

**Problem**: The CV scoring service referenced a `required_skills` field that didn't exist on the `RecruitmentRequest` model, causing the AI scoring to fail silently.

**Solution**: Added the following fields to the `RecruitmentRequest` model:
- `required_skills: JSON` - List of required skills for CV scoring
- `priority: String` - Request priority (low, normal, high, urgent)
- `expected_start_date: Date` - Expected candidate start date

**Files Changed**:
- `backend/app/models/recruitment.py`
- `backend/app/schemas/recruitment.py`

### Issue 2: Inconsistent Attribute Access

**Problem**: The code used `hasattr()` checks inconsistently for accessing model attributes.

**Solution**: Standardized to use `getattr(request, 'required_skills', None) or []` pattern for safer attribute access.

**Files Changed**:
- `backend/app/routers/recruitment.py`

---

## Task 2: Process Efficiency Improvements

### New Bulk Operations Endpoints

Added endpoints to enable bulk operations, significantly reducing processing time for common recruitment tasks.

#### 1. Bulk Stage Update
```
POST /api/recruitment/candidates/bulk/stage
```

**Purpose**: Move multiple candidates to a new stage in a single operation.

**Request Body**:
```json
{
  "candidate_ids": [1, 2, 3, 4, 5],
  "new_stage": "screening",
  "notes": "Passed initial review"
}
```

**Response**:
```json
{
  "success_count": 5,
  "failed_count": 0,
  "failed_ids": [],
  "message": "Successfully updated 5 candidates to stage 'screening'"
}
```

**Time Savings**: Reduces 5 individual API calls to 1, cutting processing time by ~80%.

#### 2. Bulk Candidate Rejection
```
POST /api/recruitment/candidates/bulk/reject
```

**Purpose**: Reject multiple candidates with a single reason.

**Request Body**:
```json
{
  "candidate_ids": [10, 11, 12],
  "rejection_reason": "Does not meet minimum experience requirements"
}
```

**Time Savings**: Especially useful during screening phase when rejecting multiple candidates.

### Enhanced Analytics Endpoint

```
GET /api/recruitment/metrics
```

**Purpose**: Provides comprehensive recruitment metrics for dashboards and reporting.

**Response includes**:
- **Request Counts**: total, active, filled, cancelled
- **Candidate Metrics**: by stage, source, and status
- **Conversion Rates**: 
  - Application → Screening rate
  - Screening → Interview rate
  - Interview → Offer rate
  - Offer acceptance rate
- **SLA Tracking**: Overdue requests count
- **Priority Distribution**: Requests by priority level

---

## Task 3: Graphics & Pass Design Enhancements

### Standardized Component Library

Created a standardized set of reusable components for consistent pass design:

#### 1. Enhanced PassHeader
- Entity-aware color theming (Agriculture = green, Default = blue)
- Consistent pass type labeling
- Subtle pattern overlays
- Responsive typography
- Standardized layout for avatar, title, subtitle, and actions

#### 2. StatusBadge Component (NEW)
- Multiple variants: success, warning, error, info, neutral, active
- Size variants: sm, md
- Optional pulse animation for active states
- Helper function `getStatusVariant()` for automatic variant detection

#### 3. Enhanced ActivityHistory
- Action-type specific icons with color coding
- Left accent lines matching action type
- Activity count badge
- Better empty state design
- Entity color support

#### 4. PassFooter Component (NEW)
- Consistent entity branding
- Subtle pattern overlays matching entity theme
- Context-aware labeling

### Visual Design Principles

1. **Entity Theming**: All passes automatically adapt colors based on entity:
   - Agriculture Division: `#00bf63` (green)
   - Default/Water: `#00B0F0` (blue)
   - Manager Pass: `#1800ad` (deep blue)

2. **Consistent Spacing**: Standardized padding and margins across all components

3. **Typography Scale**:
   - Headers: 16-18px, font-black
   - Labels: 10-11px, uppercase tracking
   - Body: 11-12px, medium weight

4. **Mobile-First**: All components are responsive with sm: breakpoints

---

## Usage Examples

### Using the New Bulk Endpoints

```python
import requests

# Bulk shortlist candidates after screening
response = requests.post(
    "/api/recruitment/candidates/bulk/stage",
    json={
        "candidate_ids": [1, 2, 3, 4, 5],
        "new_stage": "interview",
        "notes": "Shortlisted for technical interview"
    },
    headers={"Authorization": f"Bearer {token}"}
)
print(f"Updated {response.json()['success_count']} candidates")
```

### Using StatusBadge Component

```tsx
import { StatusBadge, getStatusVariant } from '../BasePass'

// Automatic variant detection
<StatusBadge 
  label={status} 
  variant={getStatusVariant(status)} 
/>

// Active status with pulse
<StatusBadge 
  label="Active" 
  variant="active" 
  pulse={true}
  entityColor="#00bf63"
/>
```

---

## API Reference

### New Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/recruitment/candidates/bulk/stage` | Bulk update candidate stages |
| POST | `/recruitment/candidates/bulk/reject` | Bulk reject candidates |
| GET | `/recruitment/metrics` | Get detailed recruitment analytics |

### Updated Schemas

#### RecruitmentRequestCreate
New optional fields:
- `required_skills: List[str]` - Skills for CV scoring
- `priority: str` - Priority level (default: "normal")
- `expected_start_date: date` - Expected start date

#### BulkOperationResult
```python
{
    "success_count": int,
    "failed_count": int,
    "failed_ids": List[int],
    "message": str
}
```

#### RecruitmentMetrics
Comprehensive metrics including conversion rates, SLA tracking, and pipeline statistics.

---

## Performance Impact

| Operation | Before | After | Improvement |
|-----------|--------|-------|-------------|
| Shortlist 10 candidates | 10 API calls | 1 API call | 90% reduction |
| Reject 20 candidates | 20 API calls | 1 API call | 95% reduction |
| Dashboard load | Multiple endpoints | Single metrics endpoint | Faster load time |

---

## Phase 2: Enhanced Features (from JSON Analysis)

### New Model Fields Added

#### RecruitmentRequest
- `location` - Work location (Abu Dhabi HQ, Dubai Office, Remote, Hybrid)
- `experience_min/max` - Experience range in years
- `education_level` - Required education level
- `benefits` - Position benefits as tags
- `reporting_to` - Position reports to

#### Candidate
- `ai_score_breakdown` - Detailed AI scoring breakdown (skills, experience, education, salary, culture fit)
- `hr_rating` - HR rating (1-5)
- `manager_rating` - Hiring manager rating (1-5)
- `last_activity_at` - Last activity timestamp

### New Models

#### Assessment
Tracks candidate assessments (soft-skills, technical, cognitive, personality):
- Links to candidate and recruitment request
- Tracks status, score, pass/fail
- Supports external assessment platforms

#### Offer
Comprehensive offer management:
- Full compensation package (base, housing, transport, other allowances)
- Employment terms (contract type, probation, working hours, leave)
- Benefits and special conditions
- Approval workflow and response tracking

#### NextStep
Structured next action for candidates:
- Label, description, instructions
- Scheduling details (date, time, location, meeting link)
- Status tracking

### New Reference Data Constants
- `INTERVIEW_ROUNDS` - Named interview rounds (HR Screening, Technical 1/2, Panel, Final, CEO)
- `WORK_LOCATIONS` - Standard work locations
- `EDUCATION_LEVELS` - Education requirements
- `CANDIDATE_SOURCES` - Application sources (LinkedIn, Indeed, Bayt, GulfTalent, etc.)
- `NOTICE_PERIODS` - Standard notice periods with days
- `AI_SCORING_CRITERIA` - Weighted scoring criteria

---

## Manager Pass Flip Feature

The Manager Pass now supports flipping to show recruitment metrics on the back:

### Front (Unchanged)
- All existing functionality remains
- New flip button added to header (chart icon)

### Back Panel (Metrics)
Shows key recruitment metrics:
1. **Days Since Request Raised** - Counter based on request creation date
2. **Applications Received** - Total candidate count
3. **Application Sources** - Agency/Direct/Referral breakdown with progress bars
4. **Candidates Shortlisted** - Number in screening+ stages
5. **Candidates Interviewed** - Completed interviews only

### Usage
- Click the chart icon in the header to flip to metrics
- Click "Tap to flip back" or the flip button to return to front

### Component
```tsx
import { PassMetricsBack } from '../ManagerPass'

<PassMetricsBack
  metrics={{
    daysSinceRequest: 15,
    applicationsReceived: 45,
    applicationSources: { agency: 10, direct: 25, referral: 10 },
    candidatesShortlisted: 12,
    candidatesInterviewed: 5
  }}
  positionTitle="Senior Developer"
  requestNumber="RR-2026-001"
  onFlip={() => setIsFlipped(false)}
/>
```

---

## Visual Alignment: Candidate Pass & Manager Pass

Both passes are now visually aligned with consistent structure and linked fields:

### Unified Header Structure
- **Colored header bar** - Entity-themed color for Candidate Pass, deep blue for Manager Pass
- **Glassmorphism info card** - Overlapping card with subtle transparency
- **QR Code** - Positioned right with hover effects
- **Stage/Status row** - Consistent color indicators and typography

### Linked Fields (Displayed on Both Passes)
| Field | Candidate Pass | Manager Pass |
|-------|----------------|--------------|
| Primary Title | Position Title | Position Title |
| Secondary | Department | Department |
| Identifier | Candidate Number | Pass ID |
| Name | Full Name | Manager Name |
| Reference | Recruitment Request # | Recruitment Request # |
| Stage | Current Stage | Current Stage |
| Status | Active/Pending | Active/In Progress |

### Centralized Theming
Both passes now use `getEntityColor()` from `entityTheme.ts` for consistent colors:
- Agriculture Division: `#00bf63` (green)
- Watergeneration/Default: `#00B0F0` (blue)
- Manager Pass Header: `#1800ad` (deep blue)

---

## Workflow Configuration: Governing Logic

### Non-Negotiable Rules
1. **Statuses do not do work — Actions do**
2. **Each status maps to ONE primary Next Action**
3. **Action Owner is singular (no shared accountability)**
4. **Candidate Pass = visibility only**
5. **HR / System triggers stage movement**
6. **Manager actions are decision-gated**
7. **HR is the superuser and only HR can manually revise passes**

### Interview Slot Selection Workflow

The interview scheduling follows this workflow:

1. **Manager Provides Availability**
   - Manager adds available time slots via the Manager Pass
   - Interview status changes to `slots_provided`
   - Candidate status changes to `slots_available`

2. **Candidate Selects Slot**
   - Available slots are displayed on Candidate Pass
   - Candidate selects their preferred time
   - Selected slot is booked and marked unavailable to other candidates

3. **Slot Exclusivity**
   - Once a slot is booked, it becomes unavailable across all interviews for that position
   - This prevents double-booking of manager's time

4. **HR Oversight**
   - Only HR can manually modify bookings or reschedule interviews
   - Managers can only provide availability, not edit bookings

### Stage-Status-Action Matrix

#### Stage 1: Application / Request

| Role | Status | Next Action | Action Owner |
|------|--------|-------------|--------------|
| Candidate | Submitted | Validate application completeness | HR |
| Candidate | Incomplete | Submit missing information | Candidate |
| Candidate | Validated | Initiate screening | HR |
| Candidate | Withdrawn | Close application | System |
| Manager | Raised | Review & approve request | Manager |
| Manager | Approved | Open application intake | HR |
| Manager | On Hold | Monitor / await decision | Manager |
| Manager | Cancelled | Close request | System |

#### Stage 2: Shortlist / Screening

| Role | Status | Next Action | Action Owner |
|------|--------|-------------|--------------|
| Candidate | Under Review | Complete screening | HR |
| Candidate | Shortlisted | Prepare interview | HR |
| Candidate | Not Shortlisted | Close candidate record | System |
| Candidate | On Hold | Await decision | HR |
| Manager | In Progress | Review candidate profile | Manager |
| Manager | Shortlisted | Confirm interview intent | Manager |
| Manager | Rejected | Close candidate | HR |
| Manager | On Hold | Reassess later | Manager |

#### Stage 3: Interview

| Role | Status | Next Action | Action Owner |
|------|--------|-------------|--------------|
| Candidate | Pending | Schedule interview | HR |
| Candidate | Slots Available | Select interview slot | Candidate |
| Candidate | Scheduled | Confirm attendance | Candidate |
| Candidate | Confirmed | Attend interview | Candidate |
| Candidate | Completed | Await feedback | HR |
| Candidate | Cancelled | Reschedule interview | HR |
| Candidate | No Show | Close or reschedule | HR |
| Manager | Pending | Provide availability | Manager |
| Manager | Slots Provided | Await candidate selection | System |
| Manager | Scheduled | Conduct interview | Manager |
| Manager | Completed | Submit feedback | Manager |
| Manager | Feedback Pending | Submit evaluation | Manager |
| Manager | Additional Required | Schedule next round | HR |

#### Stage 4: Offer / Decision

| Role | Status | Next Action | Action Owner |
|------|--------|-------------|--------------|
| Candidate | In Preparation | Await offer | HR |
| Candidate | Released | Review and respond | Candidate |
| Candidate | Accepted | Initiate onboarding | HR |
| Candidate | Declined | Close candidate | System |
| Candidate | Negotiating | Review revised terms | Candidate |
| Candidate | Expired | Close or re-offer | HR |
| Manager | Pending | Make hire/no-hire decision | Manager |
| Manager | Approved | Prepare offer letter | HR |
| Manager | Not Approved | Close candidate | HR |
| Manager | Released | Await candidate response | System |
| Manager | Accepted | Initiate onboarding | HR |
| Manager | Declined | Review pipeline | Manager |

#### Stage 5: Onboarding

| Role | Status | Next Action | Action Owner |
|------|--------|-------------|--------------|
| Candidate | Initiated | Submit onboarding documents | Candidate |
| Candidate | Documents Pending | Upload required documents | Candidate |
| Candidate | Documents Submitted | Verify documents | HR |
| Candidate | Pre-Joining | Complete pre-joining tasks | Candidate |
| Candidate | Joining Confirmed | Prepare for Day 1 | HR |
| Candidate | Completed | Convert to employee | HR |
| Candidate | No Show | Close candidate | System |
| Manager | Initiated | Monitor progress | Manager |
| Manager | Documentation | Await completion | System |
| Manager | Joining Confirmed | Prepare workspace | Manager |
| Manager | Completed | Close recruitment pass | HR |

---

## New Components: Interview Slot Management

### InterviewSlotSelector (Candidate Pass)
Located at: `frontend/src/components/CandidatePass/InterviewSlotSelector.tsx`

Features:
- Displays available time slots grouped by date
- Shows slot duration and time in local format
- Highlights already-booked slots
- Prevents selection of slots booked by other candidates
- Confirmation button with loading state
- Error handling for failed bookings

### InterviewSlotProvider (Manager Pass)
Located at: `frontend/src/components/ManagerPass/InterviewSlotProvider.tsx`

Features:
- Add new time slots with date/time pickers
- View existing slots with booked status
- See which candidates have booked slots
- Remove unbooked slots
- HR-only notice for modifying bookings

---

## API Endpoints: Interview Slot Selection

### Provide Interview Slots (Manager/HR)
```
POST /api/recruitment/interviews/{interview_id}/slots
```
Provides available time slots for an interview.

### Select Interview Slot (Candidate Self-Service)
```
POST /api/recruitment/interviews/{interview_id}/select-slot
```
Allows candidates to select a slot using their pass token.

**Request Body**:
```json
{
  "selected_slot": {
    "start": "2026-01-15T10:00:00Z",
    "end": "2026-01-15T11:00:00Z"
  },
  "pass_token": "abc123...64chars"
}
```

**Security**:
- Requires valid pass_token
- Rate limited to 10 requests/minute
- Validates candidate owns the interview
- Constant-time token comparison

---

## Migration Notes

No database migrations required for the new fields as they are nullable. The system will work with existing data - new features will simply not be available until the fields are populated.

For existing recruitment requests, you can update them to include `required_skills`:

```sql
UPDATE recruitment_requests 
SET required_skills = '["Python", "SQL", "FastAPI"]'
WHERE position_title LIKE '%Developer%';
```

---

## Assessments - LOCKED DESIGN DECISION

### Positioning (Non-Negotiable)

- Assessments live inside **STAGE 2 (SCREENING)** and **STAGE 3 (INTERVIEW)**
- They are **action-triggered events**, not standalone stages
- They are optional, role-driven, and selectable
- They create temporary blocking actions

This preserves:
- One stage at a time
- Clean enums
- No stage explosion

### Who Can Select What (LOCKED)

| Assessment Type | Triggered By | Rationale |
|-----------------|--------------|-----------|
| Technical Assessment | Manager | Owns role competence |
| Soft Skill Assessment | HR | Owns culture & behavior |
| Combined Assessment | HR + Manager | Senior / critical roles |

**No candidate self-selection. Ever.**

### Assessment Statuses (Sub-status flags, not stage drivers)

```typescript
type AssessmentStatus = 
  | 'required'    // Assessment Required
  | 'sent'        // Assessment Sent
  | 'completed'   // Assessment Completed
  | 'failed'      // Assessment Failed
  | 'waived'      // Assessment Waived
```

### Assessment Flow

1. **Triggering**: Manager selects "Technical Assessment Required" OR HR selects "Soft Skill Assessment Required"
2. **System Action**: Freeze stage progression, set assessment_required = true
3. **HR assigns**: Technical test or Soft skill assessment
4. **System sends**: Assessment to candidate
5. **Candidate completes**: Assessment in Progress (visible on pass)
6. **Review**: Manager (Technical) / HR (Soft) reviews results
7. **Decision**: Pass → Proceed to interview; Fail → Reject candidate

### Backend Model

```python
class Assessment(Base):
    __tablename__ = "assessments"
    
    id: int
    candidate_id: int
    recruitment_request_id: int
    
    # LOCKED: technical, soft_skill, combined
    assessment_type: str
    # LOCKED: manager, hr
    triggered_by: str
    # Stage when triggered: screening or interview
    linked_stage: str
    
    # LOCKED: required, sent, completed, failed, waived
    status: str
    
    # Results
    score: Optional[int]
    result: Optional[str]  # pass, fail
```

---

## Applicant List (Pipeline View) - LOCKED DESIGN

### Purpose

- Fast scanning
- Decision prioritization
- Bottleneck visibility
- Zero scrolling into profiles unless necessary

### Fields That SHOULD Appear

| Category | Field | Source |
|----------|-------|--------|
| Identity | Candidate Name | CV (auto) |
| | Current Job Title | CV (auto) |
| | Current Company | CV (auto) |
| Role Fit | Applied Position | Application form |
| | Years of Experience (rounded) | CV (auto) |
| | Location / Country | CV (auto) |
| Progress | Current Stage | System |
| | Current Status | System |
| | Assessment Status | System |
| | Interview Status | System |
| Signals | Assessment Score (if any) | Assessment |
| | Interview Outcome (icon) | Manager |
| Risk | Days in Stage (counter) | System |
| | On Hold Flag | System |

### Fields That MUST NOT Appear in List View

- CV text
- Salary expectations
- Soft skill comments
- Internal notes
- Detailed assessment breakdown

**Why**: List view is for velocity, not judgment.

---

## Applicant Profile - LOCKED DATA OWNERSHIP

### A. Auto-Extracted from CV (System-controlled)

Editable only via HR override, never directly by candidate.

| Section | Field |
|---------|-------|
| Identity | Full Name, Email, Phone |
| Professional | Current Job Title, Current Company |
| | Employment History (company + role + dates) |
| | Total Years of Experience |
| | Education (degree, institution) |
| | Core Skills (parsed keywords) |
| | Certifications (if listed) |

### B. Candidate-Filled (Form-driven, Mandatory)

| Section | Field | Why |
|---------|-------|-----|
| Profile | Preferred Name | UX |
| | Nationality | Visa logic |
| | Current Location | Hiring logistics |
| | Right to Work Status | Compliance |
| | Notice Period | Hiring timeline |
| Role Alignment | Availability to Join | Planning |
| | Willingness to Relocate | Decision |
| | Work Mode Preference | Policy |
| Compensation | Salary Expectation (range) | Offer gating |
| | Current Salary (optional) | Benchmarking |

### C. Internal Only (HR/Manager)

Hidden from candidate:
- Source (Agency/Referral/Direct)
- Recruiter Assigned
- Internal Fit Indicator
- Risk Flags (Visa, Gap, Job Hopping)
- Assessment logic, Scores, Decision rationale
- Offer readiness

---

## Manager Pass Dashboard (Multiple Recruitment Requests)

When a manager has multiple recruitment requests, they see a dashboard showing all their passes:

### Features

- View all recruitment passes at a glance
- Filter by status (Active, Screening, Interviewing, Filled, On Hold)
- Summary stats (Total Positions, Total Candidates, Interviewed)
- Click to open specific pass

### Each Pass Card Shows

- Position Title & Department
- Priority indicator (Urgent, High, Normal, Low)
- Status badge
- Days since request
- Candidate counts (Applied, Shortlisted, Interviewed)

### Usage

```tsx
import { ManagerPassDashboard } from '../ManagerPass'

<ManagerPassDashboard
  managerId="MGR-001"
  token={authToken}
  onSelectPass={(requestId) => openPass(requestId)}
/>
```

---

## HR Applicant List Component

Unified view for HR to manage candidates across ALL positions. Designed for solo HR managing multiple recruitment requests.

### Features

- Filter by position/recruitment request
- Filter by stage and status
- Filter by on-hold status
- Filter by assessment status
- Bulk actions (stage transitions, rejections)
- Sort by newest, oldest, longest in stage, best score, name

### Bulk Actions

- Move to Screening
- Move to Interview
- Reject (with reason)

### Usage

```tsx
import { HRApplicantList } from '../HRDashboard'

<HRApplicantList
  token={authToken}
  onSelectCandidate={(id) => openProfile(id)}
  onBulkAction={(action, ids) => handleBulkAction(action, ids)}
/>
```

---

## New API Endpoints

### Get Manager Passes

```
GET /api/recruitment/manager/{manager_id}/passes
```

Returns all recruitment requests/passes for a specific manager.

**Response**:
```json
[
  {
    "id": 1,
    "pass_id": "MGR-RR-2026-001",
    "position_title": "Senior Developer",
    "department": "Engineering",
    "status": "active",
    "total_candidates": 45,
    "candidates_shortlisted": 12,
    "candidates_interviewed": 5,
    "days_since_request": 15,
    "priority": "high",
    "created_at": "2026-01-01T10:00:00Z"
  }
]
```

### Enhanced Candidates for Request (Pipeline View)

```
GET /api/recruitment/requests/{request_id}/candidates
```

Now returns PIPELINE VIEW fields only:
- Identity: Name, Current Job Title, Current Company
- Role Fit: Position, Years of Experience, Location
- Progress: Stage, Status, Assessment Status, Interview Status
- Signals: Assessment Score, Interview Outcome
- Risk: Days in Stage, On Hold Flag
