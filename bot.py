import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

# Get environment variables
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
RENDER_EXTERNAL_HOSTNAME = os.getenv('RENDER_EXTERNAL_HOSTNAME')
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', 'default-secret-token')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('🚀 Hello! I am your webhook bot. How can I help you today?')

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
    🤖 Available commands:
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
        await update.message.reply_text(f"🔊 You said: {text}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(f"📩 I received: {text}")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")

def main():
    # Create the Application
    app = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("echo", echo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Add error handler
    app.add_error_handler(error_handler)

    # Webhook or polling based on environment
    if RENDER_EXTERNAL_HOSTNAME:
        # Running on Render with webhook
        webhook_url = f'https://{RENDER_EXTERNAL_HOSTNAME}/webhook'
        print(f"Starting webhook on {webhook_url}")
        app.run_webhook(
            listen="0.0.0.0",
            port=int(os.environ.get('PORT', 10000)),
            webhook_url=webhook_url,
            secret_token=WEBHOOK_SECRET
        )
    else:
        # Running locally with polling
        print("Starting in polling mode...")
        app.run_polling()

if __name__ == "__main__":
    main()
