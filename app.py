import os
from dotenv import load_dotenv
from telegram.ext import Application
from bot import app  # Replace `your_bot_file` with the name of your bot's main file (without .py)

load_dotenv()

if __name__ == "__main__":
    app.run_polling()
