import streamlit as st
import openai
from security_utils import check_password
import time
from googletrans import Translator
import random
import string

from gdrive_module import save_images_to_google_drive
from gdrive_module import record_user_activity_open_ended

# Create a Translator object
translator = Translator()

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
                page_title="IdeaSpark",
                page_icon="🚀",
                layout="wide",
                initial_sidebar_state="expanded"
                )

if check_password():
    # Display a greeting message to the user
    st.write(f'Hello, {name}!')
  
    st.image("photos/OpenEnded_Logo.png")
    st.info(""" NOTE: You can download image by\
                    right clicking on the image and select save image as option""")  

    # Create the form
    with st.form(key="image_form"):
                
                # Note for the user
                st.write("💡 **You can use either English or Malay language**")

                # Text input for the image prompt
                prompt_input = st.text_input(label="**Enter the ads prompt**")

                # Select box to select the size of the images
                size = st.selectbox(label="**Select the size of the images**", options=["256x256", "512x512", "1024x1024"])

                # Submit button
                submit_button = st.form_submit_button(label="**Generate Images**")

    # Handle form submission
    if submit_button:
                # Check if the prompt_input is blank
                if not prompt_input:
                    st.error('Error: Please enter an image prompt') 
                else:
                    # Detect the language of the image prompt
                    lang = translator.detect(prompt_input).lang

                    # If the language is Malay, translate the text
                    if lang == 'ms':
                        prompt = translator.translate(prompt_input, src='ms', dest='en').text

                        # Generate the text output
                        stock_prompt = f"{prompt} "
                    else:
                        # Define the prompt variable for other languages
                        prompt = prompt_input
                        stock_prompt = prompt_input

                    if prompt:
                        # Add a progress bar
                        progress_bar = st.progress(0)
                        for i in range(100):
                            # Update progress bar
                            progress_bar.progress(i + 1)
                            time.sleep(0.1)
                        st.write("Making some tricks....")

                        num_images=4

                        response = openai.Image.create(
                            prompt=stock_prompt,
                            n=num_images,
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
                                caption = f'StockImage_{random_string}'

                                # Append a tuple containing the image URL and caption to the generated_images list
                                st.session_state.generated_images.append((image_url, caption))
                                
                                # Display the image with its caption
                                st.image(image_url, caption=caption, use_column_width=True)


                    # Clear the progress bar
                    progress_bar.empty()  
                    
                # Initialize the session state with a default value for the "username" key
                if "username" not in st.session_state:
                    st.session_state["username"] = "Invoke People"
                
                # Record user activity to Google Sheet
                record_user_activity_open_ended(st.session_state["username"], st.secrets)
                
                # Check if the attribute generated_images exists in the st.session_state object
                if "generated_images" not in st.session_state:
                    # Initialize the attribute to an empty list if it does not exist
                    st.session_state.generated_images = []
        
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

