# HR Templates Reference Guide

This document provides a reference for the HR templates available in the Secure Renewals HR Portal.

## Available Templates

### 1. Performance Evaluation 2025 - Non-Managerial Positions

**Type:** Document  
**Purpose:** Annual performance evaluation for non-managerial employees  
**Target Users:** Line Managers, HR  

#### Template Sections:
- **Section A:** Employee Information
- **Section B:** Performance Criteria (7 criteria with weighted scoring)
  - Job Knowledge & Skills (20%)
  - Quality of Work (20%)
  - Productivity & Efficiency (15%)
  - Communication & Teamwork (15%)
  - Initiative & Problem Solving (15%)
  - Attendance & Punctuality (10%)
  - Adherence to Policies (5%)
- **Section C:** Overall Performance Score Calculation
- **Section D:** Achievements & Key Accomplishments
- **Section E:** Areas for Improvement
- **Section F:** Development Goals for 2026
- **Section G:** Employee Self-Assessment
- **Section H:** Signatures

#### Rating Scale:
| Rating | Description |
|--------|-------------|
| 5 | Outstanding |
| 4 | Exceeds Expectations |
| 3 | Meets Expectations |
| 2 | Needs Improvement |
| 1 | Needs Significant Improvement |

---

### 2. Performance Evaluation 2025 - Managerial Positions

**Type:** Document  
**Purpose:** Annual performance evaluation for managers and leaders  
**Target Users:** Senior Leadership, HR  

#### Template Sections:
- **Section A:** Manager Information
- **Section B:** Leadership Competencies (8 criteria with weighted scoring)
  - Strategic Thinking & Planning (15%)
  - Team Leadership & Development (20%)
  - Decision Making & Problem Solving (15%)
  - Communication & Stakeholder Management (15%)
  - Performance Management (10%)
  - Operational Excellence (10%)
  - Financial Acumen (10%)
  - Innovation & Change Management (5%)
- **Section C:** Departmental KPIs & Achievements
- **Section D:** Team Development
- **Section E:** Overall Performance Score
- **Section F:** Areas for Improvement
- **Section G:** Leadership Development Goals for 2026
- **Section H:** Manager Self-Assessment
- **Section I:** 360-Degree Feedback Summary (Optional)
- **Section J:** Signatures

---

### 3. Employee of the Year Nomination 2025

**Type:** Document  
**Purpose:** Nomination form for the annual Employee of the Year recognition program  
**Target Users:** All Employees  

#### Template Sections:
- **About This Award:** Criteria and eligibility
- **Section A:** Nominee Information
- **Section B:** Nominator Information
- **Section C:** Nomination Criteria (5 rating areas)
  - Job Performance
  - Company Values
  - Teamwork & Collaboration
  - Innovation & Initiative
  - Customer/Stakeholder Focus
- **Section D:** Key Achievements in 2025
- **Section E:** Impact on the Organization
- **Section F:** Nomination Statement (250 words)
- **Section G:** Supporting Endorsements (Optional)
- **Section H:** Nominator Declaration
- **HR Use Only:** Processing section

---

## How to Use Templates

### Via API

```http
# List all templates
GET /api/templates

# Get specific template by ID
GET /api/templates/{template_id}

# Filter by type
GET /api/templates?type=document

# Create new template (HR/Admin only)
POST /api/templates
Content-Type: application/json

{
  "name": "Template Name",
  "type": "document",
  "content": "Template content with {{placeholders}}"
}
```

### Via HR Portal

1. Navigate to **Templates** section
2. Select the desired template type
3. Click on the template to view/edit
4. Use "Generate Document" to create filled version

### Seeding Templates

To add these templates to a fresh database:

```bash
cd backend
uv run python ../scripts/seed_hr_templates.py
```

---

## Template Variables

Templates use `{{variable_name}}` syntax for dynamic content. When generating documents, these placeholders are replaced with actual employee data.

### Common Variables

| Variable | Description |
|----------|-------------|
| `{{employee_name}}` | Full name of the employee |
| `{{employee_number}}` | Employee ID |
| `{{job_title}}` | Current job title |
| `{{department}}` | Department name |
| `{{line_manager}}` | Direct manager's name |
| `{{evaluation_date}}` | Date of evaluation |

---

## Customization

Templates can be customized through:
1. **Revisions:** Create a new version while keeping history
2. **Direct Edit:** Update existing template (HR/Admin only)
3. **Clone:** Create a copy with different name/settings

### Creating a Revision

```http
POST /api/templates/{template_id}/revision
Content-Type: application/json

{
  "content": "Updated template content",
  "revision_note": "Added new section for compliance"
}
```

---

## Best Practices

1. **Version Control:** Always use revisions for major changes
2. **Testing:** Preview generated documents before distribution
3. **Consistency:** Use standard variable names across templates
4. **Accessibility:** Ensure templates are clear and easy to complete
5. **Compliance:** Update templates annually to reflect policy changes

---

## Related Documentation

- [HR User Guide](HR_USER_GUIDE.md)
- [HR Implementation Plan](HR_IMPLEMENTATION_PLAN.md)
- [Process Simplification (UAE)](PROCESS_SIMPLIFICATION_UAE.md)

---

*Last Updated: January 2025*
