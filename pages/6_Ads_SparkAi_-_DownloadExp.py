import streamlit as st
import openai
from security_utils import check_password
import time
import os
import requests
from PIL import Image
import base64
from io import BytesIO

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
    st.title('IdeaSpark🚀 - Download Expxx')
    st.write(f"""🛍️ Product/Service replaced with 📝 Visual Headline.
             Using the existing info from decoris.""" )
    st.info(f"""
    Ads Generation using 6 inputs:\n
    📝 Visual Headline\n
    💼 Business Industry *\n
    🎯 Marketing Objective\n
    📣 Facebook Ad Objective\n
    📢 Call to Action Headline\n
    📱 Platform\n
    Note: inputs with (*) are in Client Profile - decoris
    """)
    st.write(f"""📰 decoris - Content Section""" )
    st.image("photos\decoris_content_section.png")
    st.write(f"""🧑‍💼 decoris - Client Profile""" )
    st.image("photos\decoris_client_profile.png")
    st.write(f"""VISUAL HEADLINE EXAMPLE""" )
    st.write(f""" 
    "No more hairy armpit
    Thor X Laser Hair Removal 
    RM38
    Quick | Effective | Long-lasting" 
     """ )
  

    with st.form(key="ads_form"):
        # Text input for the product/service
        visual_headline = st.text_input(label="Visual Headline")

        # Text input for the business industry
        business_industry = st.text_input(label="Business Industry")

        # Select box for the marketing objective
        marketing_objective = st.selectbox(
            label="Marketing Objective",
            options=["Awareness", "Consideration", "Conversion"]
        )

            # Select box for the Facebook ad objective
        fb_ad_objective = st.selectbox(
            label="Facebook Ad Objective",
            options=[
                "Brand Awareness", "Reach", "Traffic", "Engagement", "App Installs",
                "Video Views", "Lead Generation", "Messages", "Conversion",
                "Catalog Sales", "Store Traffic", "Page Likes", "Event Responses",
                "Local Awareness"
            ]
        )

        # Text input for the call to action headline
        cta_headline = st.text_input(label="Call to Action Headline")

        # Checkbox for the platform
        platform = st.multiselect(
            label="Platform",
            options=["Facebook", "Instagram", "Google", "Youtube", "Linkedin"]
        )

        # Submit button
        submit_button = st.form_submit_button(label="Do the magic!")

    # Handle form submission
    if submit_button:
        # Generate the text output
        output = f"Generate a {', '.join(platform)} ads with the below details:\n\n"
        output += f"1) Visual Headline: {visual_headline}\n"
        output += f"2) Business Industry: {business_industry}\n"
        output += f"3) Marketing Objective: {marketing_objective}\n"
        output += f"4) Facebook Ad Objective: {fb_ad_objective}\n"
        output += f"5) Call to Action Headline: {cta_headline}\n"

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
            response_format="b64_json"
        )

        
        for idx in range(4):
            # Decode the Base64 encoded JSON to obtain the original image data
            image_data = base64.b64decode(response['data'][idx]['b64_json'])

            # Create a PIL Image object from the image data
            image = Image.open(BytesIO(image_data))

            # Display the image in Streamlit
            st.image(image, caption=f'Generated image: {idx+1}', 
                     use_column_width=True)

            #st.image(image_data, caption=f'Generated image: {idx+1}', use_column_width=True)

            """
            # Decode the Base64 encoded JSON to obtain the original image data
            image_data = base64.b64decode(response['data'][idx]['b64_json'])

            # Create a PIL Image object from the image data
            image = Image.open(BytesIO(image_data))

            # Save the image as a PNG file
            image.save(f'image_{idx+1}.png')

            # Add a download button to download the image
            st.download_button(
                label=f'Download image {idx+1}',
                data=image_data,
                file_name=f'image_{idx+1}.png',
                mime='image/png'
            )
            """
