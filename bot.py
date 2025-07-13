import os
import re
import logging
import secrets
import string
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def generate_valid_secret():
    """Generate a valid Telegram webhook secret"""
    alphabet = string.ascii_letters + string.digits + '_-'
    return ''.join(secrets.choice(alphabet) for _ in range(32))

# Get environment variables
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
RENDER_EXTERNAL_HOSTNAME = os.getenv('RENDER_EXTERNAL_HOSTNAME')
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', generate_valid_secret())
PORT = int(os.getenv('PORT', 10000))

# Ensure secret is valid
WEBHOOK_SECRET = re.sub(r'[^A-Za-z0-9_-]', '', WEBHOOK_SECRET)[:256] or generate_valid_secret()
logger.info(f"Using webhook secret: {WEBHOOK_SECRET}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('✅ Bot is working perfectly!')

def main():
    try:
        app = Application.builder().token(BOT_TOKEN).build()
        app.add_handler(CommandHandler("start", start))

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
        logger.error(f"Bot failed: {e}")
        raise

if __name__ == "__main__":
    main()
