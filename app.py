import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import json

st.set_page_config(
    page_title="Medical Insurance Verification | Baynunah",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

POLICY_YEAR = "2026"
RENEWAL_DEADLINE = datetime(2026, 1, 31)
SESSION_TIMEOUT_MINUTES = 15

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    .stApp {
        font-family: 'Poppins', sans-serif;
        background-color: #f5f5f5;
    }
    
    .main-header {
        background: #1E1B5C;
        padding: 18px 30px;
        margin: -80px -80px 0 -80px;
        color: white;
        position: sticky;
        top: 0;
        z-index: 999;
    }
    
    .header-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .header-left {
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .company-logo {
        width: 42px;
        height: 42px;
        background: white;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
    }
    
    .header-title h1 {
        margin: 0;
        font-size: 16px;
        font-weight: 600;
    }
    
    .header-title .subtitle {
        font-size: 11px;
        opacity: 0.8;
        margin-top: 2px;
        font-weight: 400;
    }
    
    .header-right {
        display: flex;
        align-items: center;
        gap: 25px;
    }
    
    .policy-badge {
        background: rgba(255,255,255,0.15);
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 500;
    }
    
    .user-block {
        text-align: right;
    }
    
    .user-name {
        font-size: 13px;
        font-weight: 500;
    }
    
    .user-id {
        font-size: 10px;
        opacity: 0.7;
    }
    
    .status-strip {
        background: #fff;
        border-bottom: 1px solid #e5e5e5;
        padding: 10px 30px;
        margin: 0 -80px 20px -80px;
        display: flex;
        justify-content: center;
        gap: 40px;
        font-size: 12px;
        color: #666;
    }
    
    .status-item {
        display: flex;
        align-items: center;
        gap: 6px;
    }
    
    .glass-card {
        background: #fff;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 16px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }
    
    .card-title {
        color: #1E1B5C;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 20px;
        padding-bottom: 12px;
        border-bottom: 1px solid #eee;
    }
    
    .snapshot-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px 40px;
    }
    
    .snapshot-item {
        display: flex;
        flex-direction: column;
        gap: 4px;
    }
    
    .snapshot-label {
        color: #888;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .snapshot-value {
        color: #1E1B5C;
        font-size: 14px;
        font-weight: 500;
    }
    
    .member-card {
        background: #fafafa;
        border-radius: 10px;
        padding: 18px;
        margin-bottom: 12px;
        border: 1px solid #eee;
    }
    
    .member-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 14px;
        padding-bottom: 10px;
        border-bottom: 1px solid #eee;
    }
    
    .member-name {
        color: #1E1B5C;
        font-size: 14px;
        font-weight: 600;
    }
    
    .member-badge {
        padding: 4px 12px;
        border-radius: 15px;
        font-size: 10px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .badge-principal {
        background: rgba(30, 27, 92, 0.1);
        color: #1E1B5C;
    }
    
    .badge-spouse {
        background: rgba(236, 72, 153, 0.1);
        color: #be185d;
    }
    
    .badge-child {
        background: rgba(245, 158, 11, 0.1);
        color: #b45309;
    }
    
    .member-details {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 10px 24px;
    }
    
    .member-detail-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 12px;
        padding: 2px 0;
    }
    
    .member-detail-label {
        color: #888;
    }
    
    .member-detail-value {
        color: #333;
        font-weight: 500;
    }
    
    .missing-value {
        color: #dc2626;
        font-size: 11px;
    }
    
    .missing-banner {
        background: rgba(220, 38, 38, 0.05);
        border-left: 3px solid #dc2626;
        border-radius: 0 8px 8px 0;
        padding: 10px 14px;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
        color: #b91c1c;
        font-size: 12px;
    }
    
    .confirmation-card {
        background: #fff;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 16px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }
    
    .radio-option {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 14px 16px;
        border: 2px solid #e5e5e5;
        border-radius: 10px;
        margin-bottom: 10px;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .radio-option:hover {
        border-color: #1E1B5C;
    }
    
    .radio-option.selected {
        border-color: #1E1B5C;
        background: rgba(30, 27, 92, 0.03);
    }
    
    .success-message {
        background: rgba(22, 163, 74, 0.08);
        border-radius: 12px;
        padding: 30px;
        text-align: center;
        margin: 16px 0;
    }
    
    .success-icon {
        width: 60px;
        height: 60px;
        background: rgba(22, 163, 74, 0.15);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 16px;
        font-size: 28px;
        color: #16a34a;
    }
    
    .success-title {
        color: #1E1B5C;
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 6px;
    }
    
    .success-desc {
        color: #666;
        font-size: 13px;
        line-height: 1.5;
    }
    
    .change-log {
        background: #fffbeb;
        border: 1px solid #fcd34d;
        border-radius: 8px;
        padding: 14px;
        margin-top: 14px;
    }
    
    .change-item {
        display: flex;
        gap: 8px;
        padding: 6px 0;
        border-bottom: 1px solid #fef3c7;
        font-size: 12px;
    }
    
    .change-item:last-child {
        border-bottom: none;
    }
    
    .old-value {
        color: #dc2626;
        text-decoration: line-through;
    }
    
    .new-value {
        color: #16a34a;
        font-weight: 500;
    }
    
    .login-container {
        max-width: 360px;
        margin: 60px auto;
        text-align: center;
    }
    
    .login-form-wrapper {
        max-width: 360px;
        margin: 0 auto;
    }
    
    .content-wrapper {
        max-width: 800px;
        margin: 0 auto;
        padding: 0 20px;
    }
    
    .login-header {
        margin-bottom: 25px;
    }
    
    .login-logo {
        width: 48px;
        height: 48px;
        background: #1E1B5C;
        border-radius: 12px;
        margin: 0 auto 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
    }
    
    .login-title {
        color: #1E1B5C;
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 4px;
    }
    
    .login-subtitle {
        color: #888;
        font-size: 12px;
        font-weight: 400;
    }
    
    .login-badge {
        display: inline-block;
        background: rgba(30, 27, 92, 0.08);
        color: #1E1B5C;
        padding: 5px 14px;
        border-radius: 15px;
        font-size: 11px;
        font-weight: 600;
        margin-top: 12px;
    }
    
    .stButton > button {
        background: #1E1B5C;
        color: white;
        border: none;
        padding: 12px 28px;
        font-weight: 600;
        font-size: 13px;
        letter-spacing: 1px;
        text-transform: uppercase;
        border-radius: 8px;
        width: 100%;
        transition: all 0.2s ease;
        font-family: 'Poppins', sans-serif;
    }
    
    .stButton > button:hover {
        background: #2d2a6e;
    }
    
    .signout-btn button {
        background: transparent !important;
        border: 1px solid #ddd !important;
        color: #666 !important;
        padding: 6px 16px !important;
        font-size: 11px !important;
        letter-spacing: 0.5px !important;
    }
    
    .signout-btn button:hover {
        background: #f5f5f5 !important;
    }
    
    .section-label {
        color: #666;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
        font-weight: 600;
    }
    
    div[data-testid="stForm"] {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 1px solid #ddd;
        padding: 10px 12px;
        font-family: 'Poppins', sans-serif;
        font-size: 13px;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #1E1B5C;
        box-shadow: 0 0 0 2px rgba(30, 27, 92, 0.1);
    }
    
    .stSelectbox > div > div {
        border-radius: 8px;
    }
    
    .stTextArea > div > div > textarea {
        border-radius: 8px;
        border: 1px solid #ddd;
        font-family: 'Poppins', sans-serif;
        font-size: 13px;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #1E1B5C;
        box-shadow: 0 0 0 2px rgba(30, 27, 92, 0.1);
    }
    
    .stRadio > div {
        gap: 8px;
    }
    
    .stRadio label {
        padding: 12px 16px !important;
        border: 2px solid #e5e5e5 !important;
        border-radius: 8px !important;
        margin-bottom: 8px !important;
    }
    
    .expired-notice {
        background: white;
        border-radius: 12px;
        padding: 40px 30px;
        text-align: center;
        max-width: 420px;
        margin: 80px auto;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
    }
    
    .inline-error {
        color: #dc2626;
        font-size: 11px;
        margin-top: 4px;
    }
    
    .field-hint {
        color: #888;
        font-size: 11px;
        margin-top: 4px;
    }
</style>
"""

SESSION_TIMEOUT_JS = f"""
<script>
    var sessionTimeout = {SESSION_TIMEOUT_MINUTES * 60 * 1000};
    var warningTime = {(SESSION_TIMEOUT_MINUTES - 2) * 60 * 1000};
    var sessionTimer;
    var warningTimer;
    
    function resetTimers() {{
        clearTimeout(sessionTimer);
        clearTimeout(warningTimer);
        
        warningTimer = setTimeout(function() {{
            alert('Your session will expire in 2 minutes due to inactivity.');
        }}, warningTime);
        
        sessionTimer = setTimeout(function() {{
            alert('Session expired due to inactivity. Please log in again.');
            window.location.reload();
        }}, sessionTimeout);
    }}
    
    document.addEventListener('click', resetTimers);
    document.addEventListener('keypress', resetTimers);
    document.addEventListener('scroll', resetTimers);
    
    resetTimers();
</script>
"""

DATA_FILE = "attached_assets/Medical_Insurance_Data.csv"
JOB_DATA_FILE = "attached_assets/job_data.csv"
CHANGES_FILE = "attached_assets/correction_requests.json"

@st.cache_data
def load_job_data():
    if os.path.exists(JOB_DATA_FILE):
        return pd.read_csv(JOB_DATA_FILE, encoding='utf-8-sig')
    return pd.DataFrame()

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE, encoding='utf-8-sig')
    job_df = load_job_data()
    if not job_df.empty:
        df = df.merge(job_df[['Staff Number', 'JOB TITLE', 'DEPARTMENT']], on='Staff Number', how='left')
    return df

def save_data(df):
    df.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')

def load_changes():
    if os.path.exists(CHANGES_FILE):
        with open(CHANGES_FILE, 'r') as f:
            return json.load(f)
    return []

def save_change_request(change_data):
    changes = load_changes()
    changes.append(change_data)
    with open(CHANGES_FILE, 'w') as f:
        json.dump(changes, f, indent=2)

def get_employee_data(df, staff_number):
    return df[df['Staff Number'] == staff_number]

def verify_credentials(df, staff_number, dob_input):
    principals = df[(df['Relation'] == 'PRINCIPAL') & (df['Staff Number'] == staff_number)]
    if principals.empty:
        return False, "Invalid Staff Number."
    
    principal = principals.iloc[0]
    dob_raw = principal.get('Date Of Birth', '')
    
    if pd.isna(dob_raw) or str(dob_raw).strip() == '' or str(dob_raw).strip() == 'nan':
        return False, "Account not properly configured. Please contact HR."
    
    dob_str = str(dob_raw).strip()
    
    try:
        if ' ' in dob_str:
            parts = dob_str.split(' ')
            dob_str = parts[0]
        
        formats_to_try = [
            ('%d/%m/%Y', '%d/%m/%Y'),
            ('%m/%d/%Y', '%d/%m/%Y'),
            ('%Y-%m-%d', '%d/%m/%Y'),
        ]
        
        actual_dob = None
        for parse_fmt, output_fmt in formats_to_try:
            try:
                parsed_date = datetime.strptime(dob_str, parse_fmt)
                if parsed_date.year < 1920 or parsed_date.year > 2025:
                    continue
                actual_dob = parsed_date.strftime(output_fmt)
                break
            except ValueError:
                continue
        
        if actual_dob is None:
            actual_dob = dob_str
        
        if dob_input.strip() == actual_dob:
            return True, None
        else:
            return False, "Invalid credentials. Please check your Staff Number and Date of Birth."
    except Exception:
        return False, "Account verification issue. Please contact HR."

def format_field(value):
    if pd.isna(value) or str(value).strip() == "" or str(value).strip() == "nan":
        return None
    return str(value).strip()

def check_link_expired():
    return datetime.now() > RENEWAL_DEADLINE

def render_expired_page():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    st.markdown("""
    <div class="expired-notice">
        <div style="font-size: 48px; margin-bottom: 20px;">⏰</div>
        <h2 style="color: #1a1a2e; font-size: 1.3em; margin-bottom: 12px;">Verification Period Ended</h2>
        <p style="color: #888; font-size: 0.9em; line-height: 1.6;">The medical insurance renewal verification period has closed.</p>
        <p style="color: #888; font-size: 0.85em; margin-top: 20px;">For any changes, please contact HR directly.</p>
        <a href="https://wa.me/971564966546" target="_blank" style="display: inline-block; margin-top: 25px; background: #25D366; color: white; padding: 12px 28px; border-radius: 30px; text-decoration: none; font-weight: 600; font-size: 0.85em;">
            📱 Contact HR via WhatsApp
        </a>
    </div>
    """, unsafe_allow_html=True)

def render_login():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="login-container">
        <div class="login-header">
            <div class="login-logo">🏥</div>
            <h1 class="login-title">Medical Insurance Verification</h1>
            <p class="login-subtitle">Employee Self-Service Portal</p>
            <div class="login-badge">Policy Year {POLICY_YEAR}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1.2, 1, 1.2])
    with col2:
        with st.form("login_form"):
            staff_number = st.text_input(
                "Staff Number",
                placeholder="e.g., BAYN00001",
                key="staff_input"
            )
            
            dob_input = st.text_input(
                "Date of Birth",
                placeholder="DD/MM/YYYY",
                key="dob_input"
            )
            
            submitted = st.form_submit_button("Sign In", use_container_width=True)
            
            if submitted:
                if not staff_number:
                    st.error("Please enter your Staff Number.")
                elif not dob_input:
                    st.error("Please enter your Date of Birth (DD/MM/YYYY).")
                else:
                    df = load_data()
                    is_valid, error_msg = verify_credentials(df, staff_number.upper(), dob_input)
                    
                    if is_valid:
                        st.session_state['authenticated'] = True
                        st.session_state['staff_number'] = staff_number.upper()
                        st.session_state['login_time'] = datetime.now().isoformat()
                        st.rerun()
                    else:
                        st.error(error_msg)
        
        st.markdown("""
        <div style="text-align: center; margin-top: 20px;">
            <p style="color: #aaa; font-size: 11px;">Need assistance?</p>
            <a href="https://wa.me/971564966546" target="_blank" style="color: #25D366; text-decoration: none; font-weight: 600; font-size: 12px;">
                WhatsApp HR Support
            </a>
        </div>
        """, unsafe_allow_html=True)

def render_header(principal_name, staff_number):
    st.markdown(f"""
    <div class="main-header">
        <div class="header-content">
            <div class="header-left">
                <div class="company-logo">🏥</div>
                <div class="header-title">
                    <h1>Medical Insurance Verification</h1>
                    <div class="subtitle">Employee Self-Service Portal</div>
                </div>
            </div>
            <div class="header-right">
                <div class="policy-badge">Policy Year {POLICY_YEAR}</div>
                <div class="user-block">
                    <div class="user-name">{principal_name}</div>
                    <div class="user-id">{staff_number}</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_status_strip():
    days_left = (RENEWAL_DEADLINE - datetime.now()).days
    deadline_str = RENEWAL_DEADLINE.strftime('%d %B %Y')
    st.markdown(f"""
    <div class="status-strip">
        <div class="status-item">
            <span>⏱</span>
            <span>Session timeout: {SESSION_TIMEOUT_MINUTES} min</span>
        </div>
        <div class="status-item">
            <span>📅</span>
            <span>Deadline: {deadline_str} ({days_left} days left)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_employee_snapshot(principal, staff_number):
    job_title = format_field(principal.get('JOB TITLE')) or format_field(principal.get('Job Title')) or "—"
    department = format_field(principal.get('DEPARTMENT')) or format_field(principal.get('Department')) or "—"
    emp_name = format_field(principal['Principal Name']) or '—'
    
    st.markdown(f"""
    <div class="glass-card">
        <div class="card-title">👤 Employee Snapshot</div>
        <div class="snapshot-grid">
            <div class="snapshot-item">
                <span class="snapshot-label">Employee Number</span>
                <span class="snapshot-value">{staff_number}</span>
            </div>
            <div class="snapshot-item">
                <span class="snapshot-label">Job Title</span>
                <span class="snapshot-value">{job_title}</span>
            </div>
            <div class="snapshot-item">
                <span class="snapshot-label">Employee Name</span>
                <span class="snapshot-value">{emp_name}</span>
            </div>
            <div class="snapshot-item">
                <span class="snapshot-label">Department</span>
                <span class="snapshot-value">{department}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def format_emirates_id(eid):
    if not eid:
        return None
    eid_str = str(eid).replace(' ', '').replace('-', '')
    if len(eid_str) == 15:
        return f"{eid_str[:3]}-{eid_str[3:7]}-{eid_str[7:14]}-{eid_str[14]}"
    return eid_str

def render_covered_members(employee_data):
    st.markdown("""
    <div class="glass-card">
        <div class="card-title">👥 Covered Members</div>
    """, unsafe_allow_html=True)
    
    has_missing = False
    for _, member in employee_data.iterrows():
        eid = format_field(member.get('National Identity'))
        passport = format_field(member.get('Passport number'))
        if not eid and not passport:
            has_missing = True
            break
    
    if has_missing:
        st.markdown("""
        <div class="missing-banner">
            <span>⚠️</span>
            <span>Some members have missing information. Please review and submit corrections if needed.</span>
        </div>
        """, unsafe_allow_html=True)
    
    for _, member in employee_data.iterrows():
        relation = member['Relation']
        badge_class = "badge-principal" if relation == "PRINCIPAL" else ("badge-spouse" if relation == "SPOUSE" else "badge-child")
        
        first_name = format_field(member.get('Member First Name')) or ''
        middle_name = format_field(member.get('Member Middle Name')) or ''
        last_name = format_field(member.get('Member Last Name')) or ''
        full_name = format_field(member.get('Member Full Name')) or f"{first_name} {middle_name} {last_name}".strip()
        full_name = ' '.join(full_name.split())
        
        dob = format_field(member.get('Date Of Birth'))
        if dob and ' ' in dob:
            dob = dob.split(' ')[0]
        dob = dob or "—"
        
        gender = format_field(member.get('Gender')) or "—"
        nationality = format_field(member.get('Nationality')) or "—"
        emirates_id = format_field(member.get('National Identity'))
        passport = format_field(member.get('Passport number'))
        
        eid_formatted = format_emirates_id(emirates_id) if emirates_id else None
        eid_display = eid_formatted if eid_formatted else '<span class="missing-value">Not provided</span>'
        passport_display = passport if passport else '<span class="missing-value">Not provided</span>'
        
        st.markdown(f"""
        <div class="member-card">
            <div class="member-header">
                <span class="member-name">{full_name}</span>
                <span class="member-badge {badge_class}">{relation}</span>
            </div>
            <div class="member-details">
                <div class="member-detail-item">
                    <span class="member-detail-label">Date of Birth</span>
                    <span class="member-detail-value">{dob}</span>
                </div>
                <div class="member-detail-item">
                    <span class="member-detail-label">Gender</span>
                    <span class="member-detail-value">{gender}</span>
                </div>
                <div class="member-detail-item">
                    <span class="member-detail-label">Nationality</span>
                    <span class="member-detail-value">{nationality}</span>
                </div>
                <div class="member-detail-item">
                    <span class="member-detail-label">Emirates ID</span>
                    <span class="member-detail-value">{eid_display}</span>
                </div>
                <div class="member-detail-item">
                    <span class="member-detail-label">Passport</span>
                    <span class="member-detail-value">{passport_display}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_confirmation_section(employee_data, staff_number):
    confirmed = employee_data['EmployeeConfirmed'].iloc[0] if 'EmployeeConfirmed' in employee_data.columns else ""
    if not confirmed or str(confirmed).strip() == "":
        confirmed = employee_data['Confirmed'].iloc[0] if 'Confirmed' in employee_data.columns else ""
    already_confirmed = pd.notna(confirmed) and str(confirmed).strip() != ""
    
    if already_confirmed:
        st.markdown(f"""
        <div class="success-message">
            <div class="success-icon">✓</div>
            <div class="success-title">Information Confirmed</div>
            <div class="success-desc">You confirmed your information on {confirmed}.<br>HR will proceed with the insurance renewal.</div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    if 'submission_success' in st.session_state and st.session_state['submission_success']:
        if st.session_state.get('submission_type') == 'confirmation':
            st.markdown("""
            <div class="success-message">
                <div class="success-icon">✓</div>
                <div class="success-title">Thank You!</div>
                <div class="success-desc">Your information has been confirmed.<br>HR will proceed with the renewal.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="success-message">
                <div class="success-icon">📝</div>
                <div class="success-title">Correction Request Submitted</div>
                <div class="success-desc">Your request has been recorded.<br>HR will review and contact you if needed.</div>
            </div>
            """, unsafe_allow_html=True)
        return
    
    st.markdown("""
    <div class="glass-card">
        <div class="card-title">✔️ Confirmation</div>
        <p style="color: #666; font-size: 0.9em; margin-bottom: 20px;">
            Please review the information above. If everything is correct, confirm below. 
            If you need to request changes, select the correction option.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    action = st.radio(
        "Select your action:",
        ["✅ I confirm that all information above is accurate",
         "📝 I need to request corrections"],
        key="action_choice",
        label_visibility="collapsed"
    )
    
    if "I confirm" in action:
        st.markdown("---")
        confirm_checkbox = st.checkbox(
            "I hereby confirm that all the information displayed for myself and my dependents is accurate and complete.",
            key="confirm_checkbox"
        )
        
        if st.button("Submit Confirmation", type="primary", disabled=not confirm_checkbox):
            df = load_data()
            confirmation_time = datetime.now().strftime("%d/%m/%Y %I:%M %p")
            df.loc[df['Staff Number'] == staff_number, 'EmployeeConfirmed'] = confirmation_time
            save_data(df)
            st.cache_data.clear()
            st.session_state['submission_success'] = True
            st.session_state['submission_type'] = 'confirmation'
            st.balloons()
            st.rerun()
    
    else:
        render_correction_form(employee_data, staff_number)

def render_correction_form(employee_data, staff_number):
    dependents = employee_data[employee_data['Relation'] != 'PRINCIPAL']
    principal = employee_data[employee_data['Relation'] == 'PRINCIPAL'].iloc[0]
    
    principal_eid = format_field(principal.get('National Identity')) or ""
    principal_passport = format_field(principal.get('Passport number')) or ""
    principal_has_missing = not principal_eid or not principal_passport
    
    editable_members = []
    
    if principal_has_missing:
        principal_name = format_field(principal.get('Member Full Name')) or f"{format_field(principal.get('Member First Name')) or ''} {format_field(principal.get('Member Middle Name')) or ''} {format_field(principal.get('Member Last Name')) or ''}".strip()
        principal_name = ' '.join(principal_name.split())
        editable_members.append({
            "label": f"PRINCIPAL (Self): {principal_name}",
            "row": principal,
            "is_principal": True
        })
    
    for _, member in dependents.iterrows():
        relation = member['Relation']
        name = format_field(member.get('Member Full Name')) or f"{format_field(member.get('Member First Name')) or ''} {format_field(member.get('Member Middle Name')) or ''} {format_field(member.get('Member Last Name')) or ''}".strip()
        name = ' '.join(name.split())
        editable_members.append({
            "label": f"{relation}: {name}",
            "row": member,
            "is_principal": False
        })
    
    if not editable_members:
        st.info("No corrections available. All information is complete.")
        return
    
    st.markdown("""
    <div class="glass-card">
        <div class="card-title">📝 Correction Request</div>
        <p style="color: #666; font-size: 0.85em; margin-bottom: 15px;">
            Select a member and specify the corrections needed below.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    member_options = [m["label"] for m in editable_members]
    selected_member = st.selectbox("Select Member to Correct", member_options, key="selected_member")
    
    selected_idx = member_options.index(selected_member)
    member_info = editable_members[selected_idx]
    member_row = member_info["row"]
    is_principal = member_info["is_principal"]
    member_number = member_row['Member Number']
    
    st.markdown('<p class="section-label" style="margin-top: 20px;">Fields to Correct</p>', unsafe_allow_html=True)
    
    if is_principal:
        st.caption("As the principal, you can only add missing Emirates ID or Passport information.")
    else:
        st.caption("Only fill in fields that need correction. Leave others empty.")
    
    changes = []
    
    current_name = format_field(member_row.get('Member Full Name')) or f"{format_field(member_row.get('Member First Name')) or ''} {format_field(member_row.get('Member Middle Name')) or ''} {format_field(member_row.get('Member Last Name')) or ''}".strip()
    current_name = ' '.join(current_name.split())
    
    col1, col2 = st.columns(2)
    
    with col1:
        if not is_principal:
            new_name = st.text_input("Dependent Name", value="", placeholder=f"Current: {current_name}", key="corr_name")
            if new_name and new_name != current_name:
                changes.append({"field": "Dependent Name", "old": current_name, "new": new_name})
            
            current_relation = format_field(member_row.get('Relation')) or ""
            new_relation = st.selectbox(
                "Relationship",
                ["", "SPOUSE", "CHILD"],
                index=0,
                key="corr_relation"
            )
            if new_relation and new_relation != current_relation:
                changes.append({"field": "Relationship", "old": current_relation, "new": new_relation})
        else:
            st.text_input("Name", value=current_name, disabled=True, key="corr_name_locked")
    
    with col2:
        if not is_principal:
            current_dob = format_field(member_row.get('Date Of Birth')) or ""
            new_dob = st.text_input("Date of Birth (DD/MM/YYYY)", value="", placeholder=f"Current: {current_dob}", key="corr_dob")
            if new_dob and new_dob != current_dob:
                changes.append({"field": "Date of Birth", "old": current_dob, "new": new_dob})
        
        current_eid = format_field(member_row.get('National Identity')) or ""
        current_passport = format_field(member_row.get('Passport number')) or ""
        
        if not current_eid:
            new_eid = st.text_input("Emirates ID", value="", placeholder="Not provided - add if available", key="corr_eid")
            if new_eid:
                changes.append({"field": "Emirates ID", "old": "Not provided", "new": new_eid})
        else:
            st.text_input("Emirates ID", value=current_eid, disabled=True, key="corr_eid_locked")
        
        if not current_passport:
            new_passport = st.text_input("Passport Number", value="", placeholder="Not provided - add if available", key="corr_passport")
            if new_passport:
                changes.append({"field": "Passport Number", "old": "Not provided", "new": new_passport})
        else:
            st.text_input("Passport Number", value=current_passport, disabled=True, key="corr_passport_locked")
    
    if changes:
        st.markdown('<p class="section-label" style="margin-top: 20px;">Changes Summary</p>', unsafe_allow_html=True)
        st.markdown('<div class="change-log">', unsafe_allow_html=True)
        for change in changes:
            st.markdown(f"""
            <div class="change-item">
                <strong>{change['field']}:</strong>
                <span class="old-value">{change['old']}</span> → 
                <span class="new-value">{change['new']}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<p class="section-label" style="margin-top: 20px;">Remarks</p>', unsafe_allow_html=True)
    remarks = st.text_area(
        "Please provide details for the correction (Required)",
        placeholder="e.g., 'Emirates ID was renewed' or 'Spelling correction'",
        key="corr_remarks",
        label_visibility="collapsed"
    )
    
    submit_disabled = len(changes) == 0 or not remarks.strip()
    
    if st.button("Submit Correction Request", type="primary", disabled=submit_disabled):
        change_request = {
            "staff_number": staff_number,
            "member_number": member_number,
            "member_name": selected_member,
            "changes": changes,
            "remarks": remarks,
            "submitted_at": datetime.now().isoformat(),
            "status": "pending"
        }
        
        save_change_request(change_request)
        
        df = load_data()
        df.loc[df['Staff Number'] == staff_number, 'LastEditedByStaffNo'] = staff_number
        df.loc[df['Staff Number'] == staff_number, 'LastEditedOn'] = datetime.now().strftime("%d/%m/%Y %I:%M %p")
        save_data(df)
        st.cache_data.clear()
        
        st.session_state['submission_success'] = True
        st.session_state['submission_type'] = 'correction'
        st.rerun()
    
    if submit_disabled:
        if len(changes) == 0:
            st.caption("⚠️ Please fill in at least one field to correct")
        elif not remarks.strip():
            st.caption("⚠️ Remarks are mandatory for correction requests")

def render_dashboard():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    st.markdown(SESSION_TIMEOUT_JS, unsafe_allow_html=True)
    
    staff_number = st.session_state.get('staff_number', '')
    df = load_data()
    employee_data = get_employee_data(df, staff_number)
    
    if employee_data.empty:
        st.error("No data found for your account.")
        return
    
    principal = employee_data[employee_data['Relation'] == 'PRINCIPAL'].iloc[0]
    principal_name = principal['Principal Name']
    
    render_header(principal_name, staff_number)
    render_status_strip()
    
    col1, col2, col3 = st.columns([1, 2.5, 1])
    with col2:
        signout_col1, signout_col2 = st.columns([5, 1])
        with signout_col2:
            st.markdown('<div class="signout-btn">', unsafe_allow_html=True)
            if st.button("Sign Out", use_container_width=True):
                st.session_state.clear()
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        render_employee_snapshot(principal, staff_number)
        render_covered_members(employee_data)
        render_confirmation_section(employee_data, staff_number)
        
        st.markdown("""
        <div style="text-align: center; margin-top: 30px; padding: 16px; color: #999; font-size: 11px;">
            Need help? <a href="https://wa.me/971564966546" target="_blank" style="color: #25D366; text-decoration: none;">WhatsApp HR Support</a>
        </div>
        """, unsafe_allow_html=True)

def main():
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
    
    if check_link_expired():
        render_expired_page()
        return
    
    if st.session_state['authenticated']:
        render_dashboard()
    else:
        render_login()

if __name__ == "__main__":
    main()
