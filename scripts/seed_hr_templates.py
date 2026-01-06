#!/usr/bin/env python3
"""
Seed HR Templates for Performance Evaluation and Employee Recognition

This script creates the following templates:
1. Performance Evaluation - Non-Managerial Positions (2025)
2. Performance Evaluation - Managerial Positions (2025)
3. Employee of the Year Nomination Form

Usage:
    cd backend
    uv run python ../scripts/seed_hr_templates.py
"""

import asyncio
import os
import sys

# Add backend to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.database import get_engine, AsyncSessionLocal
from app.models.template import Template
from sqlalchemy import select


# Performance Evaluation Template - Non-Managerial Positions
PERFORMANCE_EVAL_NON_MANAGERIAL = """
# PERFORMANCE EVALUATION FORM 2025
## Non-Managerial Positions

---

### SECTION A: EMPLOYEE INFORMATION

| Field | Value |
|-------|-------|
| Employee Name | {{employee_name}} |
| Employee Number | {{employee_number}} |
| Job Title | {{job_title}} |
| Department | {{department}} |
| Line Manager | {{line_manager}} |
| Evaluation Period | January 1, 2025 - December 31, 2025 |
| Date of Evaluation | {{evaluation_date}} |

---

### SECTION B: PERFORMANCE CRITERIA

Rate each criterion on a scale of 1-5:
- **1** = Needs Significant Improvement
- **2** = Needs Improvement
- **3** = Meets Expectations
- **4** = Exceeds Expectations
- **5** = Outstanding

#### 1. JOB KNOWLEDGE & SKILLS (Weight: 20%)
Understanding of job responsibilities, technical skills, and required competencies.

| Rating (1-5) | Comments |
|--------------|----------|
| {{job_knowledge_rating}} | {{job_knowledge_comments}} |

#### 2. QUALITY OF WORK (Weight: 20%)
Accuracy, thoroughness, and attention to detail in work output.

| Rating (1-5) | Comments |
|--------------|----------|
| {{quality_rating}} | {{quality_comments}} |

#### 3. PRODUCTIVITY & EFFICIENCY (Weight: 15%)
Volume of work completed, meeting deadlines, and efficient use of time.

| Rating (1-5) | Comments |
|--------------|----------|
| {{productivity_rating}} | {{productivity_comments}} |

#### 4. COMMUNICATION & TEAMWORK (Weight: 15%)
Effectiveness in verbal/written communication and collaboration with colleagues.

| Rating (1-5) | Comments |
|--------------|----------|
| {{communication_rating}} | {{communication_comments}} |

#### 5. INITIATIVE & PROBLEM SOLVING (Weight: 15%)
Proactive approach, creativity in solving problems, and willingness to take on challenges.

| Rating (1-5) | Comments |
|--------------|----------|
| {{initiative_rating}} | {{initiative_comments}} |

#### 6. ATTENDANCE & PUNCTUALITY (Weight: 10%)
Regularity, punctuality, and adherence to work schedules.

| Rating (1-5) | Comments |
|--------------|----------|
| {{attendance_rating}} | {{attendance_comments}} |

#### 7. ADHERENCE TO POLICIES (Weight: 5%)
Compliance with company policies, procedures, and workplace conduct.

| Rating (1-5) | Comments |
|--------------|----------|
| {{policies_rating}} | {{policies_comments}} |

---

### SECTION C: OVERALL PERFORMANCE SCORE

| Criterion | Weight | Rating | Weighted Score |
|-----------|--------|--------|----------------|
| Job Knowledge & Skills | 20% | {{job_knowledge_rating}} | |
| Quality of Work | 20% | {{quality_rating}} | |
| Productivity & Efficiency | 15% | {{productivity_rating}} | |
| Communication & Teamwork | 15% | {{communication_rating}} | |
| Initiative & Problem Solving | 15% | {{initiative_rating}} | |
| Attendance & Punctuality | 10% | {{attendance_rating}} | |
| Adherence to Policies | 5% | {{policies_rating}} | |
| **TOTAL** | 100% | | **{{overall_score}}** |

**Overall Rating:**
- 4.5 - 5.0: Outstanding
- 3.5 - 4.4: Exceeds Expectations
- 2.5 - 3.4: Meets Expectations
- 1.5 - 2.4: Needs Improvement
- 1.0 - 1.4: Needs Significant Improvement

---

### SECTION D: ACHIEVEMENTS & KEY ACCOMPLISHMENTS

List major achievements during the evaluation period:

{{achievements}}

---

### SECTION E: AREAS FOR IMPROVEMENT

Identify areas where the employee can improve:

{{improvement_areas}}

---

### SECTION F: DEVELOPMENT GOALS FOR 2026

| Goal | Target Date | Resources Needed |
|------|-------------|------------------|
| {{goal_1}} | {{goal_1_date}} | {{goal_1_resources}} |
| {{goal_2}} | {{goal_2_date}} | {{goal_2_resources}} |
| {{goal_3}} | {{goal_3_date}} | {{goal_3_resources}} |

---

### SECTION G: EMPLOYEE SELF-ASSESSMENT

**Employee Comments:**
{{employee_comments}}

---

### SECTION H: SIGNATURES

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Employee | {{employee_name}} | _____________ | {{employee_sign_date}} |
| Line Manager | {{line_manager}} | _____________ | {{manager_sign_date}} |
| HR Representative | {{hr_representative}} | _____________ | {{hr_sign_date}} |

---

*This evaluation is confidential and will be maintained in the employee's personnel file.*
"""


# Performance Evaluation Template - Managerial Positions
PERFORMANCE_EVAL_MANAGERIAL = """
# PERFORMANCE EVALUATION FORM 2025
## Managerial Positions

---

### SECTION A: MANAGER INFORMATION

| Field | Value |
|-------|-------|
| Manager Name | {{manager_name}} |
| Employee Number | {{employee_number}} |
| Job Title | {{job_title}} |
| Department | {{department}} |
| Reporting To | {{reporting_to}} |
| Team Size | {{team_size}} |
| Evaluation Period | January 1, 2025 - December 31, 2025 |
| Date of Evaluation | {{evaluation_date}} |

---

### SECTION B: LEADERSHIP COMPETENCIES

Rate each criterion on a scale of 1-5:
- **1** = Needs Significant Improvement
- **2** = Needs Improvement
- **3** = Meets Expectations
- **4** = Exceeds Expectations
- **5** = Outstanding

#### 1. STRATEGIC THINKING & PLANNING (Weight: 15%)
Ability to set clear goals, develop strategies, and align team objectives with organizational goals.

| Rating (1-5) | Comments |
|--------------|----------|
| {{strategic_rating}} | {{strategic_comments}} |

#### 2. TEAM LEADERSHIP & DEVELOPMENT (Weight: 20%)
Ability to motivate, coach, develop, and retain team members. Succession planning.

| Rating (1-5) | Comments |
|--------------|----------|
| {{leadership_rating}} | {{leadership_comments}} |

#### 3. DECISION MAKING & PROBLEM SOLVING (Weight: 15%)
Quality of decisions, ability to analyze complex situations, and implement solutions.

| Rating (1-5) | Comments |
|--------------|----------|
| {{decision_rating}} | {{decision_comments}} |

#### 4. COMMUNICATION & STAKEHOLDER MANAGEMENT (Weight: 15%)
Effectiveness in communicating vision, managing stakeholders, and representing the department.

| Rating (1-5) | Comments |
|--------------|----------|
| {{communication_rating}} | {{communication_comments}} |

#### 5. PERFORMANCE MANAGEMENT (Weight: 10%)
Setting expectations, providing feedback, conducting reviews, and managing underperformance.

| Rating (1-5) | Comments |
|--------------|----------|
| {{perf_mgmt_rating}} | {{perf_mgmt_comments}} |

#### 6. OPERATIONAL EXCELLENCE (Weight: 10%)
Process improvement, efficiency, quality management, and resource optimization.

| Rating (1-5) | Comments |
|--------------|----------|
| {{operations_rating}} | {{operations_comments}} |

#### 7. FINANCIAL ACUMEN (Weight: 10%)
Budget management, cost control, and understanding of financial implications.

| Rating (1-5) | Comments |
|--------------|----------|
| {{financial_rating}} | {{financial_comments}} |

#### 8. INNOVATION & CHANGE MANAGEMENT (Weight: 5%)
Driving innovation, adapting to change, and leading organizational change initiatives.

| Rating (1-5) | Comments |
|--------------|----------|
| {{innovation_rating}} | {{innovation_comments}} |

---

### SECTION C: DEPARTMENTAL KPIs & ACHIEVEMENTS

#### Key Performance Indicators

| KPI | Target | Achieved | % Achievement |
|-----|--------|----------|---------------|
| {{kpi_1_name}} | {{kpi_1_target}} | {{kpi_1_achieved}} | {{kpi_1_percentage}} |
| {{kpi_2_name}} | {{kpi_2_target}} | {{kpi_2_achieved}} | {{kpi_2_percentage}} |
| {{kpi_3_name}} | {{kpi_3_target}} | {{kpi_3_achieved}} | {{kpi_3_percentage}} |
| {{kpi_4_name}} | {{kpi_4_target}} | {{kpi_4_achieved}} | {{kpi_4_percentage}} |

#### Major Achievements

{{major_achievements}}

---

### SECTION D: TEAM DEVELOPMENT

#### Team Performance Overview

| Metric | Value |
|--------|-------|
| Team Size at Start | {{team_size_start}} |
| Team Size at End | {{team_size_end}} |
| Turnover Rate | {{turnover_rate}} |
| Promotions | {{promotions}} |
| Training Hours (Team Total) | {{training_hours}} |

#### Team Member Development Initiatives

{{team_development_initiatives}}

---

### SECTION E: OVERALL PERFORMANCE SCORE

| Criterion | Weight | Rating | Weighted Score |
|-----------|--------|--------|----------------|
| Strategic Thinking & Planning | 15% | {{strategic_rating}} | |
| Team Leadership & Development | 20% | {{leadership_rating}} | |
| Decision Making & Problem Solving | 15% | {{decision_rating}} | |
| Communication & Stakeholder Mgmt | 15% | {{communication_rating}} | |
| Performance Management | 10% | {{perf_mgmt_rating}} | |
| Operational Excellence | 10% | {{operations_rating}} | |
| Financial Acumen | 10% | {{financial_rating}} | |
| Innovation & Change Management | 5% | {{innovation_rating}} | |
| **TOTAL** | 100% | | **{{overall_score}}** |

**Overall Rating:**
- 4.5 - 5.0: Outstanding
- 3.5 - 4.4: Exceeds Expectations
- 2.5 - 3.4: Meets Expectations
- 1.5 - 2.4: Needs Improvement
- 1.0 - 1.4: Needs Significant Improvement

---

### SECTION F: AREAS FOR IMPROVEMENT

{{improvement_areas}}

---

### SECTION G: LEADERSHIP DEVELOPMENT GOALS FOR 2026

| Goal | Target Date | Resources Needed | Success Metrics |
|------|-------------|------------------|-----------------|
| {{goal_1}} | {{goal_1_date}} | {{goal_1_resources}} | {{goal_1_metrics}} |
| {{goal_2}} | {{goal_2_date}} | {{goal_2_resources}} | {{goal_2_metrics}} |
| {{goal_3}} | {{goal_3_date}} | {{goal_3_resources}} | {{goal_3_metrics}} |

---

### SECTION H: MANAGER SELF-ASSESSMENT

**Self-Assessment Comments:**
{{self_assessment}}

---

### SECTION I: 360-DEGREE FEEDBACK SUMMARY (Optional)

| Source | Key Strengths | Areas for Development |
|--------|---------------|----------------------|
| Direct Reports | {{dr_strengths}} | {{dr_development}} |
| Peers | {{peer_strengths}} | {{peer_development}} |
| Senior Leadership | {{sl_strengths}} | {{sl_development}} |

---

### SECTION J: SIGNATURES

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Manager (Self) | {{manager_name}} | _____________ | {{manager_sign_date}} |
| Reporting To | {{reporting_to}} | _____________ | {{supervisor_sign_date}} |
| HR Representative | {{hr_representative}} | _____________ | {{hr_sign_date}} |

---

*This evaluation is confidential and will be maintained in the employee's personnel file.*
"""


# Employee of the Year Nomination Form
EMPLOYEE_OF_YEAR_NOMINATION = """
# EMPLOYEE OF THE YEAR NOMINATION FORM 2025

---

## ABOUT THIS AWARD

The **Employee of the Year Award** recognizes an outstanding individual who has demonstrated exceptional performance, dedication, and embodiment of our company values throughout the year.

**Award Criteria:**
- Exceptional job performance exceeding expectations
- Demonstration of company values and culture
- Positive impact on team and organization
- Innovation and initiative
- Outstanding customer/stakeholder service
- Leadership by example (regardless of position)

---

### SECTION A: NOMINEE INFORMATION

| Field | Value |
|-------|-------|
| Nominee Name | {{nominee_name}} |
| Employee Number | {{employee_number}} |
| Job Title | {{job_title}} |
| Department | {{department}} |
| Date of Joining | {{date_of_joining}} |
| Line Manager | {{line_manager}} |

---

### SECTION B: NOMINATOR INFORMATION

| Field | Value |
|-------|-------|
| Nominator Name | {{nominator_name}} |
| Nominator Employee Number | {{nominator_employee_number}} |
| Relationship to Nominee | {{relationship}} |
| Date of Nomination | {{nomination_date}} |

---

### SECTION C: NOMINATION CRITERIA

Please rate the nominee on each criterion (1-5):
- **1** = Below Average
- **2** = Average
- **3** = Good
- **4** = Very Good
- **5** = Outstanding

#### 1. JOB PERFORMANCE

How would you rate the nominee's overall job performance?

| Rating (1-5) |
|--------------|
| {{performance_rating}} |

**Provide specific examples of exceptional performance:**
{{performance_examples}}

---

#### 2. COMPANY VALUES

How well does the nominee embody our company values?

| Rating (1-5) |
|--------------|
| {{values_rating}} |

**Provide examples of how the nominee demonstrates company values:**
{{values_examples}}

---

#### 3. TEAMWORK & COLLABORATION

How effectively does the nominee work with others?

| Rating (1-5) |
|--------------|
| {{teamwork_rating}} |

**Describe the nominee's contribution to team success:**
{{teamwork_examples}}

---

#### 4. INNOVATION & INITIATIVE

Does the nominee show initiative and bring new ideas?

| Rating (1-5) |
|--------------|
| {{innovation_rating}} |

**Describe innovations or initiatives led by the nominee:**
{{innovation_examples}}

---

#### 5. CUSTOMER/STAKEHOLDER FOCUS

How does the nominee serve customers and stakeholders?

| Rating (1-5) |
|--------------|
| {{customer_rating}} |

**Provide examples of excellent customer/stakeholder service:**
{{customer_examples}}

---

### SECTION D: KEY ACHIEVEMENTS IN 2025

List the nominee's most significant achievements during 2025:

**Achievement 1:**
{{achievement_1}}

**Achievement 2:**
{{achievement_2}}

**Achievement 3:**
{{achievement_3}}

---

### SECTION E: IMPACT ON THE ORGANIZATION

**How has this employee made a positive impact on the organization?**
{{organizational_impact}}

**What would we lose if this employee were not part of our team?**
{{employee_value}}

---

### SECTION F: NOMINATION STATEMENT

**In 250 words or less, explain why this nominee deserves the Employee of the Year Award:**

{{nomination_statement}}

---

### SECTION G: SUPPORTING ENDORSEMENTS (Optional)

| Endorser Name | Position | Signature |
|---------------|----------|-----------|
| {{endorser_1_name}} | {{endorser_1_position}} | _____________ |
| {{endorser_2_name}} | {{endorser_2_position}} | _____________ |
| {{endorser_3_name}} | {{endorser_3_position}} | _____________ |

---

### SECTION H: NOMINATOR DECLARATION

I hereby declare that:
- The information provided is true and accurate
- The nominee is not a direct family member
- I have obtained the consent of the endorsers listed above

| Nominator Signature | Date |
|---------------------|------|
| _____________ | {{declaration_date}} |

---

### FOR HR USE ONLY

| Field | Value |
|-------|-------|
| Nomination Received Date | {{received_date}} |
| Received By | {{received_by}} |
| Eligibility Verified | ☐ Yes ☐ No |
| Forwarded to Selection Committee | ☐ Yes ☐ No |
| Status | {{status}} |

---

**SUBMISSION DEADLINE: December 15, 2025**

*Submit completed forms to HR or via the HR Portal.*
"""


async def seed_templates():
    """Seed the HR templates into the database."""
    async with AsyncSessionLocal() as session:
        # Check if any of the templates already exist
        template_names = [
            "Performance Evaluation 2025 - Non-Managerial Positions",
            "Performance Evaluation 2025 - Managerial Positions",
            "Employee of the Year Nomination 2025"
        ]
        result = await session.execute(
            select(Template).where(Template.name.in_(template_names))
        )
        existing = result.scalars().all()
        if existing:
            existing_names = [t.name for t in existing]
            print(f"Templates already exist: {existing_names}. Skipping seed.")
            return

        templates = [
            Template(
                name="Performance Evaluation 2025 - Non-Managerial Positions",
                type="document",
                content=PERFORMANCE_EVAL_NON_MANAGERIAL,
                version=1,
                created_by="system",
                is_active=True,
                revision_note="Initial version for 2025 performance evaluation cycle"
            ),
            Template(
                name="Performance Evaluation 2025 - Managerial Positions",
                type="document",
                content=PERFORMANCE_EVAL_MANAGERIAL,
                version=1,
                created_by="system",
                is_active=True,
                revision_note="Initial version for 2025 performance evaluation cycle - includes leadership competencies"
            ),
            Template(
                name="Employee of the Year Nomination 2025",
                type="document",
                content=EMPLOYEE_OF_YEAR_NOMINATION,
                version=1,
                created_by="system",
                is_active=True,
                revision_note="Initial version for 2025 Employee of the Year recognition program"
            ),
        ]

        for template in templates:
            session.add(template)
            print(f"✓ Created template: {template.name}")

        await session.commit()
        print("\n✅ Successfully seeded all HR templates!")


if __name__ == "__main__":
    asyncio.run(seed_templates())
