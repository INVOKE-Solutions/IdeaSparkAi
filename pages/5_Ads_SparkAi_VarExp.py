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
    st.title('IdeaSpark🚀 - Case 1')
    st.write(f"""Same as in the proposal.""" )
    st.info(f"""
    Ads Generation using 6 inputs:\n
    🛍️ Product/Service *\n
    💼 Business Industry *\n
    🎯 Marketing Objective\n
    📢 Call to Action Headline\n
    📱  Platform\n
    📣 Facebook Ad Objective\n
    Note:\n
    📌 Inputs with (*) are in Client Profile - decoris\n
    """)
    st.write(f"""📰 decoris - Content Section""" )
    st.image("photos\decoris_content_section.png")
    st.write(f"""🧑‍💼 decoris - Client Profile""" )
    st.image("photos\decoris_client_profile.png")
  

    with st.form(key="ads_form"):
        # Text input for the product/service
        product_service = st.text_input(label="Product/Service")

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
            output += f"1) Product/Service: {product_service }\n"
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
            )

            for idx in range(4):
                image_url = response['data'][idx]['url']

                st.image(image_url, caption=f'Generated image: {idx+1}', use_column_width=True)

                # Add download button
                if st.button(f'Download Image {idx+1}'):
                    r = requests.get(image_url)
                    with open(f'image_{idx+1}.jpg', 'wb') as f:
                        f.write(r.content)

                # Add variation button
                if st.button(f'Create Variation for Image {idx+1}'):
                    variation_response = openai.Image.create_variation(
                        image_id=response['data'][idx]['id']
                    )
                    variation_url = variation_response['data'][0]['url']
                    st.image(variation_url, caption=f'Variation for Image {idx+1}', use_column_width=True)
                            



