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
PORT = int(os.getenv('PORT', 10000))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('🚀 Webhook bot ready!')

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Help message here')

def main():
    # Verify webhook dependencies are installed
    try:
        from telegram.ext._updater import WEBHOOK_DEPS_INSTALLED
        if not WEBHOOK_DEPS_INSTALLED:
            raise RuntimeError("Webhook dependencies not installed")
    except ImportError:
        raise RuntimeError("Webhook dependencies not available")

    app = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))

    if RENDER_EXTERNAL_HOSTNAME:
        print(f"Starting webhook on port {PORT}")
        app.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            webhook_url=f'https://{RENDER_EXTERNAL_HOSTNAME}/webhook',
            secret_token=WEBHOOK_SECRET
        )
    else:
        print("Starting in polling mode")
        app.run_polling()

if __name__ == "__main__":
    main()
