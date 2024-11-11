import streamlit as st
from fpdf import FPDF
from datetime import datetime

# Set up the Streamlit app
st.title("AI-Powered Resume Builder")

# Step 1: Collect Basic Information
st.header("Personal Details")
name = st.text_input("Full Name")
phone = st.text_input("Phone Number")
email = st.text_input("Email Address")
address = st.text_area("Address")

# Step 2: Education and Experience
st.header("Education Details")
degree = st.text_input("Degree")
university = st.text_input("University/School")
grad_year = st.text_input("Year of Graduation")

st.header("Work Experience")
has_experience = st.radio("Do you have work experience?", ["Yes", "No"])
experience = []

if has_experience == "Yes":
    num_jobs = st.number_input("Number of Previous Jobs", min_value=1, max_value=10, step=1, value=1)
    for i in range(num_jobs):
        company = st.text_input(f"Company Name (Job {i + 1})")
        job_title = st.text_input(f"Job Title (Job {i + 1})")
        duration = st.text_input(f"Duration (Job {i + 1})")
        description = st.text_area(f"Description (Job {i + 1})")
        experience.append({
            "company": company,
            "job_title": job_title,
            "duration": duration,
            "description": description
        })

# Step 3: Skills
st.header("Skills")
skills = st.text_area("List your skills (separated by commas)")

# Function to generate the resume PDF
def generate_resume():
    pdf = FPDF()
    pdf.add_page()

    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Resume", ln=True, align="C")

    # Basic Information
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"Name: {name}", ln=True)
    pdf.cell(0, 10, f"Phone: {phone}", ln=True)
    pdf.cell(0, 10, f"Email: {email}", ln=True)
    pdf.cell(0, 10, f"Address: {address}", ln=True)

    # Education
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Education", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"{degree}, {university} - {grad_year}", ln=True)

    # Experience
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Work Experience", ln=True)
    pdf.set_font("Arial", "", 12)
    for job in experience:
        pdf.cell(0, 10, f"Company: {job['company']}", ln=True)
        pdf.cell(0, 10, f"Title: {job['job_title']}", ln=True)
        pdf.cell(0, 10, f"Duration: {job['duration']}", ln=True)
        pdf.multi_cell(0, 10, f"Description: {job['description']}")
    
    # Skills
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Skills", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, skills.replace(",", ", "))

    # Save PDF
    pdf_output = f"{name.replace(' ', '_')}_Resume.pdf"
    pdf.output(pdf_output)
    return pdf_output

# Generate and download PDF button
if st.button("Generate Resume PDF"):
    if name and phone and email:
        pdf_file = generate_resume()
        with open(pdf_file, "rb") as file:
            st.download_button(label="Download Resume", data=file, file_name=pdf_file, mime="application/pdf")
    else:
        st.error("Please fill in all required fields.")
