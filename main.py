import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# 🔴 مهم: ضع BOT_TOKEN في Render Environment Variables
TOKEN = os.getenv("BOT_TOKEN")

OWNER_ID = 8013404749

SERIES_NAME = "Laugh with Illness Series"
BOOK_TITLE = "Laugh with Your Brain"
VOLUME = "Volume 1"

PRICE = "5 USDT"

WALLET_ADDRESS = "TS3z9oKUcQd9iMSmbjg8h8qHFotu4tEEWe"

SUPPORT_LINK = "https://t.me/Rasha2762"

SAMPLE_FILE = "sample.pdf"


# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("📖 Free Sample", callback_data="sample")],
        [InlineKeyboardButton("💰 Buy Book", callback_data="buy")],
        [InlineKeyboardButton("💬 Support", callback_data="support")]
    ]

    await update.message.reply_text(
        f"Welcome to {SERIES_NAME}\n\n{VOLUME}\n{BOOK_TITLE}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ---------------- BUTTONS ----------------
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "sample":

        try:
            with open(SAMPLE_FILE, "rb") as pdf:
                await query.message.reply_document(
                    document=pdf,
                    caption="Free Sample"
                )
        except FileNotFoundError:
            await query.message.reply_text("Sample file not found on server.")

    elif query.data == "buy":

        await query.message.reply_text(
            f"📚 {BOOK_TITLE}\n\n"
            f"💰 Price: {PRICE}\n\n"
            f"Wallet Address:\n{WALLET_ADDRESS}\n\n"
            f"After payment, send screenshot here."
        )

    elif query.data == "support":

        await query.message.reply_text(SUPPORT_LINK)


# ---------------- PHOTO HANDLER ----------------
async def receive_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.message.from_user

    await context.bot.send_photo(
        chat_id=OWNER_ID,
        photo=update.message.photo[-1].file_id,
        caption=f"Payment proof\nUser ID: {user.id}\nUsername: @{user.username}"
    )

    await update.message.reply_text("Payment proof received. Waiting for review.")


# ---------------- MAIN ----------------
def main():

    # تأكد أن التوكن موجود
    if not TOKEN:
        print("BOT_TOKEN is missing in environment variables!")
        return

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.PHOTO, receive_photo))

    app.run_polling()


if __name__ == "__main__":
    main()
