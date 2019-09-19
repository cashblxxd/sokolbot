# coding=utf-8
import logging
from json import load
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

with open('dump.json', 'r', encoding='utf-8') as f:
    data = load(f)

TOKEN = "963057313:AAFAwAgE6uDUhxqGzhKQTPu6fLkAM_WZFoc"
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


markup = ReplyKeyboardMarkup([['Какие помещения свободны?'],
                              ['Покажи помещение'],
                              ['Какая арендная ставка на площадь 20м?'],
                              ['Какая арендная ставка на площадь 200м?'],
                              ['Покажите фото офисов'],
                              ['Скиньте договор'],
                              ['Покажите фото фасада и фойе'],
                              ['Как договориться на просмотр?']], one_time_keyboard=True)

p = [["1", "2", "3", "4", "5", "6", "7", "8", "9"]]
for i in range(1, 5):
    p.append(list(map(str, range(i * 10, i * 10 + 10))))
p.append(["51", "52", "53", "54"])
places = ReplyKeyboardMarkup(p, one_time_keyboard=True)


def get_contacts():
    return 'Телефон: +7(912)675-37-77'


def start(update, context):
    update.message.reply_text('Здравствуйте! Чем могу быть полезен?', reply_markup=markup)


def help(update, context):
    update.message.reply_text('Здравствуйте! Я - бот компании \"Сокол\"! Чем могу быть полезен?', reply_markup=markup)


def contacts(update, context):
    update.message.reply_text(get_contacts(), reply_markup=markup)


def to_text(x):
    s = []
    for i in x:
        if i not in ("Вид1", "Вид2", "Вид3", "Планировка", "Фасад", "Коридор", "Фойе", "Тип Договор"):
            s.append(f"{i}: {x[i]}")
    return '\n'.join(s)


def main_texter(update, context):
    text = update.message.text.lower()
    if "просмотр" in text:
        update.message.reply_text(get_contacts(), reply_markup=markup)
        return
    if "привет" in text.lower():
        update.message.reply_text('Здравствуйте! Чем могу быть полезен?', reply_markup=markup)
        return
    if "арендная ставка" in text:
        update.message.reply_text('1000 ₽ - до 50 кв. м.\n900 ₽ или 800 ₽ - в зависимости от этажа и площади, уточняйте в /contacts', reply_markup=markup)
        return
    if "фото офисов" in text:
        update.message.reply_text("Назовите, пожалуйста, номер помещения:)", reply_markup=places)
        context.user_data["state"] = "office_photo"
        return
    if "договор" in text:
        update.message.reply_text("Назовите, пожалуйста, номер помещения:)", reply_markup=places)
        context.user_data["state"] = "agreement"
        return
    if "фойе" in text:
        update.message.reply_text("Назовите, пожалуйста, номер помещения:)", reply_markup=places)
        context.user_data["state"] = "facade"
        return
    if "помещение" in text:
        update.message.reply_text("Назовите, пожалуйста, номер помещения:)", reply_markup=places)
        context.user_data["state"] = "place"
        return
    if "свободны" in text:
        a = []
        for i in data:
            if i["Своб / Занято"] == "с":
                a.append(i["#"])
        if a:
            update.message.reply_text(f"Сейчас свободны помещения: {', '.join(a)}", reply_markup=markup)
            return
        update.message.reply_text("Свободных помещений сейчас нет.:(", reply_markup=markup)
        return
    if text.isdigit():
        if "state" not in context.user_data:
            return
        if context.user_data["state"] == "place":
            context.user_data["state"] = "place"
            for i in data:
                if i["#"] == text:
                    update.message.reply_text(to_text(i), reply_markup=markup)
                    for j in ("Вид1", "Вид2", "Вид3", "Планировка", "Фасад", "Коридор", "Фойе", "Тип Договор"):
                        if i[j]["link"]:
                            context.bot.send_photo(chat_id=update.message.from_user.id, photo=i[j]["link"], caption=i[j]["name"], reply_markup=markup)
                        else:
                            context.bot.send_message(chat_id=update.message.from_user.id, text=i[j]["name"], reply_markup=markup)
                    return
            update.message.reply_text('К сожалению, такого помещения у нас в базе не нашлось...', reply_markup=markup)
            return
        elif context.user_data["state"] == "agreement":
            context.user_data["state"] = "place"
            for i in data:
                if i["#"] == text:
                    for j in ["Тип Договор"]:
                        if i[j]["link"]:
                            context.bot.send_photo(chat_id=update.message.from_user.id, photo=i[j]["link"], caption=i[j]["name"], reply_markup=markup)
                        else:
                            context.bot.send_message(chat_id=update.message.from_user.id, text=i[j]["name"], reply_markup=markup)
                    return
            update.message.reply_text('К сожалению, такого помещения у нас в базе не нашлось...', reply_markup=markup)
            return
        elif context.user_data["state"] == "office_photo":
            context.user_data["state"] = "place"
            for i in data:
                if i["#"] == text:
                    for j in ("Вид1", "Вид2", "Вид3"):
                        if i[j]["link"]:
                            context.bot.send_photo(chat_id=update.message.from_user.id, photo=i[j]["link"], caption=i[j]["name"], reply_markup=markup)
                        else:
                            context.bot.send_message(chat_id=update.message.from_user.id, text=i[j]["name"], reply_markup=markup)
                    return
            update.message.reply_text('К сожалению, такого помещения у нас в базе не нашлось...', reply_markup=markup)
            return
        elif context.user_data["state"] == "facade":
            context.user_data["state"] = "place"
            for i in data:
                if i["#"] == text:
                    for j in ("Фасад", "Фойе"):
                        if i[j]["link"]:
                            context.bot.send_photo(chat_id=update.message.from_user.id, photo=i[j]["link"], caption=i[j]["name"], reply_markup=markup)
                        else:
                            context.bot.send_message(chat_id=update.message.from_user.id, text=i[j]["name"], reply_markup=markup)
                    return
            update.message.reply_text('К сожалению, такого помещения у нас в базе не нашлось...', reply_markup=markup)
            return
    update.message.reply_text("Повторите вопрос, пожалуйста:)", reply_markup=markup)
    return


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, error)


def keyboard(update, context):
    update.message.reply_text(" ", reply_markup=markup)


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("contacts", contacts))
    dp.add_handler(CommandHandler("keyboard", keyboard))
    dp.add_handler(MessageHandler(Filters.text, main_texter))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
