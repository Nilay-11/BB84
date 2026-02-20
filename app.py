import streamlit as st

st.set_page_config(
    page_title="Exhibit Nova",
    page_icon="???",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=Fraunces:opsz,wght@9..144,600;9..144,700&display=swap');

    :root {
      --bg: #f5f3ee;
      --ink: #1f2933;
      --muted: #6b7280;
      --accent: #0f766e;
      --accent-soft: #c9efe9;
      --card: #fffefb;
      --stroke: #e6ddd2;
    }

    .stApp {
      background:
        radial-gradient(circle at 12% 15%, #d8efe5 0%, transparent 30%),
        radial-gradient(circle at 88% 10%, #ffe7bd 0%, transparent 28%),
        linear-gradient(180deg, #fbfaf7 0%, #f2efe8 100%);
      color: var(--ink);
      font-family: 'Space Grotesk', sans-serif;
    }

    .block-container {
      max-width: 1180px;
      padding-top: 2rem;
      padding-bottom: 3rem;
    }

    .badge {
      display: inline-block;
      background: #111827;
      color: #f9fafb;
      border-radius: 999px;
      font-size: 0.78rem;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      padding: 0.35rem 0.8rem;
      margin-bottom: 1rem;
    }

    .hero-title {
      font-family: 'Fraunces', serif;
      font-size: clamp(2rem, 5vw, 4rem);
      line-height: 1.05;
      margin-bottom: 0.6rem;
      color: #0b1320;
      letter-spacing: -0.02em;
    }

    .hero-sub {
      color: var(--muted);
      font-size: 1.05rem;
      max-width: 58ch;
      margin-bottom: 1.2rem;
    }

    .glass {
      background: rgba(255, 255, 255, 0.75);
      backdrop-filter: blur(4px);
      border: 1px solid var(--stroke);
      border-radius: 16px;
      padding: 1.2rem;
      box-shadow: 0 8px 30px rgba(15, 23, 42, 0.06);
      height: 100%;
    }

    .section-title {
      font-family: 'Fraunces', serif;
      font-size: 1.7rem;
      margin: 0.2rem 0 0.8rem;
      color: #0f172a;
    }

    .section-sub {
      color: var(--muted);
      margin-bottom: 1.2rem;
    }

    .pill {
      display: inline-block;
      padding: 0.2rem 0.6rem;
      border-radius: 999px;
      border: 1px solid var(--stroke);
      background: #fff;
      margin-right: 0.45rem;
      margin-bottom: 0.45rem;
      font-size: 0.82rem;
      color: #334155;
    }

    .stat {
      border-top: 1px dashed #d2d9e2;
      margin-top: 0.8rem;
      padding-top: 0.8rem;
      color: #334155;
      font-size: 0.95rem;
    }

    .time-card {
      border-left: 4px solid var(--accent);
      background: var(--card);
      border-radius: 10px;
      border: 1px solid var(--stroke);
      padding: 0.9rem 1rem;
      margin-bottom: 0.7rem;
    }

    .time {
      color: var(--accent);
      font-weight: 700;
      font-size: 0.86rem;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      margin-bottom: 0.15rem;
    }

    .event {
      color: #0f172a;
      font-weight: 600;
      margin-bottom: 0.1rem;
    }

    .event-sub {
      color: #64748b;
      font-size: 0.9rem;
    }

    .footer {
      margin-top: 2.4rem;
      border-top: 1px solid #ddd8ce;
      padding-top: 1.1rem;
      color: #6b7280;
      font-size: 0.9rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<span class="badge">Exhibition Website</span>', unsafe_allow_html=True)
st.markdown('<h1 class="hero-title">Exhibit Nova 2026</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-sub">A clean, modern exhibition frontend built in Streamlit with an editorial visual style, curated schedule, gallery zones, and sponsor-ready callouts.</p>',
    unsafe_allow_html=True,
)

c1, c2, c3 = st.columns([1.2, 1, 1])
with c1:
    st.markdown(
        """
        <div class="glass">
          <h3 class="section-title">Theme</h3>
          <p class="section-sub">Human creativity meets intelligent systems across art, design, robotics, and quantum storytelling.</p>
          <span class="pill">Live Installations</span>
          <span class="pill">Panel Talks</span>
          <span class="pill">Interactive Booths</span>
          <div class="stat">Expected Footfall: <b>2,800+</b> visitors</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        """
        <div class="glass">
          <h3 class="section-title">Dates</h3>
          <p class="section-sub">April 18-20, 2026<br/>City Convention Pavilion, Hall B</p>
          <div class="stat">Exhibitors: <b>42</b></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        """
        <div class="glass">
          <h3 class="section-title">Passes</h3>
          <p class="section-sub">General, Student, VIP, and Media access tiers with QR-based check-in.</p>
          <div class="stat">Early Bird Ends: <b>March 30</b></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("### Program Highlights")
left, right = st.columns([1, 1])
with left:
    st.markdown(
        """
        <div class="time-card">
          <div class="time">10:00 AM</div>
          <div class="event">Opening Experience Walk</div>
          <div class="event-sub">Immersive digital corridor and keynote by resident curator.</div>
        </div>
        <div class="time-card">
          <div class="time">12:30 PM</div>
          <div class="event">Future of Creative AI Panel</div>
          <div class="event-sub">Design leaders discuss ethics, authorship, and tooling.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with right:
    st.markdown(
        """
        <div class="time-card">
          <div class="time">2:00 PM</div>
          <div class="event">Hands-on Quantum Booth</div>
          <div class="event-sub">Interactive BB84 demonstrations and guided experiments.</div>
        </div>
        <div class="time-card">
          <div class="time">5:00 PM</div>
          <div class="event">Sunset Showcase</div>
          <div class="event-sub">Live audiovisual performances from selected creators.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("### Visitor Interest")
interest = {
    "AI Art": 84,
    "Robotics": 62,
    "Quantum Tech": 73,
    "Design Systems": 58,
    "Live Installations": 79,
}
st.bar_chart(interest)

st.markdown("### Quick Contact")
col_a, col_b = st.columns(2)
with col_a:
    name = st.text_input("Your Name")
with col_b:
    email = st.text_input("Email")
msg = st.text_area("Message", placeholder="Tell us about your collaboration, sponsorship, or media request.")
if st.button("Send Inquiry"):
    if name and email and msg:
        st.success("Inquiry captured. Organizing team will respond within 24 hours.")
    else:
        st.warning("Please fill in all fields before submitting.")

st.markdown('<div class="footer">Exhibit Nova 2026 • Built with Streamlit • Ready for GitHub deployment</div>', unsafe_allow_html=True)
