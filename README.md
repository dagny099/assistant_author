## 🦖 CareerCraft: Resume and Cover Letter Customization App

Thanks for visiting the GitHub repository for **CareerCraft**, an interactive assistant for crafting tailored resumes and cover letters.


### 🌟 About This Project
CareerCraft is a publicly available **Streamlit web application** that leverages advanced language models (LLMs), including OpenAI's GPT-3.5 and GPT-4, to help job seekers customize their resumes and cover letters effectively. Originally hosted on [Streamlit Community Cloud](https://streamlit.io/cloud), the app is now primarily deployed on **Heroku** for enhanced uptime and reliability.

### 🌐 Visit the Application
- **Primary (Heroku)**: [https://careercraft.barbhs.com](https://careercraft.barbhs.com)
- **Backup (Streamlit Cloud)**: [https://barbsassistant.streamlit.app](https://barbsassistant.streamlit.app)



## 🚀 Quickstart Guide (Heroku)

### **Prerequisites**
- Python 3.8+
- Streamlit
- OpenAI Python library
- PyPDF2
- pickle
- json
- Heroku CLI (recommended)

### **Installation Steps**
1. **Clone the repository:**
   ```bash
   git clone https://github.com/dagny099/assistant_author.git
   cd assistant_author
   ```

2. **Install required Python packages:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set your OpenAI API key in Heroku:**
   ```bash
   heroku config:set OPENAI_API_KEY="your_openai_api_key_here"
   ```

### **Deploying to Heroku**
Ensure your repository contains:
- `Procfile`
- `setup.sh`

Deploy via GitHub integration or CLI:
```bash
git push heroku main
```

### 🗃️ **Important Note on Persistence:**
Heroku uses ephemeral storage. Uploaded files or generated documents stored locally will not persist across restarts. In Q2 of 2024 I'll be integrating cloud storage services like AWS S3 for persistent file management, stay tuned.

---

## 📂 Project Structure
- `main.py`: Core Streamlit application logic.
- `requirements.txt`: Dependencies.
- `Procfile`: Heroku deployment instructions.
- `setup.sh`: Streamlit server configuration for Heroku.

### 🦕 Architecture Overview
- Add a visual architecture diagram here to illustrate user workflow, integration with OpenAI APIs, and interaction with external cloud storage.
<p align="center">
  <img src="https://www.barbhs.com/assets/images/portfolio/OverallArchitecture-CareerCraft-v1.png" alt="Architecture Diagram" width="70%">
  <br>
  <em>Figure: System architecture diagram showing how different components interact</em>
</p>


## 🌟 Usage Instructions
<p align="center">
  <img src="https://www.barbhs.com/assets/images/portfolio/UserSteps_CareerCraft_v2.png" alt="Architecture Diagram" width="70%">
  <br>
</p>

✅ **1. Upload Your Resume**  
* Go to the Ingest Resume section.  
* Choose between:  *Manual text entry* or *Upload PDF or TXT file*  
* Click "Ingest Information" to process.

✅ **2. Input Job Details**  
* Use the sidebar to provide:  
Company Name | Position Title | Job Description

✅ **3. Generate First Draft**  
- In the Build First Draft section, click "Generate Cover Letter".  
- A first draft of your tailored cover letter appears immediately.  

✅ **4. Interactive Editing**  
- To modify the draft: Describe changes clearly in the text box (e.g., "make the tone more formal", "highlight leadership experience").  
- Click "Modify Cover Letter".  

✅ **5. ATS Keyword Optimization**  
* Click "Scan resume with ATS" or "Scan cover letter with ATS".
* Results show a percentage match and common keywords, highlighting any gaps.

✅ **6. Download Final Documents**  
* Use the provided download buttons to immediately save your finalized resume and cover letter.


## 🎯 Roadmap: Q4 2024

1. **Enhanced ATS Scanning:**
   - NLP-based keyword analysis (SpaCy, transformers)
2. **Additional Format Support:**
   - Microsoft Word document handling
3. **Expanded LLM Guidance:**
   - Advanced user interactions and editing suggestions


## 📜 License
Licensed under the MIT License.