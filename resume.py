# Import necessary libraries
import streamlit as st
from datetime import datetime
import google.generativeai as genai

# Configure API key for Gemini model
api_key = "AIzaSyCBQl3mTVovqddKKzk7NBJxEHx3ZaZV99I"
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Set up Streamlit app
st.title("AI-Powered Resume Builder")

# Step 1: Collect user information
st.header("Enter Your Details")

photo = st.file_uploader("Upload Your Photo", type=["jpg", "jpeg", "png"])
name = st.text_input("Full Name")
phone = st.text_input("Phone Number")
email = st.text_input("Gmail")
linkedin = st.text_input("LinkedIn Profile URL")

field_of_interest = st.selectbox(
    "Interested Field of Work",
    [
        "Data Science", "Software Development", "Digital Marketing", "Product Management",
        "Cybersecurity", "Cloud Computing", "DevOps", "UI/UX Design", "Business Analysis",
        "Quality Assurance", "IT Support", "Sales Engineering", "Technical Writing",
        "Finance and Accounting", "HR Management", "Project Management", "AI and Machine Learning",
        "Robotics Engineering", "Network Administration", "Blockchain Development", "Game Development",
        "Other"
    ]
)

# Add predefined company options
company_list = [
    "Google", "Microsoft", "Amazon", "Apple", "Facebook (Meta)", "Netflix", "Tesla", "IBM",
    "Salesforce", "Oracle", "Adobe", "Intel", "Cisco", "Spotify", "Shopify", "Twitter (X)",
    "SpaceX", "NVIDIA", "LinkedIn", "Airbnb", "Uber", "Lyft", "Zoom", "Slack", "Samsung",
    "TikTok", "Reddit", "Snap Inc.", "Dell", "HP", "Siemens", "Capgemini", "Accenture",
    "Deloitte", "PwC", "KPMG", "EY", "Spotify", "Alibaba", "Tencent", "Other"
]

company_interest = st.selectbox("Interested Company", company_list)

# Allow user to input a custom company name if "Other" is selected
if company_interest == "Other":
    company_interest = st.text_input("Enter the Name of Your Desired Company")

# Step 2: Collect educational background
st.header("Education Background")
ug_college = st.text_input("Undergraduate College Name")
ug_course = st.text_input("Undergraduate Course")
ug_year = st.text_input("Undergraduate Graduation Year")

has_pg = st.radio("Do you have a Postgraduate Degree?", ["No", "Yes"])
pg_college, pg_course, pg_year = "", "", ""
if has_pg == "Yes":
    pg_college = st.text_input("Postgraduate College Name")
    pg_course = st.text_input("Postgraduate Course")
    pg_year = st.text_input("Postgraduate Graduation Year")

has_phd = st.radio("Do you have a PhD?", ["No", "Yes"])
phd_college, phd_course, phd_year = "", "", ""
if has_phd == "Yes":
    phd_college = st.text_input("PhD College Name")
    phd_course = st.text_input("PhD Field of Study")
    phd_year = st.text_input("PhD Graduation Year")

# Step 3: Collect hobbies
st.header("Hobbies")
hobbies = st.text_area("List Your Hobbies (separate with commas)")

# Step 4: Collect previous job experience details
st.header("Previous Job Experience")
has_experience = st.radio("Do you have previous job experience?", ["Yes", "No"])

job_experience = []
if has_experience == "Yes":
    num_jobs = st.number_input("Number of Previous Jobs", min_value=1, max_value=10, step=1, value=1)
    
    for i in range(num_jobs):
        st.subheader(f"Job {i + 1}")
        company_name = st.text_input(f"Company Name (Job {i + 1})")
        job_title = st.text_input(f"Job Title (Job {i + 1})")
        years_of_experience = st.text_input(f"Years of Experience (Job {i + 1})")
        project_name = st.text_input(f"Project Name (Job {i + 1})")
        project_description = st.text_area(f"Project Short Description (Job {i + 1})")
        
        job_experience.append({
            "company_name": company_name,
            "job_title": job_title,
            "years_of_experience": years_of_experience,
            "project_name": project_name,
            "project_description": project_description
        })

# Function to generate a cover letter
def generate_cover_letter(name, field, company_interest):
    cover_letter_templates = {
        "Data Science": f"Dear Hiring Manager at {company_interest},\n\nI am {name}, a dedicated data science professional with a passion for leveraging data-driven insights to fuel impactful decision-making. With a strong background in statistical analysis, machine learning, and data visualization, I am eager to contribute my expertise to {company_interest}.\n\nYour company's innovative approach to technology and commitment to excellence align perfectly with my career aspirations. I am confident that my skills will be a valuable addition to your data-driven initiatives.\n\nThank you for considering my application. I look forward to the opportunity to discuss how I can contribute to {company_interest}.\n\nBest regards,\n{name}",
        
        "Software Development": f"Dear {company_interest} Recruitment Team,\n\nMy name is {name}, and I am a motivated software developer passionate about building scalable and efficient solutions. I am excited by the opportunity to join {company_interest} and contribute to your dynamic development team.\n\nWith a solid foundation in various programming languages and frameworks, I have a track record of creating robust applications and collaborating effectively within cross-functional teams. I am drawn to {company_interest}'s dedication to pushing technological boundaries and would be honored to be part of such an environment.\n\nThank you for your time and consideration.\n\nBest,\n{name}",
        
        "Other": f"Dear {company_interest} Hiring Manager,\n\nI am {name}, a professional keen on bringing my diverse skill set and passion for excellence to {company_interest}. Your company's values and innovative projects resonate with my career objectives, and I am eager to contribute meaningfully to your team.\n\nI am looking forward to the chance to further discuss how my experience and enthusiasm can benefit {company_interest}.\n\nSincerely,\n{name}"
    }
    return cover_letter_templates.get(field, cover_letter_templates["Other"])

# Generate Resume button logic
if st.button("Generate Resume"):
    if name and phone and email and field_of_interest and company_interest and linkedin:
        st.subheader("Generated Resume")

        if photo:
            st.image(photo, caption="Profile Photo", use_column_width=True)

        st.write("**Name:**", name)
        st.write("**Phone:**", phone)
        st.write("**Email:**", email)
        st.write("**LinkedIn:**", linkedin)
        
        # Generate AI-assisted job objective and skills recommendations
        def generate_objective(field):
            objectives = {
                "Data Science": f"As a data science enthusiast, I aim to leverage data insights to drive strategic decisions at {company_interest}.",
                "Software Development": f"Aiming to join {company_interest} to build scalable software solutions and contribute innovative ideas.",
                "Other": f"Dedicated to bringing my skills to {company_interest} in a meaningful role."
            }
            return objectives.get(field, "An enthusiastic professional seeking new opportunities.")
        
        def recommend_skills(field):
            skills = {
                "Data Science": ["Python", "Machine Learning", "Data Visualization", "SQL"],
                "Software Development": ["JavaScript", "React", "Node.js", "Python"],
                "Other": ["Communication", "Teamwork", "Adaptability", "Problem Solving"]
            }
            return skills.get(field, ["Communication", "Adaptability"])
        
        st.write("**Objective:**", generate_objective(field_of_interest))
        st.write("**Skills:**", ", ".join(recommend_skills(field_of_interest)))
        st.write("**Hobbies:**", hobbies)
        st.write("**Target Company:**", company_interest)
        st.write("**Date Created:**", datetime.now().strftime("%Y-%m-%d"))

        st.subheader("Education")
        st.write("**Undergraduate:**")
        st.write(f"- **College Name:** {ug_college}")
        st.write(f"- **Course:** {ug_course}")
        st.write(f"- **Graduation Year:** {ug_year}")
        
        if has_pg == "Yes":
            st.write("**Postgraduate:**")
            st.write(f"- **College Name:** {pg_college}")
            st.write(f"- **Course:** {pg_course}")
            st.write(f"- **Graduation Year:** {pg_year}")
        
        if has_phd == "Yes":
            st.write("**PhD:**")
            st.write(f"- **College Name:** {phd_college}")
            st.write(f"- **Field of Study:** {phd_course}")
            st.write(f"- **Graduation Year:** {phd_year}")

        st.subheader("Cover Letter")
        st.write(generate_cover_letter(name, field_of_interest, company_interest))

        if has_experience == "Yes":
            st.subheader("Previous Job Experience")
            for idx, job in enumerate(job_experience, 1):
                st.write(f"**Job {idx}:**")
                st.write(f"- **Company Name:** {job['company_name']}")
                st.write(f"- **Job Title:** {job['job_title']}")
                st.write(f"- **Years of Experience:** {job['years_of_experience']}")
                st.write(f"- **Project Name:** {job['project_name']}")
                st.write(f"- **Project Description:** {job['project_description']}")

        # Generate and display the AI-assisted response
        try:
            prompt_text = f"Generate a job application summary based on the following details: Name - {name}, Field - {field_of_interest}, Company - {company_interest}, Previous Experience - {len(job_experience)} job(s)."
            response = model.generate_content(prompt_text)
            st.subheader("AI-Powered Job Application Summary")
            st.write(response.text)
        except Exception as e:
            st.error(f"Error generating content: {e}")

    else:
        st.error("Please fill in all required fields to generate your resume.")
