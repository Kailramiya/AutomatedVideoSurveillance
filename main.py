import os
import cv2
import time
import threading
import asyncio
import numpy as np
import face_recognition
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Replace with your actual token
TELEGRAM_BOT_TOKEN = 'YOUR_BOT_TOKEN_NUMBER'  # Update with your bot token
family_faces = {}
visitor_encodings = {}
visitors_folder = r"C:\Users\amank\OneDrive\Desktop\home security\visitor_images"

# Encode faces from a given folder path
def encode_faces_from_folder(folder_path):
    encoded_faces = {}
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith(".jpg") or filename.endswith(".png"):
                img_path = os.path.join(root, filename)
                image = face_recognition.load_image_file(img_path)
                encoding = face_recognition.face_encodings(image)
                if encoding:
                    folder_name = os.path.basename(root)  # Folder name as identifier
                    encoded_faces[folder_name] = encoding[0]
    return encoded_faces

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to the Visitor Recognition System!")
    print("Bot started.")

async def send_alert(app, chat_id, frame, visitor_name):
    visitor_image_path = 'visitor.jpg'
    cv2.imwrite(visitor_image_path, frame)

    async with app:
        await app.bot.send_photo(chat_id=chat_id, photo=open(visitor_image_path, 'rb'))
        await app.bot.send_message(chat_id=chat_id, text=f"{visitor_name} has arrived.")

def recognize_and_alert(family_faces, visitor_encodings, chat_id, app, loop):
    video_capture = cv2.VideoCapture(0)  # Use 0 for default camera
    last_alert_time = 0
    cooldown_period = 60  # Cooldown period in seconds

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to capture image from camera.")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            name = "Unknown"
            visitor_name = None

            # Check against family faces
            family_matches = face_recognition.compare_faces(list(family_faces.values()), face_encoding)
            if True in family_matches:
                first_match_index = family_matches.index(True)
                name = list(family_faces.keys())[first_match_index]
            else:
                # Check against visitor faces
                visitor_matches = face_recognition.compare_faces(list(visitor_encodings.values()), face_encoding)
                if True in visitor_matches:
                    visitor_index = visitor_matches.index(True)
                    visitor_name = list(visitor_encodings.keys())[visitor_index]
                    name = visitor_name

            # Draw rectangle and label around detected face
            top, right, bottom, left = face_location
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

            current_time = time.time()
            if name == "Unknown" and (current_time - last_alert_time > cooldown_period):
                last_alert_time = current_time
                asyncio.run_coroutine_threadsafe(send_alert(app, chat_id, frame, "Unknown visitor"), loop)
            elif visitor_name and (current_time - last_alert_time > cooldown_period):
                last_alert_time = current_time
                asyncio.run_coroutine_threadsafe(send_alert(app, chat_id, frame, visitor_name), loop)

        cv2.imshow("Video", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    visitor_name = update.message.text.strip()
    print(f"Person recognized as: {visitor_name}")

    if visitor_name:
        visitor_folder = os.path.join(visitors_folder, visitor_name)
        os.makedirs(visitor_folder, exist_ok=True)
        save_new_visitor('visitor.jpg', visitor_name)
        await update.message.reply_text(f"Visitor image saved to '{visitor_name}' folder.")
    else:
        await update.message.reply_text("Please provide a valid visitor description.")

def save_new_visitor(visitor_image_path, visitor_name):
    visitor_folder = os.path.join(visitors_folder, visitor_name)
    os.makedirs(visitor_folder, exist_ok=True)
    cv2.imwrite(os.path.join(visitor_folder, "visitor.jpg"), cv2.imread(visitor_image_path))

def main():
    global family_faces, visitor_encodings
    family_faces = encode_faces_from_folder(r"C:\Users\amank\OneDrive\Desktop\home security\member_images")
    visitor_encodings = encode_faces_from_folder(visitors_folder)
    print("Family and visitor faces encoded. Starting bot...")

    loop = asyncio.get_event_loop()
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the face recognition in a separate thread for capturing and detecting faces
    thread = threading.Thread(target=recognize_and_alert, args=(family_faces, visitor_encodings, '6373962259', app, loop))
    thread.start()

    # Run the Telegram bot in the main event loop to handle messages
    loop.run_until_complete(app.run_polling())

# Run the main function
if __name__ == "__main__":
    main()
