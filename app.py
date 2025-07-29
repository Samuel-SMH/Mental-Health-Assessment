import streamlit as st
import json
import os
import pandas as pd  # For map data frame
# import openai  # Removed as requested

# ---------------- AI-Driven Adaptive Question Generator ----------------

def get_next_question(step, answers):
    base_questions = [
        {
            "text": "How often have you felt down, depressed, or hopeless in the last two weeks?",
            "options": ["Not at all", "Several days", "More than half the days", "Nearly every day"],
            "key": "q1"
        },
        {
            "text": "Have you had trouble sleeping or sleeping too much?",
            "options": ["Not at all", "Sometimes", "Often", "Almost always"],
            "key": "q2"
        },
        {
            "text": "Do you experience panic attacks?",
            "options": ["Never", "Rarely", "Sometimes", "Often"],
            "key": "q3"
        },
        {
            "text": "Do you find it hard to relax?",
            "options": ["Not at all", "Sometimes", "Often", "Almost always"],
            "key": "q4"
        },
        {
            "text": "Have you lost interest or pleasure in doing things?",
            "options": ["Not at all", "Several days", "More than half the days", "Nearly every day"],
            "key": "q5"
        }
    ]

    # Adaptive logic to prioritize deeper assessment if symptoms are more severe
    if step < len(base_questions):
        return base_questions[step]
    else:
        return {
            "text": language_data[st.session_state.language]["resources_offer"],
            "options": [language_data[st.session_state.language]["yes"], language_data[st.session_state.language]["no"]],
            "key": "q_end"
        }


st.set_page_config(page_title="Neuropsychological Adaptive Assessment", layout="centered")

SAVE_FILE = "saved_answers.json"

# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "diagnosis" not in st.session_state:
    st.session_state.diagnosis = None
if "consent_given" not in st.session_state:
    st.session_state.consent_given = False
if "feedback_submitted" not in st.session_state:
    st.session_state.feedback_submitted = False
if "language" not in st.session_state:
    st.session_state.language = "English"  # Default language

# ---------------- Multilingual Support ----------------

language_data = {
    "English": {
        "save_progress": "💾 Save Progress",
        "load_progress": "📂 Load Progress",
        "restart_assessment": "🔄 Restart Assessment",
        "export_data": "📤 Export Data",
        "select_language": "Select Language",
        "data_privacy_title": "🔒 Data Privacy and Consent",
        "data_privacy_text": """Your responses are stored locally on your device and are not shared.  
You may save or export your data anytime.  
This assessment is NOT a diagnostic tool. Please seek professional help for diagnosis.""",
        "consent_title": "🧠 GreyMatter AI Mental Health Assessment",
        "consent_english": """**Please read and agree to the following before proceeding:**  
- This tool is for educational and screening purposes only, **NOT a clinical diagnosis**.  
- Your data is stored locally and can be saved or exported.  
- If you feel distressed at any point, please use the crisis resources provided.""",
        "consent_spanish": """**Por favor lea y acepte lo siguiente antes de continuar:**  
- Esta herramienta es solo para propósitos educativos y de evaluación, **NO un diagnóstico clínico**.  
- Sus datos se almacenan localmente y pueden guardarse o exportarse.  
- Si se siente angustiado en algún momento, use los recursos de crisis proporcionados.""",
        "consent_agree_english": "I have read and agree to the terms above.",
        "consent_agree_spanish": "He leído y acepto los términos anteriores.",
        "continue_button": "Continue",
        "continuar_button": "Continuar",
        "resources_offer": "Would you like to receive resources or care options?",
        "yes": "Yes, show me options",
        "no": "No, thank you",
        "next": "Next",
        "assessment_complete": "✅ Assessment Complete! 🎉",
        "results_title": "### 🧠 Results",
        "diagnosis_label": "**Diagnosis:**",
        "phq_label": "**PHQ-9 Score:**",
        "gad_label": "**GAD-7 Score:**",
        "feedback_prompt": "Please share your feedback or thoughts on this assessment:",
        "submit_feedback": "Submit Feedback",
        "feedback_thanks": "Thank you for your feedback!",
        "feedback_already": "Feedback already submitted. Thank you!",
        "coping_title": "🛠️ Immediate Coping Strategies",
        "map_title": "📍 Houston Mental Health Facilities Map & Contact Info"
    },
    "Spanish": {
        "save_progress": "💾 Guardar Progreso",
        "load_progress": "📂 Cargar Progreso",
        "restart_assessment": "🔄 Reiniciar Evaluación",
        "export_data": "📤 Exportar Datos",
        "select_language": "Seleccione Idioma",
        "data_privacy_title": "🔒 Privacidad de Datos y Consentimiento",
        "data_privacy_text": """Sus respuestas se almacenan localmente en su dispositivo y no se comparten.  
Puede guardar o exportar sus datos en cualquier momento.  
Esta evaluación NO es una herramienta de diagnóstico. Por favor, busque ayuda profesional para un diagnóstico.""",
        "consent_title": "🧠 Evaluación de Salud Mental GreyMatter AI",
        "consent_english": """**Please read and agree to the following before proceeding:**  
- This tool is for educational and screening purposes only, **NOT a clinical diagnosis**.  
- Your data is stored locally and can be saved or exported.  
- If you feel distressed at any point, please use the crisis resources provided.""",
        "consent_spanish": """**Por favor lea y acepte lo siguiente antes de continuar:**  
- Esta herramienta es solo para propósitos educativos y de evaluación, **NO un diagnóstico clínico**.  
- Sus datos se almacenan localmente y pueden guardarse o exportarse.  
- Si se siente angustiado en algún momento, use los recursos de crisis proporcionados.""",
        "consent_agree_english": "I have read and agree to the terms above.",
        "consent_agree_spanish": "He leído y acepto los términos anteriores.",
        "continue_button": "Continue",
        "continuar_button": "Continuar",
        "resources_offer": "¿Le gustaría recibir recursos u opciones de atención?",
        "yes": "Sí, muéstrame opciones",
        "no": "No, gracias",
        "next": "Siguiente",
        "assessment_complete": "✅ ¡Evaluación Completa! 🎉",
        "results_title": "### 🧠 Resultados",
        "diagnosis_label": "**Diagnóstico:**",
        "phq_label": "**Puntaje PHQ-9:**",
        "gad_label": "**Puntaje GAD-7:**",
        "feedback_prompt": "Por favor, comparta sus comentarios o pensamientos sobre esta evaluación:",
        "submit_feedback": "Enviar Comentarios",
        "feedback_thanks": "¡Gracias por sus comentarios!",
        "feedback_already": "Comentarios ya enviados. ¡Gracias!",
        "coping_title": "🛠️ Estrategias de Afrontamiento Inmediatas",
        "map_title": "📍 Mapa de Instalaciones de Salud Mental en Houston"
    },
    "Français": {
        "save_progress": "💾 Enregistrer la progression",
        "load_progress": "📂 Charger la progression",
        "restart_assessment": "🔄 Recommencer l'évaluation",
        "export_data": "📤 Exporter les données",
        "select_language": "Choisir la langue",
        "data_privacy_title": "🔒 Confidentialité des données et consentement",
        "data_privacy_text": """Vos réponses sont stockées localement sur votre appareil et ne sont pas partagées.  
Vous pouvez sauvegarder ou exporter vos données à tout moment.  
Cette évaluation N'EST PAS un outil de diagnostic. Veuillez consulter un professionnel pour un diagnostic.""",
        "consent_title": "🧠 Évaluation de santé mentale GreyMatter AI",
        "consent_english": """**Please read and agree to the following before proceeding:**  
- This tool is for educational and screening purposes only, **NOT a clinical diagnosis**.  
- Your data is stored locally and can be saved or exported.  
- If you feel distressed at any point, please use the crisis resources provided.""",
        "consent_spanish": """**Veuillez lire et accepter ce qui suit avant de continuer:**  
- Cet outil est uniquement à des fins éducatives et de dépistage, **PAS un diagnostic clinique**.  
- Vos données sont stockées localement et peuvent être sauvegardées ou exportées.  
- Si vous vous sentez en détresse à tout moment, veuillez utiliser les ressources de crise fournies.""",
        "consent_agree_english": "I have read and agree to the terms above.",
        "consent_agree_spanish": "J'ai lu et j'accepte les termes ci-dessus.",
        "continue_button": "Continuer",
        "continuar_button": "Continuer",
        "resources_offer": "Souhaitez-vous recevoir des ressources ou options de soins ?",
        "yes": "Oui, montrez-moi les options",
        "no": "Non, merci",
        "next": "Suivant",
        "assessment_complete": "✅ Évaluation terminée ! 🎉",
        "results_title": "### 🧠 Résultats",
        "diagnosis_label": "**Diagnostic :**",
        "phq_label": "**Score PHQ-9 :**",
        "gad_label": "**Score GAD-7 :**",
        "feedback_prompt": "Merci de partager vos commentaires ou réflexions sur cette évaluation :",
        "submit_feedback": "Envoyer les commentaires",
        "feedback_thanks": "Merci pour vos commentaires !",
        "feedback_already": "Commentaires déjà soumis. Merci !",
        "coping_title": "🛠️ Stratégies d'adaptation immédiates",
        "map_title": "📍 Carte des établissements de santé mentale de Houston"
    },
    "中文": {
        "save_progress": "💾 保存进度",
        "load_progress": "📂 载入进度",
        "restart_assessment": "🔄 重新开始评估",
        "export_data": "📤 导出数据",
        "select_language": "选择语言",
        "data_privacy_title": "🔒 数据隐私和同意",
        "data_privacy_text": """您的回答保存在本地设备上，不会被分享。  
您可以随时保存或导出您的数据。  
此评估不是诊断工具。请寻求专业帮助以获得诊断。""",
        "consent_title": "🧠 GreyMatter AI心理健康评估",
        "consent_english": """**Please read and agree to the following before proceeding:**  
- This tool is for educational and screening purposes only, **NOT a clinical diagnosis**.  
- Your data is stored locally and can be saved or exported.  
- If you feel distressed at any point, please use the crisis resources provided.""",
        "consent_spanish": """**请在继续之前阅读并同意以下内容：**  
- 本工具仅用于教育和筛查目的，**不是临床诊断**。  
- 您的数据保存在本地，可以保存或导出。  
- 如果您感到不适，请使用提供的危机资源。""",
        "consent_agree_english": "I have read and agree to the terms above.",
        "consent_agree_spanish": "我已阅读并同意上述条款。",
        "continue_button": "继续",
        "continuar_button": "继续",
        "resources_offer": "您想接收资源或护理选项吗？",
        "yes": "是的，显示选项",
        "no": "不，谢谢",
        "next": "下一步",
        "assessment_complete": "✅ 评估完成！ 🎉",
        "results_title": "### 🧠 结果",
        "diagnosis_label": "**诊断：**",
        "phq_label": "**PHQ-9评分：**",
        "gad_label": "**GAD-7评分：**",
        "feedback_prompt": "请分享您对本次评估的反馈或想法：",
        "submit_feedback": "提交反馈",
        "feedback_thanks": "感谢您的反馈！",
        "feedback_already": "反馈已提交。谢谢！",
        "coping_title": "🛠️ 立即应对策略",
        "map_title": "📍 休斯顿心理健康设施地图及联系方式"
    }
}
# ---------------- Sidebar controls ----------------

st.sidebar.header("Controls")

def save_progress():
    with open(SAVE_FILE, "w") as f:
        json.dump(st.session_state.answers, f)
    st.sidebar.success(language_data[st.session_state.language]["save_progress"])

def load_progress():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
        if isinstance(data, dict):
            st.session_state.answers = data
            st.session_state.step = len(data)
            st.sidebar.success(language_data[st.session_state.language]["load_progress"])
        else:
            st.sidebar.error("Saved data corrupted.")
    else:
        st.sidebar.error("No saved data found.")

def restart_assessment():
    st.session_state.step = 0
    st.session_state.answers = {}
    st.session_state.diagnosis = None
    st.session_state.feedback_submitted = False
    st.sidebar.info(language_data[st.session_state.language]["restart_assessment"])

if st.sidebar.button(language_data[st.session_state.language]["save_progress"]):
    save_progress()
if st.sidebar.button(language_data[st.session_state.language]["load_progress"]):
    load_progress()
if st.sidebar.button(language_data[st.session_state.language]["restart_assessment"]):
    restart_assessment()
if st.sidebar.button(language_data[st.session_state.language]["export_data"]):
    st.sidebar.download_button(language_data[st.session_state.language]["export_data"],
                               json.dumps(st.session_state.answers), "answers.json")

# Language selector in sidebar
lang = st.sidebar.selectbox(language_data[st.session_state.language]["select_language"],
                            list(language_data.keys()),
                            index=list(language_data.keys()).index(st.session_state.language))
st.session_state.language = lang

# Data privacy info
with st.expander(language_data[st.session_state.language]["data_privacy_title"]):
    st.write(language_data[st.session_state.language]["data_privacy_text"])

# Consent page
def show_consent():
    st.title(language_data[st.session_state.language]["consent_title"])
    if st.session_state.language == "English":
        st.markdown(language_data["English"]["consent_english"])
        consent = st.checkbox(language_data["English"]["consent_agree_english"], key="consent")
        if consent and st.button(language_data["English"]["continue_button"]):
            st.session_state.consent_given = True
    elif st.session_state.language == "Spanish":
        st.markdown(language_data["Spanish"]["consent_spanish"])
        consent = st.checkbox(language_data["Spanish"]["consent_agree_spanish"], key="consent")
        if consent and st.button(language_data["Spanish"]["continuar_button"]):
            st.session_state.consent_given = True
    elif st.session_state.language == "Français":
        st.markdown(language_data["Français"]["consent_spanish"])
        consent = st.checkbox(language_data["Français"]["consent_agree_spanish"], key="consent")
        if consent and st.button(language_data["Français"]["continuar_button"]):
            st.session_state.consent_given = True
    else:  # 中文
        st.markdown(language_data["中文"]["consent_spanish"])
        consent = st.checkbox(language_data["中文"]["consent_agree_spanish"], key="consent")
        if consent and st.button(language_data["中文"]["continuar_button"]):
            st.session_state.consent_given = True

# ---------------- Questions & clinical scales ----------------

questions = [
    {"text": "Little interest or pleasure in doing things?", "key": "phq1"},
    {"text": "Feeling down, depressed, or hopeless?", "key": "phq2"},
    {"text": "Trouble falling or staying asleep, or sleeping too much?", "key": "phq3"},
    {"text": "Feeling tired or having little energy?", "key": "phq4"},
    {"text": "Poor appetite or overeating?", "key": "phq5"},
    {"text": "Feeling bad about yourself — or that you are a failure?", "key": "phq6"},
    {"text": "Trouble concentrating on things, such as reading or watching TV?", "key": "phq7"},
    {"text": "Moving or speaking so slowly that other people notice? Or the opposite — being restless?", "key": "phq8"},
    {"text": "Thoughts that you would be better off dead or hurting yourself?", "key": "phq9"},
    {"text": "Feeling nervous, anxious, or on edge?", "key": "gad1"},
    {"text": "Not being able to stop or control worrying?", "key": "gad2"},
    {"text": "Worrying too much about different things?", "key": "gad3"},
    {"text": "Trouble relaxing?", "key": "gad4"},
    {"text": "Being so restless that it’s hard to sit still?", "key": "gad5"},
    {"text": "Becoming easily annoyed or irritable?", "key": "gad6"},
    {"text": "Feeling afraid as if something awful might happen?", "key": "gad7"},
    {"text": "Do you experience panic attacks or sudden overwhelming fear?", "key": "panic"},
    {"text": "Do you have unwanted repetitive thoughts or compulsions?", "key": "ocd"},
    {"text": "Have you experienced traumatic events that affect you now?", "key": "trauma"},
]

options_4 = ["Not at all", "Several days", "More than half the days", "Nearly every day"]

@st.cache_data
def cached_options_index_map():
    return {opt: i for i, opt in enumerate(options_4)}

def show_question(index):
    q = questions[index]
    default_idx = 0
    if q["key"] in st.session_state.answers:
        try:
            default_idx = cached_options_index_map()[st.session_state.answers[q["key"]]]
        except KeyError:
            default_idx = 0
    ans = st.radio(q["text"], options_4, index=default_idx, key=q["key"])
    st.session_state.answers[q["key"]] = ans

@st.cache_data
def analyze_cached(answers):
    phq_keys = ["phq1","phq2","phq3","phq4","phq5","phq6","phq7","phq8","phq9"]
    gad_keys = ["gad1","gad2","gad3","gad4","gad5","gad6","gad7"]

    options_index = cached_options_index_map()

    phq_score = sum(options_index.get(answers.get(k,"Not at all"), 0) for k in phq_keys)
    gad_score = sum(options_index.get(answers.get(k,"Not at all"), 0) for k in gad_keys)

    panic = answers.get("panic","Not at all")
    ocd = answers.get("ocd","Not at all")
    trauma = answers.get("trauma","Not at all")

    diagnosis = []

    # Depression levels
    if phq_score >= 20:
        diagnosis.append("Severe Depression — Symptoms significantly impacting daily life; professional evaluation recommended.")
    elif phq_score >= 15:
        diagnosis.append("Moderately Severe Depression — Noticeable symptoms; consider seeking support.")
    elif phq_score >= 10:
        diagnosis.append("Moderate Depression — Some symptoms present; monitor and consider support.")
    elif phq_score >= 5:
        diagnosis.append("Mild Depression — Minor symptoms; maintain self-care.")
    else:
        diagnosis.append("Minimal or No Depression")

    # Anxiety levels
    if gad_score >= 15:
        diagnosis.append("Severe Anxiety — Symptoms are intense; professional help is advised.")
    elif gad_score >= 10:
        diagnosis.append("Moderate Anxiety — Symptoms noticeable; self-care and support recommended.")
    elif gad_score >= 5:
        diagnosis.append("Mild Anxiety — Mild symptoms; practice relaxation techniques.")
    else:
        diagnosis.append("Minimal or No Anxiety")

    if panic in ["More than half the days", "Nearly every day"]:
        diagnosis.append("Panic Symptoms — Consider therapy targeting panic attacks.")

    if ocd in ["More than half the days", "Nearly every day"]:
        diagnosis.append("Obsessive-Compulsive Symptoms — Professional assessment suggested.")

    if trauma in ["More than half the days", "Nearly every day"]:
        diagnosis.append("Possible PTSD or Trauma Impact — Trauma-informed support recommended.")

    return diagnosis, phq_score, gad_score

def display_resources(diagnosis):
    crisis_links = """
**If you are in crisis or need immediate support:**  
- **988 Suicide & Crisis Lifeline (US):** Dial **988** or visit [988lifeline.org](https://988lifeline.org)  
- **Crisis Text Line:** Text **HELLO** to **741741**  
- **Find international crisis helplines:** [findahelpline.com](https://findahelpline.com)
"""
    st.markdown(crisis_links)

    resources = {
        "Severe Depression — Symptoms significantly impacting daily life; professional evaluation recommended.": [
            ("National Suicide Prevention Lifeline", "https://suicidepreventionlifeline.org/"),
            ("Psychology Today - Depression Therapists", "https://www.psychologytoday.com/us/therapists/depression"),
            ("Depression and Bipolar Support Alliance", "https://www.dbsalliance.org/"),
            ("Self-help Apps: MoodKit, CBT Tools, Happify", "https://www.psycom.net/best-mental-health-apps"),
        ],
        "Moderately Severe Depression — Noticeable symptoms; consider seeking support.": [
            ("National Suicide Prevention Lifeline", "https://suicidepreventionlifeline.org/"),
            ("Psychology Today - Depression Therapists", "https://www.psychologytoday.com/us/therapists/depression"),
        ],
        "Moderate Depression — Some symptoms present; monitor and consider support.": [
            ("Psychology Today - Depression Therapists", "https://www.psychologytoday.com/us/therapists/depression"),
        ],
        "Severe Anxiety — Symptoms are intense; professional help is advised.": [
            ("Anxiety and Depression Association of America", "https://adaa.org/"),
            ("Psychology Today - Anxiety Therapists", "https://www.psychologytoday.com/us/therapists/anxiety"),
            ("Calm App (Meditation)", "https://www.calm.com/"),
            ("Headspace App", "https://www.headspace.com/"),
        ],
        "Moderate Anxiety — Symptoms noticeable; self-care and support recommended.": [
            ("Anxiety and Depression Association of America", "https://adaa.org/"),
            ("Psychology Today - Anxiety Therapists", "https://www.psychologytoday.com/us/therapists/anxiety"),
        ],
        "Panic Symptoms — Consider therapy targeting panic attacks.": [
            ("Anxiety and Depression Association of America", "https://adaa.org/"),
            ("National Panic Disorder Association", "https://panicdisorder.org/"),
        ],
        "Obsessive-Compulsive Symptoms — Professional assessment suggested.": [
            ("International OCD Foundation", "https://iocdf.org/"),
            ("NOCD App", "https://www.treatmyocd.com/"),
        ],
        "Possible PTSD or Trauma Impact — Trauma-informed support recommended.": [
            ("National Center for PTSD", "https://www.ptsd.va.gov/"),
            ("SAMHSA Trauma and Violence Info", "https://www.samhsa.gov/trauma-violence"),
            ("PTSD Coach App", "https://www.ptsd.va.gov/appvid/mobile/PTSDCoach.asp"),
        ],
    }

    shown = set()
    for d in diagnosis:
        if d in resources and d not in shown:
            st.markdown(f"### Resources for {d}:")
            for name, link in resources[d]:
                st.markdown(f"- [{name}]({link})")
            shown.add(d)

def coping_tips(diagnosis):
    st.subheader(language_data[st.session_state.language]["coping_title"])
    if any("Depression" in d for d in diagnosis):
        st.markdown("""
        - Try to maintain a routine and set small daily goals  
        - Get some sunlight and physical activity  
        - Practice mindfulness or meditation apps like Headspace or Calm  
        - Reach out to trusted friends or family  
        """)
    if any("Anxiety" in d or "Panic" in d for d in diagnosis):
        st.markdown("""
        - Practice deep breathing: Inhale 4 sec, hold 7 sec, exhale 8 sec  
        - Ground yourself by naming 5 things you can see, 4 hear, 3 feel  
        - Use progressive muscle relaxation techniques  
        - Avoid caffeine and limit screen time before bed  
        """)
    if any("Obsessive" in d for d in diagnosis):
        st.markdown("Consider consulting professionals who specialize in OCD treatments and exposure therapy.")
    if any("PTSD" in d or "Trauma" in d for d in diagnosis):
        st.markdown("Engage in trauma-informed therapy and consider support groups specialized for PTSD.")

def show_progress(step):
    progress = step / len(questions)
    st.progress(progress)
    st.write(f"{language_data[st.session_state.language]['next']} {step+1} / {len(questions)}")

# -- Map function --

def show_simple_map_with_facilities():
    st.subheader(language_data[st.session_state.language]["map_title"])

    facilities = [
        {
            "name": "Houston Behavioral Health",
            "lat": 29.7604,
            "lon": -95.3698,
            "url": "https://houstonbehavioralhealth.org"
        },
        {
            "name": "Memorial Hermann Behavioral Health",
            "lat": 29.7499,
            "lon": -95.3584,
            "url": "https://www.memorialhermann.org/services/behavioral-health"
        },
        {
            "name": "Legacy Community Health",
            "lat": 29.7633,
            "lon": -95.3633,
            "url": "https://legacycommunityhealth.org/services/behavioral-health"
        },
        {
            "name": "Houston Methodist Behavioral Health",
            "lat": 29.7455,
            "lon": -95.3550,
            "url": "https://www.houstonmethodist.org/care-treatment/behavioral-health"
        },
    ]

    df = pd.DataFrame({
        "lat": [f["lat"] for f in facilities],
        "lon": [f["lon"] for f in facilities],
        "name": [f["name"] for f in facilities],
        "url": [f["url"] for f in facilities]
    })

    st.map(df[["lat", "lon"]])

    st.markdown("### Facility Details & Links")
    for f in facilities:
        st.markdown(f"- [{f['name']}]({f['url']})")

# ---------------- Main UI Flow ----------------

def main():
    if not st.session_state.consent_given:
        show_consent()
        st.stop()

    step = st.session_state.step
    total_questions = len(questions)

    if step < total_questions:
        show_progress(step)
        show_question(step)
        if st.button(language_data[st.session_state.language]["next"]):
            with st.spinner("Loading next question..."):
                st.session_state.step += 1
    else:
        st.markdown(language_data[st.session_state.language]["assessment_complete"])

        diagnosis, phq_score, gad_score = analyze_cached(st.session_state.answers)
        st.session_state.diagnosis = diagnosis

        st.markdown(language_data[st.session_state.language]["results_title"])
        st.markdown(language_data[st.session_state.language]["diagnosis_label"])
        for d in diagnosis:
            st.write(f"- {d}")
        st.write(f"{language_data[st.session_state.language]['phq_label']} {phq_score} (Depression severity)")
        st.write(f"{language_data[st.session_state.language]['gad_label']} {gad_score} (Anxiety severity)")

        coping_tips(diagnosis)
        display_resources(diagnosis)

        # AI-driven adaptive follow-up question
        q = get_next_question(step, st.session_state.answers)
        if q and q['key'] not in st.session_state.answers:
            user_resp = st.radio(q['text'], q['options'], key=q['key'])
            st.session_state.answers[q['key']] = user_resp

        if not st.session_state.feedback_submitted:
            st.subheader("Feedback")
            feedback = st.text_area(language_data[st.session_state.language]["feedback_prompt"])
            if st.button(language_data[st.session_state.language]["submit_feedback"]):
                # Save or process feedback here
                st.session_state.feedback_submitted = True
                st.success(language_data[st.session_state.language]["feedback_thanks"])
        else:
            st.info(language_data[st.session_state.language]["feedback_already"])

        if st.button(language_data[st.session_state.language]["restart_assessment"]):
            restart_assessment()

    # Removed OpenAI Chatbot code and calls here

    # Show the Houston mental health facilities map last
    show_simple_map_with_facilities()

if __name__ == "__main__":
    main()
