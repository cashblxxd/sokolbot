import gspread
from oauth2client.service_account import ServiceAccountCredentials
from json import dump
from time import sleep
from telegram.ext import Updater, CommandHandler


TOKEN = ""


def update_db(update, context):
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'client_secret.json', scope)
    gc = gspread.authorize(credentials)
    worksheet = gc.open_by_key("1HyBOCxiRSmlZygR_oEip9AwmjqeulTur-p6ET6kH2wE").get_worksheet(0)
    d = {
        1: "#",
        2: "Помещение",
        3: "Своб / Занято",
        4: "Этаж",
        5: "Пло-дь, м. кв.",
        6: "Цена, м. кв.",
        7: "Итого цена,руб.",
        8: "Вид1",
        9: "Вид2",
        10: "Вид3",
        11: "Планировка",
        12: "Фасад",
        13: "Коридор",
        14: "Фойе",
        15: "Тип Договор"
    }
    res = []
    p = 0
    try:
        for i in range(2, 56):
            res.append({})
            for j in range(1, 8):
                res[-1][d[j]] = worksheet.cell(i, j).value
                p += 1 / 810
                update.message.reply_text(f'{p * 100} %')
                sleep(1)
            for j in range(8, 16):
                t = worksheet.cell(i, j, value_render_option='FORMULA').value
                if "HYPERLINK" not in t:
                    res[-1][d[j]] = {"link": "", "name": t}
                else:
                    t = t.strip('=HYPERLINK("').strip(")").split(";")
                    res[-1][d[j]] = {"link": t[0].strip('"'), "name": t[1].strip('"')}
                p += 1 / 810
                update.message.reply_text(f'{p * 100} %')
                sleep(1)
    except Exception as e:
        update.message.reply_text(str(e))
        print(res)
        dump(res, open('dump.json', 'w+', encoding='utf-8'), ensure_ascii=False, indent=4)
    finally:
        print(res)
        dump(res, open('dump.json', 'w+', encoding='utf-8'), ensure_ascii=False, indent=4)
    print(res)
    dump(res, open('dump.json', 'w+', encoding='utf-8'), ensure_ascii=False, indent=4)
    update.message.reply_text('Готово')


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("update", update_db))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
