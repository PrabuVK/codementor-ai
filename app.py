"""
CodeMentor AI PRO - Interactive Coding Education Platform
Powered by Amazon Q Developer
Version 2.0 - Full Featured
"""

import streamlit as st
import subprocess
import time
import re
import json
from datetime import datetime
from streamlit_ace import st_ace
import sys
from io import StringIO

# --- Page Configuration ---
st.set_page_config(
    page_title="CodeMentor AI Pro",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS ---
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .challenge-card {
        padding: 1.5rem;
        border: 2px solid #667eea;
        border-radius: 10px;
        margin: 1rem 0;
        background: #f8f9fa;
    }
    .challenge-card code {
        background: #e9ecef;
        padding: 2px 6px;
        border-radius: 3px;
        font-family: 'Courier New', monospace;
        color: #495057;
    }
    .success-badge {
        background: #28a745;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: inline-block;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-weight: bold;
    }
    /* Make hint and solution boxes wider and more readable */
    .stAlert {
        font-size: 1.05rem;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# --- Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_mode" not in st.session_state:
    st.session_state.current_mode = "Chat"
if "completed_challenges" not in st.session_state:
    st.session_state.completed_challenges = []
if "user_code" not in st.session_state:
    st.session_state.user_code = ""
if "learning_path" not in st.session_state:
    st.session_state.learning_path = "Beginner"
if "show_hint" not in st.session_state:
    st.session_state.show_hint = False
if "show_solution" not in st.session_state:
    st.session_state.show_solution = False

# --- Coding Challenges Database ---
CHALLENGES = {
    "Beginner": [
        {
            "id": "b1",
            "title": "Hello World",
            "description": "Write a function that returns 'Hello, World!'",
            "starter_code": "def hello_world():\n    # Your code here\n    # Replace 'pass' with: return 'Hello, World!'\n    pass",
            "test_input": "hello_world()",
            "expected_output": "Hello, World!",
            "hint": "Use the return statement to send back the string 'Hello, World!'"
        },
        {
            "id": "b2",
            "title": "Add Two Numbers",
            "description": "Write a function that adds two numbers and returns the result",
            "starter_code": "def add_numbers(a, b):\n    # Your code here\n    # Hint: use the + operator and return the result\n    pass",
            "test_input": "add_numbers(5, 3)",
            "expected_output": "8",
            "hint": "Use the + operator to add a and b, then return the result. Example: return a + b"
        },
        {
            "id": "b3",
            "title": "Check Even or Odd",
            "description": "Write a function that returns 'Even' if number is even, 'Odd' if odd",
            "starter_code": "def check_even_odd(n):\n    # Your code here\n    pass",
            "test_input": "check_even_odd(4)",
            "expected_output": "Even",
            "hint": "Use the modulo operator %"
        }
    ],
    "Intermediate": [
        {
            "id": "i1",
            "title": "Reverse String",
            "description": "Write a function that reverses a string",
            "starter_code": "def reverse_string(s):\n    # Your code here\n    pass",
            "test_input": "reverse_string('hello')",
            "expected_output": "olleh",
            "hint": "Use slicing [::-1]"
        },
        {
            "id": "i2",
            "title": "Find Maximum",
            "description": "Write a function that finds the maximum number in a list",
            "starter_code": "def find_max(numbers):\n    # Your code here\n    pass",
            "test_input": "find_max([1, 5, 3, 9, 2])",
            "expected_output": "9",
            "hint": "You can use max() or loop through"
        }
    ],
    "Advanced": [
        {
            "id": "a1",
            "title": "Fibonacci Sequence",
            "description": "Write a function that returns the nth Fibonacci number",
            "starter_code": "def fibonacci(n):\n    # Your code here\n    pass",
            "test_input": "fibonacci(6)",
            "expected_output": "8",
            "hint": "Use recursion or iteration"
        }
    ]
}

# --- Amazon Q Developer Integration ---
def query_amazon_q(question: str) -> str:
    """Query Amazon Q Developer using CLI"""
    try:
        result = subprocess.run(
            ['q', 'chat'],
            input=question,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            response = result.stdout.strip()
            
            # Remove ANSI codes
            response = re.sub(r'\x1b\[[0-9;]*m', '', response)
            response = re.sub(r'\x1b\].*?\x07', '', response)
            response = re.sub(r'\x1b[^m]*m', '', response)
            response = re.sub(r'\x1b.*?[a-zA-Z]', '', response)
            response = re.sub(r'^>\s*', '', response, flags=re.MULTILINE)
            
            # Format code blocks
            lines = response.split('\n')
            formatted_lines = []
            in_code_block = False
            
            for line in lines:
                if line.strip().lower() in ['python', 'javascript', 'java', 'sql']:
                    formatted_lines.append(f'\n```{line.strip().lower()}')
                    in_code_block = True
                    continue
                
                if in_code_block and (line.strip() == '' or line.strip().startswith('•')):
                    formatted_lines.append('```\n')
                    in_code_block = False
                
                formatted_lines.append(line)
            
            if in_code_block:
                formatted_lines.append('```')
            
            response = '\n'.join(formatted_lines)
            response = re.sub(r'\n{3,}', '\n\n', response).strip()
            
            return response if response else "Amazon Q returned an empty response."
        else:
            return f"Error: {result.stderr}"
    
    except Exception as e:
        return f"❌ Error: {str(e)}"

# --- Code Execution Function ---
def execute_code(code: str, test_input: str = "") -> tuple:
    """Execute Python code safely and return output"""
    try:
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        # Create execution namespace
        namespace = {}
        
        # Execute the code
        exec(code, namespace)
        
        # Run test if provided
        if test_input:
            result = eval(test_input, namespace)
            output = str(result)
        else:
            # If no test input, try to get print output or run main function
            output = sys.stdout.getvalue()
            if not output.strip():
                # Try calling a main() function if it exists
                if 'main' in namespace and callable(namespace['main']):
                    result = namespace['main']()
                    output = str(result) if result is not None else sys.stdout.getvalue()
        
        sys.stdout = old_stdout
        return True, output.strip()
    
    except Exception as e:
        sys.stdout = old_stdout
        return False, str(e)

# --- Sidebar ---
with st.sidebar:
    st.markdown("### 🎯 Navigation")
    mode = st.radio(
        "Choose Mode:",
        ["💬 Chat Assistant", "🎮 Coding Challenges", "⚡ Code Playground", "📚 Learning Path"],
        label_visibility="collapsed"
    )
    
    st.session_state.current_mode = mode
    
    st.markdown("---")
    
    # Progress Stats
    st.markdown("### 📊 Your Progress")
    total_challenges = sum(len(challenges) for challenges in CHALLENGES.values())
    completed = len(st.session_state.completed_challenges)
    
    # Display metrics
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Completed", f"{completed}")
    with col_b:
        st.metric("Remaining", f"{total_challenges - completed}")
    
    progress_pct = completed / total_challenges if total_challenges > 0 else 0
    st.progress(progress_pct)
    
    if completed > 0:
        st.success(f"🎉 {int(progress_pct * 100)}% Complete!")
        
        # Achievement badges
        achievements = []
        if completed >= 1:
            achievements.append("🏆 First Steps")
        if completed >= 3:
            achievements.append("⭐ Getting Good")
        if completed >= 6:
            achievements.append("🎓 Master Coder")
        
        if achievements:
            st.markdown("**🏅 Achievements:**")
            for achievement in achievements:
                st.markdown(f"- {achievement}")
    
    st.markdown("---")
    
    # Export Chat
    if st.button("📥 Export Chat History"):
        if st.session_state.messages:
            chat_data = json.dumps(st.session_state.messages, indent=2)
            st.download_button(
                "Download JSON",
                chat_data,
                file_name=f"codementor_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        else:
            st.warning("No chat history to export")
    
    if st.button("🗑️ Clear All Data"):
        st.session_state.messages = []
        st.session_state.completed_challenges = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("**🤖 Powered by**")
    st.markdown("Amazon Q Developer")
    st.markdown("Built for AWS Global Vibe 2025")

# --- Header ---
st.markdown("""
<div class="main-header">
    <h1>🤖 CodeMentor AI Pro</h1>
    <p>Your Complete AI-Powered Coding Education Platform</p>
</div>
""", unsafe_allow_html=True)

# Cloud deployment warning
import os
if os.environ.get('USER') == 'appuser' or 'STREAMLIT' in os.environ.get('HOME', ''):
    st.warning("⚠️ **UI DEMO MODE:** This cloud version shows the interface only. Amazon Q CLI requires local installation. See video/screenshots for full functionality.")

# --- Quick Stats Bar ---
if "Chat" not in mode:  # Don't show on chat mode for cleaner look
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    
    with stat_col1:
        st.metric("🎯 Mode", mode.split()[1] if len(mode.split()) > 1 else mode)
    with stat_col2:
        completed = len(st.session_state.completed_challenges)
        st.metric("✅ Completed", f"{completed}/6")
    with stat_col3:
        chat_count = len([m for m in st.session_state.messages if m["role"] == "user"])
        st.metric("💬 Questions Asked", chat_count)
    with stat_col4:
        st.metric("🔥 Streak", f"{min(completed, 3)}🔥")
    
    st.markdown("---")

# --- MODE 1: Chat Assistant ---
if "Chat" in mode:
    st.subheader("💬 AI Coding Assistant")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        st.markdown("**💡 Quick Questions**")
        quick_questions = [
            "What is a loop?",
            "Explain variables",
            "How to use functions?",
            "What is a class?"
        ]
        for q in quick_questions:
            if st.button(q, key=f"quick_{q}"):
                st.session_state.quick_question = q
    
    with col1:
        # Display chat
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Handle quick questions
        if "quick_question" in st.session_state:
            prompt = st.session_state.quick_question
            del st.session_state.quick_question
        else:
            prompt = st.chat_input("Ask me anything about coding...")
        
        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("🤔 Amazon Q is thinking..."):
                    response = query_amazon_q(prompt)
                st.markdown(response)
            
            st.session_state.messages.append({"role": "assistant", "content": response})

# --- MODE 2: Coding Challenges ---
elif "Challenges" in mode:
    st.subheader("🎮 Interactive Coding Challenges")
    
    # Difficulty selector
    difficulty = st.selectbox("Select Difficulty:", list(CHALLENGES.keys()))
    
    challenges = CHALLENGES[difficulty]
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 📋 Challenges")
        selected_challenge = st.radio(
            "Choose a challenge:",
            [f"{c['title']}" for c in challenges],
            label_visibility="collapsed"
        )
        
        # Reset hint/solution when challenge changes
        current_challenge_id = next(c['id'] for c in challenges if c['title'] == selected_challenge)
        if 'last_challenge_id' not in st.session_state or st.session_state.last_challenge_id != current_challenge_id:
            st.session_state.show_hint = False
            st.session_state.show_solution = False
            st.session_state.last_challenge_id = current_challenge_id
        
        # Get selected challenge
        challenge = next(c for c in challenges if c['title'] == selected_challenge)
        
        # Show challenge details
        st.markdown(f"""
        <div class="challenge-card">
            <h4>{challenge['title']}</h4>
            <p><strong>📋 Task:</strong> {challenge['description']}</p>
            <p><strong>💡 Hint:</strong> {challenge['hint']}</p>
            <p><strong>🎯 Test:</strong> We'll call <code>{challenge['test_input']}</code> and expect <code>{challenge['expected_output']}</code></p>
        </div>
        """, unsafe_allow_html=True)
        
        if challenge['id'] in st.session_state.completed_challenges:
            st.markdown('<div class="success-badge">✅ Completed!</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 💻 Your Solution")
        st.info("💡 **How to complete:** \n1. Edit the code in the black editor below\n2. Click **APPLY (CTRL+ENTER)** button at bottom right of editor\n3. Click **▶️ Run Code** to test your solution!")
        
        # Code editor
        user_code = st_ace(
            value=challenge['starter_code'],
            language='python',
            theme='monokai',
            height=300,
            key=f"editor_{challenge['id']}_{st.session_state.get('refresh_key', 0)}"
        )
        
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            if st.button("▶️ Run Code", type="primary"):
                success, output = execute_code(user_code, challenge['test_input'])
                
                if success:
                    # Check if correct
                    expected = str(challenge['expected_output']).strip()
                    actual = str(output).strip()
                    
                    if actual == expected:
                        # SUCCESS!
                        st.balloons()
                        st.success("🎉 Perfect! Challenge completed!")
                        st.code(f"✅ Output: {actual}", language="text")
                        
                        # Update completion status
                        if challenge['id'] not in st.session_state.completed_challenges:
                            st.session_state.completed_challenges.append(challenge['id'])
                            st.session_state['refresh_key'] = st.session_state.get('refresh_key', 0) + 1
                            time.sleep(1)
                            st.rerun()
                    else:
                        # INCORRECT
                        st.warning("🤔 Not quite right! Try again.")
                        st.info(f"**Your output:** `{actual if actual else '(nothing)'}`\n\n**Expected output:** `{expected}`\n\n💡 **Tip:** Make sure your function returns exactly `{expected}`")
                else:
                    # ERROR
                    st.error(f"❌ **Code Error:**\n```\n{output}\n```\n\n💡 Check your syntax and try again!")
        
        with col_b:
            show_hint_btn = st.button("💡 Get Help from Amazon Q")
        
        with col_c:
            show_solution_btn = st.button("📝 Show Solution")
        
        # Display Hint in EXPANDABLE SECTION - No rerun needed!
        if show_hint_btn or st.session_state.get('show_hint', False):
            st.session_state['show_hint'] = True
            st.session_state['show_solution'] = False
        
        if show_solution_btn or st.session_state.get('show_solution', False):
            st.session_state['show_solution'] = True
            st.session_state['show_hint'] = False
        
        # Show Hint
        if st.session_state.get('show_hint', False):
            st.markdown("---")
            with st.expander("💡 **Hint from Amazon Q** (Click arrow to hide/show)", expanded=True):
                if 'cached_hint' not in st.session_state or st.session_state.get('hint_challenge_id') != challenge['id']:
                    with st.spinner("🤔 Amazon Q is thinking..."):
                        help_prompt = f"I'm stuck on this coding challenge: {challenge['description']}. Give me a small hint (not the full solution) to help me think about how to solve it."
                        st.session_state.cached_hint = query_amazon_q(help_prompt)
                        st.session_state.hint_challenge_id = challenge['id']
                
                st.info(st.session_state.cached_hint)
        
        # Show Solution
        if st.session_state.get('show_solution', False):
            st.markdown("---")
            with st.expander("📝 **Solution from Amazon Q** (Click arrow to hide/show)", expanded=True):
                if 'cached_solution' not in st.session_state or st.session_state.get('solution_challenge_id') != challenge['id']:
                    with st.spinner("🤔 Fetching solution from Amazon Q..."):
                        solution_prompt = f"Show me a clean, well-commented Python solution for: {challenge['description']}. Include the code with explanatory comments."
                        st.session_state.cached_solution = query_amazon_q(solution_prompt)
                        st.session_state.solution_challenge_id = challenge['id']
                
                st.success("✅ Here's a working solution:")
                st.markdown(st.session_state.cached_solution)
                
                st.warning("⚠️ **Next Steps:** \n1. Copy the solution to the editor above\n2. Click **APPLY (CTRL+ENTER)** \n3. Click **▶️ Run Code** to verify it works!")

# --- MODE 3: Code Playground ---
elif "Playground" in mode:
    st.subheader("⚡ Live Code Playground")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 💻 Write Your Code")
        
        # Initialize playground refresh key
        if 'playground_refresh' not in st.session_state:
            st.session_state.playground_refresh = 0
        
        playground_code = st_ace(
            value=st.session_state.user_code or "# Write your Python code here\nprint('Hello, CodeMentor!')",
            language='python',
            theme='monokai',
            height=400,
            key=f"playground_editor_{st.session_state.playground_refresh}"
        )
        
        st.session_state.user_code = playground_code
        
        col_run, col_explain, col_fix = st.columns(3)
        
        with col_run:
            if st.button("▶️ Run Code", type="primary", key="playground_run"):
                success, output = execute_code(playground_code)
                
                st.markdown("### 📤 Output:")
                if success:
                    st.success("✅ Execution successful!")
                    st.code(output, language="text")
                else:
                    st.error(f"❌ Error:\n{output}")
        
        with col_explain:
            if st.button("🔍 Explain Code"):
                explain_prompt = f"Explain this Python code:\n\n{playground_code}"
                with st.spinner("Amazon Q is analyzing..."):
                    explanation = query_amazon_q(explain_prompt)
                st.info(explanation)
        
        with col_fix:
            if st.button("🔧 Help Fix Errors"):
                fix_prompt = f"This code has an error. Help me fix it:\n\n{playground_code}"
                with st.spinner("Debugging..."):
                    fix_suggestion = query_amazon_q(fix_prompt)
                st.warning(fix_suggestion)
    
    with col2:
        st.markdown("### 📚 Code Snippets")
        st.markdown("*Click to load into editor*")
        
        snippets = {
            "Hello World": "print('Hello, World!')",
            "For Loop": "for i in range(5):\n    print(i)",
            "Function": "def greet(name):\n    return f'Hello, {name}!'\n\nprint(greet('CodeMentor'))",
            "List Comprehension": "squares = [x**2 for x in range(10)]\nprint(squares)",
            "Read File": "# File reading example\nwith open('file.txt', 'r') as f:\n    content = f.read()\n    print(content)"
        }
        
        for name, code in snippets.items():
            if st.button(f"📎 {name}", key=f"snippet_{name}"):
                st.session_state.user_code = code
                st.session_state.playground_refresh += 1  # Increment to force editor refresh
                st.rerun()  # Force refresh to update editor

# --- MODE 4: Learning Path ---
elif "Learning Path" in mode:
    st.subheader("📚 Personalized Learning Path")
    
    path_level = st.selectbox("Your Current Level:", ["Beginner", "Intermediate", "Advanced"])
    st.session_state.learning_path = path_level
    
    paths = {
        "Beginner": [
            "1. Variables and Data Types",
            "2. Control Flow (if/else)",
            "3. Loops (for/while)",
            "4. Functions",
            "5. Lists and Dictionaries"
        ],
        "Intermediate": [
            "1. Object-Oriented Programming",
            "2. File Handling",
            "3. Error Handling",
            "4. List Comprehensions",
            "5. Modules and Packages"
        ],
        "Advanced": [
            "1. Decorators",
            "2. Generators",
            "3. Context Managers",
            "4. Async/Await",
            "5. Metaclasses"
        ]
    }
    
    st.markdown(f"### 🎯 {path_level} Learning Path")
    
    col_path, col_lesson = st.columns([1, 2])
    
    with col_path:
        for i, topic in enumerate(paths[path_level], 1):
            if st.button(f"{topic}", key=f"topic_{i}", use_container_width=True):
                st.session_state.current_topic = topic
    
    with col_lesson:
        if "current_topic" in st.session_state:
            topic = st.session_state.current_topic
            st.markdown(f"### 📖 Learning: {topic.split('.')[1] if '.' in topic else topic}")
            
            with st.spinner("🤔 Amazon Q is preparing your lesson..."):
                learn_prompt = f"Teach me about {topic.split('.')[1] if '.' in topic else topic} in Python. Include: 1) Clear explanation 2) Real-world use case 3) Code example 4) Common mistakes to avoid"
                lesson = query_amazon_q(learn_prompt)
            
            st.markdown(lesson)
            
            # Practice button
            if st.button("💪 Practice This Topic"):
                st.info("Switch to 'Coding Challenges' mode to practice!")
        else:
            st.info("👈 Select a topic from the learning path to start")

# --- Footer ---
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>✨ CodeMentor AI Pro | Powered by Amazon Q Developer CLI | Built for AWS Global Vibe Hackathon 2025</p>",
    unsafe_allow_html=True
)