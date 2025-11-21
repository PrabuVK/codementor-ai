"""
CodeMentor AI - Interactive Coding Education Platform
Powered by Amazon Q Developer
"""

import streamlit as st
import subprocess
import time
import re

# --- Page Configuration ---
st.set_page_config(
    page_title="CodeMentor AI",
    page_icon="🤖",
    layout="wide"
)

# --- Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Amazon Q Developer Integration ---
def query_amazon_q(question: str) -> str:
    """
    Query Amazon Q Developer using CLI
    
    Args:
        question: The coding question to ask
    
    Returns:
        str: Response from Amazon Q Developer
    """
    try:
        # Call Amazon Q CLI with stdin to avoid interactive mode
        result = subprocess.run(
            ['q', 'chat'],
            input=question,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            response = result.stdout.strip()
            
            # Remove ALL ANSI escape codes (multiple patterns)
            # Pattern 1: Standard ANSI codes
            response = re.sub(r'\x1b\[[0-9;]*m', '', response)
            # Pattern 2: Extended ANSI codes
            response = re.sub(r'\x1b\].*?\x07', '', response)
            # Pattern 3: Any remaining escape sequences
            response = re.sub(r'\x1b[^m]*m', '', response)
            # Pattern 4: Catch-all for any \x1b sequences
            response = re.sub(r'\x1b.*?[a-zA-Z]', '', response)
            
            # Remove the "> " prompt if present
            response = re.sub(r'^>\s*', '', response, flags=re.MULTILINE)
            
            # Format code blocks for better markdown rendering
            # Find lines that start with language keywords (python, javascript, etc.)
            # and wrap them in proper markdown code blocks
            lines = response.split('\n')
            formatted_lines = []
            in_code_block = False
            code_language = None
            
            for i, line in enumerate(lines):
                # Check if line indicates a code language
                if line.strip().lower() in ['python', 'javascript', 'java', 'cpp', 'c++', 'sql', 'html', 'css']:
                    code_language = line.strip().lower()
                    if code_language == 'cpp':
                        code_language = 'python'  # fallback for better highlighting
                    formatted_lines.append(f'\n```{code_language}')
                    in_code_block = True
                    continue
                
                # Check if we should close code block
                if in_code_block and (line.strip() == '' or line.strip().startswith('•') or line.strip().startswith('Key ')):
                    formatted_lines.append('```\n')
                    in_code_block = False
                    formatted_lines.append(line)
                else:
                    formatted_lines.append(line)
            
            # Close any remaining code block
            if in_code_block:
                formatted_lines.append('```')
            
            response = '\n'.join(formatted_lines)
            
            # Clean up extra whitespace
            response = re.sub(r'\n{3,}', '\n\n', response)
            response = response.strip()
            
            if response:
                return response
            else:
                return "Amazon Q returned an empty response. Please try again."
        else:
            error_msg = result.stderr.strip()
            if error_msg:
                return f"Error from Amazon Q CLI: {error_msg}"
            else:
                return "Amazon Q encountered an error. Please try again."
    
    except FileNotFoundError:
        return "❌ Error: Amazon Q CLI not found. Make sure it's installed and in your PATH."
    except subprocess.TimeoutExpired:
        return "⏱️ Request timed out (60s). Amazon Q might be processing a complex query. Try again."
    except Exception as e:
        return f"❌ Unexpected error: {str(e)}"

# --- UI Layout ---

# Header
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.title("🤖 CodeMentor AI")
    st.markdown("### *Powered by Amazon Q Developer*")
    st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("📚 About")
    st.markdown("""
    **CodeMentor AI** helps you learn coding through AI-powered assistance.
    
    **Features:**
    - Ask any coding question
    - Get instant explanations
    - See code examples
    - Learn best practices
    """)
    
    st.markdown("---")
    
    st.header("💡 Example Questions")
    example_questions = [
        "What is a Python function?",
        "Explain list comprehension with example",
        "How do I handle exceptions in Python?",
        "What's the difference between list and tuple?",
        "Show me how to read a CSV file"
    ]
    
    for question in example_questions:
        if st.button(question, key=question, use_container_width=True):
            st.session_state.example_clicked = question
    
    st.markdown("---")
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("Built for AWS Global Vibe Hackathon 2025")

# Main Chat Interface
st.subheader("💬 Ask me anything about code")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle example button clicks
if "example_clicked" in st.session_state:
    prompt = st.session_state.example_clicked
    del st.session_state.example_clicked
else:
    prompt = st.chat_input("Enter your question (e.g., 'what is a python function?')")

# Process user input
if prompt:
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get response from Amazon Q
    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking with Amazon Q Developer..."):
            response = query_amazon_q(prompt)
        
        st.markdown(response)
    
    # Add assistant response to chat
    st.session_state.messages.append({"role": "assistant", "content": response})

# Footer with status
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown(
        "<p style='text-align: center; color: gray;'>✨ Powered by Amazon Q Developer CLI</p>",
        unsafe_allow_html=True
    )
