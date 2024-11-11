import streamlit as st

# Set the title of the app
st.title("Simple Streamlit App")

# Input for user name
name = st.text_input("Enter your name")

# Input for user email
email = st.text_input("Enter your email")

# Display a greeting message when the user submits the form
if st.button("Submit"):
    if name and email:
        st.write(f"Hello {name}, your email is {email}.")
    else:
        st.write("Please fill in both your name and email.")
