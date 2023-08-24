import streamlit as st
import openai
from security_utils import check_password
import time
import random
import string

from gdrive_module import save_images_to_google_drive
from gdrive_module import record_user_activity_ads_spark

# Access the OpenAI API key
openai.api_key = st.secrets["api_key"]

# Check if the "username" key exists in the st.session_state object
if "username" not in st.session_state:
    # If the key does not exist, initialize it with the default value "Invoke People"
    st.session_state["username"] = "Invoke People"

# Extract the name from the username
name = st.session_state["username"].split('@')[0]

# Capitalize the first letter of the name
name = name.capitalize()

# configure the default settings of the page.
st.set_page_config(
                page_title="Ads Spark",
                page_icon="🚀",
                layout="wide",
                initial_sidebar_state="expanded"
                )

if check_password():
    # Display a greeting message to the user
    st.write(f'Hello, {name}!')
  
    st.image("photos/AdsSpark_Logo.png")
    st.info(f"""
    Ads Generation using 5 inputs:\n
    📝 Visual Headline\n
    💼 Business Industry *\n
    🎯 Marketing Objective\n
    📣 Ad Objective\n
    """)

    with st.form(key="ads_form"):

        # Note for the user
        st.write("💡 **You can use either English or Malay language**")
        
        # Text input for the product/service
        visual_headline = st.text_input(label="**Visual Headline**")

        # Text input for the business industry
        business_industry = st.text_input(label="**Business Industry**")

        # Select box for the marketing objective
        marketing_objective = st.selectbox(
            label="**Marketing Objective**",
            options=["Awareness", "Consideration", "Conversion"]
        )

            # Select box for the Facebook ad objective
        fb_ad_objective = st.selectbox(
            label="**Ad Objective**",
            options=[
                "Brand Awareness", "Reach", "Traffic", "Engagement", "App Installs",
                "Lead Generation", "Messages", "Conversion",
                "Catalog Sales", "Store Traffic", "Page Likes", "Event Responses",
                "Local Awareness"
            ]
        )
        
        # Submit button
        submit_button = st.form_submit_button(label="**Do the magic!✨**")

    # Handle form submission
    if submit_button:
        # Check if visual_headline and business_industry are blank
        if not visual_headline or not business_industry:
            st.error('Error: Please enter an image prompt')
            return
        else:
            # Generate the text output
            output = f"Generate an affective ads visual with the below details:\n\n"
            output += f"1) Visual Headline: {visual_headline}\n"
            output += f"2) Business Industry: {business_industry}\n"
            output += f"3) Marketing Objective: {marketing_objective}\n"
            output += f"4) Ad Objective: {fb_ad_objective}\n"

            # Display the text output
            st.write(output)
    
            # Assign the output to the prompt variable
            prompt = output
    
            if prompt:
                 # Add a progress bar
                progress_bar = st.progress(0)
                for i in range(100):
                    # Update progress bar
                    progress_bar.progress(i + 1)
                    time.sleep(0.1)
                st.write("Incoming... Making some tricks")
    
                response = openai.Image.create(
                prompt=prompt,
                n=4,
                size="1024x1024",
                )
    
                # Store the generated images in session state
                st.session_state.generated_images = []
                for idx in range(4):
                    image_url = response['data'][idx]['url']
    
                        # Generate a random combination of letters and numbers
                    def generate_random_string(length):
                        letters_and_digits = string.ascii_letters + string.digits
                        return ''.join(random.choice(letters_and_digits) for i in 
                        range(length))
    
                    # Generate a random combination of letters and numbers
                    random_string = generate_random_string(6)
    
                    # Create a caption that includes the random string
                    caption = f'AdsRec_{random_string}'
    
                    # Append a tuple containing the image URL and caption to the generated_images list
                    st.session_state.generated_images.append((image_url, caption))
                    
                    # Display the image with its caption
                    st.image(image_url, caption=caption, use_column_width=True)

        # Initialize the session state with a default value for the "username" key
        if "username" not in st.session_state:
            st.session_state["username"] = "Invoke People"
        
        # Record user activity to Google Sheet
        record_user_activity_ads_spark(st.session_state["username"], st.secrets)
        
        # Save generated images to Google Drive
        save_images_to_google_drive(st.session_state.generated_images, "IdeaSpark-Generated_Photo", st.secrets)

    
    # Create a button to show the history of generated images
    if st.button("Show History"):
        # Check if the generated_images attribute exists in session state
        if "generated_images" in st.session_state:
            
            # Retrieve the list of generated images from session state
            generated_images = st.session_state.generated_images

            # Display the generated images with their original captions
            for image_url, caption in generated_images:
                st.image(image_url, caption=caption, use_column_width=True)
        else:
            st.write("No images have been generated yet")
    
    st.write(f"""**Reference:**""" )
    st.write(f"""📰 decoris - Content Section""" )
    st.image("photos/decoris_content_section.png")
    st.write(f"""🧑‍💼 decoris - Client Profile""" )
    st.image("photos/decoris_client_profile.png")
