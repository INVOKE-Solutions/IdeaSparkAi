import streamlit as st
import openai
from PIL import Image
from utils import get_width_height, resize_image
from security_utils import check_password
import random
import string

import gspread
import pytz
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from pytz import timezone

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
                page_title="Image Variation",
                page_icon="🚀",
                layout="wide",
                initial_sidebar_state="expanded"
                )


if check_password():
    # Display a greeting message to the user
    st.write(f'Hello, {name}!')
  
    st.image("photos/ImageVariation_Logo.png")
    st.write("""
    ### Instructions 🗈

    1. Click the "Browse files" button to upload an image from your devices.
    2. Select the size of image required & number of variations needed.
    3. Wait for the image to be processed and for variations of the image to be generated.
    4. Scroll down to view the variations of the uploaded image.
    """)
    st.info(""" NOTE: You can download image by\
    right clicking on the image and select save image as option""")

    # Create the form
    with st.form(key="image_form"):

        # File uploader that accepts only PNG and JPG images
        uploaded_file = st.file_uploader(label="**Upload an image**", type=["png", "jpg"])

        # Select box to select the size of the images
        size = st.selectbox(label="**Select the size of the images**", options=["256x256", "512x512", "1024x1024"])

        # Number input to specify the number of images to be generated
        num_images = st.selectbox("**Enter the number of images to be generate**", (1,2,3,4))

        # Submit button
        submit_button = st.form_submit_button(label="**Generate Images**")

    # Handle form submission
    if submit_button:
        # TODO: Add code to generate images using the specified prompt, size, and number of images
        if uploaded_file is not None:

            image = Image.open(uploaded_file)

            st.image(uploaded_file, caption='Uploaded image', use_column_width=True)

            width, height = get_width_height(size)
            image = resize_image(image,width,height)
            response = openai.Image.create_variation(
                    image = image,
                    n = num_images,
                    size=size,
                )
            
            # Check if the number of images returned is less than num_images
            if len(response['data']) < num_images:
                st.error(f'Error: Only {len(response["data"])} images were generated')
            else:
                # Store the generated images in session state
                st.session_state.generated_images = []
                for idx in range(num_images):
                    image_url = response['data'][idx]['url']

                        # Generate a random combination of letters and numbers
                    def generate_random_string(length):
                        letters_and_digits = string.ascii_letters + string.digits
                        return ''.join(random.choice(letters_and_digits) for i in 
                        range(length))

                    # Generate a random combination of letters and numbers
                    random_string = generate_random_string(6)

                    # Create a caption that includes the random string
                    caption = f'ImageVar_{random_string}'

                    # Append a tuple containing the image URL and caption to the generated_images list
                    st.session_state.generated_images.append((image_url, caption))
                    
                    # Display the image with its caption
                    st.image(image_url, caption=caption, use_column_width=True)

        # Initialize the session state with a default value for the "username" key
        if "username" not in st.session_state:
            st.session_state["username"] = "Invoke People"

        # Use credentials to create a client to interact with the Google Drive API
        scope = ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive']
        
        # Load your TOML data from the st.secrets dictionary
        toml_data = st.secrets["service_account"]

        # Create credentials from the TOML data
        creds = ServiceAccountCredentials.from_json_keyfile_dict(toml_data, scope)

        # Authorize the activity
        activity = gspread.authorize(creds)

        # Find a workbook by name and open the first sheet
        sheet = activity.open("user-activity-ideaspark").get_worksheet(1)

        # Create a timezone object for the Kuala Lumpur time zone
        kl_timezone = pytz.timezone('Asia/Kuala_Lumpur')
        
        # Get the current date and time in the Kuala Lumpur time zone
        date_time = datetime.now(kl_timezone).strftime('%Y-%m-%d %H:%M:%S')
        
        # Get the username from the session state
        name = st.session_state["username"]
        
        # Append the values to the sheet
        sheet.append_row([name, date_time, "Image Variation"])

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

    


    
