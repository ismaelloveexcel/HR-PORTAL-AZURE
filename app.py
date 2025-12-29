import streamlit as st
import streamlit.components.v1 as components
import os
import base64

st.set_page_config(
    page_title="HR Portal | Baynunah",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def get_logo_base64():
    logo_path = "attached_assets/logo_1765648544636_1766742634201.png"
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

def get_page():
    params = st.query_params
    return params.get("page", "home")

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "")

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display: none;}

.stApp {
    font-family: 'Poppins', sans-serif;
    background: #e8e8e8;
}

[data-testid="stAppViewBlockContainer"] {
    padding-top: 1rem !important;
    max-width: 100% !important;
}

.portal-container {
    min-height: 90vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 20px;
}

.portal-header {
    text-align: center;
    margin-bottom: 30px;
}

.portal-logo {
    width: 120px;
    margin-bottom: 10px;
}

.portal-title {
    font-size: 1.8em;
    font-weight: 600;
    color: #333;
    margin: 0;
    letter-spacing: 0.05em;
}

.menu-grid {
    display: grid;
    grid-template-columns: repeat(2, 130px);
    gap: 8px;
    margin: 20px auto;
}

.menu-item {
    width: 130px;
    height: 130px;
    background: #e8e8e8;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-decoration: none;
    color: #333;
    font-weight: 500;
    font-size: 0.85em;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    transition: all 0.3s ease;
    box-shadow: 
        6px 6px 12px rgba(0,0,0,0.15),
        -6px -6px 12px rgba(255,255,255,0.8),
        inset 2px 5px 10px rgba(0,0,0,0.1);
}

.menu-item:hover {
    letter-spacing: 0.5em;
    transform: translateY(-8px);
    background: #171717;
    color: white;
}

.menu-item:hover img {
    filter: brightness(0) invert(1);
}

.menu-item img {
    width: 36px;
    height: 36px;
    margin-bottom: 10px;
}

.item-tl { border-radius: 60px 12px 12px 12px; }
.item-tr { border-radius: 12px 60px 12px 12px; }
.item-bl { border-radius: 12px 12px 12px 60px; }
.item-br { border-radius: 12px 12px 60px 12px; }

.portal-footer {
    margin-top: 30px;
    text-align: center;
    font-size: 0.75em;
    color: #666;
    letter-spacing: 0.1em;
}

.page-container {
    min-height: 80vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px 20px;
    text-align: center;
}

.page-title {
    font-size: 2em;
    font-weight: 600;
    color: #333;
    margin-bottom: 20px;
}

.page-message {
    font-size: 1.1em;
    color: #666;
    margin-bottom: 30px;
}

.back-btn {
    display: inline-block;
    background: #e8e8e8;
    color: #333;
    padding: 12px 30px;
    border-radius: 30px;
    text-decoration: none;
    font-weight: 500;
    box-shadow: 
        4px 4px 8px rgba(0,0,0,0.15),
        -4px -4px 8px rgba(255,255,255,0.8);
    transition: all 0.3s ease;
}

.back-btn:hover {
    background: #171717;
    color: white;
}

.admin-card {
    background: #e8e8e8;
    padding: 40px;
    border-radius: 20px;
    max-width: 400px;
    margin: 0 auto;
    box-shadow: 
        8px 8px 16px rgba(0,0,0,0.15),
        -8px -8px 16px rgba(255,255,255,0.8);
}

.admin-title {
    font-size: 1.5em;
    font-weight: 600;
    color: #333;
    margin-bottom: 20px;
    text-align: center;
}

.contact-info {
    background: #f5f5f5;
    padding: 20px;
    border-radius: 12px;
    margin: 20px 0;
}

.contact-item {
    margin: 10px 0;
    font-size: 0.95em;
}

@media (max-width: 600px) {
    .menu-grid {
        grid-template-columns: repeat(2, 110px);
    }
    .menu-item {
        width: 110px;
        height: 110px;
        font-size: 0.7em;
    }
    .portal-title {
        font-size: 1.4em;
    }
}
</style>
"""

def svg_to_data_uri(svg_content):
    import urllib.parse
    return f"data:image/svg+xml,{urllib.parse.quote(svg_content)}"

SVG_USERS = svg_to_data_uri('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#39FF14" stroke-width="1.5"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>')
SVG_CHECK = svg_to_data_uri('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#39FF14" stroke-width="1.5"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>')
SVG_GLOBE = svg_to_data_uri('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#39FF14" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>')
SVG_LOCK = svg_to_data_uri('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#39FF14" stroke-width="1.5"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>')

def render_home():
    logo_b64 = get_logo_base64()
    logo_html = f'<img src="data:image/png;base64,{logo_b64}" class="portal-logo">' if logo_b64 else ''
    
    html_content = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ 
                font-family: 'Poppins', sans-serif; 
                background: #e8e8e8;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }}
            .portal-header {{ text-align: center; margin-bottom: 30px; }}
            .portal-logo {{ width: 120px; margin-bottom: 10px; }}
            .portal-title {{ font-size: 1.8em; font-weight: 600; color: #333; letter-spacing: 0.05em; }}
            .menu-grid {{ display: grid; grid-template-columns: repeat(2, 130px); gap: 8px; margin: 20px auto; }}
            .menu-item {{
                width: 130px; height: 130px; background: #e8e8e8;
                display: flex; flex-direction: column; align-items: center; justify-content: center;
                text-decoration: none; color: #333; font-weight: 500; font-size: 0.85em;
                letter-spacing: 0.2em; text-transform: uppercase; transition: all 0.3s ease;
                box-shadow: 6px 6px 12px rgba(0,0,0,0.15), -6px -6px 12px rgba(255,255,255,0.8), inset 2px 5px 10px rgba(0,0,0,0.1);
            }}
            .menu-item:hover {{ letter-spacing: 0.5em; transform: translateY(-8px); background: #171717; color: white; }}
            .menu-item:hover img {{ filter: brightness(0) invert(1); }}
            .menu-item img {{ width: 36px; height: 36px; margin-bottom: 10px; }}
            .item-tl {{ border-radius: 60px 12px 12px 12px; }}
            .item-tr {{ border-radius: 12px 60px 12px 12px; }}
            .item-bl {{ border-radius: 12px 12px 12px 60px; }}
            .item-br {{ border-radius: 12px 12px 60px 12px; }}
            .portal-footer {{ margin-top: 30px; text-align: center; font-size: 0.75em; color: #666; letter-spacing: 0.1em; }}
            @media (max-width: 600px) {{
                .menu-grid {{ grid-template-columns: repeat(2, 110px); }}
                .menu-item {{ width: 110px; height: 110px; font-size: 0.7em; }}
                .portal-title {{ font-size: 1.4em; }}
            }}
        </style>
    </head>
    <body>
        <div class="portal-header">
            {logo_html}
            <h1 class="portal-title">HR PORTAL</h1>
        </div>
        <div class="menu-grid">
            <a href="?page=employees" class="menu-item item-tl">
                <img src="{SVG_USERS}" alt="Employees">
                <span>Employees</span>
            </a>
            <a href="?page=onboarding" class="menu-item item-tr">
                <img src="{SVG_CHECK}" alt="Onboarding">
                <span>Onboarding</span>
            </a>
            <a href="?page=external" class="menu-item item-bl">
                <img src="{SVG_GLOBE}" alt="External">
                <span>External</span>
            </a>
            <a href="?page=admin" class="menu-item item-br">
                <img src="{SVG_LOCK}" alt="Admin">
                <span>Admin</span>
            </a>
        </div>
        <div class="portal-footer">Conceptualised by Baynunah|HR|IS</div>
    </body>
    </html>
    '''
    components.html(html_content, height=700, scrolling=False)

def render_coming_soon(title):
    st.markdown(CSS, unsafe_allow_html=True)
    st.markdown(f'''
    <div class="page-container">
        <h1 class="page-title">{title}</h1>
        <p class="page-message">This section is coming soon.</p>
        <a href="?" class="back-btn">Back to Home</a>
    </div>
    ''', unsafe_allow_html=True)

def render_admin():
    st.markdown(CSS, unsafe_allow_html=True)
    
    if 'admin_authenticated' not in st.session_state:
        st.session_state.admin_authenticated = False
    
    if st.session_state.admin_authenticated:
        st.markdown('''
        <style>
            .admin-menu { display: flex; flex-direction: column; gap: 15px; margin-top: 20px; }
            .admin-menu-item {
                background: #e8e8e8; padding: 20px 30px; border-radius: 12px;
                text-decoration: none; color: #333; font-weight: 500; text-align: center;
                box-shadow: 4px 4px 8px rgba(0,0,0,0.15), -4px -4px 8px rgba(255,255,255,0.8);
                transition: all 0.3s ease;
            }
            .admin-menu-item:hover { background: #171717; color: white; transform: translateY(-3px); }
            .section-title { color: #39FF14; font-size: 0.85em; letter-spacing: 0.1em; margin-bottom: 5px; }
        </style>
        <div class="page-container">
            <div class="admin-card" style="max-width: 450px;">
                <h2 class="admin-title">HR Administration</h2>
                <div class="admin-menu">
                    <a href="?page=insurance_renewal" class="admin-menu-item">
                        <div class="section-title">FOLDER</div>
                        Insurance Renewal 2026
                    </a>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Sign Out", use_container_width=True):
                st.session_state.admin_authenticated = False
                st.rerun()
            if st.button("Back to Home", use_container_width=True):
                st.query_params.clear()
                st.rerun()
    else:
        st.markdown('''
        <div class="page-container">
            <div class="admin-card">
                <h2 class="admin-title">Admin Access</h2>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            password = st.text_input("Enter Password", type="password", key="admin_pwd")
            if st.button("Login", use_container_width=True):
                if password == ADMIN_PASSWORD and ADMIN_PASSWORD:
                    st.session_state.admin_authenticated = True
                    st.rerun()
                else:
                    st.error("Invalid password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Back to Home", use_container_width=True, key="back_home"):
                st.query_params.clear()
                st.rerun()

def render_insurance_renewal():
    st.markdown(CSS, unsafe_allow_html=True)
    
    if 'admin_authenticated' not in st.session_state or not st.session_state.admin_authenticated:
        st.query_params["page"] = "admin"
        st.rerun()
        return
    
    st.markdown('''
    <style>
        .admin-menu { display: flex; flex-direction: column; gap: 15px; margin-top: 20px; }
        .admin-menu-item {
            background: #e8e8e8; padding: 20px 30px; border-radius: 12px;
            text-decoration: none; color: #333; font-weight: 500; text-align: center;
            box-shadow: 4px 4px 8px rgba(0,0,0,0.15), -4px -4px 8px rgba(255,255,255,0.8);
            transition: all 0.3s ease;
        }
        .admin-menu-item:hover { background: #171717; color: white; transform: translateY(-3px); }
    </style>
    <div class="page-container">
        <div class="admin-card" style="max-width: 450px;">
            <h2 class="admin-title">Insurance Renewal 2026</h2>
            <div class="admin-menu">
                <a href="?page=life_insurance" class="admin-menu-item">Life Insurance</a>
                <a href="?page=medical_insurance" class="admin-menu-item">Medical Insurance</a>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Back to Admin", use_container_width=True):
            st.query_params["page"] = "admin"
            st.rerun()

def render_life_insurance():
    st.markdown(CSS, unsafe_allow_html=True)
    
    if 'admin_authenticated' not in st.session_state or not st.session_state.admin_authenticated:
        st.query_params["page"] = "admin"
        st.rerun()
        return
    
    st.markdown('''
    <div class="page-container">
        <h1 class="page-title">Life Insurance</h1>
        <p class="page-message">Life Insurance section coming soon.</p>
    </div>
    ''', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Back to Insurance Renewal", use_container_width=True):
            st.query_params["page"] = "insurance_renewal"
            st.rerun()

def render_medical_insurance():
    st.markdown(CSS, unsafe_allow_html=True)
    
    if 'admin_authenticated' not in st.session_state or not st.session_state.admin_authenticated:
        st.query_params["page"] = "admin"
        st.rerun()
        return
    
    st.markdown('''
    <div class="page-container">
        <h1 class="page-title">Medical Insurance</h1>
        <p class="page-message">Medical Insurance section coming soon.</p>
    </div>
    ''', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Back to Insurance Renewal", use_container_width=True):
            st.query_params["page"] = "insurance_renewal"
            st.rerun()

def main():
    page = get_page()
    
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
    elif page == "insurance_renewal":
        render_insurance_renewal()
    elif page == "life_insurance":
        render_life_insurance()
    elif page == "medical_insurance":
        render_medical_insurance()
    else:
        render_home()

if __name__ == "__main__":
    main()
