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
