# googlecloud.py

#REQUIRED FOR GOOGLEDRIVE GENERATED STORAGE
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from PIL import Image
import requests
from io import BytesIO

#SAVE GENERATED IMAGE TO GOOGLE DRIVE -----------------
def save_images_to_google_drive(generated_images, folder_name, secrets):
    # Use credentials to create a client to interact with the Google Drive API
    scope = ['https://www.googleapis.com/auth/drive']
    toml_data = secrets["service_account"]
    creds = Credentials.from_service_account_info(info=toml_data, scopes=scope)
    service = build('drive', 'v3', credentials=creds)

    # Search for the folder with the specified name
    query = f"mimeType='application/vnd.google-apps.folder' and trashed = false and name='{folder_name}'"
    folders = service.files().list(q=query, fields="nextPageToken, files(id, name)").execute().get("files", [])

    # If the folder does not exist, create it
    if not folders:
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = service.files().create(body=file_metadata, fields='id').execute()
        folder_id = folder.get('id')
    else:
        folder_id = folders[0].get('id')

    # Iterate over the list of generated images
    for image_url, caption in generated_images:
        # Get the image data from the URL
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
        
        # Convert the image to JPEG format
        img = img.convert('RGB')
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)

        # Create a file in Google Drive and upload the image data
        file_metadata = {
            'name': f'{caption}.jpg',
            'parents': [folder_id]
        }
        media = MediaIoBaseUpload(img_byte_arr, mimetype='image/jpeg')
        file_drive = service.files().create(body=file_metadata, media_body=media, fields='id').execute()




#REQUIRED FOR ACTIVITY RECORD FOR FEATURES USAGE
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from datetime import datetime
import pytz


#SAVE USER ACTIVITY RECORD FOR OPEN ENDED 
def record_user_activity_open_ended(username, secrets):

    '''
    Given username and secrets, return something

    Args:
        :param username:str --
        :param secrets:str ---

    Return:

    
    '''

    # Use credentials to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    toml_data = secrets["service_account"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(toml_data, scope)

    # Authorize the activity
    activity = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    sheet = activity.open("user-activity-ideaspark").get_worksheet(1)

    # Get the current date and time in UTC
    now_utc = datetime.now(pytz.utc)

    # Convert the date and time to the Kuala Lumpur timezone
    kl_tz = pytz.timezone('Asia/Kuala_Lumpur')
    now_kl = now_utc.astimezone(kl_tz)

    # Format the date and time as a string
    date_time_str = now_kl.strftime('%Y-%m-%d %H:%M:%S')

    # Append the values to the sheet
    sheet.append_row([username, date_time_str, "Open-Ended"])


#SAVE USER ACTIVITY RECORD FOR ADS SPARK 
def record_user_activity_ads_spark(username, secrets):

    '''
    Given username and secrets, return something

    Args:
        :param username:str --
        :param secrets:str ---

    Return:

    
    '''

    # Use credentials to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    toml_data = secrets["service_account"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(toml_data, scope)

    # Authorize the activity
    activity = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    sheet = activity.open("user-activity-ideaspark").get_worksheet(1)

    # Get the current date and time in UTC
    now_utc = datetime.now(pytz.utc)

    # Convert the date and time to the Kuala Lumpur timezone
    kl_tz = pytz.timezone('Asia/Kuala_Lumpur')
    now_kl = now_utc.astimezone(kl_tz)

    # Format the date and time as a string
    date_time_str = now_kl.strftime('%Y-%m-%d %H:%M:%S')

    # Append the values to the sheet
    sheet.append_row([username, date_time_str, "Ads Spark"])

#SAVE USER ACTIVITY RECORD FOR IMAGE VARIATION
def record_user_activity_image_variation(username, secrets):

    '''
    Given username and secrets, return something

    Args:
        :param username:str --
        :param secrets:str ---

    Return:

    
    '''

    # Use credentials to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    toml_data = secrets["service_account"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(toml_data, scope)

    # Authorize the activity
    activity = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    sheet = activity.open("user-activity-ideaspark").get_worksheet(1)

    # Get the current date and time in UTC
    now_utc = datetime.now(pytz.utc)

    # Convert the date and time to the Kuala Lumpur timezone
    kl_tz = pytz.timezone('Asia/Kuala_Lumpur')
    now_kl = now_utc.astimezone(kl_tz)

    # Format the date and time as a string
    date_time_str = now_kl.strftime('%Y-%m-%d %H:%M:%S')

    # Append the values to the sheet
    sheet.append_row([username, date_time_str, "Image Variation"])


#SAVE USER ACTIVITY RECORD FOR STOCK IMAGE 
def record_user_activity_stock_image(username, secrets):

    '''
    Given username and secrets, return something

    Args:
        :param username:str --
        :param secrets:str ---

    Return:

    
    '''

    # Use credentials to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    toml_data = secrets["service_account"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(toml_data, scope)

    # Authorize the activity
    activity = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    sheet = activity.open("user-activity-ideaspark").get_worksheet(1)

    # Get the current date and time in UTC
    now_utc = datetime.now(pytz.utc)

    # Convert the date and time to the Kuala Lumpur timezone
    kl_tz = pytz.timezone('Asia/Kuala_Lumpur')
    now_kl = now_utc.astimezone(kl_tz)

    # Format the date and time as a string
    date_time_str = now_kl.strftime('%Y-%m-%d %H:%M:%S')

    # Append the values to the sheet
    sheet.append_row([username, date_time_str, "Stock Image"])
    

#SAVE USER ACTIVITY RECORD FOR GOING WILD
def record_user_activity_going_wild(username, secrets):

    '''
    Given username and secrets, return something

    Args:
        :param username:str --
        :param secrets:str ---

    Return:

    
    '''

    # Use credentials to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    toml_data = secrets["service_account"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(toml_data, scope)

    # Authorize the activity
    activity = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    sheet = activity.open("user-activity-ideaspark").get_worksheet(1)

    # Get the current date and time in UTC
    now_utc = datetime.now(pytz.utc)

    # Convert the date and time to the Kuala Lumpur timezone
    kl_tz = pytz.timezone('Asia/Kuala_Lumpur')
    now_kl = now_utc.astimezone(kl_tz)

    # Format the date and time as a string
    date_time_str = now_kl.strftime('%Y-%m-%d %H:%M:%S')

    # Append the values to the sheet
    sheet.append_row([username, date_time_str, "Going Wild"])

