import os
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get environment variables
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
RENDER_EXTERNAL_HOSTNAME = os.getenv('RENDER_EXTERNAL_HOSTNAME')
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', 'default-secret-token')
PORT = int(os.getenv('PORT', 10000))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('✅ Bot is working with webhooks!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Try /start')

def main():
    """Start the bot."""
    try:
        # Create the Application
        app = Application.builder().token(BOT_TOKEN).build()

        # Add handlers
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("help", help_command))

        # Start the bot
        if RENDER_EXTERNAL_HOSTNAME:
            logger.info("Starting webhook mode")
            app.run_webhook(
                listen="0.0.0.0",
                port=PORT,
                webhook_url=f'https://{RENDER_EXTERNAL_HOSTNAME}/webhook',
                secret_token=WEBHOOK_SECRET,
                drop_pending_updates=True
            )
        else:
            logger.info("Starting polling mode")
            app.run_polling(drop_pending_updates=True)

    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise

if __name__ == "__main__":
    main()
