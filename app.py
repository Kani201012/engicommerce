import streamlit as st
import zipfile
import io
import json
from datetime import datetime
import urllib.parse

# ─── APP CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Kaydiem Titan v12.0 | Platinum Architect",
    layout="wide",
    page_icon="💎",
    initial_sidebar_state="expanded"
)

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
        border-radius: var(--radius); border: 1px solid #475569;
    }
    </style>
""", unsafe_allow_html=True)

# ─── SIDEBAR DESIGN STUDIO ───────────────────────────────────────────────────
with st.sidebar:
    st.image("https://www.gstatic.com/images/branding/product/2x/business_profile_96dp.png", width=64)
    st.title("Titan v12.0 Studio")
    st.caption("Luxury Wedding & Event Edition")

    with st.expander("🎨 Design DNA", expanded=True):
        dna = st.selectbox("Preset", [
            "Royal Velvet", "Modern Minimal Luxe", "Ethereal Romance",
            "Industrial Chic", "Glass & Gold", "Timeless Ebony"
        ])
        p_color = st.color_picker("Primary", "#4c1d95" if "Velvet" in dna else "#1e293b")
        s_color = st.color_picker("Accent", "#d4af37")
        border_rad = st.select_slider("Radius", ["0.75rem", "1.5rem", "2.5rem", "3.5rem"], value="1.5rem")

    with st.expander("✍ Typography", expanded=True):
        h_font = st.selectbox("Headings", ["Playfair Display", "Cormorant Garamond", "Cinzel", "Great Vibes", "Spectral"])
        b_font = st.selectbox("Body", ["Inter", "Lora", "Libre Baskerville", "Manrope"])
        base_size = st.slider("Base Font Size (px)", 16, 22, 18)

    gsc_tag = st.text_input("Google Site Verification")
    insta_handle = st.text_input("Instagram Handle (for feed embed)", "@redhippoplanners")
    sheet_url = st.text_input("Google Sheets CSV (Products/Services)", placeholder="https://docs.google.com/spreadsheets/d/.../pub?output=csv")

    st.info("Engineered by Kaydiem Script Lab • 2026 Ready")

# ─── MAIN TABS ───────────────────────────────────────────────────────────────
tab_names = ["Identity", "Content+SEO", "Gallery", "Live Feed", "Social Proof", "Legal+Form"]
tabs = st.tabs([f" {name} " for name in tab_names])

with tabs[0]:
    c1, c2 = st.columns([3,2])
    with c1:
        biz_name   = st.text_input("Business Name", "Red Hippo Luxury Planners")
        biz_phone  = st.text_input("Phone (verified)", "+918454002711")
        biz_email  = st.text_input("Email", "events@redhippoplanners.in")
        biz_cat    = st.text_input("Category", "Luxury Wedding & Event Planner")
    with c2:
        biz_hours  = st.text_input("Hours", "Mon–Sun: 10:00 – 20:00")
        biz_addr   = st.text_area("Full Address")
        biz_areas  = st.text_area("Service Areas (comma sep)", "South Delhi, Gurgaon, Noida, Chandigarh")
        map_iframe = st.text_area("Google Map Embed <iframe>")

    biz_logo    = st.text_input("Logo URL (transparent PNG/SVG best)")
    prod_url    = st.text_input("Live Domain", "https://yourdomain.com/")

with tabs[1]:
    hero_h   = st.text_input("Hero Headline", "Designing Timeless Love Stories Across India")
    hero_sub = st.text_input("Hero Sub / Meta Desc (160 char)", "Bespoke luxury wedding planning & décor — turning dreams into unforgettable realities.")
    seo_keys = st.text_input("Main Keywords", "luxury wedding planner delhi, premium event decorator, bespoke wedding design")
    services = st.text_area("Services (one per line)", "Full Wedding Planning\nDestination Weddings\nDécor & Floral Design\nVenue Styling\nCorporate Galas")
    about    = st.text_area("Our Story (~1000 words)", height=280)

with tabs[2]:
    st.subheader("Hero & Key Visuals")
    hero_bg  = st.text_input("Hero Background (high-res)", "https://images.unsplash.com/photo-1519741497674-611481863552")
    feat_img = st.text_input("Feature / About Image")
    gall_imgs= st.text_area("Gallery Images URLs (one per line – min 6 recommended)")

with tabs[3]:
    st.subheader("Live Dynamic Content")
    st.caption("CSV format: Name | Price/Tag | Description | Image URL")
    st.info("Leave blank to hide Products section")

with tabs[4]:
    testi = st.text_area("Testimonials (Name | Quote | optional Rating 1-5)", height=180)
    faqs  = st.text_area("FAQ (Question?Answer)", height=180)

with tabs[5]:
    priv  = st.text_area("Privacy Policy", height=220)
    terms = st.text_area("Terms & Conditions", height=220)
    cont_form_action = st.text_input("Contact Form Action URL", "https://formspree.io/f/your-id")

# ─── GENERATE BUTTON ─────────────────────────────────────────────────────────
if st.button("✨ GENERATE TITAN v12.0 PLATINUM PACKAGE"):

    # Cleanup & prepare
    wa_clean = ''.join(c for c in biz_phone if c.isdigit())
    wa_link  = f"https://wa.me/{wa_clean}"
    areas    = [a.strip() for a in biz_areas.split(",") if a.strip()]
    gallery  = [url.strip() for url in gall_imgs.splitlines() if url.strip()][:12]

    # ─── THEME CSS (modern, luxury, 2026-ready) ──────────────────────────────
    theme = f"""
    :root {{
        --p: {p_color}; --s: {s_color}; --radius: {border_rad};
        --txt: #0f172a; --light: #f8fafc; --dark: #020617;
        --trans: 0.45s cubic-bezier(0.34, 1.56, 0.64, 1);
    }}
    @media (prefers-color-scheme: dark) {{
        :root {{ --txt: #e2e8f0; --light: #0f172a; --dark: #020617; }}
        body {{ background: var(--dark); color: var(--txt); }}
    }}
    * {{ margin:0; padding:0; box-sizing:border-box; }}
    html {{ scroll-behavior:smooth; scroll-padding-top:5rem; }}
    body {{ font-family:'{b_font}', system-ui, sans-serif; color:var(--txt); background:var(--light); line-height:1.7; font-size:{base_size}px; }}
    h1,h2,h3 {{ font-family:'{h_font}', serif; font-weight:800; letter-spacing:-0.03em; line-height:1.05; }}
    a {{ color:var(--s); text-decoration:none; }}
    .btn {{ display:inline-flex; align-items:center; justify-content:center; padding:1rem 2.2rem; border-radius:var(--radius); font-weight:700; transition:var(--trans); }}
    .btn-p {{ background:var(--p); color:white; }}
    .btn-s {{ background:var(--s); color:var(--dark); }}
    .btn:hover {{ transform:translateY(-3px); box-shadow:0 16px 40px -12px color-mix(in srgb, var(--s) 30%, transparent); }}
    .glass {{ background:rgba(255,255,255,0.07); backdrop-filter:blur(16px); -webkit-backdrop-filter:blur(16px); border:1px solid rgba(255,255,255,0.12); border-radius:var(--radius); }}
    .hero {{ min-height:90vh; background:linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.35)), url('{hero_bg}') center/cover no-repeat; color:white; display:grid; place-items:center; text-align:center; padding:6rem 1.5rem; }}
    .hero h1 {{ font-size:clamp(3.2rem, 9vw, 8rem); text-shadow:0 8px 32px rgba(0,0,0,0.7); }}
    img.lazy {{ opacity:0; transition:opacity 0.6s; }}
    img.lazy.loaded {{ opacity:1; }}
    """

    # ─── JAVASCRIPT (micro-animations, dark toggle, lazy, counters) ────────────
    js = """
    // Dark mode
    const toggleDark = () => document.body.classList.toggle('dark');
    // Lazy images
    document.addEventListener("DOMContentLoaded", () => {
        let obs = new IntersectionObserver((es) => es.forEach(e => { if(e.isIntersecting){ e.target.src = e.target.dataset.src; e.target.classList.add('loaded'); obs.unobserve(e.target); }}));
        document.querySelectorAll('img[data-src]').forEach(img => obs.observe(img));
    });
    // Animate counters
    function countUp(el, target, dur=1800) {
        let start = 0, step = target/60, t=0;
        let timer = setInterval(() => {
            start += step; t += 16;
            el.textContent = Math.min(Math.round(start), target).toLocaleString();
            if(t >= dur) clearInterval(timer);
        }, 16);
    }
    """

    if sheet_url:
        js += f"""
        async function loadProducts() {{
            try {{
                let r = await fetch('{sheet_url}');
                let csv = await r.text();
                let rows = csv.split('\\n').slice(1).map(r=>r.split('|').map(s=>s.trim()));
                let cont = document.getElementById('products');
                cont.innerHTML = rows.map(([name,price,desc,img]) => `
                    <div class="glass p-6 flex flex-col gap-4 hover:scale-[1.03] transition-transform">
                        <img data-src="${{img||'{feat_img}'}}" class="lazy w-full h-64 object-cover rounded-2xl" alt="${{name}}">
                        <h3 class="text-2xl font-bold" style="color:var(--p)">${{name}}</h3>
                        <p class="text-xl font-black" style="color:var(--s)">${{price}}</p>
                        <p class="text-slate-300">${{desc}}</p>
                        <a href="{wa_link}?text=Interested in ${{encodeURIComponent(name)}}" class="btn btn-s mt-auto">Inquire Now</a>
                    </div>
                `).join('');
            }} catch(e){{ cont.innerHTML = '<p class="text-center opacity-70">Loading failed</p>'; }}
        }}
        window.onload = loadProducts;
        """

    # ─── HTML LAYOUT FUNCTION ────────────────────────────────────────────────
    def page_shell(title, desc, body, canonical=True):
        gsc = f'<meta name="google-site-verification" content="{gsc_tag}">' if gsc_tag else ''
        canon = f'<link rel="canonical" href="{prod_url}{title.lower().replace(" ","")}.html">' if canonical else ''
        return f"""<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | {biz_name}</title>
    <meta name="description" content="{desc}">
    <meta name="keywords" content="{seo_keys}">
    {gsc}{canon}
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family={h_font.replace(' ','+')}:wght@700;900&family={b_font.replace(' ','+')}:wght@400;500;700&display=swap" rel="stylesheet">
    <style>{theme}</style>
    <script type="application/ld+json">
    {json.dumps({
        "@context": "https://schema.org",
        "@type": "WeddingPlanner" if "wedding" in biz_cat.lower() else "EventPlanner",
        "name": biz_name,
        "telephone": biz_phone,
        "email": biz_email,
        "address": {"@type":"PostalAddress","streetAddress":biz_addr},
        "areaServed": areas,
        "url": prod_url,
        "image": hero_bg,
        "description": hero_sub
    }, indent=2)}
    </script>
</head>
<body class="antialiased">
    <button onclick="toggleDark()" class="fixed top-6 right-6 z-50 glass p-3 rounded-full">🌙</button>
    <nav class="fixed top-0 w-full glass z-40 backdrop-blur-xl">
        <div class="max-w-7xl mx-auto px-6 py-5 flex justify-between items-center">
            <a href="index.html" class="text-2xl font-black" style="color:var(--p)">{biz_name}</a>
            <div class="hidden md:flex gap-10 font-medium">
                <a href="index.html">Home</a>
                <a href="about.html">About</a>
                <a href="gallery.html">Portfolio</a>
                <a href="contact.html">Contact</a>
            </div>
        </div>
    </nav>
    {body}
    <footer class="bg-black text-gray-400 py-20 px-6">
        <div class="max-w-7xl mx-auto grid md:grid-cols-4 gap-12">
            <div class="md:col-span-2">
                <h4 class="text-white text-3xl font-black mb-6">{biz_name}</h4>
                <p>{biz_addr}</p>
                <p class="mt-4">{biz_phone} • {biz_email}</p>
            </div>
            <div>
                <h5 class="text-white font-bold mb-6 uppercase text-sm tracking-widest">Quick Links</h5>
                <ul class="space-y-3">
                    <li><a href="privacy.html">Privacy</a></li>
                    <li><a href="terms.html">Terms</a></li>
                </ul>
            </div>
            <div>
                <h5 class="text-white font-bold mb-6 uppercase text-sm tracking-widest">Connect</h5>
                <a href="{wa_link}" class="block text-2xl font-black hover:text-white transition">WhatsApp</a>
            </div>
        </div>
        <p class="text-center mt-16 opacity-50 text-sm">© {datetime.now().year} {biz_name} • Crafted with Titan</p>
    </footer>
    <script>{js}</script>
</body>
</html>"""

    # ─── PAGE CONTENTS ────────────────────────────────────────────────────────
    index_body = f"""
    <section class="hero">
        <div class="max-w-6xl mx-auto px-6">
            <h1 class="mb-8">{hero_h}</h1>
            <p class="text-xl md:text-3xl opacity-90 max-w-4xl mx-auto mb-12">{hero_sub}</p>
            <div class="flex flex-col sm:flex-row gap-6 justify-center">
                <a href="tel:{biz_phone}" class="btn btn-p text-lg">Call Now</a>
                <a href="{wa_link}" class="btn btn-s text-lg">WhatsApp Inquiry</a>
            </div>
        </div>
    </section>
    <!-- Stats / Trust -->
    <section class="py-24 bg-gradient-to-b from-transparent to-black/5">
        <div class="max-w-7xl mx-auto px-6 grid md:grid-cols-4 gap-12 text-center">
            <div><div class="text-5xl font-black text-[var(--s)]" data-count="150">0</div><p class="mt-3 uppercase tracking-widest text-sm">Weddings Designed</p></div>
            <div><div class="text-5xl font-black text-[var(--s)]" data-count="100">0</div><p class="mt-3 uppercase tracking-widest text-sm">Client Satisfaction</p></div>
            <!-- add more -->
        </div>
    </section>
    <!-- Services -->
    <section class="py-32 px-6 max-w-7xl mx-auto">
        <h2 class="text-6xl font-black text-center mb-20" style="color:var(--p)">Our Signature Services</h2>
        <div class="grid md:grid-cols-3 gap-10">
            {''.join(f'<div class="glass p-10 hover:scale-105 transition-transform"><h3 class="text-2xl font-bold mb-6" style="color:var(--p)">{s}</h3><p class="opacity-80">Bespoke execution with flawless detail.</p></div>' for s in services.splitlines() if s.strip())}
        </div>
    </section>
    """

    if sheet_url:
        index_body += f"""
        <section class="py-32 px-6 bg-black/30">
            <h2 class="text-6xl font-black text-center mb-20" style="color:var(--p)">Featured Collections</h2>
            <div id="products" class="grid md:grid-cols-3 lg:grid-cols-4 gap-8 max-w-7xl mx-auto"></div>
        </section>
        """

    # ─── ZIP CREATION ─────────────────────────────────────────────────────────
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("index.html", page_shell("Home", hero_sub, index_body))
        z.writestr("about.html", page_shell("About", "Our Heritage", f"<section class='py-32 px-6 max-w-5xl mx-auto'><h1 class='text-7xl font-black mb-16' style='color:var(--p)'>Our Story</h1><div class='prose prose-xl max-w-none'>{about.replace('\n','<br>')}</div><img src='{feat_img}' class='mt-20 rounded-3xl shadow-2xl w-full'></section>"))
        z.writestr("gallery.html", page_shell("Portfolio", "Our Work", "<section class='py-32 px-6'><h1 class='text-7xl font-black text-center mb-20' style='color:var(--p)'>Portfolio</h1><div class='grid md:grid-cols-3 gap-6 max-w-7xl mx-auto'>" + "".join(f"<img src='{u}' class='rounded-3xl shadow-2xl hover:scale-105 transition-transform' loading='lazy'>" for u in gallery) + "</div></section>"))
        z.writestr("contact.html", page_shell("Contact", "Get in Touch", f"<section class='py-32 px-6 text-center max-w-4xl mx-auto'><h1 class='text-7xl font-black mb-12' style='color:var(--p)'>Let's Create Magic</h1><p class='text-2xl mb-12'>{biz_addr}<br>{biz_phone}</p><iframe src='{map_iframe}' class='w-full h-96 rounded-3xl' loading='lazy'></iframe></section>"))
        z.writestr("privacy.html", page_shell("Privacy", "Legal", f"<div class='max-w-4xl mx-auto py-32 px-10 prose'>{priv}</div>"))
        z.writestr("terms.html", page_shell("Terms", "Legal", f"<div class='max-w-4xl mx-auto py-32 px-10 prose'>{terms}</div>"))

    zip_buffer.seek(0)
    filename = f"{biz_name.lower().replace(' ','_')}_titan_v12.zip"

    st.success("TITAN v12.0 PLATINUM LUXURY PACKAGE READY ✓")
    st.download_button("DOWNLOAD ZIP PACKAGE", zip_buffer, file_name=filename, mime="application/zip")

    # Optional preview
    if st.toggle("Show index.html preview (raw)"):
        st.code(page_shell("Home", hero_sub, index_body)[:4000] + "...", language="html")
