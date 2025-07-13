import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Get environment variables
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
RENDER_EXTERNAL_HOSTNAME = os.getenv('RENDER_EXTERNAL_HOSTNAME')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! I am your webhook bot. How can I help you today?')

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
    Available commands:
    /start - Start the bot
    /help - Show this help message
    /echo [text] - Echo back the provided text
    """
    await update.message.reply_text(help_text)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = ' '.join(context.args)
    if not text:
        await update.message.reply_text("Please provide some text after /echo")
    else:
        await update.message.reply_text(f"You said: {text}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(f"I received your message: {text}")

def main():
    # Create the Application
    app = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("echo", echo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Set up webhook on Render
    if RENDER_EXTERNAL_HOSTNAME:
        # Running on Render
        webhook_url = f'https://{RENDER_EXTERNAL_HOSTNAME}/webhook'
        app.run_webhook(
            listen="0.0.0.0",
            port=int(os.environ.get('PORT', 10000)),
            webhook_url=webhook_url,
            secret_token='YOUR_SECRET_TOKEN'  # Optional but recommended
        )
    else:
        # Running locally for testing
        print("Running in polling mode...")
        app.run_polling()

if __name__ == "__main__":
    main()
