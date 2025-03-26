# OCR Curse Word Filter with Discord Notifications

This project uses Optical Character Recognition (OCR) to detect curse words in screenshots. When a curse word is detected, it sends a notification to a Discord channel through a webhook, highlighting the detected word. The script can be customized with a menu interface to enable/disable notifications and start the filter.

## Features
- Captures screenshots periodically and processes the image with OCR.
- Detects curse words from a list and highlights them.
- Sends Discord notifications when curse words are detected.
- Menu system to enable/disable notifications and start/stop the filter.

## Setup

### Prerequisites

To run this project, you'll need to have Python 3.x installed along with the following libraries:

1. **pytesseract** for OCR.
2. **opencv-python** for image processing.
3. **requests** to interact with the Discord webhook API.
4. **fade** for text color fading in the terminal.

### Installation

1. Clone or download the repository.
2. Navigate to the project folder in your terminal/command prompt.
3. Install the required libraries by running:

```bash
pip install -r requirements.txt
