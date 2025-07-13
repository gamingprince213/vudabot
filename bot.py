import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Get environment variables
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
RENDER_EXTERNAL_HOSTNAME = os.getenv('RENDER_EXTERNAL_HOSTNAME')
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', 'default-secret-token')
PORT = int(os.getenv('PORT', 10000))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('🚀 Bot is working with webhooks!')

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Try /start')

def main():
    # Create application
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))

    # Webhook or polling based on environment
    if RENDER_EXTERNAL_HOSTNAME:
        print("Starting webhook mode")
        app.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            webhook_url=f'https://{RENDER_EXTERNAL_HOSTNAME}/webhook',
            secret_token=WEBHOOK_SECRET,
            drop_pending_updates=True
        )
    else:
        print("Starting polling mode")
        app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
