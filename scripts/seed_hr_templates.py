#!/usr/bin/env python3
"""
Seed HR Templates for Performance Evaluation and Employee Recognition

This script creates the following modern, flexible templates:
1. Performance Evaluation - Non-Managerial Positions (2025)
2. Performance Evaluation - Managerial Positions (2025)
3. Employee of the Year Nomination Form

Templates use a JSON-based schema for flexibility and programmatic manipulation.

Usage:
    cd backend
    uv run python ../scripts/seed_hr_templates.py
"""

import asyncio
import json
import os
import sys

# Add backend to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.database import get_engine, AsyncSessionLocal
from app.models.template import Template
from sqlalchemy import select


# Modern Performance Evaluation Template - Non-Managerial Positions
PERFORMANCE_EVAL_NON_MANAGERIAL = json.dumps({
    "schema_version": "2.0",
    "template_type": "performance_evaluation",
    "category": "non_managerial",
    "evaluation_period": {
        "year": 2025,
        "start_date": "2025-01-01",
        "end_date": "2025-12-31",
        "configurable": True
    },
    "settings": {
        "allow_self_assessment": True,
        "require_goals": True,
        "min_goals": 1,
        "max_goals": 5,
        "enable_continuous_feedback": True,
        "enable_mid_year_review": True,
        "rating_style": "stars",
        "allow_anonymous_peer_feedback": False,
        "auto_calculate_score": True
    },
    "rating_scales": {
        "default": {
            "type": "numeric",
            "min": 1,
            "max": 5,
            "labels": {
                "1": {"text": "Needs Development", "emoji": "🔴", "color": "#dc2626"},
                "2": {"text": "Developing", "emoji": "🟠", "color": "#ea580c"},
                "3": {"text": "Meets Expectations", "emoji": "🟡", "color": "#ca8a04"},
                "4": {"text": "Exceeds Expectations", "emoji": "🟢", "color": "#16a34a"},
                "5": {"text": "Outstanding", "emoji": "⭐", "color": "#059669"}
            }
        },
        "overall": {
            "type": "percentage_bands",
            "bands": [
                {"min": 90, "max": 100, "label": "Outstanding", "emoji": "🏆"},
                {"min": 75, "max": 89, "label": "Exceeds Expectations", "emoji": "⭐"},
                {"min": 60, "max": 74, "label": "Meets Expectations", "emoji": "✅"},
                {"min": 40, "max": 59, "label": "Developing", "emoji": "📈"},
                {"min": 0, "max": 39, "label": "Needs Development", "emoji": "🎯"}
            ]
        }
    },
    "employee_info": {
        "fields": [
            {"id": "employee_name", "label": "Employee Name", "type": "text", "source": "auto", "editable": False},
            {"id": "employee_number", "label": "Employee ID", "type": "text", "source": "auto", "editable": False},
            {"id": "job_title", "label": "Job Title", "type": "text", "source": "auto", "editable": False},
            {"id": "department", "label": "Department", "type": "text", "source": "auto", "editable": False},
            {"id": "line_manager", "label": "Line Manager", "type": "text", "source": "auto", "editable": False},
            {"id": "date_of_joining", "label": "Date of Joining", "type": "date", "source": "auto", "editable": False},
            {"id": "evaluation_date", "label": "Evaluation Date", "type": "date", "source": "input", "editable": True}
        ]
    },
    "competencies": {
        "configurable": True,
        "allow_custom": True,
        "categories": [
            {
                "id": "core_competencies",
                "name": "Core Competencies",
                "description": "Essential skills for all employees",
                "items": [
                    {
                        "id": "job_knowledge",
                        "name": "Job Knowledge & Skills",
                        "description": "Understanding of role, technical skills, continuous learning",
                        "weight": 20,
                        "required": True,
                        "behaviors": [
                            "Demonstrates thorough understanding of job responsibilities",
                            "Applies technical skills effectively",
                            "Seeks opportunities for professional development"
                        ]
                    },
                    {
                        "id": "quality",
                        "name": "Quality of Work",
                        "description": "Accuracy, thoroughness, attention to detail",
                        "weight": 20,
                        "required": True,
                        "behaviors": [
                            "Produces accurate, error-free work",
                            "Meets quality standards consistently",
                            "Takes pride in deliverables"
                        ]
                    },
                    {
                        "id": "productivity",
                        "name": "Productivity & Efficiency",
                        "description": "Work volume, deadline management, time optimization",
                        "weight": 15,
                        "required": True,
                        "behaviors": [
                            "Completes tasks within deadlines",
                            "Manages workload effectively",
                            "Uses time and resources efficiently"
                        ]
                    },
                    {
                        "id": "communication",
                        "name": "Communication & Collaboration",
                        "description": "Written/verbal skills, teamwork, relationship building",
                        "weight": 15,
                        "required": True,
                        "behaviors": [
                            "Communicates clearly and professionally",
                            "Collaborates effectively with team members",
                            "Builds positive working relationships"
                        ]
                    },
                    {
                        "id": "initiative",
                        "name": "Initiative & Problem Solving",
                        "description": "Proactivity, creativity, ownership",
                        "weight": 15,
                        "required": True,
                        "behaviors": [
                            "Takes initiative without being asked",
                            "Identifies and resolves problems proactively",
                            "Brings innovative ideas and solutions"
                        ]
                    }
                ]
            },
            {
                "id": "values_alignment",
                "name": "Values & Culture",
                "description": "Alignment with company values",
                "items": [
                    {
                        "id": "integrity",
                        "name": "Integrity & Ethics",
                        "description": "Honesty, ethical behavior, compliance",
                        "weight": 10,
                        "required": True,
                        "behaviors": [
                            "Acts with honesty and transparency",
                            "Follows company policies and procedures",
                            "Demonstrates ethical decision-making"
                        ]
                    },
                    {
                        "id": "adaptability",
                        "name": "Adaptability & Growth Mindset",
                        "description": "Flexibility, learning from feedback, resilience",
                        "weight": 5,
                        "required": False,
                        "behaviors": [
                            "Adapts to changing priorities",
                            "Embraces feedback for improvement",
                            "Shows resilience in challenging situations"
                        ]
                    }
                ]
            }
        ]
    },
    "sections": [
        {
            "id": "achievements",
            "name": "Key Achievements",
            "type": "dynamic_list",
            "description": "Highlight your top accomplishments this year",
            "min_items": 1,
            "max_items": 10,
            "item_schema": {
                "title": {"type": "text", "label": "Achievement", "max_length": 200},
                "description": {"type": "textarea", "label": "Details", "max_length": 1000},
                "impact": {"type": "select", "label": "Impact Level", "options": ["Individual", "Team", "Department", "Organization"]},
                "date": {"type": "date", "label": "Date Achieved"}
            }
        },
        {
            "id": "goals",
            "name": "Development Goals",
            "type": "goal_tracker",
            "description": "Set SMART goals for the next period",
            "enable_okr_format": True,
            "item_schema": {
                "goal": {"type": "text", "label": "Goal", "required": True},
                "key_results": {"type": "dynamic_list", "label": "Key Results", "max_items": 5},
                "target_date": {"type": "date", "label": "Target Date", "required": True},
                "resources": {"type": "textarea", "label": "Resources Needed"},
                "progress": {"type": "slider", "label": "Progress", "min": 0, "max": 100, "step": 5}
            }
        },
        {
            "id": "feedback",
            "name": "Continuous Feedback",
            "type": "feedback_log",
            "description": "Record ongoing feedback throughout the year",
            "auto_populated": True,
            "item_schema": {
                "date": {"type": "date"},
                "from": {"type": "text"},
                "type": {"type": "select", "options": ["Praise", "Constructive", "Suggestion"]},
                "content": {"type": "textarea"}
            }
        },
        {
            "id": "self_assessment",
            "name": "Self Assessment",
            "type": "rich_text",
            "description": "Reflect on your performance and growth",
            "prompts": [
                "What are you most proud of this year?",
                "What challenges did you overcome?",
                "How have you grown professionally?",
                "What would you do differently?"
            ],
            "max_length": 3000
        },
        {
            "id": "manager_comments",
            "name": "Manager Comments",
            "type": "rich_text",
            "role_restricted": ["manager", "hr"],
            "max_length": 3000
        },
        {
            "id": "development_areas",
            "name": "Areas for Development",
            "type": "tag_select",
            "allow_custom": True,
            "suggested_tags": [
                "Technical Skills", "Communication", "Leadership", "Time Management",
                "Project Management", "Stakeholder Management", "Data Analysis",
                "Presentation Skills", "Strategic Thinking", "Delegation"
            ]
        }
    ],
    "workflow": {
        "steps": [
            {"id": "self_review", "name": "Self Assessment", "actor": "employee", "deadline_days": 7},
            {"id": "manager_review", "name": "Manager Review", "actor": "manager", "deadline_days": 7},
            {"id": "calibration", "name": "Calibration", "actor": "hr", "optional": True},
            {"id": "discussion", "name": "Review Discussion", "actors": ["employee", "manager"], "deadline_days": 5},
            {"id": "acknowledgment", "name": "Employee Acknowledgment", "actor": "employee", "deadline_days": 3}
        ],
        "notifications": {
            "enabled": True,
            "channels": ["email", "in_app"],
            "reminders": [7, 3, 1]
        }
    },
    "signatures": {
        "required": ["employee", "manager"],
        "optional": ["hr"],
        "digital_signature": True
    }
}, indent=2)


# Modern Performance Evaluation Template - Managerial Positions
PERFORMANCE_EVAL_MANAGERIAL = json.dumps({
    "schema_version": "2.0",
    "template_type": "performance_evaluation",
    "category": "managerial",
    "evaluation_period": {
        "year": 2025,
        "start_date": "2025-01-01",
        "end_date": "2025-12-31",
        "configurable": True
    },
    "settings": {
        "allow_self_assessment": True,
        "require_goals": True,
        "min_goals": 2,
        "max_goals": 7,
        "enable_continuous_feedback": True,
        "enable_mid_year_review": True,
        "enable_360_feedback": True,
        "rating_style": "stars",
        "auto_calculate_score": True,
        "include_team_metrics": True
    },
    "rating_scales": {
        "default": {
            "type": "numeric",
            "min": 1,
            "max": 5,
            "labels": {
                "1": {"text": "Needs Development", "emoji": "🔴", "color": "#dc2626"},
                "2": {"text": "Developing", "emoji": "🟠", "color": "#ea580c"},
                "3": {"text": "Meets Expectations", "emoji": "🟡", "color": "#ca8a04"},
                "4": {"text": "Exceeds Expectations", "emoji": "🟢", "color": "#16a34a"},
                "5": {"text": "Outstanding", "emoji": "⭐", "color": "#059669"}
            }
        }
    },
    "employee_info": {
        "fields": [
            {"id": "manager_name", "label": "Manager Name", "type": "text", "source": "auto"},
            {"id": "employee_number", "label": "Employee ID", "type": "text", "source": "auto"},
            {"id": "job_title", "label": "Job Title", "type": "text", "source": "auto"},
            {"id": "department", "label": "Department", "type": "text", "source": "auto"},
            {"id": "reporting_to", "label": "Reports To", "type": "text", "source": "auto"},
            {"id": "team_size", "label": "Team Size", "type": "number", "source": "auto"},
            {"id": "evaluation_date", "label": "Evaluation Date", "type": "date", "source": "input"}
        ]
    },
    "competencies": {
        "configurable": True,
        "allow_custom": True,
        "categories": [
            {
                "id": "leadership",
                "name": "Leadership Competencies",
                "items": [
                    {
                        "id": "strategic_thinking",
                        "name": "Strategic Thinking & Vision",
                        "description": "Sets direction, aligns team with organizational goals",
                        "weight": 15,
                        "required": True,
                        "behaviors": [
                            "Develops clear strategic plans",
                            "Communicates vision effectively",
                            "Aligns team objectives with company goals"
                        ]
                    },
                    {
                        "id": "people_leadership",
                        "name": "People Leadership & Development",
                        "description": "Coaching, mentoring, talent development",
                        "weight": 20,
                        "required": True,
                        "behaviors": [
                            "Develops team members' capabilities",
                            "Provides regular coaching and feedback",
                            "Builds succession pipeline"
                        ]
                    },
                    {
                        "id": "decision_making",
                        "name": "Decision Making & Judgment",
                        "description": "Analytical thinking, sound decisions under pressure",
                        "weight": 15,
                        "required": True,
                        "behaviors": [
                            "Makes timely, well-informed decisions",
                            "Considers multiple perspectives",
                            "Takes accountability for outcomes"
                        ]
                    },
                    {
                        "id": "stakeholder_management",
                        "name": "Stakeholder Management",
                        "description": "Building relationships, influencing, communication",
                        "weight": 15,
                        "required": True,
                        "behaviors": [
                            "Builds strong cross-functional relationships",
                            "Manages expectations effectively",
                            "Represents department professionally"
                        ]
                    }
                ]
            },
            {
                "id": "operational",
                "name": "Operational Excellence",
                "items": [
                    {
                        "id": "performance_management",
                        "name": "Performance Management",
                        "description": "Setting expectations, feedback, managing underperformance",
                        "weight": 10,
                        "required": True
                    },
                    {
                        "id": "operational_efficiency",
                        "name": "Operational Efficiency",
                        "description": "Process improvement, resource optimization",
                        "weight": 10,
                        "required": True
                    },
                    {
                        "id": "financial_acumen",
                        "name": "Financial Acumen",
                        "description": "Budget management, cost awareness, ROI focus",
                        "weight": 10,
                        "required": True
                    },
                    {
                        "id": "innovation",
                        "name": "Innovation & Change Leadership",
                        "description": "Driving change, fostering innovation culture",
                        "weight": 5,
                        "required": False
                    }
                ]
            }
        ]
    },
    "sections": [
        {
            "id": "kpis",
            "name": "Key Performance Indicators",
            "type": "kpi_tracker",
            "description": "Track departmental KPIs and metrics",
            "item_schema": {
                "kpi_name": {"type": "text", "label": "KPI"},
                "target": {"type": "number", "label": "Target"},
                "achieved": {"type": "number", "label": "Achieved"},
                "unit": {"type": "select", "options": ["%", "AED", "Count", "Days", "Score"]},
                "trend": {"type": "select", "options": ["↑ Improving", "→ Stable", "↓ Declining"]}
            }
        },
        {
            "id": "team_metrics",
            "name": "Team Performance Dashboard",
            "type": "metrics_dashboard",
            "auto_populated": True,
            "metrics": [
                {"id": "team_size", "label": "Team Size", "source": "hr_system"},
                {"id": "turnover_rate", "label": "Turnover Rate", "source": "hr_system"},
                {"id": "engagement_score", "label": "Engagement Score", "source": "survey"},
                {"id": "promotions", "label": "Promotions This Year", "source": "hr_system"},
                {"id": "training_hours", "label": "Avg Training Hours", "source": "lms"}
            ]
        },
        {
            "id": "achievements",
            "name": "Major Achievements",
            "type": "dynamic_list",
            "min_items": 2,
            "max_items": 10,
            "item_schema": {
                "title": {"type": "text", "label": "Achievement"},
                "description": {"type": "textarea", "label": "Details & Impact"},
                "metrics": {"type": "text", "label": "Quantifiable Results"},
                "category": {"type": "select", "options": ["Revenue", "Cost Savings", "Process Improvement", "Team Development", "Innovation", "Customer Success"]}
            }
        },
        {
            "id": "goals",
            "name": "Strategic Goals & OKRs",
            "type": "okr_tracker",
            "item_schema": {
                "objective": {"type": "text", "label": "Objective"},
                "key_results": {
                    "type": "dynamic_list",
                    "max_items": 5,
                    "item_schema": {
                        "kr": {"type": "text"},
                        "target": {"type": "number"},
                        "current": {"type": "number"},
                        "unit": {"type": "text"}
                    }
                },
                "status": {"type": "select", "options": ["On Track", "At Risk", "Behind", "Completed"]}
            }
        },
        {
            "id": "feedback_360",
            "name": "360° Feedback Summary",
            "type": "feedback_360",
            "sources": ["direct_reports", "peers", "senior_leadership", "cross_functional"],
            "anonymous": True,
            "item_schema": {
                "source": {"type": "text"},
                "strengths": {"type": "textarea"},
                "development_areas": {"type": "textarea"},
                "themes": {"type": "tag_list"}
            }
        },
        {
            "id": "self_assessment",
            "name": "Leadership Self-Reflection",
            "type": "structured_reflection",
            "prompts": [
                {"id": "proud", "text": "What leadership achievements are you most proud of?"},
                {"id": "challenges", "text": "What were your biggest challenges and how did you overcome them?"},
                {"id": "team_growth", "text": "How have you contributed to your team's growth?"},
                {"id": "learning", "text": "What have you learned about yourself as a leader?"},
                {"id": "next_year", "text": "What will you focus on in the coming year?"}
            ]
        }
    ],
    "workflow": {
        "steps": [
            {"id": "self_review", "name": "Self Assessment", "actor": "manager", "deadline_days": 10},
            {"id": "360_collection", "name": "360° Feedback Collection", "actor": "system", "deadline_days": 14},
            {"id": "supervisor_review", "name": "Supervisor Review", "actor": "supervisor", "deadline_days": 7},
            {"id": "calibration", "name": "Leadership Calibration", "actor": "hr", "optional": False},
            {"id": "discussion", "name": "Review Discussion", "actors": ["manager", "supervisor"], "deadline_days": 5},
            {"id": "acknowledgment", "name": "Acknowledgment", "actor": "manager", "deadline_days": 3}
        ]
    },
    "signatures": {
        "required": ["manager", "supervisor"],
        "optional": ["hr_director"],
        "digital_signature": True
    }
}, indent=2)


# Modern Employee of the Year Nomination Form
EMPLOYEE_OF_YEAR_NOMINATION = json.dumps({
    "schema_version": "2.0",
    "template_type": "recognition_nomination",
    "award_type": "employee_of_the_year",
    "year": 2025,
    "settings": {
        "allow_self_nomination": False,
        "require_endorsements": False,
        "min_endorsements": 0,
        "max_endorsements": 5,
        "anonymous_nominations": False,
        "multiple_nominations_allowed": True,
        "voting_enabled": False,
        "nomination_deadline": "2025-12-15"
    },
    "award_info": {
        "name": "Employee of the Year",
        "description": "Recognizes an exceptional individual who exemplifies our values and makes outstanding contributions",
        "emoji": "🏆",
        "eligibility": [
            "Minimum 1 year of service",
            "No active disciplinary actions",
            "Demonstrated excellence across multiple areas"
        ],
        "prize": {
            "type": "configurable",
            "default": ["Certificate", "Trophy", "Cash Bonus", "Extra Leave Days"]
        }
    },
    "categories": [
        {
            "id": "performance",
            "name": "Outstanding Performance",
            "emoji": "⭐",
            "weight": 25,
            "description": "Exceptional job performance exceeding expectations",
            "rating": {"type": "stars", "max": 5},
            "evidence_required": True,
            "evidence_prompt": "Describe specific examples of exceptional performance"
        },
        {
            "id": "values",
            "name": "Living Our Values",
            "emoji": "💎",
            "weight": 20,
            "description": "Embodies and champions company values daily",
            "rating": {"type": "stars", "max": 5},
            "evidence_required": True,
            "company_values": ["Integrity", "Excellence", "Innovation", "Collaboration", "Customer Focus"]
        },
        {
            "id": "teamwork",
            "name": "Team Player",
            "emoji": "🤝",
            "weight": 20,
            "description": "Exceptional collaboration and support for colleagues",
            "rating": {"type": "stars", "max": 5},
            "evidence_required": True
        },
        {
            "id": "innovation",
            "name": "Innovation & Initiative",
            "emoji": "💡",
            "weight": 20,
            "description": "Brings fresh ideas and drives positive change",
            "rating": {"type": "stars", "max": 5},
            "evidence_required": True
        },
        {
            "id": "impact",
            "name": "Business Impact",
            "emoji": "📈",
            "weight": 15,
            "description": "Measurable positive impact on the organization",
            "rating": {"type": "stars", "max": 5},
            "evidence_required": True,
            "impact_types": ["Revenue", "Cost Savings", "Efficiency", "Customer Satisfaction", "Employee Engagement"]
        }
    ],
    "nominee_info": {
        "fields": [
            {"id": "nominee_name", "label": "Nominee Name", "type": "employee_picker", "required": True},
            {"id": "employee_number", "label": "Employee ID", "type": "text", "auto_populated": True},
            {"id": "job_title", "label": "Job Title", "type": "text", "auto_populated": True},
            {"id": "department", "label": "Department", "type": "text", "auto_populated": True},
            {"id": "tenure", "label": "Years of Service", "type": "number", "auto_populated": True}
        ]
    },
    "nominator_info": {
        "fields": [
            {"id": "nominator_name", "label": "Your Name", "type": "text", "auto_populated": True},
            {"id": "relationship", "label": "Relationship to Nominee", "type": "select", "options": ["Manager", "Peer", "Direct Report", "Cross-functional Colleague", "Senior Leader"]}
        ]
    },
    "sections": [
        {
            "id": "achievements",
            "name": "Key Achievements",
            "type": "achievement_cards",
            "description": "Highlight the nominee's top accomplishments",
            "min_items": 1,
            "max_items": 5,
            "item_schema": {
                "title": {"type": "text", "label": "Achievement Title", "max_length": 100},
                "description": {"type": "textarea", "label": "What did they do?", "max_length": 500},
                "impact": {"type": "textarea", "label": "What was the impact?", "max_length": 300},
                "date": {"type": "month", "label": "When"}
            }
        },
        {
            "id": "nomination_statement",
            "name": "Why This Person?",
            "type": "rich_text",
            "description": "Tell us why this person deserves to win",
            "min_length": 100,
            "max_length": 1500,
            "prompts": [
                "What makes this person stand out?",
                "How do they inspire others?",
                "What would we lose without them?"
            ]
        },
        {
            "id": "endorsements",
            "name": "Supporting Endorsements",
            "type": "endorsement_request",
            "optional": True,
            "description": "Invite colleagues to support this nomination",
            "item_schema": {
                "endorser": {"type": "employee_picker"},
                "relationship": {"type": "text"},
                "comment": {"type": "textarea", "max_length": 500},
                "status": {"type": "select", "options": ["Pending", "Submitted", "Declined"]}
            }
        },
        {
            "id": "media",
            "name": "Supporting Evidence",
            "type": "media_upload",
            "optional": True,
            "description": "Upload photos, videos, or documents",
            "allowed_types": ["image/jpeg", "image/png", "application/pdf", "video/mp4"],
            "max_files": 5,
            "max_file_size_mb": 10
        }
    ],
    "scoring": {
        "auto_calculate": True,
        "formula": "weighted_average",
        "display": {
            "show_score_to_nominator": False,
            "show_score_to_nominee": False,
            "show_score_to_hr": True
        }
    },
    "workflow": {
        "steps": [
            {"id": "draft", "name": "Draft", "actor": "nominator"},
            {"id": "submitted", "name": "Submitted", "actor": "nominator", "notification": True},
            {"id": "hr_review", "name": "HR Review", "actor": "hr", "deadline_days": 5},
            {"id": "committee_review", "name": "Selection Committee", "actor": "committee"},
            {"id": "winner_selected", "name": "Winner Selected", "actor": "committee"},
            {"id": "announced", "name": "Announced", "actor": "hr"}
        ],
        "notifications": {
            "on_submission": {"to": ["hr", "nominator"], "template": "nomination_received"},
            "on_endorsement": {"to": ["nominator"], "template": "endorsement_added"},
            "on_winner": {"to": ["nominee", "nominator"], "template": "winner_announcement"}
        }
    },
    "hr_admin": {
        "fields": [
            {"id": "received_date", "label": "Received Date", "type": "datetime", "auto": True},
            {"id": "reviewed_by", "label": "Reviewed By", "type": "employee_picker"},
            {"id": "eligibility_check", "label": "Eligibility Verified", "type": "checkbox"},
            {"id": "status", "label": "Status", "type": "select", "options": ["Pending", "Under Review", "Shortlisted", "Winner", "Not Selected"]},
            {"id": "notes", "label": "Internal Notes", "type": "textarea"}
        ]
    }
}, indent=2)


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
