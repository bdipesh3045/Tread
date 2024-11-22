from instapaper import instapaper as insta

# import os
import time
import requests

# import subprocess


def filter_link(links):
    # Define browser headers to mimic a real browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Connection": "keep-alive",
    }

    filtered = []
    for link in links:
        # Construct the URL using the link
        data = f"https://freedium.cfd/{link}"
        print("................")

        try:
            # Make a GET request with headers
            response = requests.get(data, headers=headers)

            # Check if the response status code is 200 (OK)
            if response.status_code == 200:
                filtered.append(data)
                print("Premium article unlocked")
                print(response.status_code)
            else:
                filtered.append(link)
                print("Usual article")

        except requests.exceptions.RequestException as e:
            # Handle exceptions (e.g., network issues, invalid URLs)
            print(f"An error occurred: {e}")
            filtered.append(link)

    return filtered


# def download(BOOK_ID):
#     if not all([CONSUMER_KEY, CONSUMER_SECRET, USERNAME, PASSWORD, BOOK_ID]):
#         print("Error: Missing required environment variables.")
#         exit(1)

#     command = [
#         "portable-wisdom",
#         "--instapaper-api-key",
#         CONSUMER_KEY,
#         "--instapaper-api-secret",
#         CONSUMER_SECRET,
#         "--instapaper-login",
#         USERNAME,
#         "--instapaper-password",
#         PASSWORD,
#         "--limit",
#         "1",
#     ]

#     # Run the command and capture the output
#     try:
#         subprocess.run(command, check=True)
#         print("EPUB download initiated successfully.")
#     except subprocess.CalledProcessError as e:
#         print(f"Error running portable-wisdom: {e}")


# Trying to add a single book
def get_folder(insta, folder_name, count):
    if count == 0:
        NEW_FOLDER_NAME = folder_name
    else:
        NEW_FOLDER_NAME = f"{folder_name}{count}"
    # Created a folder for the name
    try:
        insta.create_folder(NEW_FOLDER_NAME)
    except Exception as e:
        print("Failed to create the folder:", e)
    # Now trying to find the location of the folder

    folders = insta.folders()
    target_folder_id = None  # Initialize target_folder_id

    for folder in folders:
        if folder["title"] == folder_name:
            target_folder_id = folder["folder_id"]
            break

    if target_folder_id is None:
        print("Failed to find the target folder")
        return None
    return (target_folder_id, NEW_FOLDER_NAME)


def add_book(secrets, filename, title, links):
    links = filter_link(links)
    will_select = False
    book_count = 0
    if len(title) == len(links):
        will_select = True
    print(will_select)

    i = 0

    CONSUMER_KEY = secrets[0]
    CONSUMER_SECRET = secrets[1]
    USERNAME = secrets[2]
    PASSWORD = secrets[3]
    instapaper = insta.Instapaper(CONSUMER_KEY, CONSUMER_SECRET)

    # Authenticate with Instapaper
    instapaper.login(USERNAME, PASSWORD)
    print("Login successful")

    def new_file(no):
        # Define the name of the new folder
        if no == 0:
            NEW_FOLDER_NAME = filename
        else:
            NEW_FOLDER_NAME = f"{filename}{no}"

        # Create a new folder
        try:
            instapaper.create_folder(NEW_FOLDER_NAME)
        except Exception as e:
            print("Failed to create the folder:", e)

        folders = instapaper.folders()
        target_folder_id = None  # Initialize target_folder_id

        for folder in folders:
            if folder["title"] == NEW_FOLDER_NAME:
                target_folder_id = folder["folder_id"]
                break

        if target_folder_id is None:
            print("Failed to find the target folder")
            return False
        return (target_folder_id, NEW_FOLDER_NAME)

    for data in links:
        if i == 0 or i % 20 == 0:
            target_folder_id, NEW_FOLDER_NAME = new_file(i // 20)
            print(f"Folder created: {NEW_FOLDER_NAME}")
        if will_select:
            bookmark_params = {
                "title": f"Chapter: {i+1} {title[i]}",
                "url": data,
            }

        else:
            bookmark_params = {
                "title": f"Chapter {i+1}",
                "url": data,
            }

        time.sleep(1)
        new_bookmark = insta.Bookmark(instapaper, bookmark_params)
        i += 1

        new_bookmark.save(target_folder_id)
        print(target_folder_id)
        print(f"Book count: {i}")
    # download(target_folder_id)


# for getting medium and towards data science article for free we use


# Just a login system for the app
def main_login(CONSUMER_KEY, CONSUMER_SECRET, USERNAME, PASSWORD):
    instapaper = insta.Instapaper(CONSUMER_KEY, CONSUMER_SECRET)

    try:
        instapaper.login(USERNAME, PASSWORD)

        print("Login successful")

    except Exception as e:
        print("Failed to login:", e)
        return False
    return True
    # raise Exception("Failed to login")
    return instapaper
