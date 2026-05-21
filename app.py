import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import math
import csv
import os

st.set_page_config(
    page_title="Stylr AI",
    page_icon="logo.png",
    layout="wide"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;500;600;700&display=swap');
    
    .stApp {
        background-color: #0a0a0a;
        color: #e8e8e8;
    }
    
    .stApp, .stApp *:not(.main-title):not(.hero-title):not(.section-title) {
        font-family: 'Inter', -apple-system, sans-serif;
    }
    
    .main-title {
        font-family: 'Playfair Display', serif !important;
        font-size: 3.5rem;
        font-weight: 600;
        background: linear-gradient(90deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.02em;
        line-height: 1;
        margin: 0;
        padding: 0;
    }
    
    .hero-title {
        font-family: 'Playfair Display', serif !important;
        font-size: 5rem;
        font-weight: 600;
        background: linear-gradient(90deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.03em;
        line-height: 1;
        text-align: center;
        margin: 2rem 0 1rem 0;
    }
    
    .hero-subtitle {
        font-family: 'Inter', sans-serif;
        text-align: center;
        color: #aaa;
        font-size: 1.3rem;
        font-weight: 300;
        line-height: 1.6;
        max-width: 800px;
        margin: 0 auto 3rem auto;
        padding: 0 2rem;
        display: block;
    }
    
    .section-title {
        font-family: 'Playfair Display', serif !important;
        font-size: 2.5rem;
        font-weight: 500;
        color: #f5f5f5;
        text-align: center;
        margin: 4rem 0 1rem 0;
        letter-spacing: -0.02em;
    }
    
    .section-subtitle {
        text-align: center;
        color: #888;
        font-size: 1rem;
        font-weight: 300;
        letter-spacing: 0.05em;
        margin-bottom: 3rem;
    }
    
    .subtitle {
        text-align: center;
        color: #888;
        font-size: 0.95rem;
        font-weight: 300;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-top: 0.5rem;
        margin-bottom: 3rem;
    }
    
    h2, h3, h4 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 600;
        letter-spacing: -0.01em;
        color: #f5f5f5;
    }
    
    h4 {
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: #999;
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #2a2a2a;
    }
    
    .step-heading {
        font-size: 1.5rem;
        font-weight: 500;
        color: #f5f5f5;
        margin-bottom: 0.3rem;
    }
    
    .step-number {
        color: #667eea;
        font-weight: 600;
        margin-right: 0.5rem;
    }
    
    .step-card {
        background: #111;
        padding: 2rem;
        border-radius: 4px;
        border: 1px solid #1a1a1a;
        text-align: center;
        height: 100%;
    }
    
    .step-card-number {
        font-family: 'Playfair Display', serif;
        font-size: 3rem;
        background: linear-gradient(90deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        line-height: 1;
    }
    
    .step-card-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #fff;
        margin-bottom: 0.75rem;
    }
    
    .step-card-desc {
        font-size: 0.95rem;
        color: #999;
        line-height: 1.6;
    }
    
    .feature-block {
        padding: 2rem 1.5rem;
        border-left: 2px solid #667eea;
        margin: 1.5rem 0;
        background: #0d0d0d;
    }
    
    .feature-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #fff;
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        font-size: 0.95rem;
        color: #aaa;
        line-height: 1.6;
    }
    
    .faq-item {
        padding: 1.5rem 0;
        border-bottom: 1px solid #1a1a1a;
    }
    
    .faq-question {
        font-size: 1.1rem;
        font-weight: 600;
        color: #fff;
        margin-bottom: 0.5rem;
    }
    
    .faq-answer {
        font-size: 0.95rem;
        color: #999;
        line-height: 1.7;
    }
    
    .stButton > button {
        background-color: #1a1a1a;
        color: #e8e8e8;
        border: 1px solid #2a2a2a;
        border-radius: 4px;
        padding: 0.6rem 1.2rem;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        letter-spacing: 0.02em;
        transition: all 0.2s ease;
        font-size: 0.85rem;
    }
    
    .stButton > button:hover {
        background-color: #2a2a2a;
        border-color: #667eea;
        color: #fff;
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #667eea, #764ba2);
        border: none;
        font-weight: 600;
        font-size: 1rem;
        padding: 0.85rem 2rem;
    }
    
    .stButton > button[kind="primary"]:hover {
        opacity: 0.9;
        transform: translateY(-1px);
    }
    
    .profile-card {
        background: #111;
        padding: 1.5rem;
        border-radius: 4px;
        border: 1px solid #2a2a2a;
        margin: 1rem 0;
    }
    
    .profile-card h4 {
        font-size: 0.7rem;
        margin-top: 0;
        margin-bottom: 1rem;
        border: none;
        padding-bottom: 0;
    }
    
    .profile-card p {
        margin: 0.3rem 0;
        font-size: 0.95rem;
    }
    
    .product-card {
        background: #0f0f0f;
        padding: 1.2rem;
        border-radius: 4px;
        border: 1px solid #1a1a1a;
        margin-bottom: 1rem;
        transition: border-color 0.2s ease;
    }
    
    .product-card:hover {
        border-color: #2a2a2a;
    }
    
    .score-badge {
        background: linear-gradient(90deg, #667eea, #764ba2);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 2px;
        font-weight: 600;
        font-size: 0.75rem;
        display: inline-block;
        letter-spacing: 0.05em;
    }
    
    .help-box {
        background: #111;
        padding: 1.2rem 1.5rem;
        border-radius: 4px;
        border-left: 2px solid #667eea;
        margin: 1.5rem 0;
        font-size: 0.9rem;
        color: #ccc;
    }
    
    .error-box {
        background: #1a0a0a;
        padding: 1.5rem;
        border-radius: 4px;
        border-left: 2px solid #ff6b6b;
        margin: 1.5rem 0;
    }
    
    .section-label {
        color: #888;
        font-size: 0.7rem;
        letter-spacing: 0.25em;
        text-transform: uppercase;
        margin-bottom: 0.75rem;
        margin-top: 2rem;
        font-weight: 500;
    }
    
    .section-divider {
        border-top: 1px solid #1a1a1a;
        margin: 2rem 0 1rem 0;
    }
    
    .big-divider {
        border-top: 1px solid #2a2a2a;
        margin: 5rem 0 3rem 0;
    }
    
    .stFileUploader > div {
        background-color: #111;
        border: 1px dashed #2a2a2a;
        border-radius: 4px;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .block-container {
        padding-top: 2rem;
        max-width: 1200px;
    }
    
    .stMarkdown p {
        font-size: 0.95rem;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

mp_pose = mp.solutions.pose

BUDGET_LABELS = {
    "under-100": "Under \\$100",
    "100-300": "\\$100 to \\$300",
    "300-plus": "\\$300+"
}

ACCESSORY_CATEGORIES = {"hats", "eyewear", "jewelry", "watches", "bags", "belts"}

fit_scores = {
    "Inverted Triangle": {"slim": 90, "slim-straight": 95, "straight": 85, "tapered": 90, "relaxed": 75, "skinny": 30, "wide": 70, "chunky": 80, "athletic": 85},
    "Triangle": {"slim": 70, "slim-straight": 75, "straight": 70, "tapered": 80, "relaxed": 60, "skinny": 50, "wide": 40, "chunky": 60, "athletic": 70},
    "Rectangle": {"slim": 85, "slim-straight": 90, "straight": 85, "tapered": 85, "relaxed": 75, "skinny": 60, "wide": 70, "chunky": 75, "athletic": 85},
    "Hourglass": {"slim": 95, "slim-straight": 90, "straight": 75, "tapered": 80, "relaxed": 60, "skinny": 80, "wide": 70, "chunky": 70, "athletic": 80},
    "Pear": {"slim": 75, "slim-straight": 80, "straight": 75, "tapered": 70, "relaxed": 65, "skinny": 60, "wide": 50, "chunky": 60, "athletic": 70}
}


def analyze_image(image_bytes, gender_pref, progress_callback=None):
    if progress_callback:
        progress_callback("Loading image...")
    
    try:
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if image is None:
            return None, "Could not read the image file. Please try a different photo."
    except Exception:
        return None, "Image loading failed. Try a different photo."
    
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    height, width = image.shape[:2]
    
    if height < 400 or width < 200:
        return None, "Photo is too small. Try a larger photo."
    
    if progress_callback:
        progress_callback("Detecting body landmarks...")
    
    try:
        with mp_pose.Pose(static_image_mode=True, model_complexity=1) as pose:
            results = pose.process(image_rgb)
    except Exception:
        return None, "Body detection failed. Try a clearer photo."
    
    if not results.pose_landmarks:
        return None, "Could not detect a body. Stand facing camera, full body visible, good lighting."
    
    landmarks = results.pose_landmarks.landmark
    
    key_landmarks_visibility = [
        landmarks[11].visibility, landmarks[12].visibility,
        landmarks[23].visibility, landmarks[24].visibility,
        landmarks[27].visibility,
    ]
    
    if sum(key_landmarks_visibility) / len(key_landmarks_visibility) < 0.3:
        return None, "Could not see your full body clearly."
    
    if progress_callback:
        progress_callback("Analyzing body shape...")
    
    def distance(p1, p2):
        return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)
    
    class Point:
        pass
    
    def midpoint(p1, p2):
        m = Point()
        m.x = (p1.x + p2.x) / 2
        m.y = (p1.y + p2.y) / 2
        return m
    
    left_shoulder = landmarks[11]
    right_shoulder = landmarks[12]
    left_hip = landmarks[23]
    right_hip = landmarks[24]
    left_ankle = landmarks[27]
    mouth_left = landmarks[9]
    mouth_right = landmarks[10]
    
    shoulder_width = distance(left_shoulder, right_shoulder)
    hip_width = distance(left_hip, right_hip)
    torso_length = distance(midpoint(left_shoulder, right_shoulder), midpoint(left_hip, right_hip))
    leg_length = distance(left_hip, left_ankle)
    
    if shoulder_width == 0 or hip_width == 0 or leg_length == 0:
        return None, "Could not measure body proportions."
    
    shoulder_to_hip_ratio = shoulder_width / hip_width
    torso_to_leg_ratio = torso_length / leg_length
    
    if gender_pref == "womens":
        if shoulder_to_hip_ratio > 1.05:
            body_shape = "Inverted Triangle"
        elif shoulder_to_hip_ratio < 0.85:
            body_shape = "Pear"
        elif 0.95 <= shoulder_to_hip_ratio <= 1.05:
            body_shape = "Hourglass"
        else:
            body_shape = "Rectangle"
    else:
        if shoulder_to_hip_ratio > 1.15:
            body_shape = "Inverted Triangle"
        elif shoulder_to_hip_ratio < 0.95:
            body_shape = "Triangle"
        else:
            body_shape = "Rectangle"
    
    if torso_to_leg_ratio < 0.70:
        proportion = "Long-legged"
    elif torso_to_leg_ratio > 0.85:
        proportion = "Long-torso"
    else:
        proportion = "Balanced"
    
    if progress_callback:
        progress_callback("Analyzing skin tone...")
    
    try:
        neck_center = Point()
        neck_center.x = (left_shoulder.x + right_shoulder.x) / 2
        mouth_y = (mouth_left.y + mouth_right.y) / 2
        shoulder_y = (left_shoulder.y + right_shoulder.y) / 2
        neck_center.y = mouth_y + (shoulder_y - mouth_y) * 0.4
        
        samples = []
        for x_offset in [-0.03, 0, 0.03]:
            x = int((neck_center.x + x_offset) * width)
            y = int(neck_center.y * height)
            patch_size = 12
            x1, y1 = max(0, x - patch_size), max(0, y - patch_size)
            x2, y2 = min(width, x + patch_size), min(height, y + patch_size)
            patch = image_rgb[y1:y2, x1:x2]
            if patch.size > 0:
                samples.append(np.mean(patch, axis=(0, 1)))
        
        if not samples:
            return None, "Could not sample skin tone."
        
        avg_skin_rgb = np.mean(samples, axis=0)
        rgb_pixel = np.uint8([[avg_skin_rgb]])
        lab_pixel = cv2.cvtColor(rgb_pixel, cv2.COLOR_RGB2LAB)[0][0]
        L, a, b = lab_pixel
        
        if L < 80:
            depth = "Deep"
        elif L < 130:
            depth = "Medium"
        elif L < 180:
            depth = "Light-Medium"
        else:
            depth = "Light"
        
        warm_score = int(b) - 128
        cool_score = int(a) - 128
        
        if warm_score > cool_score + 3:
            undertone = "Warm"
        elif cool_score > warm_score + 3:
            undertone = "Cool"
        else:
            undertone = "Neutral"
    except Exception:
        depth = "Medium"
        undertone = "Neutral"
        avg_skin_rgb = [128, 128, 128]
    
    return {
        "body_shape": body_shape,
        "proportion": proportion,
        "shoulder_to_hip": round(float(shoulder_to_hip_ratio), 2),
        "skin_depth": depth,
        "undertone": undertone,
        "skin_rgb": [int(avg_skin_rgb[0]), int(avg_skin_rgb[1]), int(avg_skin_rgb[2])],
        "gender_pref": gender_pref
    }, None


def score_undertone(item_undertone, user_undertone):
    user_lower = user_undertone.lower()
    item_lower = item_undertone.lower()
    if item_lower == user_lower:
        return 100
    elif item_lower == "neutral":
        return 80
    elif user_lower == "neutral":
        return 70
    else:
        return 30


def score_tags(item_tags_str, user_tags):
    if not item_tags_str or not user_tags:
        return 50
    item_tags = set(item_tags_str.split(","))
    user_set = set(user_tags)
    overlap = item_tags.intersection(user_set)
    if not overlap:
        return 25
    return round(40 + ((len(overlap) / len(user_set)) * 60))


def score_material(item_material_str, user_materials):
    if not user_materials:
        return 50
    if not item_material_str:
        return 40
    if set(item_material_str.split(",")).intersection(set(user_materials)):
        return 90
    return 20


def score_pattern(item_pattern, user_patterns):
    if not user_patterns:
        return 50
    if not item_pattern:
        return 40
    if item_pattern in user_patterns:
        return 95
    return 25


def score_color_category(item_color_cat, user_color_cats):
    if not user_color_cats:
        return 50
    if not item_color_cat:
        return 40
    if set(item_color_cat.split(",")).intersection(set(user_color_cats)):
        return 90
    return 30


def filter_budget(item_budget, user_budget):
    if user_budget == "any":
        return True
    return item_budget == user_budget


def score_item(item, profile, user_tags, user_materials, user_patterns, user_colors):
    body_shape = profile["body_shape"]
    undertone = profile["undertone"]
    category = item.get("category", "")
    
    if category in ACCESSORY_CATEGORIES:
        fit_score = 100
    else:
        fit_score = fit_scores.get(body_shape, {}).get(item["fit"], 50)
    
    undertone_score = score_undertone(item["undertone_match"], undertone)
    tags_to_use = item.get("ai_tags") or item.get("tags", "")
    tag_score = score_tags(tags_to_use, user_tags)
    material_score = score_material(item.get("material", ""), user_materials)
    pattern_score = score_pattern(item.get("pattern", ""), user_patterns)
    color_score = score_color_category(item.get("color_category", ""), user_colors)
    
    if category in ACCESSORY_CATEGORIES:
        final_score = (undertone_score * 0.30 + tag_score * 0.30 + pattern_score * 0.15 + color_score * 0.15 + material_score * 0.10)
    else:
        final_score = (fit_score * 0.25 + undertone_score * 0.20 + tag_score * 0.20 + material_score * 0.15 + pattern_score * 0.10 + color_score * 0.10)
    
    reasons = []
    if category not in ACCESSORY_CATEGORIES and fit_score >= 85:
        reasons.append(f"great fit for {body_shape}")
    if undertone_score >= 90:
        reasons.append(f"matches your {undertone.lower()} undertone")
    if material_score >= 90:
        reasons.append("material match")
    if pattern_score >= 90:
        reasons.append("pattern match")
    
    item_tags = set(tags_to_use.split(","))
    matched = item_tags.intersection(set(user_tags))
    if matched:
        reasons.append(f"matches: {', '.join(matched)}")
    
    return round(final_score, 1), reasons


# =========================================================================
# STATE
# =========================================================================

if "profile" not in st.session_state:
    st.session_state.profile = None
if "step" not in st.session_state:
    st.session_state.step = "landing"
if "gender_pref" not in st.session_state:
    st.session_state.gender_pref = None
if "selected_tags" not in st.session_state:
    st.session_state.selected_tags = []
if "selected_materials" not in st.session_state:
    st.session_state.selected_materials = []
if "selected_patterns" not in st.session_state:
    st.session_state.selected_patterns = []
if "selected_colors" not in st.session_state:
    st.session_state.selected_colors = []
if "selected_budget" not in st.session_state:
    st.session_state.selected_budget = "any"


# =========================================================================
# HEADER (always visible)
# =========================================================================

# Centered logo + wordmark
col_a, col_b, col_c = st.columns([1, 2, 1])
with col_b:
    sub_a, sub_b = st.columns([1, 3])
    with sub_a:
        st.image("logo.png", width=80)
    with sub_b:
        st.markdown('<h1 class="main-title" style="text-align: left; padding-top: 0.5rem; margin: 0;">Stylr AI</h1>', unsafe_allow_html=True)

st.markdown('<p class="subtitle">Built around you . Built around your style</p>', unsafe_allow_html=True)


# =========================================================================
# LANDING PAGE
# =========================================================================

if st.session_state.step == "landing":
    
    # HERO
    st.markdown('<h1 class="hero-title">A stylist that<br>actually sees you.</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Stylr analyzes your body shape and skin tone, then recommends real clothing from real brands. Made for you. Not for everyone.</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Get Started", type="primary", use_container_width=True, key="hero_cta"):
            st.session_state.step = "gender"
            st.rerun()
    
    # HOW IT WORKS
    st.markdown('<div class="big-divider"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">How it works</h2>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Three steps. Two minutes. Real recommendations.</p>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="step-card">
            <div class="step-card-number">01</div>
            <div class="step-card-title">Upload your photo</div>
            <div class="step-card-desc">A single full-body photo. We analyze body shape and skin undertone using computer vision.</div>
        </div>
        """, unsafe_allow_html=True)
    
    with c2:
        st.markdown("""
        <div class="step-card">
            <div class="step-card-number">02</div>
            <div class="step-card-title">Pick your style</div>
            <div class="step-card-desc">Choose your aesthetic. Energy, fit, materials, colors, patterns, budget. As detailed as you want.</div>
        </div>
        """, unsafe_allow_html=True)
    
    with c3:
        st.markdown("""
        <div class="step-card">
            <div class="step-card-number">03</div>
            <div class="step-card-title">Shop the match</div>
            <div class="step-card-desc">Get curated picks across tops, bottoms, jewelry, accessories. Direct links to real products.</div>
        </div>
        """, unsafe_allow_html=True)
    
    # WHY STYLR
    st.markdown('<div class="big-divider"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Why Stylr</h2>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">What separates us from a generic shopping feed</p>', unsafe_allow_html=True)
    
    fc1, fc2 = st.columns(2)
    with fc1:
        st.markdown("""
        <div class="feature-block">
            <div class="feature-title">Built around your body</div>
            <div class="feature-desc">Every body shape has fits that work and fits that don't. We map your proportions to clothing geometry. Inverted Triangle. Rectangle. Hourglass. Pear. The science of dressing well, automated.</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-block">
            <div class="feature-title">Color theory, applied</div>
            <div class="feature-desc">Your skin undertone determines which colors elevate you and which fight you. We extract it from your photo, then recommend a palette that flatters. Warm. Cool. Neutral. Each undertone gets different picks.</div>
        </div>
        """, unsafe_allow_html=True)
    
    with fc2:
        st.markdown("""
        <div class="feature-block">
            <div class="feature-title">Real products. Real brands.</div>
            <div class="feature-desc">No mockups. No fake catalog. Hundreds of pieces from established brands. Every recommendation is shoppable. Direct links to the source.</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-block">
            <div class="feature-title">Granular control</div>
            <div class="feature-desc">Want streetwear, but only in neutrals, only in cotton, under $100? Done. The more you tell us, the sharper the picks. Or pick nothing and let the engine surprise you.</div>
        </div>
        """, unsafe_allow_html=True)
    
    # FAQ
    st.markdown('<div class="big-divider"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Questions</h2>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">The stuff people ask</p>', unsafe_allow_html=True)
    
    faq_items = [
        ("Is my photo stored anywhere?", "No. Your photo is analyzed in real time and immediately discarded. We never save images. Only the derived measurements (body shape, undertone) are kept during your session."),
        ("How accurate is the body shape detection?", "We use MediaPipe, the same computer vision tech behind Google's pose detection. With a clear full-body photo, accuracy is high. Bad lighting or partial photos reduce accuracy, in which case we ask you to retake."),
        ("Why these specific brands?", "We started with brands known for quality construction and intentional design. Taylor Stitch, Aimé Leon Dore, Outerknown, Stussy, Miansai. More brands and major retailers are being added."),
        ("Do you make money on this?", "Eventually, through affiliate partnerships when you click through and buy. We do not change recommendations based on commission. The matching is based on what fits you."),
        ("Can I save my profile?", "Not yet. Each session starts fresh. Saved profiles and outfit history are on the roadmap."),
        ("Does this work for any body type or gender?", "Yes. We support men's, women's, and unisex modes with shape rules tailored to each. The matching algorithm is the same regardless.")
    ]
    
    for question, answer in faq_items:
        st.markdown(f"""
        <div class="faq-item">
            <div class="faq-question">{question}</div>
            <div class="faq-answer">{answer}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # FINAL CTA
    st.markdown('<div class="big-divider"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title" style="margin-bottom: 2rem;">Ready?</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Start now", type="primary", use_container_width=True, key="footer_cta"):
            st.session_state.step = "gender"
            st.rerun()
    
    st.markdown('<br><br>', unsafe_allow_html=True)


# =========================================================================
# STEP 1: GENDER
# =========================================================================

elif st.session_state.step == "gender":
    st.markdown('<h2 class="step-heading"><span class="step-number">01</span>How do you dress?</h2>', unsafe_allow_html=True)
    st.caption("This helps us recommend appropriate fits and brands")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Men's", use_container_width=True, key="g_men"):
            st.session_state.gender_pref = "mens"
            st.session_state.step = "upload"
            st.rerun()
    
    with col2:
        if st.button("Women's", use_container_width=True, key="g_women"):
            st.session_state.gender_pref = "womens"
            st.session_state.step = "upload"
            st.rerun()
    
    with col3:
        if st.button("Unisex", use_container_width=True, key="g_both"):
            st.session_state.gender_pref = "all"
            st.session_state.step = "upload"
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Back to home"):
        st.session_state.step = "landing"
        st.rerun()


# =========================================================================
# STEP 2: UPLOAD
# =========================================================================

elif st.session_state.step == "upload":
    pref_label = {"mens": "Men's", "womens": "Women's", "all": "Unisex"}[st.session_state.gender_pref]
    st.markdown('<h2 class="step-heading"><span class="step-number">02</span>Upload your photo</h2>', unsafe_allow_html=True)
    st.caption(f"Style preference . {pref_label}")
    
    st.markdown("""
    <div class="help-box">
    <b style="color: #fff;">For best results</b><br>
    Full body in frame . Stand facing the camera . Good lighting . JPG, PNG, or WebP
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Choose a photo", type=["jpg", "jpeg", "png", "webp"])
    
    if uploaded_file is not None:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.image(uploaded_file, caption="Your photo", use_container_width=True)
        
        with col2:
            status_placeholder = st.empty()
            spinner_placeholder = st.empty()
            
            with spinner_placeholder:
                with st.spinner("Analyzing..."):
                    image_bytes = uploaded_file.read()
                    
                    def update_status(msg):
                        status_placeholder.info(msg)
                    
                    profile, error_msg = analyze_image(image_bytes, st.session_state.gender_pref, update_status)
            
            status_placeholder.empty()
            spinner_placeholder.empty()
            
            if error_msg:
                st.markdown(f"""
                <div class="error-box">
                <h4 style="color: #ff6b6b; margin-top: 0; border: none; padding: 0;">Analysis Failed</h4>
                <p style="white-space: pre-line; margin: 0; color: #ccc;">{error_msg}</p>
                </div>
                """, unsafe_allow_html=True)
            elif profile is None:
                st.error("Something went wrong.")
            else:
                st.session_state.profile = profile
                st.success("Analysis complete")
                
                st.markdown(f"""
                <div class="profile-card">
                    <h4>BODY</h4>
                    <p><b>Shape</b> . {profile['body_shape']}</p>
                    <p><b>Proportion</b> . {profile['proportion']}</p>
                </div>
                
                <div class="profile-card">
                    <h4>SKIN</h4>
                    <p><b>Depth</b> . {profile['skin_depth']}</p>
                    <p><b>Undertone</b> . {profile['undertone']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("Next: Pick your style", type="primary"):
                    st.session_state.step = "tags"
                    st.rerun()
    
    if st.button("Change preference"):
        st.session_state.step = "gender"
        st.rerun()


# =========================================================================
# STEP 3: TAGS
# =========================================================================

elif st.session_state.step == "tags":
    profile = st.session_state.profile
    st.markdown('<h2 class="step-heading"><span class="step-number">03</span>Pick your style</h2>', unsafe_allow_html=True)
    st.caption(f"Profile . {profile['body_shape']} . {profile['undertone']} undertone")
    
    tag_groups = {
        "ENERGY": ["minimalist", "bold", "muted"],
        "FIT": ["tailored", "relaxed", "tapered"],
        "AESTHETIC": ["streetwear", "workwear", "prep", "athleisure", "grunge", "y2k", "techwear", "vintage"],
        "OCCASION": ["everyday", "going-out", "office", "gym"]
    }
    
    for group, tags in tag_groups.items():
        st.markdown(f'<p class="section-label">{group}</p>', unsafe_allow_html=True)
        cols_per_row = min(len(tags), 4)
        rows_needed = (len(tags) + cols_per_row - 1) // cols_per_row
        
        for row_idx in range(rows_needed):
            cols = st.columns(cols_per_row)
            row_tags = tags[row_idx * cols_per_row:(row_idx + 1) * cols_per_row]
            for i, tag in enumerate(row_tags):
                with cols[i]:
                    is_selected = tag in st.session_state.selected_tags
                    label = f"✓ {tag}" if is_selected else tag
                    button_type = "primary" if is_selected else "secondary"
                    if st.button(label, key=f"tag_{tag}", type=button_type, use_container_width=True):
                        if is_selected:
                            st.session_state.selected_tags.remove(tag)
                        else:
                            st.session_state.selected_tags.append(tag)
                        st.rerun()
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    st.markdown('<p class="section-label">COLOR PALETTE</p>', unsafe_allow_html=True)
    color_options = [("earth-tones", "Earth Tones"), ("neutrals", "Neutrals"), ("cool-tones", "Cool Tones")]
    cols = st.columns(3)
    for i, (key, label) in enumerate(color_options):
        with cols[i]:
            is_selected = key in st.session_state.selected_colors
            disp_label = f"✓ {label}" if is_selected else label
            button_type = "primary" if is_selected else "secondary"
            if st.button(disp_label, key=f"color_{key}", type=button_type, use_container_width=True):
                if is_selected:
                    st.session_state.selected_colors.remove(key)
                else:
                    st.session_state.selected_colors.append(key)
                st.rerun()
    
    st.markdown('<p class="section-label">MATERIAL</p>', unsafe_allow_html=True)
    material_options = [("cotton", "Cotton"), ("linen", "Linen"), ("wool", "Wool / Knit"), ("denim", "Denim"), ("leather", "Leather"), ("technical", "Technical")]
    
    for row_idx in range(2):
        cols = st.columns(3)
        for i in range(3):
            idx = row_idx * 3 + i
            if idx >= len(material_options):
                break
            key, label = material_options[idx]
            with cols[i]:
                is_selected = key in st.session_state.selected_materials
                disp_label = f"✓ {label}" if is_selected else label
                button_type = "primary" if is_selected else "secondary"
                if st.button(disp_label, key=f"mat_{key}", type=button_type, use_container_width=True):
                    if is_selected:
                        st.session_state.selected_materials.remove(key)
                    else:
                        st.session_state.selected_materials.append(key)
                    st.rerun()
    
    st.markdown('<p class="section-label">PATTERN</p>', unsafe_allow_html=True)
    pattern_options = [("solid", "Solid"), ("stripes", "Stripes"), ("plaid", "Plaid / Check"), ("graphic", "Graphic"), ("floral", "Floral"), ("geometric", "Geometric")]
    
    for row_idx in range(2):
        cols = st.columns(3)
        for i in range(3):
            idx = row_idx * 3 + i
            if idx >= len(pattern_options):
                break
            key, label = pattern_options[idx]
            with cols[i]:
                is_selected = key in st.session_state.selected_patterns
                disp_label = f"✓ {label}" if is_selected else label
                button_type = "primary" if is_selected else "secondary"
                if st.button(disp_label, key=f"pat_{key}", type=button_type, use_container_width=True):
                    if is_selected:
                        st.session_state.selected_patterns.remove(key)
                    else:
                        st.session_state.selected_patterns.append(key)
                    st.rerun()
    
    st.markdown('<p class="section-label">BUDGET</p>', unsafe_allow_html=True)
    budget_options = [("any", "Any Price"), ("under-100", "Under \\$100"), ("100-300", "\\$100 to \\$300"), ("300-plus", "\\$300+")]
    
    cols = st.columns(4)
    for i, (key, label) in enumerate(budget_options):
        with cols[i]:
            is_selected = st.session_state.selected_budget == key
            disp_label = f"✓ {label}" if is_selected else label
            button_type = "primary" if is_selected else "secondary"
            if st.button(disp_label, key=f"budget_{key}", type=button_type, use_container_width=True):
                st.session_state.selected_budget = key
                st.rerun()
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    selections = []
    if st.session_state.selected_tags:
        selections.append(f"Style: {', '.join(st.session_state.selected_tags)}")
    if st.session_state.selected_colors:
        selections.append(f"Colors: {', '.join(st.session_state.selected_colors)}")
    if st.session_state.selected_materials:
        selections.append(f"Materials: {', '.join(st.session_state.selected_materials)}")
    if st.session_state.selected_patterns:
        selections.append(f"Patterns: {', '.join(st.session_state.selected_patterns)}")
    if st.session_state.selected_budget != "any":
        selections.append(f"Budget: {BUDGET_LABELS[st.session_state.selected_budget]}")
    
    summary_text = " . ".join(selections) if selections else "Make selections above"
    st.markdown(f"<p style='color: #999; font-size: 0.85rem; margin-top: 1rem;'><b>Selected . </b>{summary_text}</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Back"):
            st.session_state.step = "upload"
            st.rerun()
    with col2:
        if len(st.session_state.selected_tags) >= 1:
            if st.button("View recommendations", type="primary"):
                st.session_state.step = "results"
                st.rerun()


# =========================================================================
# STEP 4: RESULTS
# =========================================================================

elif st.session_state.step == "results":
    profile = st.session_state.profile
    user_tags = st.session_state.selected_tags
    user_materials = st.session_state.selected_materials
    user_patterns = st.session_state.selected_patterns
    user_colors = st.session_state.selected_colors
    user_budget = st.session_state.selected_budget
    gender_pref = st.session_state.gender_pref
    
    st.markdown('<h2 class="step-heading">Your recommendations</h2>', unsafe_allow_html=True)
    
    filters_active = []
    filters_active.append(f"{', '.join(user_tags)}")
    if user_colors:
        filters_active.append(', '.join(user_colors))
    if user_materials:
        filters_active.append(', '.join(user_materials))
    if user_patterns:
        filters_active.append(', '.join(user_patterns))
    if user_budget != "any":
        filters_active.append(BUDGET_LABELS[user_budget])
    
    st.caption(f"{gender_pref} . {' . '.join(filters_active)}")
    
    catalog_file = "smart_catalog.csv" if os.path.exists("smart_catalog.csv") else "real_catalog.csv"
    
    if not os.path.exists(catalog_file):
        st.markdown('<div class="error-box"><h4 style="color: #ff6b6b; margin-top: 0; border: none; padding: 0;">Catalog Unavailable</h4></div>', unsafe_allow_html=True)
    else:
        try:
            catalog = []
            with open(catalog_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                catalog = list(reader)
        except Exception:
            st.error("Could not load catalog.")
            catalog = []
        
        if catalog:
            if gender_pref == "mens":
                catalog = [item for item in catalog if item.get("gender") in ("mens", "unisex")]
            elif gender_pref == "womens":
                catalog = [item for item in catalog if item.get("gender") in ("womens", "unisex")]
            
            catalog = [item for item in catalog if filter_budget(item.get("budget_tier", "any"), user_budget)]
            
            scored_items = []
            for item in catalog:
                try:
                    score, reasons = score_item(item, profile, user_tags, user_materials, user_patterns, user_colors)
                    scored_items.append({**item, "score": score, "reasons": reasons})
                except Exception:
                    continue
            
            scored_items.sort(key=lambda x: x["score"], reverse=True)
            
            category_order = ["tops", "bottoms", "outerwear", "shoes", "hats", "eyewear", "watches", "jewelry", "bags", "belts"]
            category_labels = {
                "tops": "TOPS", "bottoms": "BOTTOMS", "outerwear": "OUTERWEAR",
                "shoes": "SHOES", "hats": "HATS", "eyewear": "EYEWEAR",
                "watches": "WATCHES", "jewelry": "JEWELRY", "bags": "BAGS", "belts": "BELTS"
            }
            
            categories_shown = 0
            for category in category_order:
                cat_items = [i for i in scored_items if i["category"] == category]
                top_3 = cat_items[:3]
                
                if not top_3:
                    continue
                
                categories_shown += 1
                st.markdown(f"#### {category_labels[category]}")
                cols = st.columns(3)
                
                for i, item in enumerate(top_3):
                    with cols[i]:
                        st.markdown(f'<div class="product-card">', unsafe_allow_html=True)
                        
                        image_url = item.get("image_url", "").strip()
                        if image_url and image_url.startswith("http"):
                            try:
                                st.image(image_url, use_container_width=True)
                            except Exception:
                                st.markdown("<p style='color: #555;'>Image unavailable</p>", unsafe_allow_html=True)
                        else:
                            st.markdown("<p style='color: #555;'>No image</p>", unsafe_allow_html=True)
                        
                        st.markdown(f"<p style='color: #fff; font-weight: 500; margin-top: 0.75rem; margin-bottom: 0.25rem;'>{item['name'][:50]}</p>", unsafe_allow_html=True)
                        
                        price = item.get('price', 'N/A')
                        brand = item.get('brand', 'Unknown')
                        st.markdown(f"<p style='color: #888; font-size: 0.85rem; margin-bottom: 0.5rem;'>\\${price} . {brand}</p>", unsafe_allow_html=True)
                        
                        st.markdown(f'<span class="score-badge">{item["score"]}/100</span>', unsafe_allow_html=True)
                        
                        reasons_text = " . ".join(item["reasons"]) if item["reasons"] else "decent match"
                        st.markdown(f"<p style='color: #777; font-size: 0.8rem; margin-top: 0.75rem; margin-bottom: 0.5rem;'>{reasons_text}</p>", unsafe_allow_html=True)
                        
                        if item.get("url"):
                            st.link_button("View Product", item["url"])
                        st.markdown('</div>', unsafe_allow_html=True)
            
            if categories_shown == 0:
                st.markdown('<div class="error-box"><h4 style="color: #ff6b6b; margin-top: 0; border: none; padding: 0;">No Matches</h4><p style="margin: 0; color: #ccc;">Try different tags or relax your filters.</p></div>', unsafe_allow_html=True)
    
    st.markdown("<br><hr style='border-color: #2a2a2a;'><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Change tags"):
            st.session_state.step = "tags"
            st.rerun()
    with col2:
        if st.button("Change preference"):
            st.session_state.step = "gender"
            st.session_state.selected_tags = []
            st.session_state.selected_materials = []
            st.session_state.selected_patterns = []
            st.session_state.selected_colors = []
            st.session_state.selected_budget = "any"
            st.rerun()
    with col3:
        if st.button("Start over"):
            st.session_state.step = "landing"
            st.session_state.profile = None
            st.session_state.selected_tags = []
            st.session_state.selected_materials = []
            st.session_state.selected_patterns = []
            st.session_state.selected_colors = []
            st.session_state.selected_budget = "any"
            st.rerun()