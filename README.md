# README.md

Hi there. :bowtie: Thanks for visting the GitHub repository for my Resume and Cover Letter Customization App. 

## About This Site
This repository is for a publicly-available **Streamlit web application** designed to assist users in creating tailored resumes and cover letters for job applications. Powered by advanced language models (LLMs) like OpenAI's GPT-3.5 and GPT-4, the app offers an interactive and user-friendly workflow to refine application materials. For the moment, the app is hosted on [Streamlit Community Cloud](https://streamlit.io/cloud) (for which there are definitely pros and cons). 

### Visit My Website
You can explore the application here: 
https://barbsassistant.streamlit.app/


## Features
1. **Resume Import**:
   - Load an existing resume in PDF or text format.
   - Alternatively, type resume content directly into a text box.

2. **Customizable Details**:
   - Input specific job details in the sidebar to customize the outputs.

3. **Applicant Information Extraction**:
   - Automatically extract applicant details from the uploaded resume and display them in the sidebar.
     - Uses text parsing techniques to identify key details like name, contact information, and professional summary.
     - Relies on pattern matching and context-based inference to ensure accuracy, with fallback mechanisms for manual edits.

4. **Cover Letter Drafting**:
   - Generate a first draft of a cover letter based on the resume and job description.
   - Edit the cover letter interactively using the LLM to request changes (e.g., tone, content).

5. **Applicant Tracking System (ATS) Keyword Check**:
   - Perform a basic ATS scan to ensure relevant keywords are present in the resume and cover letter.
     - This scan identifies critical keywords related to job descriptions and compares them with those in the resume and cover letter.
     - While modeled after common ATS systems, it focuses on identifying gaps in keyword alignment rather than emulating a specific proprietary system.

6. **Downloadable Outputs**:
   - Save the finalized cover letter as a text file.

7. **Session Management**:
   - Save and load session states to allow for easy resumption of work.
   

## Getting Started

### Prerequisites

- Python 3.8+
- Streamlit
- OpenAI Python library
- Additional libraries: `PyPDF2`, `pickle`, `json`

---

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/dagny099/assistant_author.git
   cd assistant_author
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Add your OpenAI API key to `Streamlit` secrets:
   ```plaintext
   [openai_key]
   YOUR_API_KEY
   ```
   For more details on setting up Streamlit secrets, refer to the [Streamlit documentation](https://docs.streamlit.io/library/advanced-features/secrets-management).

### Running the App

1. Start the Streamlit app:
   ```bash
   streamlit run main.py
   ```
2. Open your browser at the URL provided (usually `http://localhost:8501`).

---

## Usage

### Workflow

1. **Load Resume**:
   - Upload a PDF or text file, or type resume details directly into the text box.

2. **Customize Job Details**:
   - Input information about the target job in the sidebar.

3. **Generate Cover Letter**:
   - Click to generate a first draft of the cover letter based on the loaded resume.

4. **Interactive Editing**:
   - Use the app's interface to request edits or modifications to the draft.

5. **ATS Scan**:
   - Analyze keyword relevance for ATS compatibility (if a job description is available).

6. **Download Finalized Outputs**:
   - Save the cover letter to your local machine.

---

## Project Structure

- `main.py`: Core application logic.
- `requirements.txt`: List of dependencies.
- `saved_SESSIONS/`: Directory for storing session states.
- `saved_DOCS/`: Directory for saving resumes and cover letters.

---

## Roadmap: Q4 2024

1. **Enhanced ATS Scanning**:
   - Integrate a more sophisticated keyword analysis tool.
     - Explore NLP libraries like SpaCy or NLTK for advanced text analysis.
     - Use pre-trained models or fine-tune transformers to extract and evaluate keyword relevance.
     - Implement statistical approaches such as TF-IDF or cosine similarity to enhance keyword matching.
2. **Support for Additional Formats**:
   - Enable Word document imports/exports.
3. **Expanded LLM Features**:
   - Add detailed guidance for LLM interaction improvements.

---

## License
This project is licensed under the MIT License.

