import os
import json
import logging
import anthropic
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ── Load product data ─────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_products() -> dict:
    path = os.path.join(BASE_DIR, "products.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# ── Build product context for Claude ─────────────────────────────────────────
def build_product_context(products: dict) -> str:
    lines = ["បញ្ជីផលិតផល និងតម្លៃ៖\n"]
    for category, items in products.get("categories", {}).items():
        lines.append(f"## {category}")
        for item in items:
            line = f"- {item['name']}: ${item['price']}"
            if item.get("description"):
                line += f" | {item['description']}"
            if item.get("stock") is not None:
                stock_label = "មាន" if item["stock"] > 0 else "អស់ស្តុក"
                line += f" | ស្តុក: {stock_label}"
            lines.append(line)
        lines.append("")
    return "\n".join(lines)

# ── Ask Claude ────────────────────────────────────────────────────────────────
def ask_claude(user_question: str, product_context: str) -> str:
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        return "❌ មិនមាន ANTHROPIC_API_KEY។ សូម configure ក្នុង environment variables។"

    client = anthropic.Anthropic(api_key=api_key)

    system_prompt = f"""អ្នកជាជំនួយការលក់ផលិតផលដែលឆ្លាតវៃ និងរួសរាយរាក់ទាក់។
អ្នកឆ្លើយតែជាភាសាខ្មែរ លុះត្រាតែអតិថិជនសួរជាភាសាដទៃ។
ឆ្លើយតបត្រឹមតែផ្អែកលើទិន្នន័យផលិតផលខាងក្រោម។
បើមិនមានព័ត៌មានក្នុងបញ្ជី សូមប្រាប់ដោយស្មោះ ហើយណែនាំឲ្យទាក់ទងផ្ទាល់។

{product_context}

ការណែនាំ:
- ឆ្លើយតបខ្លីច្បាស់ (២–៤ប្រយោគ)
- បង្ហាញតម្លៃជា USD ហើយបន្ថែម KHR ប្រសិនបើពាក់ព័ន្ធ
- ប្រើ Emoji ល្មម ដើម្បីទំនុកចិត្ត
- ចុងបញ្ចប់ ណែនាំការទំនាក់ទំនង ឬការកម្មង់"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=system_prompt,
        messages=[{"role": "user", "content": user_question}],
    )
    return message.content[0].text

# ── Telegram handlers ─────────────────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    shop_name = os.environ.get("SHOP_NAME", "ហាងរបស់យើង")
    text = (
        f"👋 សូមស្វាគមន៍មកកាន់ *{shop_name}*!\n\n"
        "🤖 ខ្ញុំជា Bot ជំនួយការ អាចឆ្លើយតបសំណួរអំពី:\n"
        "• 📦 ផលិតផល និងព័ត៌មានលម្អិត\n"
        "• 💰 តម្លៃ និងការបញ្ចុះតម្លៃ\n"
        "• 📊 ស្ថានភាពស្តុក\n\n"
        "💬 *សាកសួរបានដោយសេរី!*\n"
        "ឧទាហរណ៍: _\"តម្លៃ iPhone 15 ប៉ុន្មាន?\"_"
    )
    await update.message.reply_text(text, parse_mode="Markdown")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "📋 *របៀបប្រើ Bot*\n\n"
        "• វាយសំណួរជាភាសាខ្មែរ ឬអង់គ្លេស\n"
        "• Bot នឹងឆ្លើយអំពីផលិតផល និងតម្លៃ\n\n"
        "📌 *ពាក្យបញ្ជា*\n"
        "/start – ចាប់ផ្តើម\n"
        "/help – ជំនួយ\n"
        "/products – មើលបញ្ជីផលិតផលទាំងអស់\n\n"
        "📞 *ទំនាក់ទំនង*\n"
        f"{os.environ.get('CONTACT_INFO', 'សូមទាក់ទង admin')}"
    )
    await update.message.reply_text(text, parse_mode="Markdown")


async def list_products(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    products = load_products()
    lines = ["📦 *បញ្ជីផលិតផលទាំងអស់*\n"]
    for category, items in products.get("categories", {}).items():
        lines.append(f"*{category}*")
        for item in items:
            stock_icon = "✅" if item.get("stock", 1) > 0 else "❌"
            lines.append(f"  {stock_icon} {item['name']} — *${item['price']}*")
        lines.append("")
    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text
    logger.info("User [%s]: %s", update.effective_user.id, user_text)

    # Typing indicator
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action="typing"
    )

    products = load_products()
    product_context = build_product_context(products)
    reply = ask_claude(user_text, product_context)

    await update.message.reply_text(reply)


# ── Main ──────────────────────────────────────────────────────────────────────
def main() -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("❌ TELEGRAM_BOT_TOKEN មិនទាន់ set នៅក្នុង environment!")

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("products", list_products))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("🤖 Bot is running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
