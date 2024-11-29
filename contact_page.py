import streamlit as st
import pandas as pd

def save_submission(email, message):
    # Create a DataFrame and append the new submission
    df = pd.DataFrame({"Email": [email], "Message": [message]})
    df.to_csv("submissions.csv", mode="a", header=False, index=False)



def show_contact_form():
    
    st.header("✉️ Hello! Contact Us:")
    
    contact_new_form ="""
    <form action="https://formsubmit.co/wyl_flora@hotmail.com" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Your name" required>
        <input type="email" name="email" placeholder="Your email" required>
        <textarea name="message" placeholder="Your message here"></textarea>
        <button type="submit">Send</button>
    </form>
    """
    st.markdown(contact_new_form, unsafe_allow_html=True)
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    local_css("Style/style_contact.css")

    st.markdown('<p style="text-align: center; font-size: 11px;">'
                "For more infomation and projects, visit the Creator's GitHub: "
                '<a href="https://github.com/Yuen-Ling-Wong" target="_blank">Flora Wong</a>'
                '</p>', unsafe_allow_html=True)