# Pull Request

## 📋 Description
<!-- Provide a clear and concise description of the changes -->

### What changed?
<!-- Describe what was added, modified, or removed -->

### Why was this change needed?
<!-- Explain the motivation and context -->

### Related Issue
<!-- Link to the issue this PR addresses -->
Closes #<!-- issue number -->

---

## 🧪 Testing Checklist

### Backend Testing
- [ ] Backend linting passes (`cd backend && find app -name '*.py' -exec uv run python -m py_compile {} +`)
- [ ] Database migrations tested (if applicable)
- [ ] API endpoints tested via Swagger UI (`/docs`)
- [ ] Authentication/authorization verified
- [ ] Input validation and sanitization checked

### Frontend Testing
- [ ] Frontend linting passes (`cd frontend && npm run lint`)
- [ ] TypeScript type checking passes
- [ ] UI changes tested in browser
- [ ] Responsive design verified (mobile, tablet, desktop)
- [ ] Screenshots attached for UI changes (see below)

### Integration Testing
- [ ] Backend and frontend work together correctly
- [ ] API calls return expected responses
- [ ] Error handling works as expected
- [ ] No console errors or warnings

---

## 🔒 Security Checklist

- [ ] No secrets or credentials committed
- [ ] User input is sanitized (using `sanitize_text()` for backend)
- [ ] SQL queries are parameterized (no string concatenation)
- [ ] Authentication/authorization enforced on protected endpoints
- [ ] CORS settings reviewed (if modified)
- [ ] No sensitive data in logs
- [ ] Dependencies checked for known vulnerabilities
- [ ] CodeQL security scan passed (will run automatically)

---

## 🇦🇪 UAE Compliance & HR Context

### Compliance Impact
- [ ] No impact on UAE labor law compliance
- [ ] Impact on compliance features (visa tracking, EID, medical fitness, etc.)
  - **If checked, describe impact:**

### Data Privacy
- [ ] No changes to personal data handling
- [ ] Changes respect UAE data protection requirements
- [ ] Sensitive employee data is protected

### HR User Impact
- [ ] No impact on HR admin users
- [ ] Changes affect HR users (describe below):
  - **Impact description:**
  - **Non-technical guidance provided:** [ ] Yes [ ] No

---

## 📸 Screenshots / Videos
<!-- For UI changes, please add before/after screenshots -->

### Before
<!-- Screenshot or N/A -->

### After
<!-- Screenshot or N/A -->

---

## 📚 Documentation Updates

- [ ] README.md updated (if needed)
- [ ] CONTRIBUTING.md updated (if needed)
- [ ] API documentation updated (docstrings, Swagger descriptions)
- [ ] User guide updated (docs/HR_USER_GUIDE.md)
- [ ] Comments added for complex logic
- [ ] Migration guide provided (for breaking changes)

---

## 🚀 Deployment Considerations

### Database Changes
- [ ] No database changes
- [ ] Database migrations included
  - **Migration safety:** [ ] Backwards compatible [ ] Requires downtime
  - **Rollback plan:** <!-- Describe how to rollback if needed -->

### Configuration Changes
- [ ] No configuration changes
- [ ] Environment variables added/modified
  - **Required .env updates:**
  ```
  # List new/modified env vars here
  ```

### Infrastructure Impact
- [ ] No infrastructure changes
- [ ] Infrastructure changes required:
  - **Description:**

---

## 🎯 Code Quality

### Architecture & Patterns
- [ ] Follows 3-layer pattern (Router → Service → Repository)
- [ ] Business logic is in service layer (not in routers)
- [ ] Database access is in repository layer (not in services)
- [ ] Async/await used correctly for all DB operations
- [ ] Error handling follows project conventions

### Code Style
- [ ] Python code follows PEP 8
- [ ] TypeScript follows project conventions
- [ ] Meaningful variable and function names
- [ ] Complex logic has comments
- [ ] Type hints added (Python) / TypeScript types defined

### Performance
- [ ] No obvious performance issues
- [ ] Database queries optimized (indexes considered)
- [ ] No N+1 query problems
- [ ] Large operations paginated

---

## 🧑‍💼 For Non-Technical Reviewers (HR/Admin)

<!-- This section helps non-technical stakeholders understand the change -->

### What does this change mean for HR users?
<!-- Explain in simple terms what changes and why it matters -->

### Do HR users need to do anything?
<!-- List any actions needed, or state "No action required" -->
- [ ] No action required
- [ ] Action required (describe below):

### Is training needed?
- [ ] No training needed
- [ ] Training recommended:
  - **What:** <!-- What needs to be learned -->
  - **Resources:** <!-- Link to guides, videos, etc. -->

---

## ✅ Pre-Merge Checklist

- [ ] All CI checks passing (lint, security scan)
- [ ] Code reviewed and approved
- [ ] Documentation updated
- [ ] Security checklist completed
- [ ] UAE compliance impact assessed
- [ ] Non-technical guidance provided (if needed)
- [ ] Breaking changes documented with migration guide
- [ ] Tested locally and verified working

---

## 🤖 For AI Reviewers (Copilot, etc.)

### Code Context
<!-- Help AI understand the architectural decisions -->
- **Module:** <!-- e.g., Employee Management, Compliance Tracking -->
- **Pattern:** <!-- e.g., Standard 3-layer, Public onboarding flow -->
- **Special considerations:** <!-- Anything the AI should know -->

### Review Focus Areas
<!-- What should reviewers pay special attention to? -->
- [ ] Security vulnerabilities
- [ ] Performance bottlenecks
- [ ] Code duplication
- [ ] Error handling
- [ ] UAE compliance requirements
- [ ] User experience for non-technical users

---

## 📝 Additional Notes
<!-- Any other information that reviewers should know -->

---

## 🏷️ Labels
<!-- Add appropriate labels to help triage and categorize this PR -->

**Suggested labels:**
- `enhancement` / `bug` / `documentation` / `security`
- `backend` / `frontend` / `database`
- `high-priority` / `medium-priority` / `low-priority`
- `uae-compliance` / `hr-feature`
- `breaking-change` (if applicable)
