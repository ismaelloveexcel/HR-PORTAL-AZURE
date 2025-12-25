# Medical Insurance Renewal - Employee Verification Portal

## Overview
A secure employee self-service portal for medical insurance renewal verification. Employees authenticate with Staff Number + Date of Birth to review their insurance details and either confirm accuracy OR submit correction requests.

## Current State
- **Status**: Complete and functional
- **Last Updated**: December 24, 2025
- **Policy Year**: 2026
- **Verification Deadline**: January 31, 2026

## Features

### Layout Sections
1. **Header** - Company logo placeholder, title, Policy Year badge
2. **Employee Snapshot** (Read-only) - Employee Number, Name, Job Title, Department
3. **Covered Members** - List of all dependents with key details (DOB, Gender, Nationality, Emirates ID, Passport)
4. **Confirmation** - Two-path workflow (Confirm or Request Correction)
5. **Correction Request** - Conditionally visible form with change tracking
6. **Submission Status** - Success messages

### Two-Path Workflow
- **Path A: Confirmation** - Employee confirms all information is accurate
- **Path B: Correction Request** - Employee submits change requests with:
  - Editable fields (Name, DOB, Relationship, Emirates ID, Passport)
  - Mandatory remarks field
  - Auto-capture of old value → new value with timestamp

### Security Features
- Session timeout (15 minutes of inactivity)
- Link expiration after deadline date
- Principal's DOB locked (used for authentication)

## Project Structure
```
/
├── app.py                 # Main Streamlit application
├── attached_assets/
│   ├── Medical_Insurance_-_Workings_*.csv   # Employee data
│   └── correction_requests.json              # Change requests log
├── .streamlit/
│   └── config.toml        # Streamlit server configuration
└── replit.md              # This documentation
```

## Technical Details
- **Framework**: Streamlit
- **Port**: 5000
- **Data Storage**: CSV file + JSON for correction requests
- **Authentication**: Staff Number + Date of Birth validation

## Configuration
Located at top of app.py:
- `POLICY_YEAR` - Current policy year (2026)
- `RENEWAL_DEADLINE` - Cutoff date for verification
- `SESSION_TIMEOUT_MINUTES` - Inactivity timeout (15 min)

## Sample Staff Numbers for Testing
- BAYN00008 (Mohammad Ismael Sudally) - DOB: 16/05/1988
- BAYN00047 (Alexander Manual Vaz) - DOB: 06/03/1958
- BAYN00002 (Syed Irfan Zakiuddin) - DOB: 11/03/1979
- BAYN00003 (Michael Rutman) - DOB: 21/07/1979

## Running the Application
```bash
streamlit run app.py --server.port 5000
```

## Future Enhancements (Not Yet Implemented)
- SharePoint List integration (writeback)
- Power Automate email trigger for HR notifications
