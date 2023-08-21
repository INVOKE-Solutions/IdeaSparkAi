import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from pytz import timezone

introduction = """**IdeaSpark**   

An innovative app designed to help creatives generate 
compelling ads for social media platforms such as Facebook, Instagram, LinkedIn, and more. With its advanced 
AI technology, IdeaSpark takes the guesswork out of ad creation by providing users with a wealth of ideas and inspiration. 
Whether you're looking to boost engagement, increase conversions, or simply stand out from the crowd, 
IdeaSpark is the perfect tool for any creative looking to take their social media advertising to the next level. 💡"""

def password_entered():
    """Checks whether a username and password entered by the user are correct."""

    if st.session_state["username"] in st.secrets["users"] and st.session_state["password"] == st.secrets["users"][st.session_state["username"]]:
        st.session_state["password_correct"] = True
        del st.session_state["password"]  # don't store password

        # Use credentials to create a client to interact with the Google Drive API
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('user-activity-ideaspark-aed98c90f4cb.json', scope)

        activity = gspread.authorize(creds)

        # Find a workbook by name and open the first sheet
        sheet = activity.open("user-activity-ideaspark").sheet1

        # Get the current date and time
        now = datetime.now(timezone('Asia/Kuala_Lumpur'))
        date_time = now.strftime("%m/%d/%Y %H:%M:%S")

        # Insert data into the sheet
        row = [st.session_state["username"], date_time]
        index = 2
        sheet.insert_row(row, index)
    else:
        st.session_state["password_correct"] = False



#adding a login page
def check_password():
    """Returns `True` if the user had the correct username and password."""

    if "password_correct" not in st.session_state:

        st.header("IdeaSpark")
        st.image("photos/IdeaSpark_Logo.png")  # Add this line to display the image
        st.text_input("**Username**", key="username")
        st.text_input(
            "**Password**", type="password", on_change=password_entered, key="password"
        )
        st.markdown(introduction)
        
        return False
    
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("**Username**", key="username")
        st.text_input(
            "**Password**", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Username or password incorrect")
        return False

    else:
        # Password correct.
        return True
