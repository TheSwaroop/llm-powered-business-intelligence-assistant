import streamlit as st
from src.assistant import BusinessIntelligenceAssistant

st.set_page_config(
    page_title="InsightIQ | Business Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Visual system ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');

:root {
    --ink: #17243b;
    --muted: #68758b;
    --line: #e7ebf2;
    --blue: #4169e1;
    --blue-soft: #edf2ff;
    --canvas: #f6f8fc;
}
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: var(--canvas); color: var(--ink); }
.block-container { padding-top: 1.8rem; padding-bottom: 3rem; max-width: 1440px; }
[data-testid="stSidebar"] {
    background: #111c31;
    border-right: 1px solid #26334b;
}
[data-testid="stSidebar"] * { color: #e8edf8 !important; }
[data-testid="stSidebar"] .stCaption { color: #aab6cc !important; }
[data-testid="stSidebar"] hr { border-color: #34415a; }
[data-testid="stSidebar"] [data-testid="stAlert"] {
    background: #1c2b45; border: 1px solid #344765; color: #dbe6ff;
}
h1, h2, h3 { font-family: 'Manrope', sans-serif !important; letter-spacing: -0.035em; color: var(--ink); }
.hero {
    background: linear-gradient(120deg, #172844 0%, #294b82 60%, #4169e1 100%);
    border-radius: 22px; padding: 28px 32px; color: white; margin-bottom: 24px;
    box-shadow: 0 14px 34px rgba(30, 55, 100, .13);
}
.hero h1 { color: white !important; font-size: 2.05rem; margin: 0 0 7px 0; }
.hero p { color: #dce7ff; margin: 0; font-size: 1rem; }
.eyebrow { color: #b9ccff; font-size: .72rem; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; margin-bottom: 10px; }
.metric-card {
    background: white; border: 1px solid var(--line); border-radius: 16px;
    padding: 17px 19px; min-height: 104px; box-shadow: 0 4px 14px rgba(28, 45, 75, .035);
}
.metric-label { color: var(--muted); font-size: .78rem; font-weight: 600; margin-bottom: 8px; }
.metric-value { color: var(--ink); font-family: 'Manrope'; font-size: 1.5rem; font-weight: 800; }
.section-kicker { color: #71809a; font-size: .72rem; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; margin-bottom: 5px; }
.panel {
    background: white; border: 1px solid var(--line); border-radius: 18px;
    padding: 22px 24px; box-shadow: 0 5px 18px rgba(28, 45, 75, .035);
}
.answer-panel {
    background: white; border: 1px solid #dfe7fb; border-left: 4px solid var(--blue);
    border-radius: 16px; padding: 22px 24px; box-shadow: 0 5px 18px rgba(28, 45, 75, .04);
}
.source-card {
    background: #fbfcff; border: 1px solid var(--line); border-radius: 12px;
    padding: 14px 16px; margin: 8px 0;
}
.source-meta { color: #68758b; font-size: .76rem; margin-bottom: 7px; }
div.stButton > button {
    border-radius: 10px; font-weight: 600; border: 1px solid #dbe3f2;
    min-height: 42px;
}
div.stButton > button[kind="primary"] {
    background: #4169e1; border-color: #4169e1; color: white;
}
div.stButton > button:hover { border-color: #4169e1; color: #3156c5; }
div.stButton > button[kind="primary"]:hover { color: white; background: #3156c5; }
.stTextArea textarea {
    border-radius: 12px !important; border: 1px solid #dce3ef !important;
    background: white !important; font-size: .96rem !important;
}
[data-testid="stDataFrame"] { border: 1px solid var(--line); border-radius: 12px; overflow: hidden; }
footer { visibility: hidden; }
#MainMenu { visibility: hidden; }
@media (max-width: 700px) {
    .hero { padding: 22px; }
    .hero h1 { font-size: 1.55rem; }
    .panel, .answer-panel { padding: 17px; }
}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_assistant():
    return BusinessIntelligenceAssistant()

assistant = get_assistant()

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## ◈ InsightIQ")
    st.caption("BUSINESS INTELLIGENCE WORKSPACE")
    st.markdown("---")
    st.markdown("### Workspace")
    st.markdown("**●**  Ask the data")
    st.markdown("**◌**  Documents & records")
    st.markdown("---")
    st.markdown("### System status")
    st.markdown("🟢  Application ready")
    st.markdown("🔵  SQLite business database")
    st.markdown("🟣  Semantic document search")
    st.markdown("⚪  Ollama LLM · local")
    st.markdown("---")
    st.markdown("### Knowledge base")
    st.caption("Add `.md` or `.txt` files to the `documents/` folder, then rebuild the index.")
    if st.button("↻  Rebuild document index", use_container_width=True):
        with st.spinner("Indexing documents..."):
            assistant.rebuild_index()
        st.success("Document index refreshed.")
    st.markdown("---")
    st.caption("Demo workspace · Synthetic sales data")
    st.caption("Keep confidential data out of public repositories.")

# ---------- Hero ----------
st.markdown("""
<div class="hero">
  <div class="eyebrow">AI-powered analytics workspace</div>
  <h1>Turn business data into clear answers.</h1>
  <p>Ask questions in plain English. InsightIQ searches your documents and business records, then responds with evidence.</p>
</div>
""", unsafe_allow_html=True)

# ---------- Overview cards ----------
col1, col2, col3, col4 = st.columns(4)
cards = [
    ("INTELLIGENT RETRIEVAL", "RAG", "Finds relevant document context"),
    ("BUSINESS DATA", "SQL", "Queries structured sales records"),
    ("LOCAL LANGUAGE MODEL", "Ollama", "Generates evidence-based answers"),
    ("SOURCE VISIBILITY", "Traceable", "Inspect retrieved supporting data"),
]
for col, (label, value, detail) in zip([col1, col2, col3, col4], cards):
    with col:
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">{label}</div>'
            f'<div class="metric-value">{value}</div><div style="color:#8290a5;font-size:.75rem;margin-top:5px">{detail}</div></div>',
            unsafe_allow_html=True
        )

st.write("")
left, right = st.columns([1.65, 1], gap="large")

with left:
    st.markdown('<div class="section-kicker">Ask your data</div>', unsafe_allow_html=True)
    st.markdown("### What would you like to understand?")
    question = st.text_area(
        "Business question",
        placeholder="e.g. Which region generated the highest revenue, and what might explain the result?",
        height=115,
        label_visibility="collapsed",
    )
    st.caption("Try a question about revenue, regions, products, customer segments, or the quarterly notes.")
    if st.button("✦  Generate insight", type="primary", use_container_width=True, disabled=not question.strip()):
        with st.spinner("Searching documents and querying business records..."):
            st.session_state["bi_result"] = assistant.ask(question)
            st.session_state["bi_question"] = question

    st.markdown("**Suggested questions**")
    suggestions = [
        "Which region generated the highest revenue?",
        "Compare revenue by product.",
        "What happened during Q2 2026?",
        "Which customer segment is associated with laptop purchases?",
    ]
    s_cols = st.columns(2)
    for i, prompt in enumerate(suggestions):
        with s_cols[i % 2]:
            if st.button(prompt, key=f"suggestion_{i}", use_container_width=True):
                with st.spinner("Finding evidence..."):
                    st.session_state["bi_result"] = assistant.ask(prompt)
                    st.session_state["bi_question"] = prompt

with right:
    st.markdown('<div class="section-kicker">How it works</div>', unsafe_allow_html=True)
    st.markdown("### Evidence-first answers")
    with st.container(border=True):
        st.markdown("**01 · Retrieve**")
        st.caption("Semantic search finds relevant passages in your business documents.")
        st.markdown("**02 · Query**")
        st.caption("A SQL planner retrieves matching rows from the sales database.")
        st.markdown("**03 · Generate**")
        st.caption("The LLM receives the evidence and is instructed not to invent facts.")
    st.caption("Answers depend on the quality and coverage of the source data.")

# ---------- Results ----------
if "bi_result" in st.session_state:
    result = st.session_state["bi_result"]
    st.write("")
    st.markdown('<div class="section-kicker">Analysis result</div>', unsafe_allow_html=True)
    st.markdown(f"### {st.session_state.get('bi_question', 'Your business question')}")
    st.markdown('<div class="answer-panel">', unsafe_allow_html=True)
    st.markdown("**AI-generated insight**")
    st.write(result["answer"])
    st.markdown('</div>', unsafe_allow_html=True)

    st.write("")
    tab_answer, tab_docs, tab_sql = st.tabs([
        f"Overview · {len(result['sources']) + len(result['records'])} evidence items",
        f"Document sources · {len(result['sources'])}",
        f"SQL records · {len(result['records'])}",
    ])
    with tab_answer:
        st.info("Review the supporting passages and records before using an answer for a business decision.")
        if result["sources"]:
            st.markdown("**Retrieved document passages**")
            for item in result["sources"]:
                st.markdown(
                    f'<div class="source-card"><div class="source-meta">📄 {item["source"]} &nbsp; · &nbsp; Similarity {item["score"]:.3f}</div>{item["text"]}</div>',
                    unsafe_allow_html=True,
                )
        if result["records"]:
            st.markdown("**Matching business records**")
            st.dataframe(result["records"], use_container_width=True, hide_index=True)
    with tab_docs:
        if result["sources"]:
            for idx, item in enumerate(result["sources"], 1):
                with st.expander(f"{idx}. {item['source']}  ·  similarity {item['score']:.3f}", expanded=idx == 1):
                    st.write(item["text"])
        else:
            st.warning("No document passages were retrieved for this question.")
    with tab_sql:
        if result["records"]:
            st.dataframe(result["records"], use_container_width=True, hide_index=True)
        else:
            st.caption("No SQL rows were returned. The question may have been answered from documents only.")
        with st.expander("SQL planner output"):
            st.code(result["sql"], language="sql")

st.markdown("---")
st.markdown(
    '<div style="text-align:center;color:#8995a8;font-size:.76rem;">INSIGHTIQ · RAG + VECTOR SEARCH + SQL + LLM &nbsp; | &nbsp; Built with Python and Streamlit</div>',
    unsafe_allow_html=True,
)
