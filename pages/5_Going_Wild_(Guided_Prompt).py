import streamlit as st
import openai
from security_utils import check_password
from googletrans import Translator
import random
import string
import time

from gdrive_module import save_images_to_google_drive
from gdrive_module import record_user_activity_going_wild

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

# configure the default settings of the page.
st.set_page_config(
                page_title="Going Wild",
                page_icon="🚀",
                layout="wide",
                initial_sidebar_state="expanded"
                )


 # Define the options for each emotion type
emotions = {
    "Positive mood, low energy": ["light", "peaceful", "calm", "serene", "soothing", "relaxed", "placid", "comforting", "cosy", "tranquil", "quiet", "pastel", "delicate", "graceful", "subtle", "balmy", "mild", "ethereal", "elegant", "tender", "soft", "light"],
    "Positive mood, high energy": ["bright", "vibrant", "dynamic", "spirited", "vivid", "lively", "energetic", "colorful","joyful","romantic","expressive","bright","rich","kaleidoscopic","psychedelic","saturated","ecstatic","brash","exciting","passionate","hot"],
    "Negative mood, low energy": ["muted","bleak","funereal","somber","melancholic","mournful","gloomy","dismal","sad","pale","washed-out","desaturated","grey","subdued","dull","dreary","depressing","weary","tired"],
    "Negative mood, high energy": ["dark","ominous","threatening","haunting","forbidding","gloomy","stormy","doom","apocalyptic","sinister","shadowy","ghostly","unnerving","harrowing","dreadful","frightful","shocking" ,"terror" ,"hideous" ,"ghastly"]
}

if check_password():
    st.image("photos/GoingWild_Logo.png")

    # Create the form
    with st.form(key="creative_form"):

        st.write("**Your Prompt**")
        # Note for the user
        st.write("💡 You may use either English or Malay language")

        # Input prompt
        prompt_input = st.text_input("Enter a subject or element:")

        st.write("**Emotion**")

        # Create a multiselect widget for each emotion type
        selected_options = {}
        for emotion_type, emotion_options in emotions.items():
            selected_options[emotion_type] = st.multiselect(f"Choose options for {emotion_type}:", emotion_options)

        st.write("**Looks/Vibe**")
        
        # Single selection for looks
        looks = ["None", "Vaporwave", "Post-apocalyptic", "memphis", "Gothic, fantasy:", "dieselpunk", "steampunk", "Cybernetic, sci-fi", "Cyberpunk"]
        selected_look = st.selectbox("Select look:", looks)

        st.write("**Photography**")

        # Single selection for camera angle proximity
        proximities = ["None", "extreme close-up", "close-up", "medium shot", "long shot", "wide shot", "full shot", "extreme long shoot", "extreme wide shot"]
        selected_proximity = st.selectbox("Select camera angle proximity:", proximities)

        # Single selection for camera angle position
        positions = ["None","crane shot","Overhead view", "low angle","worms-eye-view", "aerial view","drone photography" "dutch angle", "over-the-shoulder shot"]
        selected_position = st.selectbox("Select camera angle position:", positions)

        # Single selection for camera settings
        camera_settings = ["None","Fast shutter speed,","Slow shutter speed", "Bokeh","Tilt shift photography", "Motion blur","Telephoto lens," "Wide angle lens, 15mm", "Deep depth of field,"]
        selected_camera_settings = st.selectbox("Select camera settings/lenses:", camera_settings)

        st.write("**Illustration**")

        # Single selection for illustration style
        illustration_styles = ["None","Stencil, street art, Banksy,","Ballpoint pen art", 
                               "Pencil sketch","Pencil drawing","Woodcut","Field journal line art" , 
                               "Colouring-in sheet", "Crayon", "Child's drawing / children' drawing", "Acrylic on canvas",
                               "Watercolor", "Coloured pencil, detailed", "Oil painting", "Ukiyo-e", "Chinese watercolor",
                                "Pastels", "Airbrush", "Alegria, 'corporate memphis'", "Collage, photocollage,magazine collage",
                                "Vector art","Watercolor & pen", "Screen printing" , "Low poly", "Layered paper", "Sticker illustration"
                                "Storybook" , "Digital painting"]
        selected_illustration_styles = st.selectbox("Select illustration styles:", illustration_styles)

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
                prompt_input = f"{prompt} "

            # Generate final prompt
            final_prompt = f"{prompt_input}"
            if selected_options != "None":
                final_prompt += f",{', '.join([', '.join(emotion_options) for emotion_options in selected_options.values() if emotion_options])}"
            if selected_look != "None":
                final_prompt += f", {selected_look}"
            if selected_proximity != "None":
                final_prompt += f", {selected_proximity}"
            if selected_position != "None":
                final_prompt += f", {selected_position}"
            if selected_camera_settings != "None":
                final_prompt += f", {selected_camera_settings}"
            if selected_illustration_styles != "None":
                final_prompt += f", {selected_illustration_styles}"



            # Display the text output
            st.write(final_prompt)

            if final_prompt:
                # Add a progress bar
                progress_bar = st.progress(0)
                for i in range(100):
                    # Update progress bar
                    progress_bar.progress(i + 1)
                    time.sleep(0.1)
                st.write("Making some tricks....")

            response = openai.Image.create(
                model="dall-e-3",
                prompt=final_prompt,
                size="1024x1024",
                response_format="url",
                api_key=openai.api_key
            )

            num_images = len(response['data'])


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
                    caption = f'GWild_{random_string}'

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
                record_user_activity_going_wild(st.session_state["username"], st.secrets)
                
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