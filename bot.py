import os
import asyncio
from telegram import Update, LabeledPrice
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    PreCheckoutQueryHandler,
    MessageHandler,
    filters,
    ContextTypes
)
import asyncio
import sys


BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Use /buy to purchase with Stars.")

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_invoice(
        title="Premium Access",
        description="Unlock premium features",
        payload="premium_001",
        provider_token="",  # Stars uses empty provider token
        currency="XTR",
        prices=[LabeledPrice("Premium", 1)],
    )

async def precheckout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.pre_checkout_query

    # Optional payload validation
    if query.invoice_payload != "premium_001":
        await query.answer(ok=False, error_message="Invalid payload.")
        return

    await query.answer(ok=True)

async def successful(update: Update, context: ContextTypes.DEFAULT_TYPE):
    payment = update.message.successful_payment
    stars = payment.total_amount
    await update.message.reply_text(f"Payment received! You paid {stars} Stars.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("buy", buy))
    app.add_handler(PreCheckoutQueryHandler(precheckout))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful))

    app.run_polling()

if __name__ == "__main__":
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    main()