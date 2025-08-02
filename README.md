# 📝 MindMemos  

MindMemos is a smart note-generation web app built with Streamlit, Google Gemini AI, and MongoDB. It allows users to upload PDFs or DOCX files and automatically generate different types of notes.  

## ✨ Features  
- 🔐 User Authentication: Secure Sign Up / Login system with password hashing  
- 📂 Upload PDF or DOCX: Supports multiple document formats  
- 🤖 AI-Powered Notes: Generate  
  - Summary Notes  
  - Detailed Notes  
  - Q&A Format Notes  
- 🗂 User History: Save and view previous uploads anytime  
- ⬇️ Download Notes: Export generated notes as PDF  
- 💬 Feedback: Submit feedback after downloading notes  

## 🛠 Tech Stack  
- Frontend & Backend: Streamlit (Python)  
- AI Model: Google Gemini API (Generative AI)  
- Database: MongoDB Atlas  
- Libraries:  
  - PyPDF2 (Extract text from PDFs)  
  - python-docx (Extract text from DOCX)  
  - bcrypt (Password hashing)  
  - python-dotenv (Manage environment variables)  
  - ReportLab (Export generated notes as PDF)  

## ⚙️ Installation & Setup  
1. Clone the repo 
   git clone https://github.com/Kanikaekcoshiya/MindMemos.git
2. Create & activate virtual environment - python -m venv venv
  - Windows- venv\Scripts\activate
  - Mac/Linux- source venv/bin/activate
3. Install dependencies- pip install -r requirements.txt 
4. Run the app - streamlit run app.py 

## Made with ❤️ by Kanika Ekcoshiya 

