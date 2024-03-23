import gdown
import requests
from bs4 import BeautifulSoup
import base64
import re


# Dictionary to store episode URLs
episodes_url = {


        }

def get_episodes_url(url):
    """
    Retrieves all episode URLs from the provided webpage.

    Args:
        url (str): URL of the webpage containing episode links.
    """
    
    response = requests.get(url)
    if response.status_code == 200:
        # the episode links are in this format:
        # <a href="javascript:void(0);" onclick="openEpisode('base64_encoded_url')">الحلقة 104</a>
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # find all <a> tags
        links = soup.find_all('a')
        counter = 1
        for link in links:    
            # get the onclick value if the tag has one
            onclick = link.get('onclick')
            if onclick:
                # get the value inside openEpisode('')
                result = re.search(r"\('([^']+)'\)", onclick)
                if result:
                    extracted_value = result.group(1)
                    episodes_url[counter] = base64.b64decode(extracted_value)
                    counter += 1
    else:
        print("Error: Failed to retrieve the webpage.")





def find_google_drive_link(url):
    
    """
    Finds the Google Drive link in the webpage HTML.

    Args:
        url (str): URL of the webpage to search for the link.

    Returns:
        str: Google Drive URL if found, None otherwise.
    """
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # store every <a> tag
        download_links = soup.find_all('a', class_='btn btn-default download-link')
        for link in download_links:
            # the google drive links are in this formats:
            # <a class="btn btn-default download-link" data-url="base64_encoded_url" target="_blank"><span class="notice">google drive</span>
            data_url = link.get('data-url')
            # decode the url from base64
            decoded_url = base64.b64decode(data_url).decode('utf-8')
            # return the url if it was a google drive url
            if "drive.google.com" in decoded_url:
                print("Google Drive URL:", decoded_url)
                return decoded_url
    else:
        print("Failed to retrieve the webpage. Status code:", response.status_code)



def extract_google_drive_id(url):
    """
    Extracts Google Drive file ID from the URL.

    Args:
        url (str): Google Drive URL.

    Returns:
        str: Google Drive file ID.
    """
    pattern = r'(?:id=|/d/)([a-zA-Z0-9-_]+)'
    match = re.search(pattern, url)
    if match:
        return f"https://drive.google.com/uc?id={match.group(1)}"
    else:
        return None




def download_from_google_drive(url, output_file):
    """
    Downloads file from Google Drive using gdown library.
    
    Args:
        url (str): URL of the file to be downloaded.
        output_file (str): Path where the downloaded file will be saved.
    """
    gdown.download(url, output_file, quiet=False)



# any episode url for the anime
anime_url = input("Enter the anime url:")

# get all episodes urls
get_episodes_url(anime_url)

# download episodes from "from_episode" to "to_episode"
from_episode = int(input("Enter the start episode: "))
to_episode = int(input("Enter the end episode: "))

# for every episode I need to download
for x in range(from_episode, to_episode+1):
    episode_url = episodes_url[x]                                       # get the episode url
    episode_google_drive_link = find_google_drive_link(episode_url)     # get the episode google drive url
    episode_id = extract_google_drive_id(episode_google_drive_link)     # extract the google drive link id

    download_from_google_drive(episode_id,f"{x}.mp4")                   # download the episode

