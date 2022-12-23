import telebot
from extensions import *

if __name__ == "__main__":
    tb = TelebotCurrency()
    bot = telebot.TeleBot(tb.tb_token)


    @bot.message_handler(commands=['start'])
    def handle_start_help(message):
#        print(message)
        str_ = f"Здравствуйте, *{message.chat.first_name}*\. \n\n"\
"Я бот \- el convertore валют по текущему курсу\. \n\n Запросите: \n *\<исходная валюта\> \<целевая валюта\> \<сумма для обмена\>* \n" \
"\nВалюту смотрю по ее коду или названию, мне не важно\. \n\n"\
"/help для подробного списка команд\. \n\n"\
"__P\.S\. Но вы можете попробовать прислать мне песню, видео, голосовое сообщение, свое местоположение, али стикер какой\.__"
        bot.send_message(message.chat.id, str_, parse_mode='MarkdownV2')
#bot.send_message(message.chat.id, '__Нижнее подчёркивание\.__', parse_mode='MarkdownV2')

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
                raise TBExceptions("*Запрос не соответствует шаблону по числу параметров*\.")

            base, quote, amount = str_

            source, target = tb.text_checking(base, quote, amount)
            result = TelebotCurrency.get_price(source, target, amount)
        except TBExceptions as e:
            bot.send_message(message.chat.id, f"Ошибка ввода пользователя\.\n{e}", parse_mode='MarkdownV2')
        except Exception as e:
            bot.send_message(message.chat.id, f"Проблема с обработкой\. {e}", parse_mode='MarkdownV2')
        else:
            bot.send_message(message.chat.id, f"Меняем шило на мыло. {source} {target} {result}")


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

"""
1. Базовые эксепшены
2. Базовый класс и методы
3. Работа с файлом конфига
4. Работа с БД Redis
5. Основная обработка: парсинг валют, пересчет
6. Логирование действий и вывод лога для пользователя по отдельной команде

sticker — стикер.


Бот возвращает цену на определённое количество валюты (евро, доллар или рубль).
Человек должен отправить сообщение боту в виде <имя валюты, цену которой он хочет узнать> <имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>.

При ошибке пользователя (например, введена неправильная или несуществующая валюта или неправильно введено число) вызывать собственно написанное исключение APIException с текстом пояснения ошибки.
Текст любой ошибки с указанием типа ошибки должен отправляться пользователю в сообщения.

Для отправки запросов к API описать класс со статическим методом get_price(), который принимает три аргумента и возвращает нужную сумму в валюте:
имя валюты, цену на которую надо узнать, — base;
имя валюты, цену в которой надо узнать, — quote;
количество переводимой валюты — amount.

"""
