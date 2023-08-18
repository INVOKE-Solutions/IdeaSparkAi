import streamlit as st
import openai
from PIL import Image
from utils import get_width_height, resize_image
from security_utils import check_password
import random
import string

# Access the OpenAI API key
openai.api_key = st.secrets["api_key"]

# configure the default settings of the page.
st.set_page_config(
                page_title="Image Variation",
                page_icon="🚀",
                layout="wide",
                initial_sidebar_state="expanded"
                )


if check_password():
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

    


    
