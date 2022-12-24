import telebot
from extensions import *

if __name__ == "__main__":

    tb = TelebotCurrency()
    bot = telebot.TeleBot(tb.tb_token)

    @bot.message_handler(commands=['start'])
    def handle_start_help(message):
        str_ = f"Здравствуйте, *{message.chat.first_name}*\. \n\n"\
"Я бот \- el convertore валют по текущему курсу\. \n\n Запросите, через пробел: \n *\<исходная валюта\> \<целевая валюта\> \<сумма для обмена\>*\n" \
"\nВалюту смотрю по ее коду или названию, мне не важно\. \n\n"\
"/help для подробного списка команд\. \n\n"\
"__P\.S\. Но вы можете попробовать прислать мне песню, видео, голосовое сообщение, свое местоположение, али стикер какой\.__"
        bot.send_message(message.chat.id, str_, parse_mode='MarkdownV2')


    @bot.message_handler(commands=['help'])
    def handle_start_help(message):
        str_ = "*Перечень допустимых команд\:* \n\n"\
"Общее описание робота el convertore \- /start\n"\
"Данный список команд \- /help\n"\
"Список доступных мне валют \- /value\n"\
f"История ваших, {message.chat.first_name}, запросов \- /history\n"
        bot.send_message(message.chat.id, str_, parse_mode='MarkdownV2')


    @bot.message_handler(commands=['value'])
    def handle_start_help(message):
        str_ = "Бот знает следующие валюты\: \n\n"
        for k,v in CURRENCY.items():
            str_ = str_ + f"*{k}*  \-  {v} \n"
        bot.send_message(message.chat.id, str_, parse_mode='MarkdownV2')


    @bot.message_handler(commands=['history'])
    def handle_start_help(message):
        bot.send_message(message.chat.id, f"Выводим вашу историю запросов.")


    @bot.message_handler(content_types=['text', ])
    def say_lmao(message: telebot.types.Message):
        try:
            str_ = message.text.split(" ")

            if len(str_) != 3:
                raise TBUserExceptions("*Запрос не соответствует шаблону по числу параметров*\.")

            base, quote, amount = str_
            TelebotCurrency.text_checking(base, quote, amount)
            source, target = TelebotCurrency.normalize(base, quote)

            result, p_result, n_source, n_target = TelebotCurrency.get_price(source, target, amount)

        except TBUserExceptions as e:
            bot.send_message(message.chat.id, f"Вы ошиблись при вводе\.\n{e}", parse_mode='MarkdownV2')
        except TBExceptions as e:
            bot.send_message(message.chat.id, f"Ошибка обработки сервером\.\n{e}", parse_mode='MarkdownV2')
        except Exception as e:
            bot.send_message(message.chat.id, f"Проблема с обработкой\.\n{e}", parse_mode='MarkdownV2')
        else:
            amount_ = amount.replace(".", "\.")
            result_ = str(result).replace(".", "\.")
            p_result_ = str(p_result).replace(".", "\.")

            if result == p_result:
                str_ = f"\nКурс не изменялся, раньше получили\-бы столько\-же\."
            elif result > p_result:
                str_ = f"\n*Хороший курс, раньше был хуже\.*\nВы\-бы получили *{p_result_}*\."
            else:
                str_ = f"\n*Не выгодный курс, прежний был лучше\.*\nВы могли получить *{p_result_}*\."

            str_ = f"При обмене *{amount_}* {n_source} на {n_target} вы получите *{result_}*\." + str_
            bot.send_message(message.chat.id, str_, parse_mode='MarkdownV2')


    @bot.message_handler(content_types=['audio', ])
    def say_lmao(message: telebot.types.Message):
        bot.send_message(message.chat.id, 'Сочный звук, мне нра. Хотя ОЙ, ушей-то у меня нет. Вру.')


    @bot.message_handler(content_types=['photo', ])
    def say_lmao(message: telebot.types.Message):
        bot.send_message(message.chat.id, 'Для меня картинки все на одну точку, ничего не вижу, глаз-то нет.')


    @bot.message_handler(content_types=['voice', ])
    def say_lmao(message: telebot.types.Message):
        bot.send_message(message.chat.id, 'Я робот, мной непостижимы голоса из внешнего мира.')


    @bot.message_handler(content_types=['video', ])
    def say_lmao(message: telebot.types.Message):
        bot.send_message(message.chat.id, 'Что-то мельтешит такое, но не распознаю. Я-ж не нейросеть, робот простой.')


    @bot.message_handler(content_types=['document', ])
    def say_lmao(message: telebot.types.Message):
        bot.send_message(message.chat.id, 'Видать что-то дельное написано. Но мне не понять, я больше по валютам.')


    @bot.message_handler(content_types=['location', ])
    def say_lmao(message: telebot.types.Message):
        bot.send_message(message.chat.id, 'Теперь я знаю, где вы находитесь. Но мне это знание бесполезно, уже забыл.')

    @bot.message_handler(content_types=['contact', ])
    def say_lmao(message: telebot.types.Message):
        bot.send_message(message.chat.id, 'Будь у меня мозги, я-б пообщался. Но я не Страшила-Мудрый, мне нечем думать.')

    @bot.message_handler(content_types=['sticker'])
    def say_lmao(message: telebot.types.Message):
        bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAOMY6WAdMw1TO1RLiHv6M807AcmZgsAAh4AA8A2TxOhYFstqwAB3gQsBA")

    bot.polling(none_stop=True)