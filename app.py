import streamlit as st
import os
import google.generativeai as genai
import PyPDF2 as pdf

from dotenv import load_dotenv
load_dotenv() ## Load all the ENV Varaible

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

## GEMINI PRO RESPONSE

def get_gemini_response(input):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(input)
    return response.text

## PDF TO TEXT
def input_pdf_to_text(uploadedfile):
    reader = pdf.PdfReader(uploadedfile)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text    


#Prompt Template

input_prompt = """
Hello! Please act as an advanced, highly skilled ATS (Applicant Tracking System) with deep expertise in the tech field, covering areas such as software engineering, data science, data analytics, and big data engineering. Your task is to evaluate the candidate’s resume based on the provided job description.

Consider the competitive job market and provide top-notch guidance to help improve the resume. 
1. Assign a precise percentage match based on the job description.
2. Identify any crucial missing keywords with high accuracy.
3. Generate a Profile Summary detailing the candidate's strengths and areas for improvement related to the job description.

Below are the details:
Resume Content: {text}
Job Description: {jd}

Please structure the response as follows:
{
  "JD Match": "%", 
  "MissingKeywords": [], 
  "Profile Summary": ""
}
"""



## StreamLit Interface

st.set_page_config(page_title="ATS Resume EXpert")
st.title("AI Resume Evaluator")
st.text("Improve Your ATS Score")
JD = st.text_area("Paste The Job Description")
uploaded_file = st.file_uploader("Upload Your Resume" , type = "pdf", help = "Please Upload the as PDF")

submit = st.button("Get Your FeedBack")

if submit:
    if uploaded_file is not None:
        text = input_pdf_to_text(uploaded_file)
        response = get_gemini_response(input_prompt)
        st.subheader(response)
    else:
        st.error("Please Upload Your Resume")