 🌙 Somnia – AI Dream Interpreter

Somnia is an **AI-powered dream interpretation app** that analyzes user-entered dreams (text or speech) using **NLP + GPT-4** to provide symbolic and psychological insights.

---

## ✨ Features
- 📝 **Dream Analysis** – Understands and interprets dream text.  
- 🎙 **Voice Input** – Record dreams with speech-to-text (Whisper API).  
- 🔮 **Symbol Mapping** – Uses a curated dream-symbol dictionary.  
- 🤖 **AI Insights** – GPT-4 generates deep interpretations.  
- 💬 **Chat Interface** – Interactive Q&A about dreams.  
- ⭐ **Feedback System** – Users can refine results.

---

## ⚙️ Tech Stack
- **Frontend:** Next.js, TailwindCSS, shadcn/ui  
- **Backend:** FastAPI + PostgreSQL  
- **AI/NLP:** HuggingFace models + GPT-4 + Whisper  
- **Deployment:** Docker + Docker Compose  

---

This project was personally developed by Prajwal Dikshit and Vibudhan Dubey as part of our MCA learning journey to explore AI + NLP + Web Development.


---

🚀 Getting Started

1. Clone the Repo
git clone https://github.com/prajwaldikshit/Somnia-AI_Dream_Interpreter.git
cd Somnia-AI_Dream_Interpreter

2. Setup Environment
bash
cp .env.example .env
# Add your OpenAI API key inside .env

3. Run with Docker (Recommended)
bash
docker-compose up -d
Frontend → http://localhost:3000

Backend → http://localhost:8000/docs

📂 Project Structure

Somnia/
├── app/        # Frontend (Next.js)
├── backend/    # Backend (FastAPI + NLP logic)
├── data/       # Dream symbol dictionary
├── docker-compose.yml
└── .env.example

🔑 Example API Usage
import httpx
r = httpx.post("http://localhost:8000/analyze_dream", json={
  "dream_text": "I was flying over an ocean holding a golden key..."
})
print(r.json()["interpretation"])
