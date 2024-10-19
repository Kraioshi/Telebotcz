import os
import random
from dotenv import load_dotenv
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from quiz import read_csv, PATH

load_dotenv()
TOKEN: Final = os.getenv('TOKEN')
BOT_USERNAME: Final = '@slovicko_bot'

word_list = read_csv(PATH)


def create_app() -> Application:
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('play', play_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    return app


# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! I was made to aid you with Czech language!\n'
                                    'Type /play to start practicing.\n'
                                    'Type /help to get an illusion of help.')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a very helpful help command. Helps a lot, doesn't it?\n"
                                    "Type /play to start practicing. ")


async def play_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['game_active'] = True
    await update.message.reply_text('Starting! Type "stop" to end.')
    await pick_game_question(update, context)


async def pick_game_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('game_active', False):
        pair = random.choice(word_list)
        question = pair[1]
        answer = pair[0]
        context.user_data['correct_answer'] = answer
        await update.message.reply_text(f"Translate to Czech: {question}")


# Responses 💩💩💩

async def handle_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    processed_text: str = update.message.text.lower()

    if context.user_data.get('game_active', False):
        if processed_text == 'stop':
            context.user_data['game_active'] = False
            response = 'Stopping. Type /play to start again'
            await update.message.reply_text(response)
            return response  # Return the response text for logging

        correct_answer = context.user_data.get('correct_answer')
        if processed_text == correct_answer.lower():
            response = 'Correct! 🎉🎉🎉'
        else:
            response = f'Wrong! 💩💩💩\nCorrect answer is {correct_answer}'

        # Send the message to the user
        await update.message.reply_text(response)

        # After responding, ask the next question
        await pick_game_question(update, context)

        return response  # Return the response text for logging

    # If the game is not active and the message isn't "stop"
    response = 'I do not understand. Type /play to start the game.'
    await update.message.reply_text(response)
    return response  # Return the response text for logging


# Message handle
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Inform whether it is a group chat or private chat
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f"User ({update.message.chat.id}) in {message_type}: '{text}'")

    if message_type == 'group':
        if BOT_USERNAME in text:
            # Remove bot mention and process the remaining text
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            print(f"Processed text in group: {new_text}")  # For debugging
            response: str = await handle_response(update, context)
            print(f'Bot response: {response}')  # Log the bot response
        else:
            return
    else:
        # Private chats
        response: str = await handle_response(update, context)
        print(f'Bot response: {response}')  # Log the bot response


# Errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
    print('Starting Bot!')
    app = create_app()
    print('Polling...')
    app.run_polling(poll_interval=3)
