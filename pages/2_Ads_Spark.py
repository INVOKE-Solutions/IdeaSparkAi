import streamlit as st
import openai
from security_utils import check_password
import time
import random
import string


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
    📢 Call to Action Headline\n
    Note: inputs with (*) are in Client Profile - decoris
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
                "Video Views", "Lead Generation", "Messages", "Conversion",
                "Catalog Sales", "Store Traffic", "Page Likes", "Event Responses",
                "Local Awareness"
            ]
        )

        # Text input for the call to action headline
        cta_headline = st.text_input(label="**Call to Action Headline**")

        # Submit button
        submit_button = st.form_submit_button(label="**Do the magic!✨**")

    # Handle form submission
    if submit_button:
        # Generate the text output
        output = f"Generate an ads with the below details:\n\n"
        output += f"1) Visual Headline: {visual_headline}\n"
        output += f"2) Business Industry: {business_industry}\n"
        output += f"3) Marketing Objective: {marketing_objective}\n"
        output += f"4) Ad Objective: {fb_ad_objective}\n"
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
            sheet.append_row([name, date_time, "Ads Spark"])

    
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
