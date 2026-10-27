"""Streamlit UI for the LangGraph customer feedback analysis workflow."""


import html
import json
import streamlit as st

from src.app.pipelines.pipeline import customer_feedback_Analysis


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Feedback AI | Command Center",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* Global theme */
    html,
    body,
    [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #0b1020 0%, #111a30 55%, #101827 100%);
        color: #edf2ff;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #0c1325;
        border-right: 1px solid #25314b;
    }

    [data-testid="stSidebar"] * {
        color: #e5ecff;
    }

    [data-testid="stSidebar"] hr {
        border-color: #2c3b59;
    }

    /* Hero section */
    .hero {
        padding: 30px;
        border: 1px solid #344568;
        border-radius: 22px;
        background: linear-gradient(120deg, #172849, #25204b, #123b4a);
        margin-bottom: 24px;
    }

    .hero-tag {
        color: #72e4d1;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    .hero h1 {
        color: #ffffff !important;
        font-size: 36px;
        font-weight: 800;
        line-height: 1.25;
        margin: 10px 0;
    }

    .hero p {
        color: #c5d2ed !important;
        font-size: 15px;
        line-height: 1.8;
        margin-bottom: 0;
    }

    /* Headings */
    .section-title {
        font-size: 18px;
        font-weight: 700;
        color: #f0f5ff;
        margin: 12px 0 16px;
    }

    h1,
    h2,
    h3,
    h4,
    h5,
    h6 {
        color: #f0f5ff !important;
    }

    p,
    li,
    label {
        color: #e5ecff;
    }

    [data-testid="stCaptionContainer"] p {
        color: #aebbd4 !important;
    }

    /* Content panels */
    .panel {
        background: rgba(23, 34, 57, 0.92);
        border: 1px solid #2c3b59;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 16px;
        overflow-wrap: anywhere;
    }

    .panel-label {
        color: #9cafd0 !important;
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .panel-value {
        color: #f4f7ff !important;
        font-size: 21px;
        font-weight: 700;
        line-height: 1.6;
        margin-top: 8px;
        overflow-wrap: anywhere;
        word-break: break-word;
    }

    .muted {
        color: #aebbd4 !important;
        font-size: 13px;
        line-height: 1.7;
    }

    /* Text inputs */
    .stTextInput input,
    .stTextArea textarea,
    .stNumberInput input {
        background-color: #111b30 !important;
        color: #f1f5ff !important;
        -webkit-text-fill-color: #f1f5ff !important;
        caret-color: #ffffff !important;
        border: 1px solid #435575 !important;
        border-radius: 12px !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 14px !important;
    }

    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder {
        color: #8494b2 !important;
        -webkit-text-fill-color: #8494b2 !important;
        opacity: 1 !important;
    }

    .stTextInput input:focus,
    .stTextArea textarea:focus,
    .stNumberInput input:focus {
        border-color: #818cff !important;
        box-shadow: 0 0 0 2px rgba(91, 108, 255, 0.20) !important;
        outline: none !important;
    }

    .stTextInput label,
    .stTextArea label,
    .stNumberInput label,
    .stSelectbox label,
    .stMultiSelect label {
        color: #e5ecff !important;
        font-weight: 600 !important;
    }

    /* Email preview */
    .stTextArea textarea,
    .stTextArea textarea:disabled {
        background-color: #111b30 !important;
        color: #f1f5ff !important;
        -webkit-text-fill-color: #f1f5ff !important;
        opacity: 1 !important;
        line-height: 1.8 !important;
        font-size: 14px !important;
    }

    .stTextArea textarea:disabled {
        cursor: text !important;
    }

    /* Buttons */
    .stButton > button,
    .stDownloadButton > button,
    [data-testid="stFormSubmitButton"] button {
        background: linear-gradient(90deg, #5b6cff, #7c5cff) !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        border: 1px solid #7c8cff !important;
        border-radius: 11px !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        min-height: 46px;
        padding: 10px 18px;
        opacity: 1 !important;
        box-shadow: 0 4px 14px rgba(91, 108, 255, 0.20);
        transition: background 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    }

    .stButton > button *,
    .stDownloadButton > button *,
    [data-testid="stFormSubmitButton"] button * {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover,
    [data-testid="stFormSubmitButton"] button:hover {
        background: linear-gradient(90deg, #7180ff, #9675ff) !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        border-color: #c0c7ff !important;
        box-shadow: 0 6px 20px rgba(91, 108, 255, 0.35);
    }

    .stButton > button:focus-visible,
    .stDownloadButton > button:focus-visible,
    [data-testid="stFormSubmitButton"] button:focus-visible {
        outline: 2px solid #aeb8ff !important;
        outline-offset: 3px;
    }

    .stButton > button:disabled,
    .stDownloadButton > button:disabled,
    [data-testid="stFormSubmitButton"] button:disabled {
        background: #28344b !important;
        color: #aebbd4 !important;
        -webkit-text-fill-color: #aebbd4 !important;
        border-color: #3a4963 !important;
        box-shadow: none !important;
        opacity: 0.8 !important;
    }

    /* Checkbox */
    .stCheckbox {
        padding: 5px 0;
    }

    .stCheckbox label,
    .stCheckbox label p,
    .stCheckbox label span {
        color: #e5ecff !important;
        -webkit-text-fill-color: #e5ecff !important;
        font-size: 13px !important;
    }

    .stCheckbox input {
        accent-color: #7c5cff;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background: #172239;
        border: 1px solid #2c3b59;
        border-radius: 15px;
        padding: 18px;
    }

    [data-testid="stMetricLabel"],
    [data-testid="stMetricLabel"] p {
        color: #aebbd4 !important;
        font-size: 13px !important;
    }

    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-weight: 800 !important;
        overflow-wrap: anywhere;
    }

    [data-testid="stMetricDelta"] {
        color: #72e4d1 !important;
    }

    /* Expanders */
    [data-testid="stExpander"] {
        background: #121c30;
        border: 1px solid #2c3b59;
        border-radius: 12px;
        overflow: hidden;
    }

    [data-testid="stExpander"] summary {
        color: #edf2ff !important;
        background: #172239;
    }

    [data-testid="stExpander"] summary:hover {
        background: #202e49;
    }

    [data-testid="stExpander"] summary p {
        color: #edf2ff !important;
        font-weight: 600;
    }

    /* JSON output */
    [data-testid="stJson"],
    [data-testid="stCode"],
    .stJson {
        background: #111b30 !important;
        color: #e5ecff !important;
        border-radius: 10px;
    }

    pre,
    code {
        color: #dbe7ff !important;
    }

    /* Status and alerts */
    .status {
        padding: 12px 15px;
        border-radius: 10px;
        background: #172b3c;
        border: 1px solid #31556a;
        color: #b6f2e6 !important;
        font-weight: 600;
    }

    [data-testid="stAlert"] {
        border-radius: 12px;
    }

    /* Download button */
    .stDownloadButton {
        margin-top: 10px;
    }

    .stDownloadButton > button {
        width: 100%;
    }

    /* Dividers */
    hr {
        border-color: #2c3b59 !important;
    }

    /* Responsive layout */
    @media (max-width: 768px) {
        .block-container {
            padding: 1rem;
        }

        .hero {
            padding: 22px;
        }

        .hero h1 {
            font-size: 28px;
        }

        .panel {
            padding: 16px;
        }

        .panel-value {
            font-size: 18px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def display_value(value):
    """Convert dictionaries and other values into readable text."""
    if value is None:
        return "Not available"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, indent=2, ensure_ascii=False, default=str)
    return str(value)


def display_analysis(analysis):
    """Normalize analysis output from a Pydantic model, dict, or JSON string."""
    if hasattr(analysis, "model_dump"):
        return analysis.model_dump()
    if isinstance(analysis, dict):
        return analysis
    if isinstance(analysis, str):
        try:
            parsed = json.loads(analysis)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            pass
        return {"details": analysis}
    if analysis is None:
        return {}
    return {"details": display_value(analysis)}


def metric_card(label, value, help_text=None):
    """Render a Streamlit metric card."""
    st.metric(label=label, value=value, help=help_text)


def safe_html(value):
    """Escape dynamic values before inserting them into HTML."""
    return html.escape(display_value(value))


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.markdown("## 🤖 Feedback AI")
    st.caption("CUSTOMER EXPERIENCE PLATFORM")
    st.divider()

    st.markdown("### Workflow")
    st.markdown(
        """
        **01** · Sentiment classification

        **02** · Conditional routing

        **03** · Complaint analysis

        **04** · Email generation

        **05** · Email delivery
        """
    )

    st.divider()
    st.markdown("### Built with")
    st.markdown(
        """
        - Python
        - Streamlit
        - LangGraph
        - LangChain
        - Groq LLM
        - Pydantic
        """
    )
    st.divider()
    st.caption("AI-powered customer feedback automation")


# --------------------------------------------------
# HERO SECTION
# --------------------------------------------------

st.markdown(
    """
    <div class="hero">
        <div class="hero-tag">AI Automation · Live Demo</div>
        <h1>Customer Feedback<br>Command Center</h1>
        <p>
            Turn customer feedback into actionable insights.
            Classify sentiment, analyze complaints, and generate
            customer-support emails with your LangGraph workflow.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# INPUT SECTION
# --------------------------------------------------

left, right = st.columns([1.15, 0.85], gap="large")

with left:
    st.markdown(
        '<div class="section-title">✍️ Customer Feedback</div>',
        unsafe_allow_html=True,
    )

    with st.form("feedback_form"):
        customer_name = st.text_input(
            "Customer name",
            value="Alex Johnson",
            placeholder="Enter customer name",
        )

        feedback = st.text_area(
            "Feedback message",
            value=(
                "The product is good, but delivery was late "
                "and customer support did not help me."
            ),
            height=180,
            placeholder="Enter the customer's feedback...",
        )

        st.caption(
            "The feedback is passed to your existing "
            "customer_feedback_Analysis() pipeline."
        )

        acknowledge_email = st.checkbox(
            "I understand that running the workflow may send a real email."
        )

        submitted = st.form_submit_button(
            "▶  Analyze Feedback & Run Workflow",
            use_container_width=True,
        )

with right:
    st.markdown(
        '<div class="section-title">⚡ What the AI does</div>',
        unsafe_allow_html=True,
    )

    workflow_steps = [
        ("01", "Sentiment Detection", "Identify positive or negative feedback."),
        ("02", "Smart Routing", "Choose the correct LangGraph branch."),
        ("03", "Issue Analysis", "Extract issue type, tone, and severity."),
        ("04", "Email Generation", "Draft a context-aware support email."),
        ("05", "Delivery", "Execute your configured email sender."),
    ]

    for number, title, description in workflow_steps:
        st.markdown(
            f"""
            <div class="panel">
                <div class="panel-label">STEP {number}</div>
                <div class="panel-value">{title}</div>
                <div class="muted">{description}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# --------------------------------------------------
# RUN EXISTING PIPELINE
# --------------------------------------------------

if submitted:
    if not feedback.strip():
        st.error("Please enter customer feedback before continuing.")
    elif not acknowledge_email:
        st.warning(
            "Please confirm that you understand the workflow may send "
            "a real email before running it."
        )
    else:
        try:
            with st.spinner(
                "AI agents are processing feedback. Please wait..."
            ):
                result = customer_feedback_Analysis(feedback.strip(), customer_name.strip())

            if not isinstance(result, dict):
                st.error(
                    "The pipeline did not return a dictionary. "
                    "Check customer_feedback_Analysis() output."
                )
                st.stop()

            st.session_state["feedback_result"] = result
            st.session_state["customer_name"] = (
                customer_name.strip() or "Customer"
            )

            st.success("Workflow execution completed.")

        except Exception as exc:
            st.error("Workflow execution failed.")
            st.exception(exc)


# --------------------------------------------------
# RESULTS DASHBOARD
# --------------------------------------------------

result = st.session_state.get("feedback_result")

if result:
    st.divider()

    st.markdown(
        '<div class="section-title">📊 AI Analysis Dashboard</div>',
        unsafe_allow_html=True,
    )

    sentiment = str(result.get("sentiment", "Unknown")).upper()
    sentiment_reason = result.get("sentiment_reason", "Not available")
    analysis = display_analysis(result.get("analysis", {}))

    severity = str(analysis.get("severity", "N/A")).upper()
    issue_type = str(analysis.get("issue_type", "N/A")).replace("_", " ").title()
    tone = str(analysis.get("tone", "N/A")).title()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card("Sentiment", sentiment)

    with col2:
        metric_card("Issue Type", issue_type)

    with col3:
        metric_card("Severity", severity)

    with col4:
        metric_card("Customer Tone", tone)

    # ----------------------------------------------
    # SENTIMENT DETAILS
    # ----------------------------------------------

    st.markdown("### 🧠 Sentiment Intelligence")

    sentiment_col, reason_col = st.columns([0.7, 1.3])

    with sentiment_col:
        st.markdown(
            f"""
            <div class="panel">
                <div class="panel-label">DETECTED SENTIMENT</div>
                <div class="panel-value">{safe_html(sentiment)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with reason_col:
        st.markdown(
            f"""
            <div class="panel">
                <div class="panel-label">AI REASONING</div>
                <div class="muted">{safe_html(sentiment_reason)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ----------------------------------------------
    # ISSUE ANALYSIS
    # ----------------------------------------------

    st.markdown("### 🔎 Complaint Analysis")

    summary = analysis.get("summary", "Not available")
    suggested_action = analysis.get("suggested_action", "Not available")

    detail_col, action_col = st.columns(2)

    with detail_col:
        st.markdown(
            f"""
            <div class="panel">
                <div class="panel-label">ISSUE SUMMARY</div>
                <div class="panel-value">{safe_html(summary)}</div>
                <br>
                <div class="panel-label">EMOTIONAL TONE</div>
                <div class="muted">{safe_html(tone)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with action_col:
        st.markdown(
            f"""
            <div class="panel">
                <div class="panel-label">RECOMMENDED NEXT ACTION</div>
                <div class="panel-value">{safe_html(suggested_action)}</div>
                <br>
                <div class="panel-label">ISSUE CATEGORY</div>
                <div class="muted">{safe_html(issue_type)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with st.expander("View complete structured analysis"):
        st.json(analysis)

    # ----------------------------------------------
    # GENERATED EMAIL
    # ----------------------------------------------

    st.markdown("### ✉️ Generated Customer Email")

    email_subject = result.get("email_subject", "")
    email_body = result.get("email_body", "")

    email_col, status_col = st.columns([1.5, 0.7])

    with email_col:
        st.markdown(
            f"""
            <div class="panel">
                <div class="panel-label">EMAIL SUBJECT</div>
                <div class="panel-value">{safe_html(email_subject)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.text_area(
            "Email body preview",
            value=display_value(email_body),
            height=300,
            disabled=True,
            key="email_preview",
            help="The email body generated by your AI workflow.",
        )

        if email_body:
            st.download_button(
                "⬇️ Download email body",
                data=display_value(email_body),
                file_name="customer_support_email.txt",
                mime="text/plain",
            )

    with status_col:
        email_status = str(result.get("email_status", "Unknown"))

        st.markdown(
            f"""
            <div class="panel">
                <div class="panel-label">DELIVERY STATUS</div>
                <div class="panel-value">{safe_html(email_status.upper())}</div>
                <p class="muted">
                    Status returned by your existing email-sender node.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("**Workflow result**")

        st.write(
            "Positive branch"
            if sentiment == "POSITIVE"
            else "Negative-feedback branch"
        )

        st.caption(
            "The displayed status reflects the pipeline result; "
            "it does not independently verify inbox delivery."
        )

    # ----------------------------------------------
    # COMPLETE OUTPUT
    # ----------------------------------------------

    st.markdown("### 🧾 Complete Pipeline Output")

    with st.expander("Inspect raw result returned by the pipeline"):
        st.json(result)

    st.download_button(
        "⬇️ Download complete analysis as JSON",
        data=json.dumps(result, indent=2, ensure_ascii=False, default=str),
        file_name="customer_feedback_analysis.json",
        mime="application/json",
    )

else:
    st.info(
        "Your analysis will appear here after you run the workflow."
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Customer Feedback AI Command Center · "
    "Powered by Streamlit, LangGraph, LangChain and Groq"
)
