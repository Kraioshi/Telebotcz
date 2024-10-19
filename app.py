import os
from dotenv import load_dotenv
from bot import create_app  # Import the create_app function

load_dotenv()

app = create_app()  # Create the application instance

def main():
    print('Starting Bot!')
    app.run_polling()  # Start polling

if __name__ == "__main__":
    main()
