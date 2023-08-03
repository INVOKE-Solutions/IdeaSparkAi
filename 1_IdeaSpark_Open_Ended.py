import streamlit as st
import openai
from security_utils import check_password
import time
import requests


# Access the OpenAI API key
openai.api_key = st.secrets["api_key"]

# configure the default settings of the page.
st.set_page_config(
                page_title="IdeaSpark",
                page_icon="🚀",
                layout="wide",
                initial_sidebar_state="expanded"
                )

if check_password():
    st.image("photos\IdeaSpark_Logo.png")
    st.title('IdeaSpark🚀 - Open Ended')
    st.write(f"""Surprisingly the ads visuals managed to generate ONLY with 📝***Visual Headline***""" )
    st.write(f"""Example:""")
    st.write(f"""Get ready for a mouth-watering experience with our delicious, freshly-made pizzas! 
             Made with the finest ingredients and baked to perfection, our pizzas are sure to satisfy 
             your cravings. Take advantage of our special promotion and enjoy a piping hot pizza at an unbeatable price. Order now and taste the difference!"""
             )

    st.info(""" NOTE: You can download image by\
                    right clicking on the image and select save image as option""")  

    # Create the form
    with st.form(key="image_form"):
                # Text input for the image prompt
                prompt = st.text_input(label="Enter the ads prompt")

                # Select box to select the size of the images
                size = st.selectbox(label="Select the size of the images", options=["256x256", "512x512", "1024x1024", "1080x1080"])

                # Number input to specify the number of images to be generated
                num_images = st.selectbox("Enter the number of images to be generated", (1,2,3,4))

                # Submit button
                submit_button = st.form_submit_button(label="Generate Images")

    # Handle form submission
    if submit_button:
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
                        n=num_images,
                        size=size,
                    )

                    for idx in range(num_images):
                        image_url = response['data'][idx]['url']

                        st.image(image_url, caption=f'Generated image: {idx+1}',
                                use_column_width=True)
                        
                    # Add a download button for the image
                    st.download_button(
                        label="Download Image",
                        data=requests.get(image_url).content,
                        file_name=f"generated_image_{idx+1}.jpg",
                        mime="image/jpeg"
                    )


                    # Clear the progress bar
                    progress_bar.empty()                 



