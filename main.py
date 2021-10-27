import datetime
import time
from multiprocessing.context import Process

import schedule
import telebot
from pycbrf.toolbox import ExchangeRates
import dateutil.relativedelta

import nicehash
from settings import Nicehash, Telegram
from msg import *


bot = telebot.TeleBot(Telegram.token, parse_mode='HTML')

access_list = [
    191707625,  # Вежливый Человек
    447112770,  # Maks
    886969895,  # Александр
    2081302780,  # Владимир
    2041822130,  # Артём
    910542534,  # Юля

]

# Настройки API nicehash
host = 'https://api2.nicehash.com'
organisation_id = Nicehash.organization_id
key = Nicehash.key
secret = Nicehash.secret
private_api = nicehash.private_api(host, organisation_id, key, secret)
public_api = nicehash.public_api(host, True)


# Запуск Process
def start_process():
    Process(target=P_schedule.start_schedule, args=()).start()


def logging(msg):
    with open('log.txt', 'a') as f:
        f.write('%s: %s;\n' % (datetime.datetime.now().strftime('%m.%d.%Y - %H:%M:%S'), msg))


# Class для работы с schedule
class P_schedule:
    @staticmethod
    def start_schedule():  # Запуск schedule
        # Параметры для schedule
        # Отпавка по времени
        schedule.every().day.at("11:27").do(P_schedule.send_stat_last_day)
        # Отправка по таймеру
        # schedule.every(1).minutes.do(P_schedule.send_message2)

        # Запуск цикла
        while True:
            schedule.run_pending()
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                # todo другое место вызова
                logging('bot stopped')
                return 0

    # Функции для выполнения заданий по времени
    @staticmethod
    def send_stat_last_day():

        btcrub = public_api.get_price()['BTCUSDT'] * float(ExchangeRates()['USD'].value) * 0.9898
        pay_btc = 0.0
        # список выплат
        for pay in private_api.mining_payouts()['list'][:6]:
            pay_btc += float(pay['amount'])
        pay_rub = round(float(pay_btc) * btcrub * 0.9898, 2)

        logging('%s send stat last day' % 191707625)
        bot.send_message(191707625, '%s, %s' % (round(pay_btc, 8), pay_rub))


# Настройки команд telebot
@bot.message_handler(func=lambda message: message.chat.id not in access_list)
def pd_message(message):
    logging('%s permission_denied' % message.chat.id)
    # get name user
    if message.chat.first_name and message.chat.last_name:
        user_name = message.chat.first_name + ' ' + message.chat.last_name
    elif message.chat.first_name:
        user_name = message.chat.first_name
    else:
        user_name = 'друг'
    print(message.chat.id, user_name)

    bot.send_message(message.chat.id, msg_permission_denied)


@bot.message_handler(commands=['start'])
def start_message(message):
    logging('%s /start' % message.chat.id)
    # get name user
    if message.chat.first_name and message.chat.last_name:
        user_name = message.chat.first_name + ' ' + message.chat.last_name
    elif message.chat.first_name:
        user_name = message.chat.first_name
    else:
        user_name = 'друг'

    bot.send_message(message.chat.id, msg_start % user_name)
    bot.send_message(message.chat.id, msg_help)


@bot.message_handler(commands=['info'])
def info_message(message):
    logging('%s /info' % message.chat.id)
    btc_rub = round(public_api.get_price()['BTCUSDT'] * float(ExchangeRates()['USD'].value) * 0.9898, 2)

    profitability_btc = private_api.mining_status()['algorithms']['SCRYPT']['profitability']
    profitability_rub = round(float(profitability_btc) * btc_rub * 0.99, 2)

    balance_btc = private_api.get_accounts()['total']['totalBalance']
    balance_rub = round(float(balance_btc) * btc_rub, 2)

    unpaid_btc = private_api.mining_status()['algorithms']['SCRYPT']['unpaid']
    unpaid_rub = round(float(unpaid_btc) * btc_rub * 0.99, 2)

    btc_usd = round(public_api.get_price()['BTCUSDT'], 2)
    usd_rub = round(ExchangeRates()['USD'].value, 2)

    bot.send_message(message.chat.id, msg_stat % (profitability_btc, profitability_rub) + '\n\n' +
                     msg_balance % (balance_btc, balance_rub, unpaid_btc, unpaid_rub) + '\n\n' +
                     msg_rate % (usd_rub, btc_usd, btc_rub))


@bot.message_handler(commands=['help'])
def help_message(message):
    logging('%s /help' % message.chat.id)
    bot.send_message(message.chat.id, msg_help)


@bot.message_handler(commands=['balance'])
def balance_message(message):
    logging('%s /balance' % message.chat.id)
    balance_btc = private_api.get_accounts()['total']['totalBalance']

    # курс битка в рублях
    btcrub = public_api.get_price()['BTCUSDT'] * float(ExchangeRates()['USD'].value) * 0.9898
    balance_rub = round(float(balance_btc) * btcrub, 2)

    # невыплаченная прибыль
    unpaid_btc = private_api.mining_status()['algorithms']['SCRYPT']['unpaid']
    unpaid_rub = round(float(unpaid_btc) * btcrub * 0.99, 2)

    bot.send_message(message.chat.id, msg_balance % (balance_btc, balance_rub, unpaid_btc, unpaid_rub))


@bot.message_handler(commands=['stat'])
def stat_message(message):
    logging('%s /stat' % message.chat.id)
    profitability_btc = private_api.mining_status()['algorithms']['SCRYPT']['profitability']
    btsrub = public_api.get_price()['BTCUSDT'] * float(ExchangeRates()['USD'].value) * 0.9898
    profitability_rub = round(float(profitability_btc) * btsrub * 0.99, 2)

    bot.send_message(message.chat.id, msg_stat % (profitability_btc, profitability_rub))


@bot.message_handler(commands=['rate'])
def rate_message(message):
    logging('%s /rate' % message.chat.id)
    # текущая цена биткойна в $
    btc_usd = public_api.get_price()['BTCUSDT']
    # курс доллара в рублях
    usd_rub = round(ExchangeRates()['USD'].value, 2)
    # курс битка в рублях
    btc_rub = round(btc_usd * float(ExchangeRates()['USD'].value) * 0.9898, 2)

    bot.send_message(message.chat.id, msg_rate % (usd_rub, btc_usd, btc_rub))


@bot.message_handler(commands=['pays'])
def pays_message(message):
    logging('%s /pays' % message.chat.id)
    bot.send_message(message.chat.id, msg_pays)


@bot.message_handler(commands=['pays_last'])
def pays_message_last(message):
    logging('%s /pays_last' % message.chat.id)
    btcrub = public_api.get_price()['BTCUSDT'] * float(ExchangeRates()['USD'].value) * 0.9898
    msg_pays = ''

    # список выплат
    for pay in private_api.mining_payouts()['list'][:12]:
        datetime_pay = datetime.datetime.fromtimestamp(pay['created'] // 1000).strftime('%d.%m.%Y')
        pay_btc = pay['amount']
        pay_rub = round(float(pay_btc) * btcrub * 0.9898, 2)
        msg_pays += '<u>%s:</u> %s <i>BTC</i> (%s <i>руб</i>).\n' % (datetime_pay, pay_btc, pay_rub)

    bot.send_message(message.chat.id, msg_pays)


@bot.message_handler(commands=['pays_days'])
def pays_message_days(message):
    logging('%s /pays_days' % message.chat.id)
    btcrub = public_api.get_price()['BTCUSDT'] * float(ExchangeRates()['USD'].value) * 0.9898
    msg_pays = ''

    # получаем последние 30 дней
    days = {}
    for i in range(30):
        days[(datetime.date.today() - datetime.timedelta(days=i))] = 0.0

    # список с прошлого кошелька
    if datetime.date(2021, 10, 16) in days:
        days[datetime.date(2021, 10, 16)] = 0.00041011
    if datetime.date(2021, 10, 17) in days:
        days[datetime.date(2021, 10, 17)] = 0.00044202
    if datetime.date(2021, 10, 18) in days:
        days[datetime.date(2021, 10, 18)] = 0.00053709
    if datetime.date(2021, 10, 19) in days:
        days[datetime.date(2021, 10, 19)] = 0.00047750
    if datetime.date(2021, 10, 20) in days:
        days[datetime.date(2021, 10, 20)] = 0.00051211
    if datetime.date(2021, 10, 21) in days:
        days[datetime.date(2021, 10, 21)] = 0.00050883
    if datetime.date(2021, 10, 22) in days:
        days[datetime.date(2021, 10, 22)] = 0.00045213
    if datetime.date(2021, 10, 23) in days:
        days[datetime.date(2021, 10, 23)] = 0.00008671

    # список выплат
    for pay in private_api.mining_payouts()['list'][:70]:
        datetime_pay = datetime.datetime.fromtimestamp(pay['created'] // 1000).date()
        # print(pay)
        pay_btc = float(pay['amount']) - float(pay['feeAmount'])
        if datetime_pay in days:
            days[datetime_pay] += float(pay_btc)

    # формируем строку вывода
    for day in days:
        pay_btc = days[day]
        pay_rub = round(float(pay_btc) * btcrub * 0.9898, 2)
        msg_pays += '<u>%s:</u> %s <i>BTC</i>(%s <i>руб</i>)\n' % (day, round(pay_btc, 8), pay_rub)

    bot.send_message(message.chat.id, msg_pays)


@bot.message_handler(commands=['pays_months'])
def pays_message_months(message):
    logging('%s /pays_months' % message.chat.id)
    btcrub = public_api.get_price()['BTCUSDT'] * float(ExchangeRates()['USD'].value) * 0.9898
    msg_pays = ''

    # получаем последние 12 месяцев
    months = {}
    for i in range(12):
        months[(datetime.datetime.now() + dateutil.relativedelta.relativedelta(months=-i)).month] = 0.0

    # список с прошлого кошелька
    months[10] += 0.00031825
    months[10] += 0.00044202
    months[10] += 0.00053709
    months[10] += 0.00047750
    months[10] += 0.00051211
    months[10] += 0.00050883
    months[10] += 0.00045213
    months[10] += 0.00008671

    # список выплат
    for pay in private_api.mining_payouts()['list'][:2190]:
        datetime_pay = datetime.datetime.fromtimestamp(pay['created'] // 1000).date().month
        pay_btc = float(pay['amount']) - float(pay['feeAmount'])

        months[datetime_pay] += float(pay_btc)
#
    # формируем строку вывода
    for month in months:
        pay_btc = months[month]
        pay_rub = round(float(pay_btc) * btcrub * 0.9898, 2)
        month_list = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь',
                      'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь']
        msg_pays += '<u>%s:</u> <b>%s</b> <i>BTC</i> (<b>%s</b> <i>руб</i>)\n' % (month_list[month-1],
                                                                    round(pay_btc, 8), pay_rub)
#
    bot.send_message(message.chat.id, msg_pays)


@bot.message_handler(commands=['contact'])
def contact_message(message):
    logging('%s /contact' % message.chat.id)
    bot.send_message(message.chat.id, msg_contact)


# @bot.message_handler(content_types=['text'])
# def sent_text(message):
#     bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    # сообщения по времени
    start_process()

    #  запуск бота
    logging('bot started')
    bot.polling()
