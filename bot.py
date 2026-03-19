import os
import anthropic
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """Ты — умный AI-ассистент Telegram-канала ИИ + Крипта 🚀
Помогаешь разбираться в криптовалютах и AI-инструментах для заработка.
Отвечай на русском, дружелюбно, с эмодзи. Не давай финансовых советов."""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Привет! Я AI-ассистент канала ИИ + Крипта 🚀\n\nСпроси меня всё про крипту и ИИ!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.chat.send_action("typing")
    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": update.message.text}]
        )
        await update.message.reply_text(response.content[0].text)
    except Exception:
        await update.message.reply_text("😔 Ошибка. Попробуй ещё раз!")

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
print("✅ Бот запущен!")
app.run_polling()
