import streamlit as st

introduction = """**IdeaSpark**   

An innovative app designed to help creatives generate 
compelling ads for social media platforms such as Facebook, Instagram, LinkedIn, and more. With its advanced 
AI technology, IdeaSpark takes the guesswork out of ad creation by providing users with a wealth of ideas and inspiration. 
Whether you're looking to boost engagement, increase conversions, or simply stand out from the crowd, 
IdeaSpark is the perfect tool for any creative looking to take their social media advertising to the next level. 💡"""

def password_entered():
    """Checks whether a password entered by the user is correct."""

    if st.session_state["password"] == st.secrets["password"]: 
        st.session_state["password_correct"] = True
        del st.session_state["password"]  # don't store password
    else:
        st.session_state["password_correct"] = False

#adding a login page
def check_password():
    """Returns `True` if the user had the correct password."""

    if "password_correct" not in st.session_state:

        st.header("IdeaSpark")
        st.image("photos/IdeaSpark_Logo.png")  # Add this line to display the image
        st.text_input(
        "Please enter your password", type="password", on_change=password_entered, key="password"
        )
        st.markdown(introduction)
        
        return False
    
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Please enter your password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False

    else:
        # Password correct.
        return True
