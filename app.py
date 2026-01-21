import streamlit as st
import zipfile
import io
import json
from datetime import datetime
import urllib.parse

# =============================================================================
#   MUST BE THE VERY FIRST STREAMLIT COMMAND
# =============================================================================
st.set_page_config(
    page_title="Kaydiem Titan v12.5 | Diamond Elite Architect",
    page_icon="💎",           # Most reliable cross-browser option
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/streamlit/streamlit/issues',
        'Report a bug': "https://github.com/streamlit/streamlit/issues/new/choose",
        'About': "Luxury Wedding & Event Site Generator • Kaydiem Lab 2026"
    }
)

# Fallback favicon injection (helps especially in Safari and some deployments)
st.markdown(
    """
    <link rel="icon" type="image/png" sizes="32x32" href="https://img.icons8.com/emoji/32/000000/gem-stone.png">
    <link rel="icon" type="image/svg+xml" href="https://img.icons8.com/emoji/32/000000/gem-stone.png">
    """,
    unsafe_allow_html=True
)

# Custom styling
st.markdown("""
    <style>
    :root { --radius: 1.5rem; --transition: 0.4s cubic-bezier(0.4, 0, 0.2, 1); }
    .main { background: #0f172a; color: white; padding-bottom: 4rem; }
    .stTabs [data-baseweb="tab"] { color: white !important; font-weight: 700; font-size: 1.15rem; }
    .stButton > button {
        width: 100%; border-radius: var(--radius); height: 4.2rem;
        background: linear-gradient(135deg, #1e293b, #334155);
        color: white; font-weight: 900; font-size: 1.35rem; border: none;
        box-shadow: 0 12px 32px rgba(0,0,0,0.45); transition: var(--transition);
    }
    .stButton > button:hover { transform: translateY(-3px); filter: brightness(1.15); }
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        border-radius: var(--radius); border: 1px solid #475569; background: #1e293b; color: white;
    }
    </style>
""", unsafe_allow_html=True)

# =============================================================================
#   SIDEBAR
# =============================================================================
with st.sidebar:
    st.image("https://www.gstatic.com/images/branding/product/2x/business_profile_96dp.png", width=64)
    st.title("Titan v12.5 Studio")
    st.caption("Luxury Wedding & Event Edition – 2026 Ready")

    with st.expander("🎨 Design DNA", expanded=True):
        dna_preset = st.selectbox("Style Preset", [
            "Royal Velvet", "Modern Minimal Luxe", "Ethereal Romance",
            "Industrial Chic", "Glass & Gold", "Timeless Ebony"
        ])
        primary_color   = st.color_picker("Primary Color",   "#4c1d95" if "Velvet" in dna_preset else "#1e293b")
        accent_color    = st.color_picker("Accent / CTA",    "#d4af37")
        corner_radius   = st.select_slider("Corner Radius", ["0.75rem", "1.5rem", "2.5rem", "3.5rem"], value="1.5rem")

    with st.expander("✍ Typography", expanded=True):
        heading_font = st.selectbox("Headings", ["Playfair Display", "Cormorant Garamond", "Cinzel", "Great Vibes", "Spectral"])
        body_font    = st.selectbox("Body Text", ["Inter", "Lora", "Libre Baskerville", "Manrope"])
        base_font_px = st.slider("Base Font Size (px)", 15, 22, 18)

    gsc_code = st.text_input("Google Search Console Verification Code")
    insta_username = st.text_input("Instagram Handle (for future embed)", "@example")
    products_csv_url = st.text_input("Google Sheets CSV URL (products)", placeholder="https://docs.google.com/spreadsheets/d/.../pub?output=csv")

    st.info("Engineered by Kaydiem Script Lab")

# =============================================================================
#   MAIN TABS
# =============================================================================
tab_names = ["Business Info", "Content & SEO", "Visuals", "Live Products", "Proof & FAQ", "Legal & Form"]
tabs = st.tabs(tab_names)

with tabs[0]:
    col1, col2 = st.columns([3, 2])
    with col1:
        business_name   = st.text_input("Business Name", "Red Hippo Luxury Planners")
        phone_number    = st.text_input("Phone (with country code)", "+966xxxxxxxxx")
        email_address   = st.text_input("Email", "events@redhippoplanners.in")
        category        = st.text_input("Main Category", "Luxury Wedding & Event Planner")
    with col2:
        working_hours   = st.text_input("Business Hours", "Mon–Sun: 10:00 – 20:00")
        full_address    = st.text_area("Complete Physical Address")
        service_areas   = st.text_area("Service Areas (comma separated)", "Riyadh, Jeddah, Dammam, Khobar")
        map_embed_code  = st.text_area("Google Maps Embed <iframe> code")

    logo_url = st.text_input("Logo URL (preferably transparent PNG/SVG)")
    live_domain = st.text_input("Production / Live URL", "https://yourdomain.com/")

with tabs[1]:
    hero_title      = st.text_input("Hero Headline", "Designing Timeless Love Stories")
    hero_subtitle   = st.text_input("Hero Subtitle / Meta Description", "Bespoke luxury wedding planning & décor in Saudi Arabia and beyond.")
    main_keywords   = st.text_input("Primary SEO Keywords", "luxury wedding planner riyadh, premium event decorator jeddah")
    services_list   = st.text_area("Services (one per line)", "Complete Wedding Planning\nDestination Weddings\nLuxury Décor & Florals\nVenue Transformation\nCorporate & Private Events")
    about_us_text   = st.text_area("About Us Story", height=280)

with tabs[2]:
    st.subheader("Hero & Key Visuals")
    hero_background_url = st.text_input("Hero Background Image URL", "https://images.unsplash.com/photo-1519741497674-611481863552")
    feature_image_url   = st.text_input("About / Feature Image URL")
    gallery_urls        = st.text_area("Gallery Images (one full URL per line – 6–12 recommended)")

with tabs[3]:
    st.subheader("Dynamic Product / Package Feed")
    st.caption("CSV format expected: Name | Price/Tag | Short Description | Image URL")

with tabs[4]:
    testimonials_raw = st.text_area("Testimonials\nFormat: Name | Quote | optional Rating (1–5)", height=160)
    faq_raw          = st.text_area("FAQ\nFormat: Question?Answer", height=160)

with tabs[5]:
    privacy_policy_text   = st.text_area("Privacy Policy Content", height=220)
    terms_conditions_text = st.text_area("Terms & Conditions Content", height=220)
    form_action_url       = st.text_input("Contact Form POST URL", "https://formspree.io/f/yourformid")

# =============================================================================
#   GENERATE BUTTON + LOGIC
# =============================================================================
if st.button("✨ GENERATE TITAN v12.5 LUXURY PACKAGE", type="primary"):

    # Prepare clean data
    wa_number_clean = ''.join(c for c in phone_number if c.isdigit())
    whatsapp_link   = f"https://wa.me/{wa_number_clean}"
    service_areas_list = [a.strip() for a in service_areas.split(",") if a.strip()]
    gallery_images   = [url.strip() for url in gallery_urls.splitlines() if url.strip()][:12]

    # Quick & dirty SEO check
    def mini_seo_check():
        issues = []
        if len(hero_title) < 30 or len(hero_title) > 70:
            issues.append("Hero headline ideally 40–60 characters")
        if len(hero_subtitle) > 160:
            issues.append("Meta description too long (>160 chars)")
        if len(about_us_text.split()) < 350:
            issues.append("About text is quite short – aim for 600+ words")
        score = max(40, 100 - len(issues) * 18)
        return score, issues

    seo_score, seo_issues = mini_seo_check()

    st.subheader("Quick SEO & Quality Check")
    colA, colB = st.columns([1,3])
    with colA:
        st.metric("SEO Score", f"{seo_score}/100")
    with colB:
        if seo_issues:
            st.warning("\n".join(f"• {issue}" for issue in seo_issues))
        else:
            st.success("Looks good! Strong foundation for search visibility.")

    # ─── THEME & STYLES ───────────────────────────────────────────────────────
    css_theme = f"""
    :root {{
        --primary: {primary_color};
        --accent: {accent_color};
        --radius: {corner_radius};
        --transition: 0.45s cubic-bezier(0.34, 1.56, 0.64, 1);
    }}
    * {{ margin:0; padding:0; box-sizing:border-box; }}
    body {{ font-family: '{body_font}', system-ui, sans-serif; font-size: {base_font_px}px; line-height:1.7; }}
    h1, h2, h3 {{ font-family: '{heading_font}', serif; }}
    """

    # Very basic preview HTML (you can expand this massively)
    preview_html = f"""
    <div style="padding:2rem; background:#0f172a; color:white; font-family:sans-serif;">
        <h1 style="color:{primary_color};">{business_name}</h1>
        <h2>{hero_title}</h2>
        <p>{hero_subtitle}</p>
        <p style="color:#aaa; font-size:0.9rem;">(This is a simplified preview – full site is much richer)</p>
    </div>
    """

    # Save for live preview tab
    if 'last_preview' not in st.session_state:
        st.session_state.last_preview = ""
    st.session_state.last_preview = preview_html

    # ─── ZIP CREATION (placeholder – expand as needed) ────────────────────────
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("index.html", f"<!DOCTYPE html><html><head><title>{business_name}</title><style>{css_theme}</style></head><body>{preview_html}</body></html>")
        zf.writestr("README.txt", "Generated by Kaydiem Titan v12.5 – January 2026")

    zip_buffer.seek(0)

    # Offer download
    safe_name = business_name.lower().replace(" ", "_").replace(",", "")
    st.download_button(
        label="📦 DOWNLOAD ZIP PACKAGE",
        data=zip_buffer,
        file_name=f"{safe_name}_titan_v12_5.zip",
        mime="application/zip"
    )

    # Live preview tab content
    st.subheader("Live Preview (basic)")
    st.components.v1.html(st.session_state.last_preview, height=600, scrolling=True)

st.caption("Note: This is still a simplified skeleton. The full luxury version would contain many more sections, responsive design, animations, schema.org, etc.")
