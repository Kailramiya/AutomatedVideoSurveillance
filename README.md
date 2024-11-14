# Automated Video Surveillance System using Telegram Bot and OpenCV

This project implements an **Automated Video Surveillance System** that uses real-time face recognition to identify visitors and family members. The system captures video using OpenCV, processes each frame to detect faces, and then sends alerts via a **Telegram bot** if an unknown visitor is detected.

## Features:
- Real-time face detection using a webcam.
- Recognizes family members and identifies new visitors.
- Sends Telegram alerts with a photo of unknown visitors.
- Tracks visitors by categorizing them into folders (e.g., "milkman", "delivery").
- Allows family member recognition for allowing access.
- Saves and retrieves visitor images for future reference.

## Requirements:
Before running the script, make sure you have the following installed:
- Python 3.x
- OpenCV (`opencv-python`)
- `face_recognition`
- `python-telegram-bot` library
- `asyncio` and `threading` for managing multiple tasks
- A connected webcam

To install the required Python libraries, you can run:

```bash
pip install opencv-python face_recognition python-telegram-bot
```
Setup Instructions:
Telegram Bot Setup:

Create a Telegram bot using BotFather on Telegram.
Replace the TELEGRAM_BOT_TOKEN in the script with your bot's token.
Family Member Images:

Store images of family members in a folder. These images will be used to recognize family members.
Modify the path to the family member images in the code.
Visitor Images:

The system stores images of visitors in specific folders. Each folder corresponds to a visitor's name (e.g., "milkman", "delivery").
The script will check for unknown faces in these folders and send alerts via Telegram.
How It Works:
The system continuously captures video frames from your webcam.
The faces in the frames are recognized using the face_recognition library.
If a face is recognized as a family member, the program proceeds without any alerts.
If the face is unknown, an alert with the visitor's photo is sent to your Telegram bot.
If the visitor's folder exists, the bot sends a message saying, "Milkman has arrived" (example).
Usage:
Run the script by executing:
bash
Copy code
python main.py
The bot will start monitoring for visitors and send alerts when unknown people arrive.
License:
This project is licensed under the MIT License - see the LICENSE file for details.

Author- Aman Kumar

Email- amankundu369@gmail.com
