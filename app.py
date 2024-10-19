import os
from dotenv import load_dotenv
from bot import create_app

load_dotenv()

app = create_app()

def main():
    app.run_polling()

if __name__ == "__main__":
    main()
