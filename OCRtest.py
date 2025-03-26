import pytesseract
import cv2
import requests
import re
import time
from PIL import ImageGrab
import numpy as np
import fade  # To handle the color fading

# Replace this with your actual webhook URL
webhook_url = 'https://your.webhook/random_caracters.xyz'

# List of French curse words (you can extend this list)
curse_words = ['merde', 'putain', 'con', 'salaud', 'saloperie', 'bordel', 'enculé', 'crève', 'dégueulasse']

# Create the regex pattern to match curse words with potential letter variations (including accented letters)
def create_regex(curse_words):
    regex_parts = []
    for word in curse_words:
        # Add variations with accented characters
        word_variations = re.sub(r'[a-z]', lambda x: f'[{x.group(0)}aàáäâéèêëîïôöùûü]', word)
        regex_parts.append(word_variations)
    # Combine all variations and apply the global (?i) case-insensitivity flag
    return f"(?i)({'|'.join(regex_parts)})"

regex_pattern = create_regex(curse_words)

def capture_screenshot():
    screenshot = ImageGrab.grab()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    return screenshot

def extract_text_from_image(image):
    return pytesseract.image_to_string(image)

def regex_for_curse_words(text, regex_pattern):
    matches = re.findall(regex_pattern, text)  # Find all matches for curse words
    if matches:
        return matches  # Return the matched curse words
    return []

def send_to_discord(extracted_text, curse_word=None, notify=False):
    # If curse word detected, set the embed color to red, else blue
    embed_color = 16711680 if notify else 3447003  # Red for curse word, Blue for regular
    title = "CURSE WORD" if notify else "📝 Extracted Text"
    description = f"**CURSE WORD HAS BEEN FOUND**\nDetected word: **{curse_word}**" if notify else f"**Extracted Text:**\n```{extracted_text}```"

    data = {
        "content": "@everyone" if notify else "",
        "embeds": [
            {
                "title": title,
                "description": description,
                "color": embed_color  # Red for curse word detection
            }
        ]
    }
    response = requests.post(webhook_url, json=data)
    return response

# Menu display with fade effect
def display_menu():
    menu_text = """
▄▄▌ ▐ ▄▌ ▄ .▄ ▄▄▄· ▄▄▄▄▄.▄▄ ·  ▄▄▄·  ▄▄▄· ▄▄▄·    ·▄▄▄▪  ▄▄▌  ▄▄▄▄▄▄▄▄ .▄▄▄  
██· █▌▐███▪▐█▐█ ▀█ •██  ▐█ ▀. ▐█ ▀█ ▐█ ▄█▐█ ▄█    ▐▄▄·██ ██•  •██  ▀▄.▀·▀▄ █·
██▪▐█▐▐▌██▀▐█▄█▀▀█  ▐█.▪▄▀▀▀█▄▄█▀▀█  ██▀· ██▀·    ██▪ ▐█·██▪   ▐█.▪▐▀▀▪▄▐▀▀▄ 
▐█▌██▐█▌██▌▐▀▐█ ▪▐▌ ▐█▌·▐█▄▪▐█▐█ ▪▐▌▐█▪·•▐█▪·•    ██▌.▐█▌▐█▌▐▌ ▐█▌·▐█▄▄▌▐█•█▌
 ▀▀▀▀ ▀▪▀▀▀ · ▀  ▀  ▀▀▀  ▀▀▀▀  ▀  ▀ .▀   .▀       ▀▀▀ ▀▀▀.▀▀▀  ▀▀▀  ▀▀▀ .▀  ▀
"""
    # Use fade to color the ASCII art and menu options
    print(fade.purpleblue(menu_text))  # Apply purple-blue fade effect to ASCII and menu
    print(fade.purpleblue("1. Enable Curse Word Notifications"))
    print(fade.purpleblue("2. Disable Curse Word Notifications"))
    print(fade.purpleblue("3. Start the Filter"))
    print(fade.purpleblue("4. Exit"))

def adjust_notifications():
    notification_enabled = False  # Variable to track whether notifications are enabled or not

    while True:
        display_menu()  # Display menu
        choice = input(fade.purpleblue("Choose an option (1-4): "))
        
        if choice == '1':
            notification_enabled = True
            print(fade.purpleblue("Notifications Enabled!"))
            break
        elif choice == '2':
            notification_enabled = False
            print(fade.purpleblue("Notifications Disabled!"))
            break
        elif choice == '3':
            print(fade.purpleblue("Starting the filter..."))
            break
        elif choice == '4':
            print(fade.purpleblue("Exiting..."))
            exit()
        else:
            print(fade.purpleblue("Invalid option, please try again."))
    
    return notification_enabled

# Main loop for OCR and monitoring
def main_loop():
    notification_enabled = adjust_notifications()  # Ask the user whether to enable notifications
    if notification_enabled:
        print(fade.purpleblue("Filter is now active!"))
    else:
        print(fade.purpleblue("Filter is not active."))
        
    while True:
        start_time = time.time()  # Track time for 20 ms interval
        screenshot = capture_screenshot()  # Capture the screenshot
        extracted_text = extract_text_from_image(screenshot)  # Perform OCR on the screenshot
        print(f"Extracted Text: {extracted_text}")  # Display extracted text for debugging

        # Check for curse words and get exact matches
        matched_curse_words = regex_for_curse_words(extracted_text, regex_pattern)
        if matched_curse_words:
            for word in matched_curse_words:
                if notification_enabled:
                    send_to_discord(extracted_text, curse_word=word, notify=True)  # Send @everyone notification with detected word
        else:
            send_to_discord(extracted_text, notify=False)  # Send normal extracted text without @everyone

        elapsed_time = time.time() - start_time
        sleep_time = max(0, 0.02 - elapsed_time)  # Sleep for 20 ms, adjusting for the processing time
        time.sleep(sleep_time)  # Wait for the next 20 ms interval

# Start the main loop
main_loop()
