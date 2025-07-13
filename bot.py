import os
import re
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def validate_secret_token(token: str) -> bool:
    """Validate the webhook secret token format"""
    return bool(re.match(r'^[A-Za-z0-9_-]{1,256}$', token))

# Get environment variables
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
RENDER_EXTERNAL_HOSTNAME = os.getenv('RENDER_EXTERNAL_HOSTNAME')
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', 'default-secret-token')
PORT = int(os.getenv('PORT', 10000))

# Validate secret token
if not validate_secret_token(WEBHOOK_SECRET):
    logger.error("Invalid WEBHOOK_SECRET format. Must contain only A-Z, a-z, 0-9, _, - and be 1-256 chars long")
    exit(1)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('✅ Bot is working!')

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
