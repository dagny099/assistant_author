import streamlit as st
from openai import OpenAI
import os
from PyPDF2 import PdfReader
import pickle
import json
import ast
from datetime import datetime

# ============================================= #

# Setup session
st.set_page_config(
    page_title="CoverCraft",
    page_icon="🦖",
    layout="wide",
   initial_sidebar_state="expanded",
)

# Pre-upload this file if it exists in the main directory
pre_upload_file_path = "./Barbara_Hidalgo-Sotelo_Resume_2024 Long.txt"  
pre_upload_job_description = './JOB_DESCRIPTION.txt'
client = OpenAI(
    api_key = st.secrets["openai_key"]
)

sessionFolder = 'saved_SESSIONS'
docsFolder = 'saved_DOCS'

chatmodels = ['gpt-3.5-turbo', 'gpt-3.5-turbo-1106', 'gpt-4o', 'davinci-002', 'babbage-002']

save_resume = "Resume_text.txt" 
save_cover_letter = "Draft_cover_letter.txt"

# ============================================= #

# Function to save session state to a file
def save_session_state(filename):
    session_state = {key: st.session_state[key] for key in st.session_state.keys()}
    with open(sessionFolder+os.path.sep+filename, 'wb') as file:
        pickle.dump(session_state, file)
        # json.dump(session_state, file)
    st.sidebar.success(f"Session state saved to {filename}")


# # Function to load session state from a file
def load_session_state(filename):
    excludekeys = ['use_def_res']
    try:
        with open(sessionFolder+os.path.sep+filename, 'rb') as file:
            session_state = pickle.load(file)
            # session_state = json.load(file)
        for key, value in session_state.items():
            if key  not in excludekeys:
                st.session_state[key] = value
        st.sidebar.success(f"Session state loaded from {filename}")
    except FileNotFoundError:
        st.sidebar.error(f"No saved state found with filename {filename}")

# Function to generate the first draft of the cover letter
def extract_applicant_info(resume_text):
    completion = client.chat.completions.create(
      model = "gpt-3.5-turbo",
      temperature=0.9,
      response_format={ "type": "json_object" },
      messages = [
          {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
          {"role": "user", "content": f"Based only on an applicants RESUME below, extract this data about the applicant: NAME, EMAIL, ADDRESS, PHONE NUMBER, and SKILLS"},
          {"role": "user", "content": f"If any of these elements are unclear or ambiguous, you can use UNSURE in place of the extracted value."},
          {"role": "user", "content": f"You MUST respond with a python dictionary containing the data elements as keys and the extracted values."},
          {"role": "user", "content": f"Here is the document: {resume_text}"}
      ]
    )
    return json.loads(completion.choices[0].message.content)



# Function to generate the first draft of the cover letter
def generate_cover_letter(resume_text):
    user_name = "Barbara Hidalgo-Sotelo"
    if "job_description" in st.session_state:
        job_description = st.session_state['job_description']
    else:
        job_description = ""

    if "position_title" in st.session_state:
        position_title = st.session_state['position_title']
    else:
        position_title = "DATA SCIENTIST ROLE"

    if "company_name" in st.session_state:
        company_name = st.session_state['company_name']
    else:
        company_name = ""
    
    response = client.chat.completions.create(
        model = st.session_state['model'],
        temperature=st.session_state['temperature'],
        messages = [
            {"role": "user", "content" : f"You will need to generate a cover letter based on specific resume and a job description"},
            {"role": "user", "content" : f"My resume text: {resume_text}"},
            {"role": "user", "content" : f"The job description is: {job_description}"},
            {"role": "user", "content" : f"The candidate's name to include on the cover letter: {user_name}"},
            {"role": "user", "content" : f"The job title/role : {position_title}"},
            # {"role": "user", "content" : f"The hiring manager is: {manager}"},
            # {"role": "user", "content" : f"How you heard about the opportunity: {referral}"},
            {"role": "user", "content" : f"The company to which you are generating the cover letter for (if available) is: {company_name}"},
            {"role": "user", "content" : f"The cover letter should have three content paragraphs"},
            {"role": "user", "content" : f""" 
            In the first paragraph focus on the following: you will convey who you are, what position you are interested in, and where you heard
            about it, and summarize what you have to offer based on the above resume
            """},
                {"role": "user", "content" : f""" 
            In the second paragraph focus on why the candidate is a great fit drawing parallels between the experience included in the resume 
            and the qualifications on the job description.
            """},
                    {"role": "user", "content" : f""" 
            In the 3RD PARAGRAPH: Conclusion
            Restate your interest in the organization and/or job and summarize what you have to offer and thank the reader for their time and consideration.
            """},
            {"role": "user", "content" : f""" 
            note that contact information may be found in the included resume text and use and/or summarize specific resume context for the letter
                """},
            {"role": "user", "content" : f"Use {user_name} as the candidate"},
            
            {"role": "user", "content" : f"Generate a specific cover letter based on the above. Generate the response and include appropriate spacing between the paragraph text"}
        ]
        )
    return response.choices[0].message.content


def optimize_resume(resume, modification):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant that helps users modify their cover letters."},
            {"role": "user", "content": f"Here is the cover letter: {cover_letter}"},
            {"role": "user", "content": f"Please modify it as follows: {modification}"}
        ],
        temperature=st.session_state['temperature']
    )
    return response.choices[0].message.content



# Function to extract applicant information from the resume
def extract_role_info(job_path):
    job_info_text = read_text_file(job_path)
    completion = client.chat.completions.create(
      model = "gpt-3.5-turbo",
      temperature=0.9,
      response_format={ "type": "json_object" },
      messages = [
        {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
        {"role": "user", "content": "Based only on the JOB DESCRIPTION below, extract this data: COMPANY NAME, POSITION TITLE, and JOB DESCRIPTION."},
        {"role": "user", "content": "If any of these elements are unclear or ambiguous, you can use 'UNSURE' in place of the extracted value."},
        {"role": "user", "content": "You MUST respond with a JSON object containing the data elements as keys and the extracted values."},
        {"role": "user", "content": "Here is the JOB DESCRIPTION text:\n" + job_info_text}
      ]
    )
    return json.loads(completion.choices[0].message.content)


# Function to interact with the cover letter
def interact_with_cover_letter(cover_letter, modification):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant that helps users modify their cover letters."},
            {"role": "user", "content": f"Here is the cover letter: {cover_letter}"},
            {"role": "user", "content": f"Please modify it as follows: {modification}"}
        ],
        temperature=st.session_state['temperature']
    )
    return response.choices[0].message.content


# Function to perform ATS scan
def ats_scan(cover_letter, job_description):
    cover_letter_words = set(cover_letter.lower().split())
    job_description_words = set(job_description.lower().split())
    common_words = cover_letter_words.intersection(job_description_words)
    match_percentage = len(common_words) / len(job_description_words) * 100
    
    tmpstr = ", ".join(common_words)
    OUTPUT_STR = f"ATS Match Percentage: {match_percentage:.2f}% \n\n\nCommon words/phrases found:\n{tmpstr}"
    return OUTPUT_STR, match_percentage, common_words


def save_changes(save_modified):
    st.session.state['save_modified'] = True


def read_pdf(res_file):
    pdf_reader = PdfReader(res_file)

    # Collect text from pdf
    res_text = ""
    for page in pdf_reader.pages:
        res_text += page.extract_text()
    return res_text


# Function to read text from a file
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def make_filename(prefix):
    today_date = datetime.today().strftime('%Y-%m-%d') ## Get today's date
    current_hour = datetime.now().hour  ## Get the current hour
    time_suffix = "am" if current_hour < 12 else "pm"  ## Determine if it's AM or PM

    return f"{prefix}_{today_date}_{time_suffix}"


# ============================================= #

# List all saved session files:
try:
    savedSessions = os.listdir(sessionFolder)
    if ".gitkeep" in savedSessions:
        savedSessions.remove(".gitkeep")
except FileNotFoundError:
    st.error(f"The directory '{sessionFolder}' does not exist.")
    savedSessions = []

# ============================================= #

if "user_input" in st.session_state:
    DEF_TEMP = st.session_state["user_input"]
else:
    st.session_state["user_input"] = ""

if "model" not in st.session_state:
    model = 'gpt-3.5-turbo'

if "temperature" not in st.session_state:
    DEF_TEMP = 0.7
else:
    DEF_TEMP = st.session_state["temperature"]

if "ats_results_resume" not in st.session_state:
    st.session_state["ats_results_resume"] = None

if "ats_results_letter" not in st.session_state:
    st.session_state["ats_results_letter"] = None

if "candidate_info" not in st.session_state:
    DEF_NAME = ""
    DEF_EMAIL = ""
    DEF_SKILLS = ""
else:
    candidate_info = st.session_state["candidate_info"]
    DEF_NAME = candidate_info["NAME"]
    DEF_EMAIL = candidate_info["EMAIL"]
    DEF_SKILLS = candidate_info["SKILLS"]
    # del st.session_state['candidate_info']  #Remove candidate_info once it gets to a model

# Check if a pre-uploaded job description exists
if 'role_info_extracted' not in st.session_state:
    if os.path.exists(pre_upload_job_description):
        # Extract the JOB ROLE information
        st.session_state['role_info_extracted'] = extract_role_info(pre_upload_job_description)

if "role_info_extracted" in st.session_state:
    role_info = st.session_state['role_info_extracted']
    st.session_state['company_name']  = role_info.get('COMPANY NAME', '')
    st.session_state['position_title'] = role_info.get('POSITION TITLE', '')
    st.session_state['job_description'] = role_info.get('JOB DESCRIPTION', '')
    del st.session_state['role_info_extracted']  #Remove role_info_extracted once it gets to a model
else:
    if "company_name" not in st.session_state:
        st.session_state['company_name']  = ""
    if "position_title" not in st.session_state:
        st.session_state['position_title'] = ""
    if "job_description" not in st.session_state:
        st.session_state['job_description'] = ""

# ============================================= #
side_title = st.sidebar.title('Enter Customizing Details')
job_session_header = st.sidebar.empty()
job_session_1 =  st.sidebar.empty()
job_session_2 =  st.sidebar.empty()
job_session_3 =  st.sidebar.empty()
job_session_space = st.sidebar.empty()

cand_session_header = st.sidebar.empty()
cand_session_1 = st.sidebar.empty()
cand_session_2 =  st.sidebar.empty()
cand_session_3 =  st.sidebar.empty()
cand_session_4 =  st.sidebar.empty()
cand_session_space =  st.sidebar.empty()

sec_session_header = st.sidebar.empty()
sec_session_1 = st.sidebar.empty()
sec_session_2 = st.sidebar.empty()
sec_session_3 = st.sidebar.empty()
sec_session_4 = st.sidebar.empty()
sec_session_5 = st.sidebar.empty()
sec_session_6 = st.sidebar.empty()
sec_session_7 = st.sidebar.empty()
sec_session_8 = st.sidebar.empty()
sec_session_9 = st.sidebar.empty()
sec_session_10 = st.sidebar.empty()
sec_session_space = st.sidebar.empty()

mod_session_header = st.sidebar.empty()
mod_session_1 = st.sidebar.empty()
mod_session_2 = st.sidebar.empty()
mod_session_space = st.sidebar.empty()

# ============================================= #

# Sidebar for model features
mod_session_header.subheader("Specify Model Parameters for Writing Tasks:")
model = mod_session_1.selectbox("Choose OpenAI Model:", chatmodels,) #, key="model")
st.session_state['model'] = model
temperature = mod_session_2.slider("Temperature:", min_value=0.0, max_value=1.0, value=DEF_TEMP,) # key="temperature")
st.session_state['temperature'] = temperature
mod_session_space.markdown("<hr>", unsafe_allow_html=True)

# Sidebar for job features
job_session_header.subheader("About the Job")
company_name = job_session_1.text_input("Company Name", value=st.session_state['company_name']) #,  on_change="company_name")
st.session_state['company_name'] = company_name
position_title = job_session_2.text_input("Position Title", value=st.session_state['position_title']) #key="position_title")
st.session_state['position_title'] = position_title
job_description = job_session_3.text_area("Job Description", value=st.session_state['job_description']) #key="job_description")
st.session_state['job_description'] = job_description
job_session_space.markdown("<hr>", unsafe_allow_html=True)

# Sidebar for applicant features
cand_session_header.header("About the Applicant")
applicant_name = cand_session_1.text_input("Applicant Name", value=DEF_NAME) #,  key="applicant_name")
st.session_state['applicant_name'] = applicant_name
applicant_email = cand_session_2.text_input("Applicant Email", value=DEF_EMAIL) #,  key="applicant_email")
st.session_state['applicant_email'] = applicant_email
applicant_skills = cand_session_3.text_area("Applicant Skills", value=DEF_SKILLS) #,  key="applicant_skills")
st.session_state['applicant_skills'] = applicant_skills
cand_session_space.markdown("<hr>", unsafe_allow_html=True)

            
# Sidebar button to Save Session State 
sec_session_header.header("Session State Management")
sec_session_1.subheader("Save Session")
DEF_save_session = make_filename(st.session_state["company_name"])
save_session_name = sec_session_2.text_input("Enter filename to save session state:", value=DEF_save_session) #, key='save_session_name')
if sec_session_3.button("Save Session State"):
    if save_session_name:
        save_session_state(save_session_name)
    else:
        sec_session_4.error("Please enter a filename to save the session state.")

sec_session_5.subheader("Load Session")
# load_filename = sec_session_6.text_input("Enter filename to load session state:", value='')
load_filename = sec_session_6.selectbox("Select a saved session", savedSessions)
if sec_session_7.button("Load Session State"):
    if load_filename:
        load_session_state(load_filename)
        st.rerun()
    else:
        sec_session_8.error("Please enter a filename to load the session state.")

if sec_session_9.button("Show session state variable:"):  # Display the session state for debugging purposes
    sec_session_10.write(st.session_state)
sec_session_space.markdown("<hr>", unsafe_allow_html=True)

# ============================================= #
pre_uploaded_resume = ""

# Streamlit App
st.title("CareerCraft: My Job App Co-Pilot")

st.write('Welcome! This app is a personalized assistant for crafting tailored resumes and cover letters. From generating professional drafts to ensuring ATS compatibility, it’s your all-in-one tool for job application success.')

# Section 1: Ingest Information
st.subheader("1. Ingest Resume :clipboard:")
with st.expander("CLICK TO OPTIMIZE RESUME WITH AI", expanded=False):
    # st.subheader("Ingest base resume:")
    st.markdown("<h5>Step 1) Start with base resume:</h5>", unsafe_allow_html=True)
    sec0 = st.empty()
    sec1 = st.empty()
    sec2 = st.empty()
    sec3 = st.empty()
    # Text Area Input
    sec2.checkbox("Check to load default RESUME.txt ", value=False, key="use_def_res")
    if 'text_input' in st.session_state:
        DEF_USER_TEXT = st.session_state['text_input']
    else:
        DEF_USER_TEXT = ""

    if st.session_state["use_def_res"]:
        if os.path.exists(pre_upload_file_path):
            DEF_USER_TEXT = read_text_file(pre_upload_file_path)
        else: 
            st.write('No existing RESUME.txt found')
    else:
        DEF_USER_TEXT = ""


    text_input = sec1.text_area("Enter your information here (e.g., job title, company name, your skills, etc.):", 
                            value=DEF_USER_TEXT) #, key="text_input")
    st.session_state['text_input'] = text_input

    # File Upload Input
    file_input = sec3.file_uploader("Or upload a text file or PDF file", type=["txt", "pdf"])

    # Buttons for 
    colIngest_1, colShow2 = st.columns(2)

    with  colIngest_1:
        # 1 - Input txt
        if st.button("Ingest Information"):
            # From the text box
            if st.session_state['text_input']:
                st.session_state['user_input'] = st.session_state['text_input']
                st.write("Information ingested from text area.")

            # From the file uploader
            elif file_input:
                if file_input.type == "text/plain":
                    user_input = file_input.read().decode("utf-8")
                    st.session_state['user_input'] = user_input
                    st.write("Information ingested from text file.")
                elif file_input.type == "application/pdf":
                    user_input = read_pdf(file_input)
                    st.session_state['user_input'] = user_input
                    st.write("Information ingested from PDF file.")
            st.session_state['candidate_info'] = extract_applicant_info(st.session_state['user_input'])            
            
            # Create a download button
            sec0.download_button(
                label = "Download Resume (text file)",
                data = st.session_state['user_input'],
                file_name = save_resume,
                mime='text/plain'
            )
            st.write("Click the button above to download the file.")
            # else:
            #     st.write("Please enter your information in the text area or upload a file.")


    with  colShow2:
        if 'candidate_info' in st.session_state:
            st.write(st.session_state['candidate_info'])
            # keep_info = colIngest_1.selectbox("Are you satisfied with the extracted info?", ["","No", "Yes"])
            # if keep_info=="Yes":
            #     st.rerun()
            # elif keep_info=="No":
            #     del st.session_state['candidate_info']
                


# Section 2: Build First Draft
st.subheader("2. Build First Draft :pencil:")
if 'first_draft' not in st.session_state:
    if st.button("Generate Cover Letter"):
        if st.session_state['user_input']:
            cover_letter = generate_cover_letter(st.session_state['user_input'])
            st.session_state['first_draft'] = cover_letter
            st.session_state['cover_letter'] = cover_letter
        else:
            st.write("Please enter your information in the section above.")
else:
    with st.expander("Display First Draft"):
        st.write(st.session_state['first_draft'])

# Section 3: Interact with Cover Letter
st.subheader("3. Interact with Cover Letter :love_letter:")
if 'cover_letter' in st.session_state:
    with st.expander("Display Current Draft:"):
        st.write(st.session_state['cover_letter'])
    
    modification = st.text_area("Describe the changes you want to make (e.g., change the tone to be more formal, add more details about a specific skill, etc.):") #, key="modification")
    if st.button("Modify Cover Letter"):
        if modification:
            modified_cover_letter = interact_with_cover_letter(st.session_state['cover_letter'], modification)
            st.session_state['cover_letter'] = modified_cover_letter

            with st.expander("Display Modified Draft:"):
                st.write(modified_cover_letter)
        else:
            st.write("Please describe the changes you want to make.")
else:
    st.write("Please generate a first draft of the cover letter in the section above.")

# DONE - Default values to speed testing. (Check for files "RESUME.txt", "JOB DESCRIPTION.txt" & load it by default)
# DONE - Add ability to load session state. (Load saved values and display)
# DONE - Add option to run RESUME or COVER LETTER through the ATS
# TODO?? Ugh! I TRIED FOR AN HR AND FAILED - Add a button to save/reject modifications to st.session_state['cover_letter'] 


# Section 4: ATS Scanning
st.subheader("4. Review ATS Scanning :dart:")
colRes, colCover = st.columns(2)
with colRes:
    if 'user_input' in st.session_state:
        st.write('Comparing RESUME (key=user_input) to Job Description (sidebar):')
        if st.button("Scan resume with ATS"):
            if st.session_state['job_description'] :
                OUTPUT_STR, match_percentage, common_words = ats_scan(st.session_state['user_input'], st.session_state['job_description'])
                st.session_state['ats_results_resume']=OUTPUT_STR
            else:
                st.write("Please paste the job description into the sidebar.")
        if st.session_state['ats_results_resume']:
            st.write(st.session_state['ats_results_resume'])
    else:
        st.write("Please ingest resume info in Section 1 above.")

with colCover:
    if 'cover_letter' in st.session_state:
        st.write('Comparing COVER LETTER to Job Description (sidebar):')
        if st.button("Scan cover letter with ATS"):
            if st.session_state['job_description'] :
                OUTPUT_STR, match_percentage, common_words = ats_scan(st.session_state['cover_letter'], st.session_state['job_description'])
                st.session_state['ats_results_letter']=OUTPUT_STR
            else:
                st.write("Please paste the job description into the sidebar.")
        if st.session_state['ats_results_resume']:
            st.write(st.session_state['ats_results_letter'])
    else:
        st.write("Please generate cover letter in Section 2 and (optionally) modify it in Section 3 above.")


# Section 5: Save Final Cover Letter
st.subheader("5. Save Final Cover Letter :label:")
if 'cover_letter' in st.session_state:

    # Create a download button
    st.download_button(
        label = "Download Covere Letter (text file)",
        data = st.session_state['cover_letter'],
        file_name = save_cover_letter,
        mime='text/plain'
    )
    st.write("Click the button above to download the file.")
    st.write("OR")
    save_cover_letter = st.text_input("Enter filename to save Cover Letter:") #,key='save')  #
    if st.button("Save Cover Letter"):
        if save_cover_letter:
            with open(save_cover_letter, "w") as file:
                file.write(st.session_state['cover_letter'])
            st.write(f"Cover letter saved as {save_cover_letter}")
        else:
            st.error("Please enter a filename to save the cover letter.")
else:
    st.write("Please generate and modify your cover letter in the sections above.")
