import locale
import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CallbackContext,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

load_dotenv()

from messages import *

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filename="logs.log",
    encoding="utf-8",
    filemode="a",
)

logger = logging.getLogger(__name__)

# Import the token and connect to the bot
token = os.getenv("TELEGRAM_BOT_TOKEN")

# Define conversation states
NET_AMOUNT, PERCENT = range(2)


# Start handler (unchanged)
async def start(update: Update, context: CallbackContext) -> None:
    try:
        user_language = update.effective_user.language_code

        context.user_data["chat_id"] = update.effective_chat.id
        context.user_data["name"] = update.message.from_user.first_name

        # Reply to the user
        await update.message.reply_text(
            await start_message(context.user_data["name"], user_language),
        )
    except Exception as e:
        logger.error("An error occurred:", e)


# Calculate handler to start the conversation
async def calculate(update: Update, context: CallbackContext) -> None:
    # Prompt the user for the net monthly amount
    user_language = update.effective_user.language_code
    await update.message.reply_text(
        await net_amount(user_language),
    )
    return NET_AMOUNT


# First step: user inputs the net monthly amount
async def get_net_amount(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text
    try:
        context.user_data["net_amount"] = float(user_input)
        user_language = update.effective_user.language_code
        await update.message.reply_text(
            await percentage(user_language),
        )
        return PERCENT
    except ValueError:
        await update.message.reply_text(
            await net_amount_error(user_language),
        )
        return NET_AMOUNT


# Second step: user inputs the percentage
async def get_percentage(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text
    user_language = update.effective_user.language_code
    net_amount = context.user_data["net_amount"]
    yearly_net_amount = net_amount * 12
    try:
        percentage = float(user_input)
        if user_language == "fr":
            # Calculate the gross amount of money the PEA will give
            pea_max = 150000
            pea_max_yield = pea_max * (percentage / 100)
            pea_net_year = pea_max_yield - (pea_max_yield * (17.2 / 100))
            new_yearly_net_amount = yearly_net_amount - pea_net_year
            yearly_gross_amount = new_yearly_net_amount / 0.7
            result = yearly_gross_amount / (percentage / 100)
            currency_symbol, formatted_result = await get_formatted_currency(
                result, user_language
            )
            total_invest = result + pea_max
            currency_symbol, formatted_total_invest = await get_formatted_currency(
                total_invest, user_language
            )
            await update.message.reply_text(
                await result_message_pea(
                    user_language,
                    net_amount,
                    percentage,
                    formatted_result,
                    currency_symbol,
                    pea_net_year,
                    formatted_total_invest,
                ),
            )
        else:
            yearly_gross_amount = yearly_net_amount / 0.7
            result = yearly_gross_amount / (percentage / 100)
            currency_symbol, result = await get_formatted_currency(
                result, user_language
            )
            await update.message.reply_text(
                await result_message(
                    user_language, net_amount, percentage, result, currency_symbol
                ),
            )
        return ConversationHandler.END
    except ValueError:
        await update.message.reply_text(
            await percentage_error(user_language),
        )
        return PERCENT


# Conversation handler
async def cancel(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Operation canceled.")
    return ConversationHandler.END


# Start handler (unchanged)
async def help(update: Update, context: CallbackContext) -> None:
    try:
        user_language = update.effective_user.language_code

        context.user_data["chat_id"] = update.effective_chat.id
        context.user_data["name"] = update.message.from_user.first_name

        # Reply to the user
        await update.message.reply_text(
            await help_message(context.user_data["name"], user_language),
        )
    except Exception as e:
        logger.error("An error occurred:", e)


async def get_formatted_currency(amount: float, user_language: str) -> str:
    try:
        # Set the locale based on the user's language
        if user_language == "fr":
            locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")  # French locale
        elif user_language == "de":
            locale.setlocale(locale.LC_ALL, "de_DE.UTF-8")  # German locale
        elif user_language == "en":
            locale.setlocale(locale.LC_ALL, "en_US.UTF-8")  # English locale
        elif user_language == "es":
            locale.setlocale(locale.LC_ALL, "es_ES.UTF-8")  # Spanish locale
        # Add more languages as needed
        else:
            # Fallback to US locale if language is not recognized
            locale.setlocale(locale.LC_ALL, "en_US.UTF-8")

        # Retrieve the currency symbol
        currency_symbol = locale.localeconv()["currency_symbol"]

        if currency_symbol == "Eu":
            currency_symbol = "€"

        # Format the amount as currency manually if needed
        if user_language == "en":
            # For English locale, use comma as a thousand separator and period as a decimal
            formatted_currency = f"{currency_symbol}{amount:,.2f}"
        else:
            # For other locales like French, format using space as thousand separator and comma as decimal
            formatted_currency = f"{amount:,.2f}{currency_symbol}".replace(
                ",", " "
            ).replace(".", ",")

        return currency_symbol, formatted_currency
    except Exception as e:
        print(f"Error in get_formatted_currency: {e}")
        return None, str(amount)


if __name__ == "__main__":
    application = Application.builder().token(token).build()

    # Conversation handler
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("calculate", calculate)],
        states={
            NET_AMOUNT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_net_amount)
            ],
            PERCENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_percentage)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # Add the start handler
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(conversation_handler)

    print("Starting bot ...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)
