import datetime
import math

from matplotlib import pyplot as plt
import numpy as nm

import nicehash
from nicehash import private_api
from settings import Nicehash


def get_current_pays():
    days = {}
    for i in range(24):
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
    for pay in private_api.mining_payouts(186)['list']:
        datetime_pay = datetime.datetime.fromtimestamp(pay['created'] // 1000).date()
        # print(pay)
        pay_btc = float(pay['amount']) - float(pay['feeAmount'])
        if datetime_pay in days:
            days[datetime_pay] += float(pay_btc)

    return days


def average_profit():
    # host = 'https://api2.nicehash.com'
    # organisation_id = Nicehash.organization_id
    # key = Nicehash.key
    # secret = Nicehash.secret
    # private_api = nicehash.private_api(host, organisation_id, key, secret)
    # public_api = nicehash.public_api(host, True)
    #
    # pay_dict = get_current_pays()
    # x = [day for day in pay_dict.keys()]
    # y = pay_dict.values()
    #
    # print(x)
    # print(y)

    x = [datetime.date(2021, 11, 5), datetime.date(2021, 11, 4), datetime.date(2021, 11, 3), datetime.date(2021, 11, 2),
         datetime.date(2021, 11, 1), datetime.date(2021, 10, 31), datetime.date(2021, 10, 30),
         datetime.date(2021, 10, 29), datetime.date(2021, 10, 28), datetime.date(2021, 10, 27),
         datetime.date(2021, 10, 26), datetime.date(2021, 10, 25), datetime.date(2021, 10, 24),
         datetime.date(2021, 10, 23), datetime.date(2021, 10, 22), datetime.date(2021, 10, 21),
         datetime.date(2021, 10, 20), datetime.date(2021, 10, 19), datetime.date(2021, 10, 18),
         datetime.date(2021, 10, 17), datetime.date(2021, 10, 16)]
    y = [0.00044239999999999997, 0.00054924, 0.00058194, 0.00055332, 0.00056535, 0.00055599, 0.00057418, 0.00029434,
         0.0005635600000000001, 0.0005349899999999999, 0.00057376, 0.00055582, 0.00054724, 0.00065331, 0.00045213,
         0.00050883, 0.00051211, 0.0004775, 0.00053709, 0.00044202, 0.00041011]
    x = [i.strftime('%d') for i in x]

    plt.plot(x[::-1], y[::-1], label='BTC', linewidth=7)

    plt.ylim(0, max(y) + 0.0001)

    plt.title('Доход по дням', fontsize=25, pad=10)
    plt.xlabel('Средний доход 5 асиков в день: {}'.format(round(nm.average(y), 10)), fontsize=18)
    plt.legend(loc='upper left', frameon=False, fontsize=18)

    plt.grid()

    # plt.show()
    plt.savefig('average_profit')


def relevance_of_6_asic():
    # средний доход 5 асиков
    average_profit_5 = 0.0005183443
    # средний доход одного асика
    average_profit_1 = average_profit_5 / 5
    # текущая стоимость BTC
    btc = 4354404
    # цена 5-и асиков по текущей цене BTC
    price_5_asics = 500000 / btc
    # цена 5-и асиков по текущей цене BTC
    price_6_asics = 600000 / btc
    # доходы асиков по месяцам
    payback_5_asics = [average_profit_1 * 5 * 30 * (i+1) for i in range(9)]
    payback_6_asics = [payback_5_asics[i] + (average_profit_1 * 30 * i) for i in range(9)]
    payback_5_asics.insert(0, 0)
    payback_6_asics.insert(0, 0)

    print(payback_5_asics)
    print(payback_6_asics)

    x = [i for i in range(10)]

    plt.plot(x, payback_5_asics, label='Доход 5 асиков', linewidth=2, marker='o')
    plt.plot(x, [price_5_asics for i in range(10)], label='Порог окупаемости 5 асиков', linewidth=2)

    plt.plot(x, payback_6_asics, label='Доход 6 асиков', linewidth=2, marker='o')
    plt.plot(x, [price_6_asics for i in range(10)], label='Порог окупаемости 6 асиков', linewidth=2)

    plt.ylim(-0.02, max(payback_6_asics) + 0.02)

    plt.title('Доход по месяцам', fontsize=25, pad=10)
    # plt.xlabel('Окупаемость 5 асиков и 6 асиков будет примерно одинаковой, \n'
    #            'при учете что первый месяц в обоих случаях работало лишь 5 машинок! \n'
    #            'так как их доход в месяц будет {}'.format(round(average_profit_1 * 6 * btc, 10)),
    #            fontsize=12, )
    plt.legend(loc='upper left', frameon=False, fontsize=9)

    plt.grid()

    plt.show()
    # plt.savefig('relevance of 6 asics')

    plt.clf()

    # доходы асиков по месяцам
    payback_5_asics = [average_profit_1 * 5 * 30 * (i + 1) for i in range(23)]
    payback_6_asics = [payback_5_asics[i] + (average_profit_1 * 30 * i) for i in range(23)]
    payback_5_asics.insert(0, 0)
    payback_6_asics.insert(0, 0)

    print(payback_5_asics)
    print(payback_6_asics)

    x = [i for i in range(24)]

    plt.plot(x, payback_5_asics, label='Доход 5 асиков', linewidth=2, marker='o')
    plt.plot(x, payback_6_asics, label='Доход 6 асиков', linewidth=2, marker='o')
    plt.ylim(-0.02, max(payback_6_asics) + 0.02)

    plt.title('Доход по месяцам', fontsize=25, pad=10)
    plt.xlabel('Через 2 года прирост прибыли составит: %s' %
               (average_profit_1 * 30 * 24 * 6 - average_profit_1 - average_profit_1 * 30 * 24 * 5))
    plt.legend(loc='upper left', frameon=False, fontsize=9)

    plt.grid()

    plt.show()
    # plt.savefig('relevance of 6 asics_2')


if __name__ == '__main__':
    # average_profit()
    relevance_of_6_asic()
