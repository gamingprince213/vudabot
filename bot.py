from telegram.ext import Application, CommandHandler

async def start(update, context):
    await update.message.reply_text('বট কাজ করছে! ✅')

def main():
    app = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()
    
    # হ্যান্ডলার রেজিস্টার করুন
    app.add_handler(CommandHandler("start", start))
    
    # ওয়েবহুক কনফিগারেশন
    if os.getenv('RENDER'):
        PORT = int(os.getenv('PORT', 10000))
        app.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            webhook_url=f'https://{os.getenv("RENDER_EXTERNAL_HOSTNAME")}/webhook',
            secret_token=os.getenv('WEBHOOK_SECRET')
        )
    else:
        app.run_polling()

if __name__ == "__main__":
    main()
