import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import json

st.set_page_config(
    page_title="Medical Insurance Renewal - Employee Verification",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

POLICY_YEAR = "2026"
RENEWAL_DEADLINE = datetime(2026, 1, 31)
SESSION_TIMEOUT_MINUTES = 15

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;600;700&display=swap');
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    .stApp {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background-color: #f5f5f5;
    }
    
    .main-header {
        background: linear-gradient(135deg, #0078d4 0%, #005a9e 100%);
        padding: 20px 30px;
        margin: -80px -80px 30px -80px;
        color: white;
    }
    
    .header-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .header-left {
        display: flex;
        align-items: center;
        gap: 20px;
    }
    
    .company-logo {
        width: 60px;
        height: 60px;
        background: white;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
    }
    
    .header-title h1 {
        margin: 0;
        font-size: 22px;
        font-weight: 600;
    }
    
    .header-title .subtitle {
        font-size: 13px;
        opacity: 0.9;
        margin-top: 4px;
    }
    
    .policy-badge {
        background: rgba(255,255,255,0.2);
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: 600;
    }
    
    .section-card {
        background: white;
        border-radius: 8px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border: 1px solid #e8e8e8;
    }
    
    .section-title {
        font-size: 16px;
        font-weight: 600;
        color: #0078d4;
        margin-bottom: 20px;
        padding-bottom: 12px;
        border-bottom: 2px solid #0078d4;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .info-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px;
    }
    
    .info-item {
        padding: 12px;
        background: #f8f9fa;
        border-radius: 6px;
    }
    
    .info-label {
        font-size: 11px;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }
    
    .info-value {
        font-size: 15px;
        color: #1a1a1a;
        font-weight: 500;
    }
    
    .info-value.placeholder {
        color: #999;
        font-style: italic;
    }
    
    .dependent-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 15px;
    }
    
    .dependent-table th {
        background: #f0f0f0;
        padding: 12px;
        text-align: left;
        font-size: 12px;
        font-weight: 600;
        color: #444;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .dependent-table td {
        padding: 12px;
        border-bottom: 1px solid #eee;
        font-size: 14px;
    }
    
    .relation-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    .badge-principal { background: #0078d4; color: white; }
    .badge-spouse { background: #d83b01; color: white; }
    .badge-child { background: #107c10; color: white; }
    
    .path-container {
        display: flex;
        gap: 20px;
        margin-top: 20px;
    }
    
    .path-option {
        flex: 1;
        padding: 20px;
        border: 2px solid #e0e0e0;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .path-option:hover {
        border-color: #0078d4;
        background: #f8fbff;
    }
    
    .path-option.selected {
        border-color: #0078d4;
        background: #f0f7ff;
    }
    
    .path-icon {
        font-size: 32px;
        margin-bottom: 10px;
    }
    
    .path-title {
        font-size: 16px;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 5px;
    }
    
    .path-desc {
        font-size: 13px;
        color: #666;
    }
    
    .success-message {
        background: #dff6dd;
        border: 1px solid #107c10;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        margin: 20px 0;
    }
    
    .success-icon {
        font-size: 48px;
        margin-bottom: 10px;
    }
    
    .success-title {
        font-size: 18px;
        font-weight: 600;
        color: #107c10;
        margin-bottom: 5px;
    }
    
    .success-desc {
        color: #444;
        font-size: 14px;
    }
    
    .change-log {
        background: #fff8e6;
        border: 1px solid #ffb900;
        border-radius: 6px;
        padding: 15px;
        margin-top: 15px;
    }
    
    .change-item {
        display: flex;
        gap: 10px;
        padding: 8px 0;
        border-bottom: 1px solid #ffe5a0;
        font-size: 13px;
    }
    
    .change-item:last-child {
        border-bottom: none;
    }
    
    .old-value {
        color: #d83b01;
        text-decoration: line-through;
    }
    
    .new-value {
        color: #107c10;
        font-weight: 500;
    }
    
    .login-container {
        max-width: 420px;
        margin: 80px auto;
        background: white;
        padding: 40px;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    
    .login-header {
        text-align: center;
        margin-bottom: 30px;
    }
    
    .login-logo {
        width: 80px;
        height: 80px;
        background: linear-gradient(135deg, #0078d4, #005a9e);
        border-radius: 16px;
        margin: 0 auto 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 36px;
    }
    
    .stButton > button {
        background-color: #0078d4;
        color: white;
        border: none;
        padding: 12px 24px;
        font-weight: 600;
        border-radius: 6px;
        width: 100%;
        transition: background-color 0.2s;
    }
    
    .stButton > button:hover {
        background-color: #005a9e;
    }
    
    .expired-notice {
        background: #fde7e9;
        border: 1px solid #d83b01;
        border-radius: 8px;
        padding: 30px;
        text-align: center;
        margin: 100px auto;
        max-width: 500px;
    }
    
    .timeout-warning {
        background: #fff4ce;
        border: 1px solid #ffb900;
        border-radius: 6px;
        padding: 10px 15px;
        font-size: 13px;
        color: #6a5700;
        margin-bottom: 20px;
        text-align: center;
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

DATA_FILE = "attached_assets/Medical_Insurance_-_Workings_1766604832610.csv"
CHANGES_FILE = "attached_assets/correction_requests.json"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE, encoding='utf-8-sig')
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
            dob_str = dob_str.split(' ')[0]
        
        for fmt in ['%d/%m/%Y', '%m/%d/%Y', '%Y-%m-%d']:
            try:
                parsed_date = datetime.strptime(dob_str, fmt)
                actual_dob = parsed_date.strftime('%d/%m/%Y')
                break
            except ValueError:
                continue
        else:
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
        <div style="font-size: 48px; margin-bottom: 15px;">⏰</div>
        <h2 style="color: #d83b01; margin-bottom: 10px;">Verification Period Ended</h2>
        <p style="color: #666;">The medical insurance renewal verification period has ended.</p>
        <p style="color: #666; margin-top: 15px;">If you need to make changes, please contact HR directly.</p>
        <a href="https://wa.me/971564966546" target="_blank" style="display: inline-block; margin-top: 20px; background: #25D366; color: white; padding: 12px 24px; border-radius: 25px; text-decoration: none; font-weight: 600;">
            📱 Contact HR via WhatsApp
        </a>
    </div>
    """, unsafe_allow_html=True)

def render_login():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("""
        <div class="login-container">
            <div class="login-header">
                <div class="login-logo">🏥</div>
                <h1 style="color: #1a1a1a; font-size: 22px; margin-bottom: 8px;">Medical Insurance Renewal</h1>
                <p style="color: #666; font-size: 14px;">Employee Verification Portal</p>
                <div style="background: #e8f4fd; padding: 8px 16px; border-radius: 20px; display: inline-block; margin-top: 15px;">
                    <span style="color: #0078d4; font-weight: 600;">Policy Year """ + POLICY_YEAR + """</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
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
            <p style="color: #999; font-size: 12px;">Need help? Contact HR</p>
            <a href="https://wa.me/971564966546" target="_blank" style="color: #25D366; text-decoration: none; font-weight: 600;">
                📱 WhatsApp HR Support
            </a>
        </div>
        """, unsafe_allow_html=True)

def render_header(principal_name, staff_number):
    st.markdown(f"""
    <div class="main-header">
        <div class="header-content">
            <div class="header-left">
                <div class="company-logo">🏢</div>
                <div class="header-title">
                    <h1>Medical Insurance Renewal</h1>
                    <div class="subtitle">Employee Verification Portal</div>
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 30px;">
                <div class="policy-badge">📅 Policy Year {POLICY_YEAR}</div>
                <div style="text-align: right;">
                    <div style="font-size: 13px; opacity: 0.8;">Logged in as</div>
                    <div style="font-weight: 600;">{principal_name}</div>
                    <div style="font-size: 12px; opacity: 0.8;">{staff_number}</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_employee_snapshot(principal, staff_number):
    job_title = format_field(principal.get('Job Title')) or "—"
    department = format_field(principal.get('Department')) or "—"
    
    st.markdown(f"""
    <div class="section-card">
        <div class="section-title">👤 Section 1: Employee Snapshot</div>
        <div class="info-grid">
            <div class="info-item">
                <div class="info-label">Employee Number</div>
                <div class="info-value">{staff_number}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Employee Name</div>
                <div class="info-value">{format_field(principal['Principal Name']) or '—'}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Job Title</div>
                <div class="info-value placeholder">{job_title}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Department</div>
                <div class="info-value placeholder">{department}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_insurance_details(employee_data):
    dependents_count = len(employee_data)
    spouse_count = len(employee_data[employee_data['Relation'] == 'SPOUSE'])
    children_count = len(employee_data[employee_data['Relation'] == 'CHILD'])
    
    st.markdown(f"""
    <div class="section-card">
        <div class="section-title">📋 Section 2: Current Insurance Details</div>
        <div class="info-grid">
            <div class="info-item">
                <div class="info-label">Insurance Provider</div>
                <div class="info-value placeholder">To be updated</div>
            </div>
            <div class="info-item">
                <div class="info-label">Policy Number</div>
                <div class="info-value placeholder">To be updated</div>
            </div>
            <div class="info-item">
                <div class="info-label">Plan Type</div>
                <div class="info-value placeholder">To be updated</div>
            </div>
            <div class="info-item">
                <div class="info-label">Coverage Category</div>
                <div class="info-value placeholder">To be updated</div>
            </div>
        </div>
        
        <div style="margin-top: 20px; padding-top: 15px; border-top: 1px solid #eee;">
            <div class="info-label" style="margin-bottom: 10px;">DEPENDENTS LISTED ({dependents_count} members)</div>
            <div style="display: flex; gap: 15px;">
                <span class="relation-badge badge-principal">Principal: 1</span>
                <span class="relation-badge badge-spouse">Spouse: {spouse_count}</span>
                <span class="relation-badge badge-child">Children: {children_count}</span>
            </div>
        </div>
        
        <table class="dependent-table">
            <thead>
                <tr>
                    <th>Relation</th>
                    <th>Full Name</th>
                    <th>Date of Birth</th>
                    <th>Gender</th>
                    <th>Emirates ID / Passport</th>
                </tr>
            </thead>
            <tbody>
    """, unsafe_allow_html=True)
    
    rows_html = ""
    for _, member in employee_data.iterrows():
        relation = member['Relation']
        badge_class = "badge-principal" if relation == "PRINCIPAL" else ("badge-spouse" if relation == "SPOUSE" else "badge-child")
        
        full_name = format_field(member.get('Member Full Name')) or f"{format_field(member.get('Member First Name', '')) or ''} {format_field(member.get('Member Last Name', '')) or ''}".strip()
        dob = format_field(member.get('Date Of Birth')) or "—"
        gender = format_field(member.get('Gender')) or "—"
        emirates_id = format_field(member.get('National Identity')) or "—"
        passport = format_field(member.get('Passport number')) or "—"
        id_display = emirates_id if emirates_id != "—" else passport
        
        rows_html += f"""
            <tr>
                <td><span class="relation-badge {badge_class}">{relation}</span></td>
                <td>{full_name}</td>
                <td>{dob}</td>
                <td>{gender}</td>
                <td>{id_display}</td>
            </tr>
        """
    
    st.markdown(rows_html + """
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

def render_confirmation_section(employee_data, staff_number):
    confirmed = employee_data['EmployeeConfirmed'].iloc[0]
    already_confirmed = pd.notna(confirmed) and str(confirmed).strip() != ""
    
    if already_confirmed:
        st.markdown(f"""
        <div class="success-message">
            <div class="success-icon">✅</div>
            <div class="success-title">Information Confirmed</div>
            <div class="success-desc">You confirmed your information on {confirmed}. HR will proceed with renewal.</div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    if 'submission_success' in st.session_state and st.session_state['submission_success']:
        if st.session_state.get('submission_type') == 'confirmation':
            st.markdown("""
            <div class="success-message">
                <div class="success-icon">✅</div>
                <div class="success-title">Thank You!</div>
                <div class="success-desc">Your information has been confirmed. HR will proceed with the renewal.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="success-message">
                <div class="success-icon">📝</div>
                <div class="success-title">Correction Request Submitted</div>
                <div class="success-desc">Your request has been recorded. HR will review and contact you if needed.</div>
            </div>
            """, unsafe_allow_html=True)
        return
    
    st.markdown("""
    <div class="section-card">
        <div class="section-title">✔️ Section 3: Confirmation</div>
        <p style="color: #444; margin-bottom: 20px;">Please review the information above carefully. If everything is correct, confirm below. If you need to request corrections, select that option instead.</p>
    </div>
    """, unsafe_allow_html=True)
    
    action = st.radio(
        "Select your action:",
        ["✅ I confirm that all information above is accurate as of today",
         "📝 I need to request corrections to some information"],
        key="action_choice",
        label_visibility="collapsed"
    )
    
    if "I confirm" in action:
        st.markdown("---")
        confirm_checkbox = st.checkbox(
            "I hereby confirm that all the information displayed above for myself and my dependents is accurate and complete.",
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
    st.markdown("""
    <div class="section-card">
        <div class="section-title">📝 Section 4: Correction Request</div>
        <p style="color: #444; margin-bottom: 15px;">Please specify the corrections needed. Only fill in fields that require changes.</p>
    </div>
    """, unsafe_allow_html=True)
    
    member_options = []
    for _, member in employee_data.iterrows():
        relation = member['Relation']
        name = format_field(member.get('Member Full Name')) or f"{format_field(member.get('Member First Name', '')) or ''} {format_field(member.get('Member Last Name', '')) or ''}".strip()
        member_options.append(f"{relation}: {name}")
    
    selected_member = st.selectbox("Select Member to Correct", member_options, key="selected_member")
    
    selected_idx = member_options.index(selected_member)
    member_row = employee_data.iloc[selected_idx]
    member_number = member_row['Member Number']
    
    st.markdown("#### Fields to Correct")
    st.caption("Only fill in fields that need correction. Leave others empty.")
    
    changes = []
    
    col1, col2 = st.columns(2)
    
    with col1:
        current_name = format_field(member_row.get('Member Full Name')) or ""
        new_name = st.text_input("Full Name", value="", placeholder=f"Current: {current_name}", key="corr_name")
        if new_name and new_name != current_name:
            changes.append({"field": "Full Name", "old": current_name, "new": new_name})
        
        current_dob = format_field(member_row.get('Date Of Birth')) or ""
        if member_row['Relation'] != 'PRINCIPAL':
            new_dob = st.text_input("Date of Birth (DD/MM/YYYY)", value="", placeholder=f"Current: {current_dob}", key="corr_dob")
            if new_dob and new_dob != current_dob:
                changes.append({"field": "Date of Birth", "old": current_dob, "new": new_dob})
        else:
            st.text_input("Date of Birth", value=current_dob, disabled=True, key="corr_dob_locked")
            st.caption("Principal's DOB cannot be changed (used for authentication)")
    
    with col2:
        current_relation = format_field(member_row.get('Relation')) or ""
        if member_row['Relation'] != 'PRINCIPAL':
            new_relation = st.selectbox(
                "Relationship",
                ["", "SPOUSE", "CHILD"],
                index=0,
                key="corr_relation"
            )
            if new_relation and new_relation != current_relation:
                changes.append({"field": "Relationship", "old": current_relation, "new": new_relation})
        
        current_eid = format_field(member_row.get('National Identity')) or ""
        new_eid = st.text_input("Emirates ID", value="", placeholder=f"Current: {current_eid or 'Not provided'}", key="corr_eid")
        if new_eid and new_eid != current_eid:
            changes.append({"field": "Emirates ID", "old": current_eid or "Not provided", "new": new_eid})
    
    current_passport = format_field(member_row.get('Passport number')) or ""
    new_passport = st.text_input("Passport Number", value="", placeholder=f"Current: {current_passport or 'Not provided'}", key="corr_passport")
    if new_passport and new_passport != current_passport:
        changes.append({"field": "Passport Number", "old": current_passport or "Not provided", "new": new_passport})
    
    if changes:
        st.markdown("#### Changes Summary")
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
    
    st.markdown("#### Remarks")
    remarks = st.text_area(
        "Please provide additional details or reason for the correction (Required)",
        placeholder="e.g., 'Emirates ID was renewed' or 'Spelling correction for dependent name'",
        key="corr_remarks"
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
    
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("🚪 Sign Out", use_container_width=True):
            st.session_state.clear()
            st.rerun()
    
    days_left = (RENEWAL_DEADLINE - datetime.now()).days
    if days_left > 0:
        st.markdown(f"""
        <div class="timeout-warning">
            ⏱️ Session timeout: {SESSION_TIMEOUT_MINUTES} minutes of inactivity | 
            📅 Verification deadline: {RENEWAL_DEADLINE.strftime('%d %B %Y')} ({days_left} days remaining)
        </div>
        """, unsafe_allow_html=True)
    
    render_employee_snapshot(principal, staff_number)
    render_insurance_details(employee_data)
    render_confirmation_section(employee_data, staff_number)
    
    st.markdown("""
    <div style="text-align: center; margin-top: 40px; padding: 20px; color: #999; font-size: 12px;">
        Need assistance? <a href="https://wa.me/971564966546" target="_blank" style="color: #25D366;">Contact HR via WhatsApp</a>
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
