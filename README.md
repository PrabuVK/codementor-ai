# 🤖 CodeMentor AI Pro
### AI-Powered Interactive Coding Education Platform
**Built for AWS Global Vibe Hackathon 2025**

[![Watch the Demo Video](https://img.youtube.com/vi/QtzdVztaiCs/maxresdefault.jpg)](https://youtu.be/QtzdVztaiCs)

### 🔗 Quick Links
- **📺 Watch Demo:** [YouTube Video](https://youtu.be/QtzdVztaiCs)
- **🚀 Live App:** [codementor-ai.streamlit.app](https://codementor-ai.streamlit.app)
- **📄 Devpost/DoraHacks:** [Submission Page](https://dorahacks.io/hackathon/awsvibecoding)

---

## 💡 What is CodeMentor AI?
CodeMentor AI Pro is not just a chatbot—it is a complete, gamified education platform powered by **Amazon Q Developer**. It bridges the gap between passive learning and active mastery by providing:

1.  **💬 Chat Assistant:** Instant, context-aware coding help.
2.  **🎮 Interactive Challenges:** Real coding tasks with auto-grading and AI hints.
3.  **⚡ Code Playground:** A secure, sandboxed environment for experimentation.
4.  **📚 Learning Paths:** Structured curriculum generated on-the-fly.

---

## 🛠️ How I Used AWS Tools (Mandatory Proof)
This project was built entirely using the next-generation AWS developer ecosystem.

### 1. Intelligence Engine: Amazon Q Developer CLI
The app's reasoning core is powered by the **Amazon Q Developer CLI** running locally. I built a custom Python wrapper (`subprocess`) to pipe user queries from Streamlit directly to the Q CLI. This enables enterprise-grade AI reasoning within the education workflow.

### 2. Development Environment: Amazon Kiro IDE
I used **Amazon Kiro** as my primary IDE. Its spec-driven development features and AI integration helped me scaffold the UI and manage the project structure 2x faster.

## 📸 Proof of AWS Integration
<img width="1919" height="997" alt="proof_1_amazon_kiro_ide_code" src="https://github.com/user-attachments/assets/4287c7b8-854f-49d0-a945-103bdbe17f14" />
<img width="1228" height="903" alt="proof_2_amazon_q_cli_terminal" src="https://github.com/user-attachments/assets/06340329-912e-4586-bed5-8df0b183b0a5" />

---

## 🏗️ Tech Stack
- **AI Engine:** Amazon Q Developer CLI
- **IDE:** Amazon Kiro
- **Frontend:** Streamlit (Python)
- **Editor:** Streamlit-Ace (Monaco)
- **Deployment:** Streamlit Community Cloud

## 🚀 Installation (Local)
To run this app locally with full AI features:

1.  **Install Amazon Q Developer CLI:**
    ```bash
    # Follow AWS documentation to install 'q'
    q login
    ```
2.  **Clone the Repo:**
    ```bash
    git clone [https://github.com/PrabuVK/codementor-ai.git](https://github.com/PrabuVK/codementor-ai.git)
    cd codementor-ai
    ```
3.  **Run the App:**
    ```bash
    pip install -r requirements.txt
    streamlit run app.py
    ```

