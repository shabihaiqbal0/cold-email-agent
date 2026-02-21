import streamlit as st
import time
import random
from datetime import datetime

# Set up the Streamlit page with custom styling
st.set_page_config(
    page_title="AI Cold Email Generator Pro",
    page_icon="📧",
    layout="wide"
)

# Custom CSS for modern design
st.markdown("""
<style>
    /* Main background and text colors */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Header styling */
    .header {
        text-align: center;
        padding: 2rem 0;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .header h1 {
        font-size: 3rem;
        margin-bottom: 1rem;
        background: linear-gradient(45deg, #ff9a9e, #fad0c4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Card styling */
    .card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(45deg, #ff6b6b, #ffa502);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.8rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    
    /* Progress bar styling */
    .progress-container {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Status indicators */
    .status-active {
        color: #4ade80;
        font-weight: bold;
    }
    
    .status-pending {
        color: #fbbf24;
        font-weight: bold;
    }
    
    .status-complete {
        color: #60a5fa;
        font-weight: bold;
    }
    
    /* Email preview styling */
    .email-preview {
        background: #1e293b;
        color: #e2e8f0;
        border-radius: 10px;
        padding: 1.5rem;
        font-family: 'Courier New', monospace;
        border-left: 4px solid #3b82f6;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Input field styling */
    .stTextInput>div>div>input {
        border-radius: 10px;
        border: 2px solid #e2e8f0;
    }
    
    .stSelectbox>div>div>select {
        border-radius: 10px;
        border: 2px solid #e2e8f0;
    }
    
    /* Animation keyframes */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
</style>
""", unsafe_allow_html=True)

# Header section
st.markdown("""
<div class="header">
    <h1>📧 AI Cold Email Generator Pro</h1>
    <p style="font-size: 1.2rem; color: #f0f0f0;">Generate personalized business outreach emails in seconds</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'generated_email' not in st.session_state:
    st.session_state.generated_email = ""
if 'is_processing' not in st.session_state:
    st.session_state.is_processing = False
if 'progress_step' not in st.session_state:
    st.session_state.progress_step = 0

# Sidebar with service information
with st.sidebar:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("🚀 Our Services")
    
    services = [
        {
            "name": "SEO Optimization",
            "description": "Boost organic traffic and search rankings",
            "icon": "🔍"
        },
        {
            "name": "Web Development", 
            "description": "Modern, responsive website solutions",
            "icon": "💻"
        },
        {
            "name": "AI Automation",
            "description": "Streamline repetitive business processes",
            "icon": "🤖"
        },
        {
            "name": "Digital Marketing",
            "description": "Comprehensive online marketing strategy",
            "icon": "📈"
        },
        {
            "name": "E-commerce Solutions",
            "description": "Scale your online business operations",
            "icon": "🛒"
        }
    ]
    
    for service in services:
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.2); padding: 10px; border-radius: 8px; margin: 10px 0;">
            <h4>{service['icon']} {service['name']}</h4>
            <p style="font-size: 0.9rem; margin: 0;">{service['description']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    st.info("💡 **Pro Tip**: The more specific your target URL, the better the personalized results!")
    st.markdown('</div>', unsafe_allow_html=True)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("🎯 Target Company")
    
    # URL input with validation
    target_url = st.text_input(
        "Company Website URL", 
        placeholder="https://example.com",
        help="Enter the URL of the company you want to reach out to"
    )
    
    # Validation
    if target_url and not target_url.startswith(('http://', 'https://')):
        st.warning("⚠️ Please enter a valid URL starting with http:// or https://")
    
    st.subheader("📝 Email Preferences")
    
    # Email configuration in columns
    pref_col1, pref_col2 = st.columns(2)
    
    with pref_col1:
        email_tone = st.selectbox(
            "Tone",
            ["Professional", "Friendly", "Casual", "Direct"],
            help="Choose the tone that best fits your outreach style"
        )
        
        email_length = st.slider(
            "Length (words)",
            min_value=50,
            max_value=300,
            value=150,
            step=25,
            help="Set the desired length of the generated email"
        )
    
    with pref_col2:
        creativity = st.slider(
            "Creativity Level", 
            min_value=0.0, 
            max_value=1.0, 
            value=0.7, 
            step=0.1,
            help="Higher values make the output more creative"
        )
        
        focus_service = st.selectbox(
            "Focus Service",
            ["Any", "SEO Optimization", "Web Development", "AI Automation", "Digital Marketing", "E-commerce"],
            help="Specify which service to prioritize in the email"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("📊 Preview")
    
    if st.session_state.generated_email:
        st.markdown('<div class="status-complete">✅ Email Ready!</div>', unsafe_allow_html=True)
        st.markdown('<div class="email-preview">', unsafe_allow_html=True)
        st.text(st.session_state.generated_email)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Download button
        st.download_button(
            label="📥 Download Email",
            data=st.session_state.generated_email,
            file_name=f"cold_email_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    else:
        st.info("📝 Enter company details and click 'Generate Email' to see the result here.")
        
        # Show sample email structure
        st.subheader("📋 Email Structure")
        st.markdown("""
        - **Subject Line**: Compelling hook
        - **Greeting**: Personalized opening
        - **Value Proposition**: Clear benefit
        - **Social Proof**: Credibility markers
        - **Call to Action**: Clear next step
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Advanced options expander
with st.expander("⚙️ Advanced Options"):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    adv_col1, adv_col2 = st.columns(2)
    
    with adv_col1:
        st.subheader("🎯 Targeting")
        industry_focus = st.multiselect(
            "Industry Focus",
            ["Technology", "Healthcare", "Finance", "E-commerce", "Education", "Manufacturing"],
            help="Select industries to tailor the approach"
        )
        
        urgency_level = st.radio(
            "Urgency Level",
            ["Low", "Medium", "High"],
            help="How urgent is the proposed solution?"
        )
    
    with adv_col2:
        st.subheader("📊 Analysis Depth")
        competitor_analysis = st.checkbox("Include Competitor Analysis")
        market_trends = st.checkbox("Reference Market Trends")
        case_studies = st.checkbox("Include Case Studies")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Real-time processing simulation
def simulate_processing():
    """Simulate real-time email generation process"""
    steps = [
        "🔍 Analyzing company website...",
        "📊 Identifying business opportunities...",
        "🎯 Matching with optimal services...",
        "✍️ Crafting personalized message...",
        "✅ Finalizing email content..."
    ]
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, step in enumerate(steps):
        st.session_state.progress_step = i + 1
        progress_bar.progress((i + 1) / len(steps))
        status_text.markdown(f'<div class="status-active pulse">{step}</div>', unsafe_allow_html=True)
        time.sleep(1.5)  # Simulate processing time
    
    status_text.markdown('<div class="status-complete">✅ Analysis Complete!</div>', unsafe_allow_html=True)
    time.sleep(0.5)

# Generate button with enhanced styling
st.markdown('<div class="card">', unsafe_allow_html=True)

# Generate button
generate_col1, generate_col2, generate_col3 = st.columns([1, 2, 1])

with generate_col2:
    if st.button("🚀 Generate Cold Email", type="primary", use_container_width=True):
        if not target_url:
            st.error("❌ Please enter a company website URL.")
        elif not target_url.startswith(('http://', 'https://')):
            st.error("❌ Please enter a valid URL starting with http:// or https://")
        else:
            st.session_state.is_processing = True
            
            # Show processing simulation
            with st.spinner("Processing..."):
                simulate_processing()
            
            # Generate sample email (hardcoded for demo)
            sample_emails = [
                f"""Subject: Quick question about {target_url.split('//')[1].split('/')[0]}'s growth potential

Hi there,

I was browsing {target_url.split('//')[1].split('/')[0]} recently and noticed some great work on your digital presence. Your approach to [specific aspect from website] really stood out.

I'm reaching out because we've helped similar companies in your space increase their [relevant metric] by 40-60% through our {focus_service if focus_service != 'Any' else 'digital solutions'}.

Would you be open to a brief 15-minute call this week to discuss how we might help {target_url.split('//')[1].split('/')[0]} reach its next growth milestone?

Best regards,
[Your Name]""",
                
                f"""Subject: {focus_service if focus_service != 'Any' else 'Growth opportunity'} for {target_url.split('//')[1].split('/')[0]}

Hello,

Your work at {target_url.split('//')[1].split('/')[0]} caught my attention - particularly your approach to [website-specific element]. 

Many companies in your position face challenges with [relevant pain point]. We specialize in {focus_service if focus_service != 'Any' else 'comprehensive digital solutions'} that have helped businesses like yours achieve measurable results.

I'd love to explore whether there's a fit for collaboration. Are you available for a quick conversation this week?

Looking forward to connecting,
[Your Name]""",
                
                f"""Subject: {email_tone} inquiry about {target_url.split('//')[1].split('/')[0]}'s digital strategy

Greetings,

I've been following {target_url.split('//')[1].split('/')[0]}'s journey and am impressed with your [specific achievement from website]. 

From our analysis, there appears to be significant opportunity in [area of improvement]. Our {focus_service if focus_service != 'Any' else 'specialized services'} have helped similar organizations in your industry overcome these exact challenges.

Would you be interested in discussing how we might support {target_url.split('//')[1].split('/')[0]}'s continued success?

Warm regards,
[Your Name]"""
            ]
            
            # Select and customize email based on preferences
            selected_email = random.choice(sample_emails)
            
            # Apply tone adjustments
            if email_tone == "Professional":
                selected_email = selected_email.replace("[Your Name]", "Alex Johnson, Senior Solutions Architect")
            elif email_tone == "Friendly":
                selected_email = selected_email.replace("[Your Name]", "Alex from Growth Partners")
            elif email_tone == "Casual":
                selected_email = selected_email.replace("[Your Name]", "Alex")
            else:  # Direct
                selected_email = selected_email.replace("[Your Name]", "Alex Johnson")
            
            st.session_state.generated_email = selected_email
            st.session_state.is_processing = False
            st.session_state.progress_step = 0
            
            # Show success message
            st.success("🎉 Email generated successfully!")
            st.balloons()

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: white; padding: 1rem;">
    <p>📧 AI Cold Email Generator Pro v2.0 | Powered by Advanced AI Algorithms</p>
    <p style="font-size: 0.8rem; opacity: 0.8;">Real-time processing simulation with dynamic content generation</p>
</div>
""", unsafe_allow_html=True)