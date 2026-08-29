import streamlit as st
import sys
import os
import io

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import run_workflow
from config.model_armor import create_model_armor
from config.audit_logger import create_audit_logger


class LogCapture:
    """Captures print() output for display in Streamlit."""
    def __init__(self):
        self.buffer = io.StringIO()

    def write(self, text):
        if text.strip():
            self.buffer.write(text + "\n")

    def get_logs(self):
        return self.buffer.getvalue()

    def clear(self):
        self.buffer = io.StringIO()

# Page config
st.set_page_config(
    page_title="Koala Fleet - Cross-Department AI Agent",
    page_icon="🐨",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FF6B35;
        text-align: center;
        padding: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .agent-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem;
    }
    .agent-card hr {
        background-color: rgba(255,255,255,0.3);
    }
    .status-success {
        color: #28a745;
        font-weight: bold;
    }
    .status-blocked {
        color: #dc3545;
        font-weight: bold;
    }
    .metric-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 5px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🐨 Koala Fleet</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Cross-Department AI Agent Orchestration</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    st.info("**Track:** The Fortified Enterprise Fleet")
    st.info("**Tech:** Gemini + ADK + Google Cloud")
    
    st.divider()
    st.header("📊 Quick Stats")
    
    # Load audit stats
    try:
        audit = create_audit_logger(use_firestore=False)
        stats = audit.get_stats()
        st.metric("Total Actions", stats.get("total_actions", 0))
        st.metric("Agents Active", len(stats.get("by_agent", {})))
    except:
        st.metric("Total Actions", 0)
        st.metric("Agents Active", 0)
    
    st.divider()
    st.header("🛡️ Security")
    st.success("Model Armor: Active")
    st.success("Agent Gateway: Active")
    st.success("Audit Logger: Active")

# Main content
tab1, tab2, tab3 = st.tabs(["🚀 Workflow", "🛡️ Security", "📋 Audit Logs"])

# Tab 1: Workflow
with tab1:
    st.header("Run Workflow")
    
    # Example inputs
    st.subheader("📝 Example Inputs")
    examples = [
        "Hire a Senior Developer, budget $150K, need MacBook Pro",
        "Onboard new employee: create ID, setup email, order laptop",
        "Request budget approval for marketing campaign $50K"
    ]
    
    selected_example = st.selectbox("Select an example or type your own:", ["Custom"] + examples)
    
    if selected_example == "Custom":
        user_input = st.text_area(
            "Enter your request:",
            placeholder="e.g., Hire a Senior Developer, budget $150K, need MacBook Pro",
            height=100
        )
    else:
        user_input = st.text_area(
            "Enter your request:",
            value=selected_example,
            height=100
        )
    
    # Run button
    if st.button("🚀 Run Workflow", type="primary", use_container_width=True):
        if user_input:
            with st.spinner("🔄 Running workflow..."):
                # Create placeholder for live updates
                status_placeholder = st.empty()
                results_placeholder = st.empty()
                
                # Capture print output
                log_capture = LogCapture()
                old_stdout = sys.stdout
                sys.stdout = log_capture
                
                # Run workflow
                try:
                    result = run_workflow(user_input)
                finally:
                    sys.stdout = old_stdout
                
                # Display results
                if result["status"] == "blocked":
                    st.error(f"🚫 **Workflow Blocked:** {result.get('reason', 'PII Detected')}")
                else:
                    st.success(f"✅ **Workflow Complete** (ID: {result.get('workflow_id', 'N/A')})")
                    
                    # Agent status cards
                    st.subheader("🤖 Agent Status")
                    cols = st.columns(3)
                    
                    with cols[0]:
                        st.markdown("""
                        <div class="agent-card">
                            <h3>👤 HR Agent</h3>
                            <hr>
                            <p>Job Postings</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with cols[1]:
                        st.markdown("""
                        <div class="agent-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                            <h3>💰 Finance Agent</h3>
                            <hr>
                            <p>Budget & Expenses</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with cols[2]:
                        st.markdown("""
                        <div class="agent-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                            <h3>💻 IT Agent</h3>
                            <hr>
                            <p>Hardware & Software</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Detailed results
                    st.subheader("📊 Results")
                    
                    for task in result.get("results", []):
                        dept = task.department.value.upper()
                        
                        with st.expander(f"**{dept} Agent** — {task.action}", expanded=True):
                            st.write(f"**Status:** {task.status}")
                            
                            if task.result:
                                for key, value in task.result.items():
                                    if key == "posting":
                                        st.markdown("**Generated Job Posting:**")
                                        st.text_area("Job Posting", value, height=200, disabled=True, key=f"posting_{dept}")
                                    else:
                                        st.write(f"**{key}:** {value}")
                
                # Live Workflow Logs panel
                st.divider()
                with st.expander("📋 Live Workflow Logs", expanded=True):
                    logs = log_capture.get_logs()
                    if logs:
                        st.code(logs, language=None)
                    else:
                        st.info("No logs captured.")
        else:
            st.warning("⚠️ Please enter a request")

# Tab 2: Security
with tab2:
    st.header("🛡️ Security Dashboard")
    
    st.subheader("PII Detection Test")
    st.write("Test the Model Armor PII detection:")
    
    pii_input = st.text_input("Enter text to scan:", placeholder="e.g., SSN is 123-45-6789")
    
    if st.button("🔍 Scan for PII"):
        if pii_input:
            armor = create_model_armor()
            result = armor.protect(pii_input)
            
            if result["allowed"]:
                st.success("✅ **SAFE** — No blocking PII detected")
                if result.get("details", {}).get("detected"):
                    st.info(f"PII Found (auto-redacted): {[p['type'] for p in result['details']['detected']]}")
            else:
                st.error("🚫 **BLOCKED** — Sensitive PII detected")
                if result.get("details", {}).get("detected"):
                    for pii in result["details"]["detected"]:
                        st.write(f"  - Type: **{pii['type']}** | Values: {pii['values']}")
        else:
            st.warning("Enter text to scan")
    
    st.divider()
    st.subheader("🛡️ Security Components")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("**Model Armor**\n- PII Detection\n- Prompt Injection Prevention\n- Data Leakage Screening")
    
    with col2:
        st.info("**Agent Gateway**\n- Zero-Trust Authentication\n- Request Signing\n- Communication Logging")

# Tab 3: Audit Logs
with tab3:
    st.header("📋 Audit Logs")
    
    audit = create_audit_logger(use_firestore=False)
    logs = audit.get_logs(limit=50)
    
    if logs:
        st.write(f"Showing last **{len(logs)}** entries:")
        
        for log in reversed(logs):
            agent = log.get("agent", "unknown")
            action = log.get("action", "unknown")
            status = log.get("status", "unknown")
            dt = log.get("datetime", "N/A")
            
            icon = "✅" if status == "success" else "❌"
            
            with st.expander(f"{icon} **{agent}** — {action} ({dt})"):
                st.write(f"**Agent:** {agent}")
                st.write(f"**Action:** {action}")
                st.write(f"**Status:** {status}")
                st.write(f"**Time:** {dt}")
                
                if log.get("input"):
                    st.write(f"**Input:** {log['input'][:200]}")
                
                if log.get("result"):
                    st.write(f"**Result:** {log['result'][:200]}")
    else:
        st.info("No logs yet. Run a workflow to generate logs.")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>🐨 Koala Fleet | All Things Agentic Hackathon 2026</p>
    <p>The Fortified Enterprise Fleet Track</p>
</div>
""", unsafe_allow_html=True)
