📌 Multi-Agent LinkedIn Content Studio (DeepSeek Web UI)

An intelligent, production-ready multi-agent system that automates research → writing → optimization → scheduling of LinkedIn posts using DeepSeek’s LLM API and Streamlit Web UI.

✔ Generates trending topics
✔ Writes 100% original, SEO-optimized LinkedIn posts
✔ Saves long-term memory
✔ Interactive, beautiful UI
✔ Multi-agent pipeline
✔ CSV/TXT outputs
✔ LinkedIn-style preview

🚀 Features
🔥 Multi-Agent Pipeline

Research Agent → Finds trending LinkedIn topics

Writer Agent → Writes posts in your niche, tone & length

Optimizer Agent → Improves hooks, hashtags, engagement

Scheduler Agent → Suggests best posting times

Memory Manager → Stores long-term session insights

🧠 System Architecture
User Input
   ↓
Research Agent → Trending Topics
   ↓
Writer Agent → First Draft (Raw Output)
   ↓
Optimizer Agent → Refined Post (Final Output)
   ↓
Scheduler Agent → Suggested Posting Time
   ↓
Memory System → Save session | Load previous memory
   ↓
Streamlit UI → Preview | Download | History

📁 Folder Structure
LinkedIn_Agent_Web_App/
│
├── app.py                # Main Streamlit Web App
├── agent_memory.json     # Long-term memory
├── requirements.txt      # Dependencies
├── README.md             # Documentation
└── screenshots/
     ├── Main UI.PNG
     ├── Generated Topics.PNG
     ├── LinkedIn-style Post Preview.PNG
     └── History & Memory Section.PNG

🖥️ Screenshots
🏠 Main UI
<img src="screenshots/Main UI.PNG" width="90%">
🧠 Generated Topics
<img src="screenshots/Generated Topics.PNG" width="90%">
🔍 Post Preview
<img src="screenshots/LinkedIn-style Post Preview.PNG" width="90%">
📘 Memory & History
<img src="screenshots/History & Memory Section.PNG" width="90%">
📦 Installation & Running Instructions
1. Clone Repo
git clone https://github.com/tabinda331/LinkedIn_Agent_Web_App.git
cd LinkedIn_Agent_Web_App

2. Install dependencies
pip install -r requirements.txt

3. Add your DeepSeek API key

Create .env file:

DEEPSEEK_API_KEY=your_key_here

4. Run Streamlit App
streamlit run app.py

📝 Sample Output (Final LinkedIn Post)
🚀 Why Getting Jobs Is Harder Today

The job market has changed more in the last 3 years than in the last decade...

(Your post continues...)

🎯 Evaluation (For Kaggle)

This project demonstrates:

✔ Multi-Agent System

Parallel + sequential agent pipeline

✔ LLM Tool Usage

DeepSeek API for generation & rewriting

✔ Long-term Memory

Context stored across runs via JSON

✔ Logs + Traceability

Raw + final post logs + UI previews

✔ UI + Deployment

Streamlit interface = production-ready demo

🧩 Limitations & Future Work

Add auto LinkedIn publishing

Add topic sentiment analysis

Add voice input

Add user profile intelligence

📽️ Video Demo (Required by Kaggle)

Upload to YouTube or Google Drive and paste link here

📜 License

MIT License

🤝 Author & Credits

Developed by Tabinda Noreen
Part of Kaggle Agents Intensive Capstone Submission
