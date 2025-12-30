-- ============================================
-- BAYNUNAH HR PORTAL DATABASE SCHEMA
-- UAE Labor Law Compliant System
-- ============================================

-- Drop existing tables (for fresh install)
DROP TABLE IF EXISTS policy_acknowledgments CASCADE;
DROP TABLE IF EXISTS hr_announcements CASCADE;
DROP TABLE IF EXISTS hr_calendar_events CASCADE;
DROP TABLE IF EXISTS policies CASCADE;
DROP TABLE IF EXISTS benefits CASCADE;
DROP TABLE IF EXISTS leave_types CASCADE;
DROP TABLE IF EXISTS hr_requests CASCADE;
DROP TABLE IF EXISTS attendance_records CASCADE;
DROP TABLE IF EXISTS employees CASCADE;
DROP TABLE IF EXISTS passes CASCADE;
DROP TABLE IF EXISTS recruitment_requests CASCADE;
DROP TABLE IF EXISTS candidates CASCADE;

-- ============================================
-- 1. EMPLOYEES TABLE (Master Data + UAE Compliance)
-- ============================================
CREATE TABLE employees (
  id SERIAL PRIMARY KEY,
  employee_id VARCHAR(50) UNIQUE NOT NULL,
  full_name VARCHAR(200) NOT NULL,
  profile_photo TEXT,

  -- Contact Information
  personal_email VARCHAR(200),
  work_email VARCHAR(200) NOT NULL,
  mobile_number VARCHAR(50),
  personal_phone VARCHAR(50),

  -- Personal Details
  nationality VARCHAR(100),
  date_of_birth DATE,
  gender VARCHAR(20),
  marital_status VARCHAR(50),

  -- Employment Details
  job_title VARCHAR(200),
  function VARCHAR(100),
  department VARCHAR(100),
  line_manager VARCHAR(200),
  employment_status VARCHAR(50) DEFAULT 'Active',
  date_of_joining DATE,
  date_of_exit DATE,
  contract_type VARCHAR(50), -- Limited/Unlimited
  contract_start_date DATE,
  contract_end_date DATE,

  -- Work Location
  work_location VARCHAR(100),
  gps_coordinates TEXT,
  work_schedule INTEGER DEFAULT 6, -- Days per week
  overtime_type VARCHAR(50), -- Paid/Offset Days

  -- UAE Compliance Fields (Critical)
  emirates_id_number VARCHAR(50),
  emirates_id_expiry DATE,
  uae_visa_number VARCHAR(50),
  uae_visa_issue_date DATE,
  uae_visa_expiry DATE,
  labor_card_number VARCHAR(50),
  labor_card_expiry DATE,
  medical_fitness_date DATE,
  medical_fitness_expiry DATE,
  passport_number VARCHAR(50),
  passport_expiry DATE,

  -- Banking & Payroll (WPS Compliance)
  bank_name VARCHAR(100),
  bank_iban VARCHAR(50),

  -- Insurance
  iloe_subscription_status VARCHAR(50),
  iloe_expiry_date DATE,

  -- Emergency Contacts (JSON)
  emergency_contacts JSONB,

  -- Family Details (JSON)
  family_details JSONB,

  -- Life Insurance Beneficiaries (JSON)
  life_insurance_beneficiaries JSONB,

  -- System Fields
  desired_communication_channel VARCHAR(50) DEFAULT 'Email',
  actions_required TEXT,
  personal_documents TEXT,
  notes TEXT,

  -- Timestamps
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_employees_id ON employees(employee_id);
CREATE INDEX idx_employees_status ON employees(employment_status);
CREATE INDEX idx_employees_expiry ON employees(emirates_id_expiry, uae_visa_expiry);

-- ============================================
-- 2. ATTENDANCE RECORDS TABLE
-- ============================================
CREATE TABLE attendance_records (
  id SERIAL PRIMARY KEY,
  employee_id VARCHAR(50) REFERENCES employees(employee_id),
  date DATE NOT NULL,
  clock_in_time TIME,
  clock_out_time TIME,

  -- Location Tracking
  work_location VARCHAR(100),
  location_photo TEXT,
  gps_coordinates TEXT,

  -- Overtime
  overtime_hours NUMERIC(5,2) DEFAULT 0,
  offset_days NUMERIC(3,1) DEFAULT 0,
  overtime_type VARCHAR(50),

  -- Status
  attendance_status VARCHAR(50) DEFAULT 'Present',
  notes TEXT,
  manager_notified BOOLEAN DEFAULT FALSE,

  -- WFH
  wfh_approval_status VARCHAR(50),
  linked_leave_request_id INTEGER,

  -- Timestamps
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  UNIQUE(employee_id, date)
);

CREATE INDEX idx_attendance_employee ON attendance_records(employee_id);
CREATE INDEX idx_attendance_date ON attendance_records(date);
CREATE INDEX idx_attendance_status ON attendance_records(attendance_status);

-- ============================================
-- 3. HR REQUESTS TABLE
-- ============================================
CREATE TABLE hr_requests (
  id SERIAL PRIMARY KEY,
  employee_id VARCHAR(50) REFERENCES employees(employee_id),
  request_type VARCHAR(100) NOT NULL, -- Leave, Document, Parking, Reimbursement, Bank Change

  -- Request Details
  description TEXT,
  supporting_documents TEXT,
  supporting_photos TEXT,
  requested_amount NUMERIC(10,2),

  -- Leave Specific
  leave_type_id INTEGER,
  leave_start_date DATE,
  leave_end_date DATE,
  leave_days NUMERIC(4,1),

  -- Status & Approvals
  status VARCHAR(50) DEFAULT 'Submitted', -- Submitted, In Review, Approved, Rejected, Completed
  request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  date_actioned TIMESTAMP,

  -- Manager Approval
  manager_approval_required BOOLEAN DEFAULT FALSE,
  manager_comments TEXT,

  -- Communication
  desired_communication_channel VARCHAR(50) DEFAULT 'Email',

  -- Timestamps
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_requests_employee ON hr_requests(employee_id);
CREATE INDEX idx_requests_status ON hr_requests(status);
CREATE INDEX idx_requests_type ON hr_requests(request_type);

-- ============================================
-- 4. LEAVE TYPES TABLE
-- ============================================
CREATE TABLE leave_types (
  id SERIAL PRIMARY KEY,
  leave_name VARCHAR(100) NOT NULL,
  description TEXT,
  entitlement_days INTEGER,
  eligibility_conditions TEXT,

  -- Categories
  leave_category VARCHAR(50), -- Annual, Sick, Maternity, Paternity, Compassionate, Unpaid

  -- Rules
  carry_forward_allowed BOOLEAN DEFAULT FALSE,
  supporting_documents_required BOOLEAN DEFAULT FALSE,
  document_examples TEXT,
  approval_required BOOLEAN DEFAULT TRUE,

  -- UAE Labor Law Reference
  uae_labor_law_reference VARCHAR(200),

  -- Status
  active BOOLEAN DEFAULT TRUE,

  -- Timestamps
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_leave_types_active ON leave_types(active);

-- ============================================
-- 5. BENEFITS TABLE
-- ============================================
CREATE TABLE benefits (
  id SERIAL PRIMARY KEY,
  benefit_name VARCHAR(200) NOT NULL,
  description TEXT,

  -- Eligibility
  job_family VARCHAR(100),
  function VARCHAR(100),
  eligibility_criteria TEXT,

  -- Entitlement
  entitlement_value NUMERIC(10,2),
  entitlement_frequency VARCHAR(50), -- Monthly, Annually, One-Time, Per Event
  non_cash_benefit BOOLEAN DEFAULT FALSE,

  -- Status
  active BOOLEAN DEFAULT TRUE,

  -- Timestamps
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_benefits_active ON benefits(active);

-- ============================================
-- 6. POLICIES TABLE
-- ============================================
CREATE TABLE policies (
  id SERIAL PRIMARY KEY,
  policy_name VARCHAR(200) NOT NULL,
  policy_type VARCHAR(100), -- Code of Conduct, Leave Policy, Attendance Policy, etc.

  -- Dates
  effective_date DATE,
  last_updated DATE,

  -- Content
  policy_document TEXT,
  summary TEXT,

  -- Acknowledgment
  acknowledgement_required BOOLEAN DEFAULT FALSE,

  -- Timestamps
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_policies_type ON policies(policy_type);

-- ============================================
-- 7. POLICY ACKNOWLEDGMENTS TABLE
-- ============================================
CREATE TABLE policy_acknowledgments (
  id SERIAL PRIMARY KEY,
  policy_id INTEGER REFERENCES policies(id),
  employee_id VARCHAR(50) REFERENCES employees(employee_id),
  acknowledged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  UNIQUE(policy_id, employee_id)
);

CREATE INDEX idx_policy_acks_employee ON policy_acknowledgments(employee_id);

-- ============================================
-- 8. HR ANNOUNCEMENTS TABLE
-- ============================================
CREATE TABLE hr_announcements (
  id SERIAL PRIMARY KEY,
  announcement_title VARCHAR(300) NOT NULL,
  announcement_body TEXT,
  announcement_date DATE,
  expiry_date DATE,

  -- Audience
  audience TEXT[], -- Array: All Employees, Managers Only, etc.

  -- Media
  announcement_photo TEXT,

  -- Related
  related_policy_id INTEGER REFERENCES policies(id),

  -- Acknowledgment
  acknowledgement_required BOOLEAN DEFAULT FALSE,

  -- Timestamps
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_announcements_date ON hr_announcements(announcement_date);

-- ============================================
-- 9. HR CALENDAR EVENTS TABLE
-- ============================================
CREATE TABLE hr_calendar_events (
  id SERIAL PRIMARY KEY,
  event_name VARCHAR(200) NOT NULL,
  event_date DATE NOT NULL,
  event_type VARCHAR(100), -- Public Holiday, Compliance Deadline, HR Event, Company Event
  description TEXT,
  location VARCHAR(200),
  event_photo TEXT,
  is_mandatory BOOLEAN DEFAULT FALSE,

  -- Timestamps
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_calendar_date ON hr_calendar_events(event_date);

-- ============================================
-- 10. PASSES TABLE (Universal Pass System)
-- ============================================
CREATE TABLE passes (
  id VARCHAR(50) PRIMARY KEY, -- CAND-2025-001, EMP-2025-042, MAN-2025-031
  type VARCHAR(50) NOT NULL, -- candidate, employee, manager

  -- Module Configuration
  enabled_modules JSONB NOT NULL, -- Array of enabled modules

  -- All Pass Data (Universal JSON)
  data JSONB NOT NULL,

  -- Timestamps
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_passes_type ON passes(type);

-- ============================================
-- 11. RECRUITMENT REQUESTS TABLE (RRF)
-- ============================================
CREATE TABLE recruitment_requests (
  id SERIAL PRIMARY KEY,
  rrf_number VARCHAR(50) UNIQUE NOT NULL, -- RRF-BWT-05-120

  -- Request Details
  department VARCHAR(100),
  job_title VARCHAR(200),
  reason_for_hiring TEXT,
  replacing_whom VARCHAR(200),
  job_description TEXT,
  required_skills TEXT,

  -- Compensation
  salary_range VARCHAR(100),
  location VARCHAR(100),
  hiring_urgency VARCHAR(50),

  -- Approvals
  status VARCHAR(50) DEFAULT 'Pending', -- Pending, Approved, Rejected
  requested_by VARCHAR(200),
  hr_approved BOOLEAN DEFAULT FALSE,
  ceo_approved BOOLEAN DEFAULT FALSE,

  -- Timestamps
  request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_rrf_status ON recruitment_requests(status);

-- ============================================
-- 12. CANDIDATES TABLE
-- ============================================
CREATE TABLE candidates (
  id SERIAL PRIMARY KEY,
  candidate_id VARCHAR(50) UNIQUE NOT NULL, -- CAND-2025-001
  rrf_id INTEGER REFERENCES recruitment_requests(id),

  -- Personal Details
  full_name VARCHAR(200) NOT NULL,
  contact_email VARCHAR(200),
  contact_phone VARCHAR(50),
  nationality VARCHAR(100),

  -- Position Details
  position VARCHAR(200),

  -- Recruitment Stage
  current_stage INTEGER DEFAULT 1, -- 1-6 (Application → Onboarding)
  stage_status VARCHAR(200),
  days_in_stage INTEGER DEFAULT 0,

  -- Evaluation Scores
  profile_fit NUMERIC(3,1),
  soft_skills NUMERIC(3,1),
  technical_skills NUMERIC(3,1),
  interview_score NUMERIC(3,1),

  -- Employment Details
  current_location VARCHAR(100),
  willing_to_relocate BOOLEAN,
  visa_status VARCHAR(100),
  notice_period VARCHAR(100),
  expected_salary VARCHAR(100),

  -- Documents & Notes
  documents TEXT,
  notes JSONB,

  -- Timestamps
  application_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_candidates_stage ON candidates(current_stage);
CREATE INDEX idx_candidates_rrf ON candidates(rrf_id);

-- ============================================
-- SEED DATA - UAE Leave Types (Labor Law Compliant)
-- ============================================
INSERT INTO leave_types (leave_name, description, entitlement_days, leave_category, uae_labor_law_reference, active) VALUES
('Annual Leave', 'Paid annual leave after 1 year of service', 30, 'Annual', 'Article 29', true),
('Sick Leave', 'Paid sick leave with medical certificate', 90, 'Sick', 'Article 31', true),
('Maternity Leave', 'Maternity leave for female employees', 60, 'Maternity', 'Article 30', true),
('Paternity Leave', 'Paternity leave for new fathers', 5, 'Paternity', 'Federal Law No. 6/2020', true),
('Compassionate Leave', 'Leave for family emergencies or bereavement', 5, 'Compassionate', 'Custom Policy', true),
('Unpaid Leave', 'Unpaid leave subject to manager approval', 0, 'Unpaid', 'Article 32', true),
('Hajj Leave', 'One-time paid leave for Hajj pilgrimage', 30, 'Other', 'Custom Policy', true);

-- ============================================
-- VIEWS FOR REPORTING
-- ============================================

-- Compliance Dashboard View (Expiring Documents)
CREATE OR REPLACE VIEW compliance_expiring_soon AS
SELECT
  employee_id,
  full_name,
  department,
  emirates_id_expiry,
  uae_visa_expiry,
  labor_card_expiry,
  medical_fitness_expiry,
  passport_expiry,
  LEAST(
    COALESCE(emirates_id_expiry, '2099-12-31'),
    COALESCE(uae_visa_expiry, '2099-12-31'),
    COALESCE(labor_card_expiry, '2099-12-31'),
    COALESCE(medical_fitness_expiry, '2099-12-31'),
    COALESCE(passport_expiry, '2099-12-31')
  ) AS next_expiry_date
FROM employees
WHERE employment_status = 'Active'
  AND (
    emirates_id_expiry <= CURRENT_DATE + INTERVAL '60 days'
    OR uae_visa_expiry <= CURRENT_DATE + INTERVAL '60 days'
    OR labor_card_expiry <= CURRENT_DATE + INTERVAL '60 days'
    OR medical_fitness_expiry <= CURRENT_DATE + INTERVAL '60 days'
    OR passport_expiry <= CURRENT_DATE + INTERVAL '60 days'
  )
ORDER BY next_expiry_date;

-- Attendance Summary View
CREATE OR REPLACE VIEW attendance_summary_current_month AS
SELECT
  e.employee_id,
  e.full_name,
  e.department,
  COUNT(*) FILTER (WHERE a.attendance_status = 'Present') AS days_present,
  COUNT(*) FILTER (WHERE a.attendance_status = 'Absent') AS days_absent,
  COUNT(*) FILTER (WHERE a.attendance_status = 'Late') AS days_late,
  SUM(a.overtime_hours) AS total_overtime_hours,
  SUM(a.offset_days) AS total_offset_days
FROM employees e
LEFT JOIN attendance_records a ON e.employee_id = a.employee_id
WHERE EXTRACT(MONTH FROM a.date) = EXTRACT(MONTH FROM CURRENT_DATE)
  AND EXTRACT(YEAR FROM a.date) = EXTRACT(YEAR FROM CURRENT_DATE)
GROUP BY e.employee_id, e.full_name, e.department;

-- Pending Requests View
CREATE OR REPLACE VIEW pending_requests_summary AS
SELECT
  request_type,
  COUNT(*) AS pending_count,
  AVG(EXTRACT(DAY FROM (CURRENT_TIMESTAMP - request_date))) AS avg_days_pending
FROM hr_requests
WHERE status IN ('Submitted', 'In Review')
GROUP BY request_type;

-- ============================================
-- FUNCTIONS
-- ============================================

-- Function to update updated_at timestamp automatically
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = CURRENT_TIMESTAMP;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create triggers for all tables
CREATE TRIGGER update_employees_updated_at BEFORE UPDATE ON employees
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_attendance_updated_at BEFORE UPDATE ON attendance_records
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_requests_updated_at BEFORE UPDATE ON hr_requests
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_leaves_updated_at BEFORE UPDATE ON leave_types
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_benefits_updated_at BEFORE UPDATE ON benefits
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_policies_updated_at BEFORE UPDATE ON policies
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_announcements_updated_at BEFORE UPDATE ON hr_announcements
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_events_updated_at BEFORE UPDATE ON hr_calendar_events
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_passes_updated_at BEFORE UPDATE ON passes
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_rrf_updated_at BEFORE UPDATE ON recruitment_requests
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_candidates_updated_at BEFORE UPDATE ON candidates
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- COMPLETION MESSAGE
-- ============================================
DO $$
BEGIN
  RAISE NOTICE '✅ Baynunah HR Portal Database Schema Created Successfully';
  RAISE NOTICE '📊 Tables: 12 core tables + 3 views';
  RAISE NOTICE '🇦🇪 UAE Labor Law Compliance: Enabled';
  RAISE NOTICE '🎫 Universal Pass System: Ready';
  RAISE NOTICE '📅 Leave Types: 7 UAE-compliant types seeded';
END $$;
