from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    LabeledPrice,
    BotCommand
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    PreCheckoutQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)
import os
import sys
import asyncio
import nest_asyncio
nest_asyncio.apply()


BOT_TOKEN = os.getenv("BOT_TOKEN")

app = ApplicationBuilder().token(BOT_TOKEN).build()

# --- Command Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hey 💫 I’m Sophie —\n"
        "Wanna glow up with premium perks? Tap /buy and let’s get you sorted."
    )

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "I’m Sophie —, 6 / 7 Telegram channels deep.\n"
        "I’m a tiny little sex fiend-teen dream.  I'm here to help you level up when you're ready to get off for me.\n"
        "Wanna see what I’m about? Tap /channels to explore my exclusive spaces 💅"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Need a hand, babe? I gotchu 💅\n\n"
        "Here’s what I can do:\n"
        "• /buy – Treat yourself to premium\n"
        "• /channels – Explore 6 / 7 exclusive Telegram spaces\n"
        "• /about – Wanna know who I really am?\n"
        "• /menu – Tap-friendly options, obvs\n"
        "• /help – You’re literally here rn 😘"
    )

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
    if query.invoice_payload != "premium_001":
        await query.answer(ok=False, error_message="Invalid payload.")
        return
    await query.answer(ok=True)

async def successful(update: Update, context: ContextTypes.DEFAULT_TYPE):
    payment = update.message.successful_payment
    stars = payment.total_amount
    await update.message.reply_text(f"Payment received! You paid {stars} Stars.")

async def channels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("😈 Tier 1: Previews/PPV – Free", url="https://t.me/sophies_previews")],
        [InlineKeyboardButton("🎬 Tier 2: All Main Content – AMC (£39)", url="https://t.me/+OQ2SZ-rbji5jZDlk")],
        [InlineKeyboardButton("🧃 Tier 3: Innocent (£49)", url="https://t.me/+m6N0qoaYgyBmODVk")],
        [InlineKeyboardButton("💦 Tier 4: Pee (£39)", url="https://t.me/+1LxKZZFjydxhMjE0")],
        [InlineKeyboardButton("💩 Tier 5: 💩 (£39)", url="https://t.me/+PGIBbwa7xXgzODNk")],
        [InlineKeyboardButton("🌐 Tier 6: All Channels Deal – ACD (£75)", url="https://t.me/+pE4R58f8yf5mZmRk")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Alright, here’s the tea ☕\n"
        "I’ve got 6 channels (7 soon 👀) — each one’s a vibe, a mood, a whole moment.\n\n"
        "**Pricing:**\n"
        "• Tier 1: Free\n"
        "• Tier 2–5: £39–£49\n"
        "• Tier 6: All-in for £75\n\n"
        "Wanna peek? Tap below and pick your tier 💅",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🛒 Buy Premium", callback_data="buy")],
        [InlineKeyboardButton("ℹ️ About Sophie", callback_data="about")],
        [InlineKeyboardButton("❓ Help", callback_data="help")],
        [InlineKeyboardButton("📡 Channels", callback_data="channels")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Here’s your glow-up menu, love 💫\nPick your vibe and let’s gooo:",
        reply_markup=reply_markup
    )

# --- Callback Handler ---

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "about":
        await about(update, context)
    elif query.data == "help":
        await help_command(update, context)
    elif query.data == "buy":
        await buy(update, context)
    elif query.data == "channels":
        await channels(update, context)

# --- Set Telegram Command List ---

async def set_commands(app):
    commands = [
        BotCommand("about", "Who is Sophie?"),
        BotCommand("start", "Start chatting with Sophie"),
        BotCommand("help", "What Sophie can do"),
        BotCommand("buy", "Buy premium access"),
        BotCommand("channels", "Explore Sophie’s Telegram channels"),
        BotCommand("menu", "Quick access buttons"),
    ]
    await app.bot.set_my_commands(commands)

# --- Main ---

async def main():
   
    # Register commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("buy", buy))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("channels", channels))
    app.add_handler(CommandHandler("menu", menu))

    # Payment handlers
    app.add_handler(PreCheckoutQueryHandler(precheckout))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful))

    # Button callbacks
    app.add_handler(CallbackQueryHandler(button_handler))

    # Set command list
    await set_commands(app)

    print("Sophie is live and glowing ✨")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    import nest_asyncio
    nest_asyncio.apply()

    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    app.run_polling()

