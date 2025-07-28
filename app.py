import streamlit as st
import json
import os

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

# Sidebar controls
st.sidebar.header("Controls")

def save_progress():
    with open(SAVE_FILE, "w") as f:
        json.dump(st.session_state.answers, f)
    st.sidebar.success("Progress saved.")

def load_progress():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
        if isinstance(data, dict):
            st.session_state.answers = data
            st.session_state.step = len(data)
            st.sidebar.success("Progress loaded.")
        else:
            st.sidebar.error("Saved data corrupted.")
    else:
        st.sidebar.error("No saved data found.")

def restart_assessment():
    st.session_state.step = 0
    st.session_state.answers = {}
    st.session_state.diagnosis = None
    st.session_state.feedback_submitted = False
    st.sidebar.info("Assessment restarted.")

if st.sidebar.button("💾 Save Progress"):
    save_progress()
if st.sidebar.button("📂 Load Progress"):
    load_progress()
if st.sidebar.button("🔄 Restart Assessment"):
    restart_assessment()
if st.sidebar.button("📤 Export Data"):
    st.sidebar.download_button("Download answers as JSON", json.dumps(st.session_state.answers), "answers.json")

# Data privacy info
with st.expander("🔒 Data Privacy and Consent"):
    st.write("""
        Your responses are stored locally on your device and are not shared.  
        You may save or export your data anytime.  
        This assessment is NOT a diagnostic tool. Please seek professional help for diagnosis.
    """)

# Consent page
def show_consent():
    st.title("🧠 Neuropsychological Adaptive Assessment")
    st.markdown("""
    **Please read and agree to the following before proceeding:**  
    - This tool is for educational and screening purposes only, **NOT a clinical diagnosis**.  
    - Your data is stored locally and can be saved or exported.  
    - If you feel distressed at any point, please use the crisis resources provided.  
    """)
    consent = st.checkbox("I have read and agree to the terms above.", key="consent")
    if consent:
        if st.button("Continue"):
            st.session_state.consent_given = True

# Questions & clinical scales
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

def show_question(index):
    q = questions[index]
    default_idx = 0
    if q["key"] in st.session_state.answers:
        try:
            default_idx = options_4.index(st.session_state.answers[q["key"]])
        except ValueError:
            default_idx = 0
    ans = st.radio(q["text"], options_4, index=default_idx, key=q["key"])
    st.session_state.answers[q["key"]] = ans

def analyze(answers):
    phq_keys = ["phq1","phq2","phq3","phq4","phq5","phq6","phq7","phq8","phq9"]
    gad_keys = ["gad1","gad2","gad3","gad4","gad5","gad6","gad7"]

    phq_score = sum(options_4.index(answers.get(k,"Not at all")) for k in phq_keys)
    gad_score = sum(options_4.index(answers.get(k,"Not at all")) for k in gad_keys)

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
    st.subheader("🛠️ Immediate Coping Strategies")
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
    st.write(f"Question {step+1} of {len(questions)}")

# Main UI Flow
def main():
    if not st.session_state.consent_given:
        show_consent()
        st.stop()

    step = st.session_state.step
    total_questions = len(questions)

    if step < total_questions:
        show_progress(step)
        show_question(step)
        if st.button("Next"):
            with st.spinner("Loading next question..."):
                st.session_state.step += 1
    else:
        st.success("✅ Assessment Complete")
        diagnosis, phq_score, gad_score = analyze(st.session_state.answers)
        st.session_state.diagnosis = diagnosis

        st.write("### 🧠 Results")
        st.write("**Diagnosis:**")
        for d in diagnosis:
            st.write(f"- {d}")
        st.write(f"**PHQ-9 Score:** {phq_score} (Depression severity)")
        st.write(f"**GAD-7 Score:** {gad_score} (Anxiety severity)")

        coping_tips(diagnosis)
        display_resources(diagnosis)

        if not st.session_state.feedback_submitted:
            st.subheader("Feedback")
            feedback = st.text_area("Please share your feedback or thoughts on this assessment:")
            if st.button("Submit Feedback"):
                # Save or process feedback here
                st.session_state.feedback_submitted = True
                st.success("Thank you for your feedback!")
        else:
            st.info("Feedback already submitted. Thank you!")

        if st.button("🔄 Restart Assessment"):
            restart_assessment()

if __name__ == "__main__":
    main()
