import os
import streamlit as st
from graph import build_graph
from report import build_report, save_report

st.set_page_config(page_title="CodePilot AI", page_icon="🤖", layout="wide")

st.title("🤖 CodePilot AI")
st.caption("Multi-Agent Intelligent Code Review and Explanation Platform — powered by Groq")

with st.sidebar:
    st.header("📥 Input")
    uploaded_file = st.file_uploader("Upload a source file (any language)", type=None)
    pasted_code = st.text_area("...or paste code directly", height=220, placeholder="Paste your code here")
    run_button = st.button("▶ Run Review", type="primary", use_container_width=True)
    st.markdown("---")
    st.caption("Models used: `openai/gpt-oss-120b` (deep analysis) & `openai/gpt-oss-20b` (fast agents)")

if "result" not in st.session_state:
    st.session_state.result = None

if run_button:
    if uploaded_file is not None:
        code = uploaded_file.read().decode("utf-8", errors="replace")
        filename = uploaded_file.name
    elif pasted_code.strip():
        code = pasted_code
        filename = "pasted_snippet.txt"
    else:
        st.warning("Upload a file or paste some code first.")
        st.stop()

    with st.spinner("Running multi-agent analysis... (Planning → Review/Bugs → Complexity/Security → Optimizer → Docs → Explanation)"):
        graph = build_graph()
        initial_state = {"filename": filename, "code": code}
        result = graph.invoke(initial_state)

    st.session_state.result = result
    st.session_state.filename = filename

result = st.session_state.result

if result:
    st.success(f"✅ Analysis complete — detected language: **{result.get('language', 'Unknown')}**")

    tabs = st.tabs(
        ["📝 Review", "🐞 Bugs", "⏱ Complexity", "🔒 Security",
         "⚡ Optimization", "📄 Docs", "🎓 Explanation", "📊 Full Report"]
    )

    with tabs[0]:
        st.markdown(result.get("review", "N/A"))
    with tabs[1]:
        st.markdown(result.get("bugs", "N/A"))
    with tabs[2]:
        st.markdown(result.get("complexity", "N/A"))
    with tabs[3]:
        st.markdown(result.get("security", "N/A"))
    with tabs[4]:
        st.markdown(result.get("optimization", "N/A"))
    with tabs[5]:
        st.markdown(result.get("documentation", "N/A"))
    with tabs[6]:
        st.markdown(result.get("explanation", "N/A"))
    with tabs[7]:
        report_md = build_report(result)
        st.markdown(report_md)
        report_path = save_report(report_md, f"{st.session_state.filename}_report.md")
        with open(report_path, "rb") as f:
            st.download_button(
                "⬇ Download Full Report (Markdown)",
                f,
                file_name=os.path.basename(report_path),
            )
else:
    st.info("Upload or paste code in the sidebar, then click **Run Review** to start the multi-agent analysis.")
