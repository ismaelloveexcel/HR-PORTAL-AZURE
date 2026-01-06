# HR Templates Reference Guide

This document provides a reference for the modern, flexible HR templates available in the Secure Renewals HR Portal.

## Template Architecture

All templates use a **JSON-based schema** (v2.0) that provides:
- 🔧 **Configurable competencies** - Add, remove, or reweight criteria
- ⭐ **Modern rating scales** - Stars, emojis, color-coded indicators
- 📊 **OKR support** - Objectives and Key Results tracking
- 🔄 **Continuous feedback** - Year-round feedback logging
- 📱 **Dynamic sections** - Flexible forms that adapt to your needs
- 🔔 **Workflow automation** - Built-in notifications and deadlines

---

## Available Templates

### 1. Performance Evaluation 2025 - Non-Managerial Positions

**Type:** `performance_evaluation`  
**Category:** `non_managerial`  
**Schema Version:** 2.0

#### Key Features:
- ⭐ Star-based ratings with emoji indicators
- 📈 Configurable competency weights
- 🎯 SMART goal tracking with OKR format
- 💬 Continuous feedback throughout the year
- ✍️ Self-assessment with guided prompts
- 📧 Automated workflow notifications

#### Competency Categories:

**Core Competencies (85% total weight)**
| Competency | Weight | Configurable |
|------------|--------|--------------|
| Job Knowledge & Skills | 20% | ✅ |
| Quality of Work | 20% | ✅ |
| Productivity & Efficiency | 15% | ✅ |
| Communication & Collaboration | 15% | ✅ |
| Initiative & Problem Solving | 15% | ✅ |

**Values & Culture (15% total weight)**
| Competency | Weight | Required |
|------------|--------|----------|
| Integrity & Ethics | 10% | ✅ |
| Adaptability & Growth Mindset | 5% | Optional |

#### Rating Scale:
| Rating | Label | Visual |
|--------|-------|--------|
| 5 | Outstanding | ⭐ |
| 4 | Exceeds Expectations | 🟢 |
| 3 | Meets Expectations | 🟡 |
| 2 | Developing | 🟠 |
| 1 | Needs Development | 🔴 |

#### Workflow Steps:
1. **Self Assessment** (Employee, 7 days)
2. **Manager Review** (Manager, 7 days)
3. **Calibration** (HR, optional)
4. **Review Discussion** (Employee + Manager, 5 days)
5. **Acknowledgment** (Employee, 3 days)

---

### 2. Performance Evaluation 2025 - Managerial Positions

**Type:** `performance_evaluation`  
**Category:** `managerial`  
**Schema Version:** 2.0

#### Key Features:
- 📊 360° feedback integration
- 📈 KPI tracking dashboard
- 👥 Team performance metrics
- 🎯 Strategic OKR tracking
- 💼 Leadership competency framework

#### Leadership Competencies:

| Competency | Weight |
|------------|--------|
| Strategic Thinking & Vision | 15% |
| People Leadership & Development | 20% |
| Decision Making & Judgment | 15% |
| Stakeholder Management | 15% |
| Performance Management | 10% |
| Operational Efficiency | 10% |
| Financial Acumen | 10% |
| Innovation & Change Leadership | 5% |

#### Team Metrics (Auto-Populated):
- Team size and turnover rate
- Engagement scores
- Promotions this year
- Average training hours

#### Workflow Steps:
1. **Self Assessment** (Manager, 10 days)
2. **360° Feedback Collection** (System, 14 days)
3. **Supervisor Review** (Supervisor, 7 days)
4. **Leadership Calibration** (HR, required)
5. **Review Discussion** (Manager + Supervisor, 5 days)
6. **Acknowledgment** (Manager, 3 days)

---

### 3. Employee of the Year Nomination 2025

**Type:** `recognition_nomination`  
**Award Type:** `employee_of_the_year`  
**Schema Version:** 2.0

#### Key Features:
- 🏆 Modern nomination experience
- 📸 Media upload support (photos, videos)
- 👥 Endorsement requests
- 📊 Automatic scoring
- 🔔 Status notifications

#### Nomination Categories:

| Category | Weight | Emoji |
|----------|--------|-------|
| Outstanding Performance | 25% | ⭐ |
| Living Our Values | 20% | 💎 |
| Team Player | 20% | 🤝 |
| Innovation & Initiative | 20% | 💡 |
| Business Impact | 15% | 📈 |

#### Workflow:
1. **Draft** - Save and edit nomination
2. **Submitted** - Notification sent to HR
3. **HR Review** - Eligibility verification (5 days)
4. **Selection Committee** - Evaluation and scoring
5. **Winner Selected** - Committee decision
6. **Announced** - Winner notification

---

## API Usage

### List All Templates
```http
GET /api/templates
```

### Get Template by Type
```http
GET /api/templates?type=performance_evaluation
```

### Get Specific Template
```http
GET /api/templates/{template_id}
```

### Create New Template
```http
POST /api/templates
Content-Type: application/json

{
  "name": "Custom Evaluation",
  "type": "performance_evaluation",
  "content": { /* JSON schema */ }
}
```

### Create Template Revision
```http
POST /api/templates/{template_id}/revision
Content-Type: application/json

{
  "content": { /* Updated JSON schema */ },
  "revision_note": "Added new competency category"
}
```

---

## JSON Schema Reference

### Template Structure
```json
{
  "schema_version": "2.0",
  "template_type": "performance_evaluation",
  "category": "non_managerial",
  "settings": {
    "allow_self_assessment": true,
    "enable_continuous_feedback": true,
    "rating_style": "stars"
  },
  "rating_scales": { ... },
  "competencies": { ... },
  "sections": [ ... ],
  "workflow": { ... },
  "signatures": { ... }
}
```

### Competency Definition
```json
{
  "id": "job_knowledge",
  "name": "Job Knowledge & Skills",
  "description": "Understanding of role, technical skills",
  "weight": 20,
  "required": true,
  "behaviors": [
    "Demonstrates understanding of responsibilities",
    "Applies technical skills effectively"
  ]
}
```

### Section Types
| Type | Description |
|------|-------------|
| `dynamic_list` | Add multiple items (achievements, goals) |
| `goal_tracker` | SMART goals with OKR support |
| `feedback_log` | Continuous feedback entries |
| `rich_text` | Long-form text with prompts |
| `tag_select` | Select from predefined tags |
| `kpi_tracker` | KPI metrics with targets |
| `metrics_dashboard` | Auto-populated metrics |
| `okr_tracker` | Objectives and Key Results |
| `feedback_360` | 360° feedback collection |
| `achievement_cards` | Visual achievement cards |
| `media_upload` | File attachments |

---

## Customization Guide

### Adding Custom Competencies
```json
{
  "competencies": {
    "allow_custom": true,
    "categories": [
      {
        "id": "custom_skills",
        "name": "Department-Specific Skills",
        "items": [
          {
            "id": "custom_1",
            "name": "Your Custom Competency",
            "weight": 10,
            "required": true
          }
        ]
      }
    ]
  }
}
```

### Changing Rating Style
Options: `"stars"`, `"numeric"`, `"emoji"`, `"slider"`

```json
{
  "settings": {
    "rating_style": "emoji"
  },
  "rating_scales": {
    "default": {
      "type": "emoji",
      "options": ["🔴", "🟠", "🟡", "🟢", "⭐"]
    }
  }
}
```

### Configuring Workflows
```json
{
  "workflow": {
    "steps": [
      {"id": "step1", "name": "Review", "actor": "manager", "deadline_days": 7}
    ],
    "notifications": {
      "enabled": true,
      "channels": ["email", "in_app"],
      "reminders": [7, 3, 1]
    }
  }
}
```

---

## Seeding Templates

To populate templates in a fresh database:

```bash
cd backend
uv run python ../scripts/seed_hr_templates.py
```

---

## Best Practices

1. 🔧 **Customize weights** to match your organization's priorities
2. 📅 **Enable mid-year reviews** for continuous performance management
3. 💬 **Use continuous feedback** instead of annual-only reviews
4. 🎯 **Set clear OKRs** with measurable key results
5. 👥 **Enable 360° feedback** for leadership roles
6. 📊 **Track metrics** that matter to your business

---

## Related Documentation

- [HR User Guide](HR_USER_GUIDE.md)
- [HR Implementation Plan](HR_IMPLEMENTATION_PLAN.md)
- [Process Simplification (UAE)](PROCESS_SIMPLIFICATION_UAE.md)

---

*Last Updated: January 2025 | Schema Version 2.0*
