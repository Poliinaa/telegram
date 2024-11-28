import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

# Укажите токен вашего бота
API_TOKEN = '7475948235:AAEKG5t-a10ZmqwMH37yQcW2pSc7QaUeuhI'

# Логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Главное меню
main_menu = InlineKeyboardMarkup(row_width=2).add(
    InlineKeyboardButton("Первая помощь", callback_data="first_aid"),
    InlineKeyboardButton("Места нахождения аптечек", callback_data="medkits"),
    InlineKeyboardButton("Алгоритм действий", callback_data="actions"),
    InlineKeyboardButton("Контакты", callback_data="contacts"),
    InlineKeyboardButton("Список несчастных случаев", callback_data="incidents")
)

# Подменю первой помощи
first_aid_menu = InlineKeyboardMarkup(row_width=2).add(
    InlineKeyboardButton("Носовое кровотечение", callback_data="nosebleed"),
    InlineKeyboardButton("Ушибы", callback_data="bruises"),
    InlineKeyboardButton("Царапины и порезы", callback_data="cuts"),
    InlineKeyboardButton("Обморок", callback_data="fainting"),
    InlineKeyboardButton("Назад в меню", callback_data="main_menu"),
)

# Подменю ушибов
bruises_menu = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("Ушиб руки", callback_data="bruise_hand"),
    InlineKeyboardButton("Ушиб ноги", callback_data="bruise_leg"),
    InlineKeyboardButton("Ушиб головы", callback_data="bruise_head"),
    InlineKeyboardButton("Ушиб позвоночника", callback_data="bruise_back"),
    InlineKeyboardButton("Назад", callback_data="first_aid")
)

# Подменю аптечек
medkits_menu = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("1 этаж", callback_data="floor_1"),
    InlineKeyboardButton("2 этаж", callback_data="floor_2"),
    InlineKeyboardButton("3 этаж", callback_data="floor_3"),
    InlineKeyboardButton("4 этаж", callback_data="floor_4"),
    InlineKeyboardButton("Назад в меню", callback_data="main_menu"),
)

# Информация о несчастных случаях
incidents_info = """
Примерный список несчастных случаев:
1. Телесные повреждения (травмы), в том числе нанесенные другим лицом (драки).
2. Острое отравление.
3. Тепловой удар.
4. Ожог.
5. Обморожение.
6. Поражение электрическим током.
7. Иные повреждения здоровья, вызванные внешними факторами.
"""

# Информация о действиях
actions_info = """
Алгоритм действий сотрудника МАУДО «ЦДТ»:
1. Немедленно сообщить заместителю директора Зиновьевой Е.В. (89505654776), если номер недоступен — директору Матухно Н.Н. (89042015742).
2. Организовать первую помощь и вызов скорой медицинской помощи.
3. Запрещается отпускать пострадавшего одного.
4. Сообщить родителям пострадавшего.
5. Принять меры по предотвращению дальнейших инцидентов.
6. Зафиксировать обстановку происшествия.
7. Педагог должен предоставить письменный отчет директору.
8. Ежедневно информировать родителей о состоянии ребенка до выздоровления.
"""

# Обработчик команды /start
@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.reply("Выберите интересующий вас раздел:", reply_markup=main_menu)

# Обработчик callback-данных
@dp.callback_query_handler(lambda c: True)
async def process_callback(callback_query: types.CallbackQuery):
    data = callback_query.data

    if data == "main_menu":
        await callback_query.message.edit_text("Выберите интересующий вас раздел:", reply_markup=main_menu)
    elif data == "first_aid":
        await callback_query.message.edit_text("Выберите вид первой помощи:", reply_markup=first_aid_menu)
    elif data == "medkits":
        await callback_query.message.edit_text("Выберите этаж:", reply_markup=medkits_menu)
    elif data.startswith("floor_"):
        floor = data.split("_")[1]
        await callback_query.message.edit_text(
            f"Места нахождения аптечек, {floor} этаж:\n[здесь можно вставить списки кабинетов]\n",
            reply_markup=medkits_menu
        )
    elif data == "contacts":
        await callback_query.message.edit_text(
            "Контакты:\n1. Заместитель директора Зиновьева Е.В.: 89505654776\n2. Директор Матухно Н.Н.: 89042015742",
            reply_markup=main_menu
        )
    elif data == "actions":
        await callback_query.message.edit_text(actions_info, reply_markup=main_menu)
    elif data == "incidents":
        await callback_query.message.edit_text(incidents_info, reply_markup=main_menu)
    elif data == "nosebleed":
        await callback_query.message.edit_text(
            "Носовое кровотечение:\n1. Усадить пострадавшего, наклонить голову вперед.\n"
            "2. Приложить холод на 15-20 минут.\n"
            "3. Если кровотечение не прекращается, вызвать скорую помощь.\n"
            "При этом пострадавший должен дышать ртом!",
            reply_markup=first_aid_menu
        )
    elif data == "bruises":
        await callback_query.message.edit_text("Выберите тип ушиба:", reply_markup=bruises_menu)
    elif data == "bruise_hand":
        await bot.send_photo(callback_query.message.chat.id, photo=open("hand_bruise.jpg", "rb"))
        await callback_query.message.edit_text(
            "Ушиб руки:\n1. Обеспечить покой.\n2. Приложить холод на 20 минут.\n3. Наложить тугую повязку.\n"
            "Необходимо ребенка отдать родителям. Одного отправлять нельзя!",
            reply_markup=bruises_menu
        )
    elif data == "bruise_leg":
        await callback_query.message.edit_text(
            "Ушиб ноги:\n1. Обеспечить покой.\n2. Приподнять травмированную ногу.\n3. Приложить холод.\n"
            "Необходимо ребенка отдать родителям.",
            reply_markup=bruises_menu
        )
    elif data == "bruise_head":
        await callback_query.message.edit_text(
            "Ушиб головы:\n1. Покой и холод на 20 минут.\n2. Симптомы сотрясения: головокружение, тошнота. При наличии симптомов — вызвать скорую.",
            reply_markup=bruises_menu
        )
    elif data == "bruise_back":
        await callback_query.message.edit_text(
            "Ушиб позвоночника:\n1. Положить пострадавшего на твердую поверхность.\n2. Вызвать скорую помощь.\n"
            "Необходимо организовать сопровождение ребенка.",
            reply_markup=bruises_menu
        )

# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
