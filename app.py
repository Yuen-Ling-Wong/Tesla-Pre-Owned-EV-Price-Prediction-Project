import streamlit as st
from predict_page import show_predict_page
from explore_page import show_explore_page
from contact_page import show_contact_form
from streamlit_option_menu import option_menu


with st.sidebar:
    selected = option_menu(
    menu_title = None,
    options = ["Predict","Explore", "Contact"],
    icons = ["app-indicator","search","envelope"],
    menu_icon = "cast",
    default_index = 0)
  
if selected == "Predict":
    show_predict_page()
elif selected == "Explore":
    show_explore_page()
else:
    show_contact_form()
      


        