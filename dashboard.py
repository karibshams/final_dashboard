# dashboard.py - Modern Web Dashboard for Testing AI Responses

import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv
from app import SocialMediaAI
from ghl_integration import GHLIntegration
import time

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Social Media AI Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for ChatGPT-like styling
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background-color: black;
    }
    
    /* Chat message styling */
    .user-message {
        background-color: blue;
        border-radius: 15px;
        padding: 15px 20px;
        margin: 10px 0;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        border-left: 4px solid #10a37f;
    }
    
    .ai-message {
        background-color: #f0f0f0;
        border-radius: 15px;
        padding: 15px 20px;
        margin: 10px 0;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        border-left: 4px solid #6366f1;
    }
    
    /* Category badges */
    .category-badge {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 14px;
        margin: 5px 0;
    }
    
    .lead-badge { background-color: #10b981; color: white; }
    .praise-badge { background-color: #3b82f6; color: white; }
    .spam-badge { background-color: #ef4444; color: white; }
    .question-badge { background-color: #f59e0b; color: white; }
    .complaint-badge { background-color: #dc2626; color: white; }
    
    /* GHL status styling */
    .ghl-status {
        background-color: #e0e7ff;
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
        border: 1px solid #6366f1;
    }
    
    /* Input styling */
    .stTextArea textarea {
        border-radius: 10px;
        border: 2px solid #e5e7eb;
        padding: 10px;
    }
    
    .stTextArea textarea:focus {
        border-color: #10a37f;
        box-shadow: 0 0 0 3px rgba(16, 163, 127, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'ai_initialized' not in st.session_state:
    st.session_state.ai_initialized = False
if 'ghl_initialized' not in st.session_state:
    st.session_state.ghl_initialized = False

# Header
st.title("🤖 Social Media AI Testing Dashboard")
st.markdown("Test AI responses and GHL integration in real-time")

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # API Key status
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        st.success("✅ OpenAI API Connected")
        if not st.session_state.ai_initialized:
            try:
                st.session_state.ai = SocialMediaAI(api_key)
                st.session_state.ai_initialized = True
            except Exception as e:
                st.error(f"❌ AI Init Error: {str(e)}")
    else:
        st.error("❌ OpenAI API Key Missing")
        st.code("Add to .env:\nOPENAI_API_KEY=your-key")
    
    st.divider()
    
    # GHL Configuration
    st.subheader("🔗 GoHighLevel Integration")
    
    ghl_api_key = st.text_input("GHL API Key", type="password", key="ghl_api_key")
    ghl_location_id = st.text_input("GHL Location ID", key="ghl_location_id")
    
    if st.button("Connect to GHL"):
        if ghl_api_key and ghl_location_id:
            try:
                st.session_state.ghl = GHLIntegration(ghl_api_key, ghl_location_id)
                st.session_state.ghl_initialized = True
                st.success("✅ GHL Connected")
            except Exception as e:
                st.error(f"❌ GHL Error: {str(e)}")
        else:
            st.warning("Please enter both API Key and Location ID")
    
    if st.session_state.ghl_initialized:
        st.success("✅ GHL Integration Active")
    
    st.divider()
    
    # Test Mode Options
    st.subheader("🧪 Test Options")
    auto_ghl_sync = st.checkbox("Auto-sync to GHL", value=False)
    show_raw_data = st.checkbox("Show Raw API Data", value=False)
    debug_mode = st.checkbox("Debug Mode", value=False)
    
    # Clear conversation
    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("💬 Chat Interface")
    
    # Display conversation history
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="user-message">
                <strong>📝 You:</strong><br>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            # AI response with category
            category_class = message["category"].lower() + "-badge"
            st.markdown(f"""
            <div class="ai-message">
                <strong>🤖 AI Response:</strong><br>
                {message["content"]}<br><br>
                <span class="category-badge {category_class}">
                    {message["category"]}
                </span>
            </div>
            """, unsafe_allow_html=True)
            
            # Show GHL status if enabled
            if message.get("ghl_status"):
                st.markdown(f"""
                <div class="ghl-status">
                    <strong>📊 GHL Status:</strong><br>
                    {message["ghl_status"]}
                </div>
                """, unsafe_allow_html=True)

with col2:
    st.header("📊 Analytics")
    
    # Category distribution
    if st.session_state.messages:
        categories = [msg["category"] for msg in st.session_state.messages if msg["role"] == "ai"]
        if categories:
            st.subheader("Category Distribution")
            
            # Count categories
            category_counts = {}
            for cat in categories:
                category_counts[cat] = category_counts.get(cat, 0) + 1
            
            # Display metrics
            for cat, count in category_counts.items():
                st.metric(cat, count)
            
            # Response time metrics
            st.subheader("⏱️ Performance")
            st.metric("Avg Response Time", "1.2s")
            st.metric("Total Processed", len(categories))

# Input area at the bottom
st.divider()

# Create input form
with st.form("comment_form", clear_on_submit=True):
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.text_area(
            "Enter a social media comment to test:",
            placeholder="Type your comment here... (e.g., 'I'm interested in your product!')",
            height=80,
            key="comment_input"
        )
    
    with col2:
        st.write("")  # Spacing
        st.write("")  # Spacing
        submit_button = st.form_submit_button("🚀 Send", use_container_width=True)

# Process input
if submit_button and user_input:
    if st.session_state.ai_initialized:
        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now()
        })
        
        # Show processing indicator
        with st.spinner("🤔 AI is thinking..."):
            start_time = time.time()
            
            try:
                # Get AI response
                result = st.session_state.ai.process_comment(user_input)
                
                # Calculate response time
                response_time = time.time() - start_time
                
                # Debug: Print result to console
                print(f"AI Result: {result}")
                
                # Prepare AI message
                ai_message = {
                    "role": "ai",
                    "content": result['reply'],
                    "category": result['category'],
                    "timestamp": datetime.now(),
                    "response_time": response_time
                }
                
                # GHL Integration if enabled
                if auto_ghl_sync and st.session_state.ghl_initialized:
                    try:
                        # Process GHL actions based on category
                        ghl_result = st.session_state.ghl.process_comment(
                            comment=user_input,
                            category=result['category'],
                            contact_info={
                                "email": "test@example.com",  # In production, get from actual user
                                "name": "Test User",
                                "source": "Social Media Dashboard"
                            }
                        )
                        
                        # Format GHL status
                        ghl_status = f"✅ Contact: {'Created' if ghl_result.get('contact_created') else 'Updated'}"
                        if ghl_result.get('tags_added'):
                            ghl_status += f"<br>🏷️ Tags: {', '.join(ghl_result['tags_added'])}"
                        if ghl_result.get('workflow_triggered'):
                            ghl_status += f"<br>⚡ Workflow: Triggered"
                        
                        ai_message["ghl_status"] = ghl_status
                        
                    except Exception as e:
                        ai_message["ghl_status"] = f"❌ GHL Error: {str(e)}"
                
                # Add AI message
                st.session_state.messages.append(ai_message)
                
                # Show raw data if enabled
                if show_raw_data:
                    with st.expander("🔍 Raw API Response"):
                        st.json(result)
                        st.write(f"Response time: {response_time:.2f}s")
                
                # Debug mode
                if debug_mode:
                    with st.expander("🐛 Debug Information"):
                        st.write("**Input Comment:**", user_input)
                        st.write("**Detected Category:**", result['category'])
                        st.write("**Generated Reply:**", result['reply'])
                        st.write("**API Key Status:**", "✅ Present" if st.session_state.ai.api_key else "❌ Missing")
                        st.write("**Response Time:**", f"{response_time:.2f}s")
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
        
        # Rerun to update display
        st.rerun()
    else:
        st.error("❌ AI not initialized. Please check your API key.")

# Footer with sample comments
st.divider()
st.subheader("💡 Sample Comments to Try")

sample_comments = {
    "🤝 Lead": "I'm interested in your services. How can I get started?",
    "🙌 Praise": "Amazing product! Best purchase I've made this year!",
    "🚫 Spam": "Click here for free followers!!! www.spam.com",
    "❓ Question": "What are your business hours?",
    "😡 Complaint": "My order hasn't arrived and it's been 2 weeks!"
}

cols = st.columns(5)
for idx, (label, comment) in enumerate(sample_comments.items()):
    with cols[idx]:
        if st.button(label, use_container_width=True):
            st.session_state.comment_input = comment
            st.rerun()