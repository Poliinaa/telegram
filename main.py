from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Ваш токен, который вы получили от BotFather
TOKEN = "7475948235:AAEKG5t-a10ZmqwMH37yQcW2pSc7QaUeuhI"

# Функция для обработки команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Приветственное сообщение и создание клавиатуры
    keyboard = [
        [KeyboardButton("Первая помощь"), KeyboardButton("Профилактика травм")],
        [KeyboardButton("Обучение детей безопасности"), KeyboardButton("Квиз")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Здравствуйте! Я — бот для помощи педагогам по вопросам травматизма. "
        "Выберите нужный раздел:",
        reply_markup=reply_markup
    )

# Функция для обработки раздела "Первая помощь"
async def first_aid(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Информация по первой помощи:\n"
        "1. Оцените состояние пострадавшего.\n"
        "2. Обеспечьте безопасность.\n"
        "3. Вызовите скорую помощь.\n"
        "4. Окажите первую помощь."
    )

# Функция для обработки раздела "Профилактика травм"
async def prevention(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Рекомендации по профилактике травм:\n"
        "- Следите за безопасностью на занятиях.\n"
        "- Регулярно обучайте детей правилам безопасности.\n"
        "- Используйте защитное оборудование."
    )

# Функция для обработки раздела "Обучение детей безопасности"
async def teaching_safety(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Советы для обучения детей:\n"
        "- Проводите занятия с примерами и играми.\n"
        "- Поддерживайте культуру безопасности в классе."
    )

# Функция для обработки квиза
async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [KeyboardButton("1. Прекратить занятия"), KeyboardButton("2. Убедиться в безопасности")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Вопрос: Что необходимо сделать первым делом при обнаружении травмы у ребенка?\n"
        "1. Прекратить занятия.\n"
        "2. Убедиться в безопасности окружающих.",
        reply_markup=reply_markup
    )

# Функция для обработки ответа на квиз
async def quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    answer = update.message.text
    if answer == "1. Прекратить занятия":
        await update.message.reply_text("Правильно! Прекращение занятий — первый шаг для предотвращения дальнейших инцидентов.")
    elif answer == "2. Убедиться в безопасности":
        await update.message.reply_text("Неправильно. В первую очередь нужно прекратить занятия, чтобы предотвратить дальнейшие инциденты.")
    else:
        await update.message.reply_text("Напишите 'начать', чтобы вернуться к меню.")

# Основная функция для запуска бота
def main() -> None:
    # Создаем приложение и регистрируем обработчики команд и сообщений
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Text("Первая помощь"), first_aid))
    application.add_handler(MessageHandler(filters.Text("Профилактика травм"), prevention))
    application.add_handler(MessageHandler(filters.Text("Обучение детей безопасности"), teaching_safety))
    application.add_handler(MessageHandler(filters.Text("Квиз"), quiz))
    application.add_handler(MessageHandler(filters.Text(["1. Прекратить занятия", "2. Убедиться в безопасности"]), quiz_answer))

    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    main()
