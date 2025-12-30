-- ============================================
-- RECRUITMENT SYSTEM - COMPLETE SCHEMA
-- Missing table: external_submissions
-- ============================================

-- ============================================
-- NEW TABLE: external_submissions
-- ============================================
CREATE TABLE IF NOT EXISTS external_submissions (
  id SERIAL PRIMARY KEY,
  submission_id VARCHAR(50) UNIQUE NOT NULL,

  -- Link to RRF and Recruiter
  rrf_id INTEGER REFERENCES recruitment_requests(id),
  recruiter_id VARCHAR(50) REFERENCES external_recruiters(recruiter_id),

  -- Candidate Details
  candidate_name VARCHAR(200) NOT NULL,
  candidate_email VARCHAR(200),
  candidate_phone VARCHAR(50),
  candidate_nationality VARCHAR(100),
  candidate_location VARCHAR(100),

  -- Submission Details
  cv_file_path TEXT,
  cover_letter TEXT,
  years_experience INTEGER,
  expected_salary VARCHAR(100),
  notice_period VARCHAR(100),
  visa_status VARCHAR(100),

  -- Status & Tracking
  status VARCHAR(50) DEFAULT 'Pending Review', -- Pending Review, Shortlisted, Rejected, Moved to Pipeline
  hr_review_notes TEXT,
  reviewed_by VARCHAR(200),
  reviewed_at TIMESTAMP,

  -- Moved to Candidate Pipeline
  moved_to_candidate_id VARCHAR(50), -- References candidates.candidate_id

  -- Timestamps
  submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_submissions_rrf ON external_submissions(rrf_id);
CREATE INDEX idx_submissions_recruiter ON external_submissions(recruiter_id);
CREATE INDEX idx_submissions_status ON external_submissions(status);

-- Add trigger for updated_at
CREATE TRIGGER update_external_submissions_updated_at BEFORE UPDATE ON external_submissions
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- COMPLETION MESSAGE
-- ============================================
DO $$
BEGIN
  RAISE NOTICE '✅ Recruitment Schema Completed';
  RAISE NOTICE '📊 Table Created: external_submissions';
  RAISE NOTICE '🎯 Ready for Recruitment Dashboard Development';
END $$;
