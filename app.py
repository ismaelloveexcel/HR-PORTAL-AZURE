#!/usr/bin/env python3
"""
HR Portal - React Application
Serves the pre-built React app through Streamlit.

Enhanced with improved navigation and efficiency features for solo HR.
"""
import streamlit as st
import streamlit.components.v1 as components
import os
import base64
import random
import string
from datetime import datetime, timedelta

st.set_page_config(
    page_title="HR Portal | Baynunah",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuration from environment variables
APP_BASE_URL = os.environ.get("APP_URL", "http://localhost:5000")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin2026")

# Portal Settings - Configurable by HR
# These can be toggled on/off based on company requirements
def get_portal_settings():
    """Get portal settings with sensible defaults for solo HR."""
    if 'portal_settings' not in st.session_state:
        st.session_state.portal_settings = {
            # WPS is OFF by default (company uses govt visa)
            "wps_enabled": False,
            "wps_exemption_reason": "Visa issued by government company",
            
            # Soft compliance - warn but don't block
            "soft_compliance_mode": True,
            
            # Features toggles
            "show_gratuity_calculator": True,
            "show_document_expiry": True,
            "show_leave_balance": True,
            
            # Notification settings
            "email_notifications": True,
            "document_expiry_alert_days": 60,
        }
    return st.session_state.portal_settings

def show_compliance_warning(message, alert_type="warning", allow_proceed=True):
    """
    Show compliance warning but allow user to proceed (soft compliance).
    This is an HR Portal, not a blocking HRIS.
    """
    if alert_type == "info":
        st.info(f"ℹ️ {message}")
    elif alert_type == "warning":
        st.warning(f"⚠️ {message}")
    elif alert_type == "alert":
        st.error(f"🔴 {message}")
        st.caption("📧 HR has been notified of this issue.")
    
    # Always allow proceed in soft compliance mode (default)
    settings = get_portal_settings()
    if settings.get("soft_compliance_mode", True):
        return True
    return allow_proceed

def generate_pass_sequence():
    """Generate a unique sequence number for passes."""
    # In production, this should query the database for the next sequence
    # For demo purposes, we generate a random suffix to ensure uniqueness
    return f"{random.randint(100, 999)}"

def get_logo_base64():
    logo_path = "attached_assets/logo_1765648544636_1766742634201.png"
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

def get_page():
    params = st.query_params
    return params.get("page", "home")

def svg_to_data_uri(svg_content):
    import urllib.parse
    return f"data:image/svg+xml,{urllib.parse.quote(svg_content)}"

SVG_USERS = svg_to_data_uri('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#2ecc71" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>')
SVG_CHECK = svg_to_data_uri('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#2ecc71" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>')
SVG_GLOBE = svg_to_data_uri('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#2ecc71" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>')
SVG_LOCK = svg_to_data_uri('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#2ecc71" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>')

def render_home():
    logo_b64 = get_logo_base64()
    logo_html = f'<img src="data:image/png;base64,{logo_b64}" class="portal-logo" alt="Logo">' if logo_b64 else ''

    html_content = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

            * {{ margin: 0; padding: 0; box-sizing: border-box; }}

            body {{
                font-family: 'Poppins', sans-serif;
                background: #ffffff;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                padding: 0;
                margin: 0;
                overflow: hidden;
                position: relative;
            }}

            .container {{
                position: relative;
                z-index: 1;
                text-align: center;
            }}

            /* Header styling */
            .portal-header {{
                text-align: center;
                margin-bottom: 25px;
            }}

            .portal-logo {{
                width: 110px;
                height: auto;
                margin-bottom: 15px;
                filter: drop-shadow(0 4px 12px rgba(0,0,0,0.1));
            }}

            .brand-title {{
                font-size: 2.3em;
                font-weight: 600;
                color: #2c3e50;
                letter-spacing: 0.5em;
                margin-bottom: 0;
                text-transform: uppercase;
                text-shadow: 0 2px 4px rgba(0,0,0,0.05);
            }}

            /* Menu container */
            .menu-container {{
                display: grid;
                grid-template-columns: repeat(2, 160px);
                gap: 12px;
                margin: 0 auto;
            }}

            /* Menu items */
            .menu-item {{
                width: 160px;
                height: 160px;
                background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(245,245,245,0.95) 100%);
                backdrop-filter: blur(12px);
                -webkit-backdrop-filter: blur(12px);
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                text-decoration: none;
                color: #2c3e50;
                border: none;
                outline: none;
                position: relative;
                transition: all 0.4s cubic-bezier(0.25, 1, 0.5, 1);
                box-shadow:
                    0 8px 16px rgba(0,0,0,0.12),
                    0 4px 8px rgba(0,0,0,0.08),
                    0 2px 4px rgba(0,0,0,0.06),
                    0 0 0 1px rgba(0,0,0,0.04);
            }}

            .menu-item:hover {{
                transform: translateY(-8px) scale(1.02);
                box-shadow:
                    0 16px 32px rgba(0,0,0,0.18),
                    0 8px 16px rgba(0,0,0,0.12),
                    0 4px 8px rgba(0,0,0,0.08),
                    0 0 0 1px rgba(0,0,0,0.06);
            }}

            .menu-item:active {{
                transform: translateY(-2px) scale(0.98);
            }}

            /* Content inside each button */
            .menu-content {{
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                gap: 10px;
            }}

            .menu-icon {{
                width: 40px;
                height: 40px;
                filter: drop-shadow(0 1px 3px rgba(46, 204, 113, 0.4));
                transition: transform 0.3s ease;
            }}

            .menu-item:hover .menu-icon {{
                transform: scale(1.15);
            }}

            .menu-label {{
                font-size: 0.95em;
                font-weight: 500;
                letter-spacing: 0.15em;
                text-transform: uppercase;
                line-height: 1.4;
                text-align: center;
                color: #34495e;
                text-shadow: 0 1px 3px rgba(255,255,255,0.8);
            }}

            /* Specific corner radiuses */
            .item-tl {{
                border-radius: 200px 10px 10px 10px;
                grid-column: 1;
                grid-row: 1;
            }}

            .item-tr {{
                border-radius: 10px 200px 10px 10px;
                grid-column: 2;
                grid-row: 1;
            }}

            .item-bl {{
                border-radius: 10px 10px 10px 200px;
                grid-column: 1;
                grid-row: 2;
            }}

            .item-br {{
                border-radius: 10px 10px 200px 10px;
                grid-column: 2;
                grid-row: 2;
            }}

            /* Footer */
            .portal-footer {{
                margin-top: 35px;
                margin-bottom: 0;
                font-size: 0.65em;
                color: #95a5a6;
                letter-spacing: 0.2em;
                text-transform: uppercase;
                font-weight: 400;
            }}

            /* Responsive design */
            @media (max-width: 768px) {{
                .portal-logo {{
                    width: 90px;
                }}

                .brand-title {{
                    font-size: 1.9em;
                }}

                .portal-header {{
                    margin-bottom: 20px;
                }}

                .menu-container {{
                    grid-template-columns: repeat(2, 145px);
                    gap: 10px;
                }}

                .menu-item {{
                    width: 145px;
                    height: 145px;
                }}

                .menu-icon {{
                    width: 35px;
                    height: 35px;
                }}

                .menu-label {{
                    font-size: 0.82em;
                }}

                .portal-footer {{
                    margin-top: 30px;
                }}
            }}

            @media (max-width: 500px) {{
                .portal-logo {{
                    width: 75px;
                    margin-bottom: 12px;
                }}

                .brand-title {{
                    font-size: 1.5em;
                    letter-spacing: 0.3em;
                }}

                .portal-header {{
                    margin-bottom: 18px;
                }}

                .menu-container {{
                    grid-template-columns: repeat(2, 135px);
                    gap: 10px;
                }}

                .menu-item {{
                    width: 135px;
                    height: 135px;
                }}

                .menu-icon {{
                    width: 32px;
                    height: 32px;
                }}

                .menu-label {{
                    font-size: 0.72em;
                    letter-spacing: 0.12em;
                }}

                .portal-footer {{
                    margin-top: 25px;
                    font-size: 0.6em;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="portal-header">
                {logo_html}
                <h1 class="brand-title">HR Portal</h1>
            </div>

            <div class="menu-container">
                <a href="?page=employees" class="menu-item item-tl">
                    <div class="menu-content">
                        <img src="{SVG_USERS}" alt="Employees" class="menu-icon">
                        <span class="menu-label">Employees</span>
                    </div>
                </a>

                <a href="?page=onboarding" class="menu-item item-tr">
                    <div class="menu-content">
                        <img src="{SVG_CHECK}" alt="Onboarding" class="menu-icon">
                        <span class="menu-label">Onboarding</span>
                    </div>
                </a>

                <a href="?page=external" class="menu-item item-bl">
                    <div class="menu-content">
                        <img src="{SVG_GLOBE}" alt="External Users" class="menu-icon">
                        <span class="menu-label">External<br>Users</span>
                    </div>
                </a>

                <a href="?page=admin" class="menu-item item-br">
                    <div class="menu-content">
                        <img src="{SVG_LOCK}" alt="Admin" class="menu-icon">
                        <span class="menu-label">Admin</span>
                    </div>
                </a>
            </div>

            <div class="portal-footer">
                Conceptualised by Baynunah|HR|IS
            </div>
        </div>
    </body>
    </html>
    '''
    components.html(html_content, height=520, scrolling=False)

def render_coming_soon(title):
    st.markdown(f'''
    <div style="min-height: 70vh; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 40px;">
        <h1 style="font-size: 2.5em; color: #2c3e50; margin-bottom: 20px;">{title}</h1>
        <p style="font-size: 1.2em; color: #7f8c8d; margin-bottom: 30px;">This section is coming soon.</p>
        <a href="?" style="background: linear-gradient(135deg, #39FF14 0%, #2ecc71 100%); color: white; padding: 12px 30px; border-radius: 25px; text-decoration: none; font-weight: 600; letter-spacing: 0.1em;">Back to Home</a>
    </div>
    ''', unsafe_allow_html=True)

def render_admin():
    if 'admin_authenticated' not in st.session_state:
        st.session_state.admin_authenticated = False

    if st.session_state.admin_authenticated:
        st.markdown('''
        <div style="padding: 40px; text-align: center;">
            <h2 style="color: #2c3e50; margin-bottom: 30px;">HR Administration</h2>
        </div>
        ''', unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🎯 Recruitment Dashboard", use_container_width=True):
                st.query_params["page"] = "recruitment_dashboard"
                st.rerun()

            if st.button("Insurance Renewal 2026", use_container_width=True):
                st.query_params["page"] = "insurance_renewal"
                st.rerun()

            st.markdown('<br>', unsafe_allow_html=True)

            if st.button("Sign Out", use_container_width=True):
                st.session_state.admin_authenticated = False
                st.rerun()
            if st.button("Back to Home", use_container_width=True):
                st.query_params.clear()
                st.rerun()
    else:
        st.markdown('''
        <div style="min-height: 70vh; display: flex; align-items: center; justify-content: center; padding: 20px;">
            <div style="width: 100%; max-width: 400px; padding: 50px 40px; background: linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 100%); border-radius: 24px; box-shadow: 0 20px 60px rgba(0,0,0,0.3);">
                <h2 style="text-align: center; color: #2c3e50; margin-bottom: 10px; font-size: 1.8em;">Admin Portal</h2>
                <p style="text-align: center; color: #7f8c8d; margin-bottom: 30px; font-size: 0.9em; letter-spacing: 0.1em; text-transform: uppercase;">Baynunah HR System</p>
            </div>
        </div>
        ''', unsafe_allow_html=True)

        col1, col2, col3 = st.columns([0.25, 0.5, 0.25])
        with col2:
            password = st.text_input("Password", type="password", key="admin_pwd", label_visibility="collapsed", placeholder="Enter Password")
            if st.button("Login", use_container_width=True):
                if password == ADMIN_PASSWORD and ADMIN_PASSWORD:
                    st.session_state.admin_authenticated = True
                    st.rerun()
                else:
                    st.error("Invalid password")

            if st.button("Back to Home", use_container_width=True, key="back_home"):
                st.query_params.clear()
                st.rerun()

def render_insurance_renewal():
    if 'admin_authenticated' not in st.session_state or not st.session_state.admin_authenticated:
        st.query_params["page"] = "admin"
        st.rerun()
        return

    st.markdown('''
    <div style="padding: 40px; text-align: center;">
        <h2 style="color: #2c3e50; margin-bottom: 30px;">Insurance Renewal 2026</h2>
    </div>
    ''', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Life Insurance", use_container_width=True):
            st.query_params["page"] = "life_insurance"
            st.rerun()
        if st.button("Medical Insurance", use_container_width=True):
            st.query_params["page"] = "medical_insurance"
            st.rerun()
        st.markdown('<br>', unsafe_allow_html=True)
        if st.button("Back to Admin", use_container_width=True):
            st.query_params["page"] = "admin"
            st.rerun()

def render_life_insurance():
    if 'admin_authenticated' not in st.session_state or not st.session_state.admin_authenticated:
        st.query_params["page"] = "admin"
        st.rerun()
        return

    render_coming_soon("Life Insurance")

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Back to Insurance Renewal", use_container_width=True):
            st.query_params["page"] = "insurance_renewal"
            st.rerun()

def render_medical_insurance():
    if 'admin_authenticated' not in st.session_state or not st.session_state.admin_authenticated:
        st.query_params["page"] = "admin"
        st.rerun()
        return

    render_coming_soon("Medical Insurance")

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Back to Insurance Renewal", use_container_width=True):
            st.query_params["page"] = "insurance_renewal"
            st.rerun()

def render_recruitment_dashboard():
    if 'admin_authenticated' not in st.session_state or not st.session_state.admin_authenticated:
        st.query_params["page"] = "admin"
        st.rerun()
        return

    st.markdown('''
    <div style="padding: 40px; text-align: center;">
        <h2 style="color: #2c3e50; margin-bottom: 10px;">Recruitment Dashboard</h2>
        <p style="color: #7f8c8d; margin-bottom: 30px;">Manage recruitment requests, candidate pool, and hiring pipeline</p>
    </div>
    ''', unsafe_allow_html=True)

    # Quick actions
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("➕ Create New RRF", use_container_width=True):
            st.success("RRF creation coming soon - use React dashboard for full functionality")

        if st.button("🎫 Generate Pass", use_container_width=True):
            st.success("Pass generation coming soon")

        if st.button("📊 View Active Positions", use_container_width=True):
            st.query_params["page"] = "recruitment_active_rrfs"
            st.rerun()

        st.markdown('<br>', unsafe_allow_html=True)

        if st.button("Back to Admin", use_container_width=True):
            st.query_params["page"] = "admin"
            st.rerun()

def render_active_rrfs():
    if 'admin_authenticated' not in st.session_state or not st.session_state.admin_authenticated:
        st.query_params["page"] = "admin"
        st.rerun()
        return

    st.markdown('''
    <div style="padding: 40px;">
        <h2 style="color: #2c3e50; margin-bottom: 30px;">Active Recruitment Requests</h2>
    </div>
    ''', unsafe_allow_html=True)

    # Display info about the 2 positions
    st.info("🎯 **Ready to add the 2 job positions:**\n\n1. Electronics Engineer - Baynunah Watergeneration Technologies\n2. Thermodynamics Engineer - Baynunah Watergeneration Technologies")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### Electronics Engineer
        **Department:** Engineering / R&D
        **Location:** Abu Dhabi
        **Urgency:** High
        **Salary:** 15,000 - 25,000 AED

        **Key Responsibilities:**
        - Design and maintain control electronics for AWG products
        - Develop embedded firmware and control logic
        - Lead testing, validation, and troubleshooting
        """)

    with col2:
        st.markdown("""
        ### Thermodynamics Engineer
        **Department:** Engineering / R&D
        **Location:** Abu Dhabi
        **Urgency:** High
        **Salary:** 15,000 - 25,000 AED

        **Key Responsibilities:**
        - Model and optimize refrigeration cycles
        - Execute lab testing and validation
        - Produce technical documentation
        """)

    st.markdown('<br>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Back to Recruitment Dashboard", use_container_width=True):
            st.query_params["page"] = "recruitment_dashboard"
            st.rerun()

def render_sidebar():
    """
    Render sidebar navigation for quick access.
    Improves efficiency for solo HR by reducing clicks.
    """
    with st.sidebar:
        # Logo and title
        logo_b64 = get_logo_base64()
        if logo_b64:
            st.markdown(f'''
            <div style="text-align: center; padding: 10px 0 20px 0;">
                <img src="data:image/png;base64,{logo_b64}" style="width: 60px; height: auto;" alt="Baynunah">
            </div>
            ''', unsafe_allow_html=True)
        
        st.markdown("### ⚡ Quick Navigation")
        
        # Main navigation buttons with icons
        if st.button("🏠 Home", use_container_width=True, key="nav_home"):
            st.query_params.clear()
            st.rerun()
        
        if st.button("🎯 Recruitment", use_container_width=True, key="nav_recruitment"):
            if st.session_state.get('admin_authenticated'):
                st.query_params["page"] = "recruitment_dashboard"
            else:
                st.query_params["page"] = "admin"
            st.rerun()
        
        if st.button("📋 Active RRFs", use_container_width=True, key="nav_rrfs"):
            if st.session_state.get('admin_authenticated'):
                st.query_params["page"] = "recruitment_active_rrfs"
            else:
                st.query_params["page"] = "admin"
            st.rerun()
        
        if st.button("🎫 Pass Generation", use_container_width=True, key="nav_passes"):
            if st.session_state.get('admin_authenticated'):
                st.query_params["page"] = "pass_generation"
            else:
                st.query_params["page"] = "admin"
            st.rerun()
        
        # UAE Compliance Section
        if st.button("🇦🇪 UAE Compliance", use_container_width=True, key="nav_compliance"):
            if st.session_state.get('admin_authenticated'):
                st.query_params["page"] = "uae_compliance"
            else:
                st.query_params["page"] = "admin"
            st.rerun()
        
        if st.button("💰 Gratuity Calculator", use_container_width=True, key="nav_gratuity"):
            if st.session_state.get('admin_authenticated'):
                st.query_params["page"] = "gratuity_calculator"
            else:
                st.query_params["page"] = "admin"
            st.rerun()
        
        st.divider()
        
        # Quick Stats Section
        st.markdown("### 📊 Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Open RRFs", "2", help="Active recruitment requests")
        with col2:
            st.metric("Pending", "0", help="Submissions awaiting review")
        
        # UAE Compliance Stats
        st.markdown("### 🇦🇪 Compliance")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🔴 Expiring", "2", delta="-3 from last month", delta_color="inverse", 
                     help="Documents expiring in 30 days")
        with col2:
            st.metric("🟢 Valid", "45", help="All documents valid")
        
        st.divider()
        
        # Quick Actions
        st.markdown("### 🚀 Quick Actions")
        
        if st.button("➕ Create RRF", use_container_width=True, key="quick_create_rrf", type="primary"):
            if st.session_state.get('admin_authenticated'):
                st.query_params["page"] = "create_rrf"
            else:
                st.query_params["page"] = "admin"
            st.rerun()
        
        if st.button("🎫 New Pass", use_container_width=True, key="quick_new_pass"):
            if st.session_state.get('admin_authenticated'):
                st.query_params["page"] = "pass_generation"
            else:
                st.query_params["page"] = "admin"
            st.rerun()
        
        # Portal Settings
        if st.button("⚙️ Portal Settings", use_container_width=True, key="quick_settings"):
            if st.session_state.get('admin_authenticated'):
                st.query_params["page"] = "portal_settings"
            else:
                st.query_params["page"] = "admin"
            st.rerun()
        
        st.divider()
        
        # Help Section
        with st.expander("❓ Need Help?"):
            st.markdown("""
            **This is an HR Portal, not HRIS**
            - Streamlines HR processes
            - Provides UAE Labor Law guidance
            - Warns but doesn't block actions
            
            **UAE Labor Law Resources:**
            - Federal Decree-Law No. 33 of 2021 (New Labor Law)
            - Federal Law No. 8 of 1980 (Gratuity calculations)
            - MOHRE Guidelines
            
            **Support:**
            Contact IT Support for technical issues.
            """)
        
        # Footer with version
        st.markdown('''
        <div style="position: fixed; bottom: 10px; left: 10px; font-size: 0.7em; color: #95a5a6;">
            HR Portal v1.2.0 🇦🇪
        </div>
        ''', unsafe_allow_html=True)

def render_portal_settings():
    """Portal settings page for HR to configure features."""
    if 'admin_authenticated' not in st.session_state or not st.session_state.admin_authenticated:
        st.query_params["page"] = "admin"
        st.rerun()
        return
    
    st.markdown('''
    <div style="padding: 20px 0;">
        <h2 style="color: #2c3e50; margin-bottom: 10px;">⚙️ Portal Settings</h2>
        <p style="color: #7f8c8d;">Configure portal features to match your company's needs.</p>
    </div>
    ''', unsafe_allow_html=True)
    
    settings = get_portal_settings()
    
    # WPS Settings
    st.markdown("### 💳 WPS (Wage Protection System)")
    
    wps_enabled = st.toggle(
        "Enable WPS Module",
        value=settings.get("wps_enabled", False),
        help="Disable if your company is exempt from WPS (e.g., government-linked, certain free zones)"
    )
    
    if not wps_enabled:
        st.info("""
        ℹ️ **WPS Module Disabled**
        
        This is appropriate if:
        - Your visas are issued by a government company
        - You're in a free zone with WPS exemption
        - You have special arrangements with MOHRE
        
        Salaries can still be processed through your normal banking channels.
        """)
        
        exemption_reason = st.text_input(
            "Exemption Reason (for records)",
            value=settings.get("wps_exemption_reason", ""),
            placeholder="e.g., Visa issued by government company"
        )
        settings["wps_exemption_reason"] = exemption_reason
    
    settings["wps_enabled"] = wps_enabled
    
    st.markdown("---")
    
    # Compliance Mode
    st.markdown("### 🔔 Compliance Behavior")
    
    soft_mode = st.toggle(
        "Soft Compliance Mode (Recommended)",
        value=settings.get("soft_compliance_mode", True),
        help="When enabled, compliance issues show warnings but don't block actions"
    )
    
    if soft_mode:
        st.success("""
        ✅ **Soft Compliance Mode Active**
        
        - Compliance issues will show warnings
        - Users can still proceed with actions
        - HR is notified of potential issues
        - This is an HR Portal, not a blocking HRIS
        """)
    else:
        st.warning("""
        ⚠️ **Strict Compliance Mode**
        
        Some actions may be blocked if compliance requirements aren't met.
        Only recommended for highly regulated environments.
        """)
    
    settings["soft_compliance_mode"] = soft_mode
    
    st.markdown("---")
    
    # Document Expiry Alerts
    st.markdown("### 📅 Document Expiry Alerts")
    
    alert_days = st.slider(
        "Alert before expiry (days)",
        min_value=30,
        max_value=90,
        value=settings.get("document_expiry_alert_days", 60),
        help="How many days before expiry to start showing alerts"
    )
    settings["document_expiry_alert_days"] = alert_days
    
    st.markdown("---")
    
    # Feature Toggles
    st.markdown("### 🎛️ Feature Toggles")
    
    col1, col2 = st.columns(2)
    
    with col1:
        settings["show_gratuity_calculator"] = st.checkbox(
            "💰 Gratuity Calculator",
            value=settings.get("show_gratuity_calculator", True)
        )
        settings["show_document_expiry"] = st.checkbox(
            "📋 Document Expiry Dashboard",
            value=settings.get("show_document_expiry", True)
        )
    
    with col2:
        settings["show_leave_balance"] = st.checkbox(
            "🏖️ Leave Balance Tracking",
            value=settings.get("show_leave_balance", True)
        )
        settings["email_notifications"] = st.checkbox(
            "📧 Email Notifications",
            value=settings.get("email_notifications", True)
        )
    
    # Save settings
    st.session_state.portal_settings = settings
    
    st.markdown("---")
    
    st.success("✅ Settings are automatically saved")
    
    st.markdown('<br>', unsafe_allow_html=True)
    if st.button("← Back to Dashboard", use_container_width=False, key="settings_back"):
        st.query_params["page"] = "recruitment_dashboard"
        st.rerun()

def render_pass_generation():
    """Render pass generation page with improved UX."""
    if 'admin_authenticated' not in st.session_state or not st.session_state.admin_authenticated:
        st.query_params["page"] = "admin"
        st.rerun()
        return
    
    st.markdown('''
    <div style="padding: 20px 0;">
        <h2 style="color: #2c3e50; margin-bottom: 10px;">🎫 Pass Generation</h2>
        <p style="color: #7f8c8d;">Generate secure access passes for managers, candidates, and employees.</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Pass type selection
    pass_type = st.selectbox(
        "Select Pass Type",
        ["Hiring Manager Pass", "Candidate Pass", "Employee Pass", "Manager Pass (3-in-1)"],
        help="Choose the type of pass to generate"
    )
    
    st.markdown("---")
    
    if pass_type == "Hiring Manager Pass":
        st.markdown("### 👔 Hiring Manager Pass")
        st.info("This pass allows hiring managers to review candidates and conduct interviews for specific positions.")
        
        col1, col2 = st.columns(2)
        with col1:
            manager_name = st.text_input("Manager Name *", placeholder="Enter full name")
            manager_email = st.text_input("Manager Email *", placeholder="name@company.com")
        with col2:
            manager_phone = st.text_input("Phone Number", placeholder="+971 XX XXX XXXX")
            department = st.text_input("Department", placeholder="e.g., Engineering")
        
        rrf_select = st.selectbox(
            "Select RRF / Position *",
            ["RRF-BWT-12-001 - Electronics Engineer", "RRF-BWT-12-002 - Thermodynamics Engineer"],
            help="Select the recruitment request this pass is for"
        )
        
        if st.button("Generate Hiring Manager Pass", type="primary", use_container_width=True):
            if manager_name and manager_email:
                pass_seq = generate_pass_sequence()
                pass_id = f"HM-{datetime.now().year}-{pass_seq}"
                st.success("✅ Pass generated successfully!")
                st.markdown(f"""
                **Pass ID:** {pass_id}
                
                **Access URL:** `{APP_BASE_URL}/pass/{pass_id}`
                
                **Expires:** {(datetime.now() + timedelta(days=90)).strftime('%B %d, %Y')}
                """)
                st.balloons()
            else:
                st.error("Please fill in all required fields")
    
    elif pass_type == "Candidate Pass":
        st.markdown("### 👤 Candidate Pass")
        st.info("This pass allows candidates to track their application status and upload documents.")
        
        col1, col2 = st.columns(2)
        with col1:
            candidate_name = st.text_input("Candidate Name *", placeholder="Enter full name")
            candidate_email = st.text_input("Candidate Email *", placeholder="name@email.com")
        with col2:
            candidate_phone = st.text_input("Phone Number", placeholder="+971 XX XXX XXXX")
            position = st.selectbox("Position Applied For *", 
                ["Electronics Engineer", "Thermodynamics Engineer"])
        
        if st.button("Generate Candidate Pass", type="primary", use_container_width=True):
            if candidate_name and candidate_email:
                pass_seq = generate_pass_sequence()
                pass_id = f"CAND-{datetime.now().year}-{pass_seq}"
                st.success("✅ Candidate pass generated!")
                st.markdown(f"""
                **Pass ID:** {pass_id}
                
                **Access URL:** `{APP_BASE_URL}/pass/{pass_id}`
                
                **Expires:** {(datetime.now() + timedelta(days=60)).strftime('%B %d, %Y')}
                """)
            else:
                st.error("Please fill in all required fields")
    
    elif pass_type == "Employee Pass":
        st.markdown("### 🏢 Employee Pass")
        st.info("Standard employee self-service pass for attendance, leave, and payslip access.")
        
        col1, col2 = st.columns(2)
        with col1:
            emp_id = st.text_input("Employee ID *", placeholder="e.g., EMP-2025-001")
            emp_name = st.text_input("Full Name *", placeholder="Enter full name")
            emp_email = st.text_input("Email *", placeholder="name@baynunah.ae")
        with col2:
            emp_phone = st.text_input("Phone", placeholder="+971 XX XXX XXXX")
            emp_dept = st.text_input("Department", placeholder="e.g., Engineering")
            emp_title = st.text_input("Job Title", placeholder="e.g., Senior Engineer")
        
        line_manager = st.text_input("Line Manager", placeholder="Manager name")
        
        if st.button("Generate Employee Pass", type="primary", use_container_width=True):
            if emp_id and emp_name and emp_email:
                st.success("✅ Employee pass generated!")
                st.markdown(f"""
                **Pass ID:** {emp_id}
                
                **Access URL:** `{APP_BASE_URL}/pass/{emp_id}`
                
                **Expires:** Never (Employee passes are permanent)
                """)
            else:
                st.error("Please fill in all required fields")
    
    else:  # Manager Pass (3-in-1)
        st.markdown("### 👑 Manager Pass (3-in-1)")
        st.info("Combined pass with Personal + Team Management + Recruitment capabilities.")
        
        col1, col2 = st.columns(2)
        with col1:
            mgr_id = st.text_input("Employee ID *", placeholder="e.g., EMP-2025-001")
            mgr_name = st.text_input("Full Name *", placeholder="Enter full name")
            mgr_email = st.text_input("Email *", placeholder="name@baynunah.ae")
        with col2:
            mgr_phone = st.text_input("Phone", placeholder="+971 XX XXX XXXX")
            mgr_dept = st.text_input("Department", placeholder="e.g., Engineering")
            mgr_title = st.text_input("Job Title", placeholder="e.g., Engineering Manager")
        
        team_size = st.number_input("Team Size", min_value=0, max_value=100, value=5)
        
        if st.button("Generate Manager Pass", type="primary", use_container_width=True):
            if mgr_id and mgr_name and mgr_email:
                pass_id = f"MGR-{mgr_id}"
                st.success("✅ Manager 3-in-1 pass generated!")
                st.markdown(f"""
                **Pass ID:** {pass_id}
                
                **Access URL:** `{APP_BASE_URL}/pass/{pass_id}`
                
                **Expires:** Never (Manager passes are permanent)
                
                **Enabled Modules:**
                - ✅ Personal: Attendance, Leave, Payslip
                - ✅ Team: Approve Leave, View Attendance, Performance
                - ✅ Recruitment: Review Candidates, Interviews, Decisions
                """)
            else:
                st.error("Please fill in all required fields")
    
    st.markdown('<br>', unsafe_allow_html=True)
    if st.button("← Back to Dashboard", use_container_width=False):
        st.query_params["page"] = "recruitment_dashboard"
        st.rerun()

def main():
    page = get_page()
    
    # Render sidebar for authenticated users or on admin pages
    if page not in ["home"] or st.session_state.get('admin_authenticated'):
        render_sidebar()

    if page == "home":
        render_home()
    elif page == "employees":
        render_coming_soon("Employees")
    elif page == "onboarding":
        render_coming_soon("Onboarding")
    elif page == "external":
        render_coming_soon("External Users")
    elif page == "admin":
        render_admin()
    elif page == "recruitment_dashboard":
        render_recruitment_dashboard()
    elif page == "recruitment_active_rrfs":
        render_active_rrfs()
    elif page == "pass_generation":
        render_pass_generation()
    elif page == "portal_settings":
        render_portal_settings()
    elif page == "uae_compliance":
        render_uae_compliance()
    elif page == "gratuity_calculator":
        render_gratuity_calculator()
    elif page == "insurance_renewal":
        render_insurance_renewal()
    elif page == "life_insurance":
        render_life_insurance()
    elif page == "medical_insurance":
        render_medical_insurance()
    else:
        render_home()

def render_uae_compliance():
    """UAE Compliance Dashboard - Document expiry tracking and compliance status."""
    if 'admin_authenticated' not in st.session_state or not st.session_state.admin_authenticated:
        st.query_params["page"] = "admin"
        st.rerun()
        return
    
    settings = get_portal_settings()
    
    st.markdown('''
    <div style="padding: 20px 0;">
        <h2 style="color: #2c3e50; margin-bottom: 10px;">🇦🇪 UAE Compliance Dashboard</h2>
        <p style="color: #7f8c8d;">Track document expirations and ensure UAE Labor Law alignment.</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Show portal mode reminder
    if settings.get("soft_compliance_mode", True):
        st.info("ℹ️ **Soft Compliance Mode:** Issues shown as warnings only. Actions are not blocked.")
    
    # Document Expiry Overview
    st.markdown("### 📋 Document Expiry Status")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🔴 Expired",
            value="0",
            help="Documents already expired - URGENT"
        )
    
    with col2:
        st.metric(
            label="🟠 <30 Days",
            value="2",
            delta="-1",
            delta_color="inverse",
            help="Expiring within 30 days"
        )
    
    with col3:
        st.metric(
            label="🟡 <60 Days",
            value="5",
            help="Expiring within 60 days"
        )
    
    with col4:
        st.metric(
            label="🟢 Valid",
            value="45",
            help="Valid for 60+ days"
        )
    
    st.markdown("---")
    
    # Document Types Breakdown
    st.markdown("### 📄 Documents by Type")
    
    documents = [
        {"type": "Emirates ID", "icon": "🪪", "expiring_30": 1, "expiring_60": 2, "valid": 44},
        {"type": "UAE Visa", "icon": "📋", "expiring_30": 1, "expiring_60": 1, "valid": 45},
        {"type": "Labor Card", "icon": "💼", "expiring_30": 0, "expiring_60": 1, "valid": 46},
        {"type": "Medical Fitness", "icon": "🏥", "expiring_30": 0, "expiring_60": 1, "valid": 46},
        {"type": "Passport", "icon": "📕", "expiring_30": 0, "expiring_60": 0, "valid": 47},
    ]
    
    for doc in documents:
        col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 2])
        with col1:
            st.write(f"{doc['icon']} **{doc['type']}**")
        with col2:
            if doc['expiring_30'] > 0:
                st.error(f"🔴 {doc['expiring_30']}")
            else:
                st.write("✅ 0")
        with col3:
            if doc['expiring_60'] > 0:
                st.warning(f"🟠 {doc['expiring_60']}")
            else:
                st.write("✅ 0")
        with col4:
            st.success(f"🟢 {doc['valid']}")
        with col5:
            progress = doc['valid'] / (doc['valid'] + doc['expiring_30'] + doc['expiring_60'])
            st.progress(progress)
    
    st.markdown("---")
    
    # UAE Public Holidays 2026
    st.markdown("### 🗓️ UAE Public Holidays 2026")
    
    holidays = [
        {"name": "New Year's Day", "date": "Jan 1", "days": 1},
        {"name": "Eid Al Fitr (Expected)", "date": "Mar 20-23", "days": 4},
        {"name": "Eid Al Adha (Expected)", "date": "May 27-30", "days": 4},
        {"name": "Islamic New Year", "date": "Jun 17", "days": 1},
        {"name": "Prophet's Birthday", "date": "Aug 26", "days": 1},
        {"name": "Commemoration Day", "date": "Nov 30", "days": 1},
        {"name": "UAE National Day", "date": "Dec 2-3", "days": 2},
    ]
    
    for holiday in holidays:
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            st.write(f"🎉 **{holiday['name']}**")
        with col2:
            st.write(f"📅 {holiday['date']}")
        with col3:
            st.write(f"{holiday['days']} day(s)")
    
    st.markdown("---")
    
    # UAE Leave Types Reference
    st.markdown("### 📚 UAE Leave Types (Labor Law Reference)")
    
    leave_types = [
        {"type": "Annual Leave", "days": 30, "article": "Article 29", "condition": "After 1 year of service"},
        {"type": "Sick Leave", "days": 90, "article": "Article 31", "condition": "15 full + 30 half + 45 unpaid"},
        {"type": "Maternity Leave", "days": 60, "article": "Article 30", "condition": "45 full pay + 15 half pay"},
        {"type": "Paternity Leave", "days": 5, "article": "Law No. 6/2020", "condition": "Within 1 month of birth"},
        {"type": "Hajj Leave", "days": 30, "article": "Custom", "condition": "Once during employment"},
        {"type": "Compassionate", "days": 5, "article": "Article 32", "condition": "Death of close relative"},
    ]
    
    for leave in leave_types:
        with st.expander(f"📅 {leave['type']} - {leave['days']} days"):
            st.markdown(f"""
            - **Legal Reference:** {leave['article']}
            - **Entitlement:** {leave['days']} days
            - **Conditions:** {leave['condition']}
            """)
    
    st.markdown('<br>', unsafe_allow_html=True)
    if st.button("← Back to Dashboard", use_container_width=False, key="compliance_back"):
        st.query_params["page"] = "recruitment_dashboard"
        st.rerun()

def calculate_uae_gratuity(basic_salary: float, years_of_service: float) -> dict:
    """
    Calculate UAE End of Service Gratuity per Federal Law No. 8 of 1980.
    
    Rules:
    - First 5 years: 21 days basic salary per year
    - After 5 years: 30 days basic salary per year
    - Maximum: 2 years' total salary
    """
    if years_of_service < 1:
        return {"total": 0, "first_tier": 0, "second_tier": 0, "daily_rate": 0}
    
    daily_rate = basic_salary / 30
    
    # First 5 years: 21 days per year
    years_first_tier = min(years_of_service, 5)
    gratuity_first = years_first_tier * 21 * daily_rate
    
    # After 5 years: 30 days per year
    years_second_tier = max(0, years_of_service - 5)
    gratuity_second = years_second_tier * 30 * daily_rate
    
    total_gratuity = gratuity_first + gratuity_second
    
    # Cap at 2 years' salary
    max_gratuity = basic_salary * 24
    final_gratuity = min(total_gratuity, max_gratuity)
    
    return {
        "total": final_gratuity,
        "first_tier": gratuity_first,
        "second_tier": gratuity_second,
        "daily_rate": daily_rate,
        "years_first_tier": years_first_tier,
        "years_second_tier": years_second_tier,
        "capped": total_gratuity > max_gratuity
    }

def render_gratuity_calculator():
    """UAE End of Service Gratuity Calculator per Federal Law No. 8 of 1980."""
    if 'admin_authenticated' not in st.session_state or not st.session_state.admin_authenticated:
        st.query_params["page"] = "admin"
        st.rerun()
        return
    
    st.markdown('''
    <div style="padding: 20px 0;">
        <h2 style="color: #2c3e50; margin-bottom: 10px;">💰 End of Service Gratuity Calculator</h2>
        <p style="color: #7f8c8d;">Calculate gratuity per UAE Federal Law No. 8 of 1980 (as amended).</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Legal Reference
    st.info("""
    **📚 UAE Gratuity Rules (Federal Law No. 8 of 1980):**
    - **First 5 years:** 21 days of basic salary per year
    - **After 5 years:** 30 days of basic salary per year  
    - **Maximum:** Total gratuity cannot exceed 2 years' salary
    - **Minimum tenure:** 1 year required for eligibility
    """)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        basic_salary = st.number_input(
            "Basic Salary (AED/month) *", 
            min_value=0, 
            max_value=500000,
            value=10000,
            step=500,
            help="Enter monthly basic salary (excluding allowances)"
        )
        
        years = st.number_input(
            "Years of Service *", 
            min_value=0.0, 
            max_value=50.0, 
            value=5.0, 
            step=0.5,
            help="Enter total years worked"
        )
    
    with col2:
        contract_type = st.selectbox(
            "Contract Type",
            ["Limited (Fixed Term)", "Unlimited"],
            help="Type of employment contract (affects resignation rules)"
        )
        
        termination = st.selectbox(
            "Termination By",
            ["Employer", "Employee (Resigned)"],
            help="Who initiated the termination (may affect pro-rata calculation)"
        )
    
    st.markdown("---")
    
    # Note about contract type and termination
    if termination == "Employee (Resigned)" and years < 5:
        st.warning("""
        ⚠️ **Note:** If employee resigns before completing 5 years, gratuity may be pro-rated:
        - 1-3 years: 1/3 of gratuity
        - 3-5 years: 2/3 of gratuity
        - 5+ years: Full gratuity
        
        The calculation below shows the full entitlement. Consult HR for the final amount.
        """)
    
    if st.button("Calculate Gratuity", type="primary", use_container_width=True):
        if basic_salary > 0 and years >= 1:
            result = calculate_uae_gratuity(basic_salary, years)
            
            st.success(f"### 💵 Estimated Gratuity: **AED {result['total']:,.2f}**")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Daily Rate", f"AED {result['daily_rate']:,.2f}")
            
            with col2:
                st.metric("First 5 Years", f"AED {result['first_tier']:,.2f}")
            
            with col3:
                st.metric("After 5 Years", f"AED {result['second_tier']:,.2f}")
            
            if result['capped']:
                st.warning("⚠️ Gratuity has been capped at 2 years' salary as per UAE law.")
            
            st.markdown("---")
            st.markdown("#### 📊 Calculation Breakdown")
            st.markdown(f"""
            | Component | Calculation | Amount |
            |-----------|-------------|--------|
            | Daily Rate | AED {basic_salary:,.0f} ÷ 30 days | AED {result['daily_rate']:,.2f} |
            | First Tier | {result['years_first_tier']:.1f} years × 21 days × AED {result['daily_rate']:,.2f} | AED {result['first_tier']:,.2f} |
            | Second Tier | {result['years_second_tier']:.1f} years × 30 days × AED {result['daily_rate']:,.2f} | AED {result['second_tier']:,.2f} |
            | **Total** | | **AED {result['total']:,.2f}** |
            """)
            
        elif years < 1:
            st.error("❌ Employee must complete at least 1 year of service to be eligible for gratuity.")
        else:
            st.error("❌ Please enter a valid basic salary.")
    
    st.markdown("---")
    
    # Quick Reference Table
    with st.expander("📋 Quick Gratuity Reference Table"):
        st.markdown("""
        | Years of Service | Gratuity Formula |
        |-----------------|------------------|
        | < 1 year | Not eligible |
        | 1-5 years | 21 days × years × (basic salary ÷ 30) |
        | 5+ years | (21 × 5) + (30 × remaining years) × daily rate |
        | Maximum | 24 months' basic salary |
        """)
    
    st.markdown('<br>', unsafe_allow_html=True)
    if st.button("← Back to Dashboard", use_container_width=False, key="gratuity_back"):
        st.query_params["page"] = "recruitment_dashboard"
        st.rerun()

if __name__ == "__main__":
    main()
