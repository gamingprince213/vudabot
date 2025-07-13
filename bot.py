from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask, request, jsonify  # Flask যোগ করুন

app = Flask(__name__)

# টেলিগ্রাম বট সেটআপ
bot_app = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('বট কাজ করছে! ✅')

# Flask এন্ডপয়েন্ট
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('X-Telegram-Bot-Api-Secret-Token') != os.getenv('WEBHOOK_SECRET'):
        return jsonify({"status": "forbidden"}), 403
    
    update = Update.de_json(request.get_json(), bot_app.bot)
    bot_app.process_update(update)
    return jsonify({"status": "ok"}), 200

def main():
    bot_app.add_handler(CommandHandler("start", start))
    
    if os.getenv('RENDER'):
        # Render-এ Flask রান করবে
        app.run(host='0.0.0.0', port=int(os.getenv('PORT', 10000)))
    else:
        # লোকাল ডেভেলপমেন্টে পোলিং মোড
        bot_app.run_polling()

if __name__ == "__main__":
    main()
