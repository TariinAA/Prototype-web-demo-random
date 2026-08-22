"""
Forensic Scientist's Case Notebook
AI Classification of Saliva & Sweat Stains

A Streamlit web app styled as a hand-drawn forensic case notebook.
Users upload photos of an unknown stain, and a pre-trained EfficientNetB0
Keras model (best_model_final.keras) classifies each one as Saliva or
Sweat with a confidence score.

This file is UI ONLY. Model loading lives in utils/model_loader.py and
preprocessing / inference logic lives in utils/predictor.py -- app.py
never touches TensorFlow directly.
"""

import os
import io
import random
import string
import time
from datetime import date

import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt

from utils.model_loader import load_trained_model
from utils.predictor import predict_stain, CLASS_NAMES
from assets.doodles import MICROSCOPE, DNA, DROPLET, TEST_TUBE, MAGNIFIER, CELL

# ---------------------------------------------------------------------------
# PAGE CONFIG + CSS
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Forensic Case Notebook | Saliva & Sweat AI",
    page_icon="🔬",
    layout="centered",
    initial_sidebar_state="collapsed",
)

CSS_PATH = os.path.join(os.path.dirname(__file__), "assets", "style.css")
with open(CSS_PATH, "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

COLOR_MAP = {"Saliva": "#4F97AE", "Sweat": "#4CA88A"}
BADGE_CLASS = {"Saliva": "badge-saliva", "Sweat": "badge-sweat"}


# ---------------------------------------------------------------------------
# SESSION STATE INIT
# ---------------------------------------------------------------------------
def init_state():
    defaults = {
        "page": "cover",
        "case_id": "DD-" + "".join(random.choices(string.digits, k=3)),
        "case_date": date.today().strftime("%B %d, %Y"),
        "investigator": "",
        "evidence": [],   # list of dicts: {"name": str, "bytes": bytes}
        "results": [],    # list of dicts returned by predict_stain + name
        "notes": "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def go_to(page_name: str):
    st.session_state.page = page_name


init_state()


# ---------------------------------------------------------------------------
# PAGE: COVER
# ---------------------------------------------------------------------------
def render_cover():
    icon_cols = st.columns(5)
    icons = [MICROSCOPE, DNA, DROPLET, TEST_TUBE, CELL]
    for col, icon in zip(icon_cols, icons):
        with col:
            st.markdown(f"<div style='text-align:center'>{icon}</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="cover-card">
            <div class="tape" style="top:-14px; left:36px; transform:rotate(-8deg);"></div>
            <div class="tape" style="top:-14px; right:36px; transform:rotate(8deg);"></div>
            <div class="cover-kicker">FORENSIC LAB</div>
            <div class="cover-title">🔬 CASE NOTEBOOK</div>
            <div class="cover-sub">Saliva &amp; Sweat Classification</div>
            <div class="cover-question">"Can AI tell what this stain is?"</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    c1, c2, c3 = st.columns([1, 1.3, 1])

    with c2:
        if st.button("📂 OPEN CASE FILE", use_container_width=True):
            go_to("case_file")
            st.rerun()

        if st.button("🎲 RANDOM SAMPLE DEMO", use_container_width=True):
            go_to("random")
            st.rerun()


# ---------------------------------------------------------------------------
# PAGE: CASE FILE INFO
# ---------------------------------------------------------------------------
def render_case_file():
    st.markdown(
        f"""
        <div class="case-card">
            <span class="case-id">CASE FILE #{st.session_state.case_id}</span>
            <div class="case-row"><span>🧾 Evidence:</span><span>Unknown Stain</span></div>
            <div class="case-row"><span>📅 Date:</span><span>{st.session_state.case_date}</span></div>
            <div class="case-row"><span>🕵️ Investigator:</span><span>{st.session_state.investigator or "—"}</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.session_state.investigator = st.text_input(
        "Investigator's name (optional)", value=st.session_state.investigator,
        placeholder="e.g. Agent Nueng"
    )

    st.markdown(
        "<p class='cover-question' style='text-align:center;'>What could this stain be? Let's investigate!</p>",
        unsafe_allow_html=True,
    )
    st.markdown(f"<div style='text-align:center'>{MAGNIFIER}</div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1.3, 1])
    with c2:
        if st.button("🧪 BEGIN INVESTIGATION →", use_container_width=True):
            go_to("upload")
            st.rerun()


# ---------------------------------------------------------------------------
# PAGE: UPLOAD EVIDENCE
# ---------------------------------------------------------------------------
def render_upload():
    st.markdown(
        """
        <div class="section-step">
            <div class="section-num">01</div>
            <div class="section-title">COLLECT THE EVIDENCE</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("Upload one or more photos of the stain. Drag & drop, or click to browse — you can remove any photo before analyzing.")

    uploaded_files = st.file_uploader(
        "＋ ADD EVIDENCE",
        type=["jpg", "jpeg", "png", "webp"],
        accept_multiple_files=True,
        label_visibility="visible",
    )

    # Snapshot uploaded files into session_state so they survive the page change
    if uploaded_files is not None:
        st.session_state.evidence = [
            {"name": f.name, "bytes": f.getvalue()} for f in uploaded_files
        ]

    evidence = st.session_state.evidence

    if evidence:
        st.write("")
        st.markdown("**Evidence Preview**")
        cols = st.columns(4)
        rotations = ["-4deg", "3deg", "-2deg", "5deg", "-3deg", "2deg"]
        for i, item in enumerate(evidence):
            with cols[i % 4]:
                img_b64 = _to_data_uri(item["bytes"])
                rot = rotations[i % len(rotations)]
                st.markdown(
                    f"""
                    <div class="polaroid-wrap">
                        <div class="paperclip">📎</div>
                        <div class="polaroid" style="--rot:{rot};">
                            <img src="{img_b64}" />
                            <div class="polaroid-caption">Evidence #{i+1:03d}</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        st.info(f"🗂️ {len(evidence)} piece(s) of evidence collected. Remove unwanted photos from the uploader above (click the ✕ on a file) before analyzing.")
    else:
        st.warning("No evidence uploaded yet — add at least one photo to continue.")

    st.write("")
    c1, c2, c3 = st.columns([1, 1.4, 1])
    with c1:
        if st.button("← Back", use_container_width=True):
            go_to("case_file")
            st.rerun()
    with c3:
        if st.button("🔍 ANALYZE →", use_container_width=True, disabled=(len(evidence) == 0)):
            go_to("analyzing")
            st.rerun()


def _to_data_uri(img_bytes: bytes) -> str:
    import base64
    b64 = base64.b64encode(img_bytes).decode()
    return f"data:image/png;base64,{b64}"


# ---------------------------------------------------------------------------
# PAGE: AI INVESTIGATION (runs inference)
# ---------------------------------------------------------------------------
def render_analyzing():
    st.markdown(
        """
        <div class="section-step">
            <div class="section-num">02</div>
            <div class="section-title">EXAMINE THE EVIDENCE</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f"<div style='text-align:center'>{MICROSCOPE}</div>", unsafe_allow_html=True)
    with col2:
        st.markdown(
            "<p class='cover-question'>🧑‍🔬 AI is examining the evidence...</p>",
            unsafe_allow_html=True,
        )
        st.caption("Image → Preprocessing → EfficientNetB0 → Prediction → Saliva / Sweat → Confidence Score")

    status = st.empty()
    progress = st.progress(0)

    with st.spinner("Loading trained model..."):
        model = load_trained_model()

    evidence = st.session_state.evidence
    results = []
    total = len(evidence)

    for i, item in enumerate(evidence):
        status.markdown(f"🔎 Examining **Evidence #{i+1:03d}** — *{item['name']}*")
        image = Image.open(io.BytesIO(item["bytes"]))
        outcome = predict_stain(model, image)
        outcome["name"] = item["name"]
        outcome["bytes"] = item["bytes"]
        results.append(outcome)
        progress.progress(int(((i + 1) / total) * 100))
        time.sleep(0.15)  # brief pause so the loading animation is visible

    status.markdown("✅ **Examination complete.**")
    st.session_state.results = results
    time.sleep(0.4)
    go_to("results")
    st.rerun()

# —————————————————————————

# PAGE: RANDOM SAMPLE DEMO

# —————————————————————————

def render_random_sample():

    st.markdown(
        """
        <div class="section-step">
            <div class="section-num">04</div>
            <div class="section-title">RANDOM SAMPLE DEMO</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("สุ่มภาพตัวอย่าง 8 ภาพจากชุดข้อมูล หรือเลือกภาพของคุณเอง")

    option = st.radio(
        "Choose source:",
        [
            "Random from Dataset",
            "Upload Your Own Images"
        ]
    )

    images = []

    if option == "Random from Dataset":

        dataset_path = "sample_dataset"
        classes = ["saliva", "sweat"]

        selected_class = random.choice(classes)
        folder = os.path.join(dataset_path, selected_class)

        if os.path.exists(folder):

            files = [
                f for f in os.listdir(folder)
                if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))
            ]

            selected = random.sample(files, min(8, len(files)))

            st.success(f"Random Class: {selected_class.capitalize()}")

            for f in selected:
                file_path = os.path.join(folder, f)

                with open(file_path, "rb") as img:
                    img_bytes = img.read()

                images.append({
                    "name": f,
                    "bytes": img_bytes
                })

        else:
            st.warning("ยังไม่มีโฟลเดอร์ sample_dataset")

    else:

        uploaded_files = st.file_uploader(
            "Upload images",
            type=["jpg", "jpeg", "png", "webp"],
            accept_multiple_files=True
        )

        if uploaded_files:

            selected = random.sample(uploaded_files, min(8, len(uploaded_files)))

            for f in selected:
                images.append({
                    "name": f.name,
                    "bytes": f.getvalue()
                })

    if images:

        st.divider()

        cols = st.columns(4)

        for i, img in enumerate(images):

            with cols[i % 4]:
                st.image(
                    img["bytes"],
                    caption=img["name"]
                )

        st.write("")

        if st.button("🔍 ANALYZE RANDOM SAMPLE →", use_container_width=True):

            st.session_state.evidence = images
            go_to("analyzing")
            st.rerun()

# ---------------------------------------------------------------------------
# PAGE: RESULTS / CASE FINDINGS
# ---------------------------------------------------------------------------
def render_results():
    st.markdown(
        """
        <div class="section-step">
            <div class="section-num">03</div>
            <div class="section-title">CASE FINDINGS</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<span class='stamp'>CASE ANALYZED ✓</span>", unsafe_allow_html=True)
    st.write("")

    results = st.session_state.results
    total = len(results)
    saliva_count = sum(1 for r in results if r["class"] == "Saliva")
    sweat_count = sum(1 for r in results if r["class"] == "Sweat")

    m1, m2, m3 = st.columns(3)
    m1.metric("Total Images", total)
    m2.metric("SALIVA", saliva_count)
    m3.metric("SWEAT", sweat_count)

    # ---- Pie chart ----
    if total > 0 and (saliva_count > 0 or sweat_count > 0):
        fig, ax = plt.subplots(figsize=(3.6, 3.6))
        fig.patch.set_alpha(0.0)
        labels, sizes, colors = [], [], []
        if saliva_count:
            labels.append("Saliva"); sizes.append(saliva_count); colors.append(COLOR_MAP["Saliva"])
        if sweat_count:
            labels.append("Sweat"); sizes.append(sweat_count); colors.append(COLOR_MAP["Sweat"])
        wedges, texts, autotexts = ax.pie(
            sizes, labels=labels, colors=colors, autopct="%1.0f%%",
            startangle=90, wedgeprops=dict(width=0.45, edgecolor="#FBF5E6", linewidth=3),
            textprops={"fontsize": 11, "color": "#3A3226"}
        )
        ax.set_title("Evidence Breakdown", fontsize=12, color="#3A3226")
        c1, c2, c3 = st.columns([1, 1.4, 1])
        with c2:
            st.pyplot(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("### 🗂️ Evidence Cards")

    for i, r in enumerate(results):
        img_uri = _to_data_uri(r["bytes"])
        badge_cls = BADGE_CLASS[r["class"]]
        bar_color = COLOR_MAP[r["class"]]
        st.markdown(
            f"""
            <div class="evidence-card">
                <div class="evidence-thumb"><img src="{img_uri}" /></div>
                <div style="flex:1; min-width:200px;">
                    <div style="font-family:'Kalam'; font-weight:700; font-size:1.1rem;">Evidence #{i+1:03d}</div>
                    <div style="color:var(--ink-soft); font-size:0.85rem; margin-bottom:6px;">{r['name']}</div>
                    <div style="margin:6px 0;">
                        <span style="font-size:0.8rem; color:var(--ink-soft);">AI CLASSIFICATION</span><br/>
                        <span class="badge {badge_cls}">{r['class'].upper()}</span>
                    </div>
                    <div style="margin-top:8px;">
                        <span style="font-size:0.8rem; color:var(--ink-soft);">CONFIDENCE — {r['confidence']}%</span>
                        <div class="confidence-bar-bg">
                            <div class="confidence-bar-fill" style="width:{r['confidence']}%; background:{bar_color};"></div>
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ---- Investigator's notes ----
    st.markdown("### 📝 Investigator's Notes")
    st.markdown("<div class='notes-frame'>", unsafe_allow_html=True)
    st.session_state.notes = st.text_area(
        "What did you discover?",
        value=st.session_state.notes,
        height=150,
        placeholder="Write your observations here...",
        label_visibility="collapsed",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    c1, c2, c3 = st.columns([1, 1.4, 1])
    with c1:
        if st.button("← Back to Evidence", use_container_width=True):
            go_to("upload")
            st.rerun()
    with c3:
        if st.button("📕 CLOSE CASE", use_container_width=True):
            go_to("closed")
            st.rerun()


# ---------------------------------------------------------------------------
# PAGE: CASE CLOSED
# ---------------------------------------------------------------------------
def render_closed():
    results = st.session_state.results
    total = len(results)
    saliva_count = sum(1 for r in results if r["class"] == "Saliva")
    sweat_count = sum(1 for r in results if r["class"] == "Sweat")

    st.markdown(
        f"""
        <div class="cover-card">
            <div class="cover-kicker">FORENSIC LAB</div>
            <div class="cover-title">📕 CASE CLOSED</div>
            <div class="case-row" style="justify-content:center; gap:2rem; margin-top:1rem;">
                <span>🗂️ Case ID: <b>{st.session_state.case_id}</b></span>
            </div>
            <div class="case-row" style="justify-content:center; gap:2rem;">
                <span>Total Evidence: <b>{total}</b></span>
                <span>Saliva: <b>{saliva_count}</b></span>
                <span>Sweat: <b>{sweat_count}</b></span>
            </div>
            <div class="closed-stamp-wrap">
                <span class="stamp">CLASSIFIED</span>
                &nbsp;&nbsp;
                <span class="stamp" style="transform:rotate(5deg); color:var(--mint-deep); border-color:var(--mint-deep);">CASE CLOSED</span>
            </div>
            <div class="cover-question">"Every stain tells a story."</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    c1, c2, c3 = st.columns([1, 1.3, 1])
    with c2:
        if st.button("📂 START A NEW CASE", use_container_width=True):
            for k in ["evidence", "results", "notes"]:
                st.session_state[k] = [] if k != "notes" else ""
            st.session_state.case_id = "DD-" + "".join(random.choices(string.digits, k=3))
            go_to("cover")
            st.rerun()


# ---------------------------------------------------------------------------
# ROUTER
# ---------------------------------------------------------------------------
PAGES = {
    "cover": render_cover,
    "case_file": render_case_file,
    "upload": render_upload,
    "analyzing": render_analyzing,
    "results": render_results,
    "closed": render_closed,
    "random": render_random_sample,
}

PAGES[st.session_state.page]()
