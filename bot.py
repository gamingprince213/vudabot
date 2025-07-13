import os  # এই লাইনটি যোগ করুন
from telegram.ext import Application, CommandHandler

async def start(update, context):
    await update.message.reply_text('বট কাজ করছে! ✅')

def main():
    # টোকেন চেক করুন
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not bot_token:
        print("Error: TELEGRAM_BOT_TOKEN environment variable is not set!")
        exit(1)

    app = Application.builder().token(bot_token).build()
    
    # হ্যান্ডলার রেজিস্টার করুন
    app.add_handler(CommandHandler("start", start))
    
    # ওয়েবহুক কনফিগারেশন
    if os.getenv('RENDER'):
        PORT = int(os.getenv('PORT', 10000))
        webhook_url = f'https://{os.getenv("RENDER_EXTERNAL_HOSTNAME")}/webhook'
        secret_token = os.getenv('WEBHOOK_SECRET')
        
        print(f"Starting webhook on port {PORT} with URL: {webhook_url}")
        app.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            webhook_url=webhook_url,
            secret_token=secret_token
        )
    else:
        print("Starting in polling mode...")
        app.run_polling()

if __name__ == "__main__":
    main()
