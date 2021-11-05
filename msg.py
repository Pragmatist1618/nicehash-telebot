from aiogram.utils.markdown import text

msg_start ='Привет, %s! Я создан, чтобы радовать Вас каждый день благими новостями и помогать ориентироваться ' \
           'в этом тяжелом мире!'
msg_help = text('<b>Команды для управления:</b>\n',
                '/info - Полная информация по пулу;\n',
                '/balance - Проверить текущий баланс кошелька;\n',
                '/stat - Статистика прибыльности;\n',
                '/rate - Текущий курс USD и BTC;\n',
                '/pays - Информация по выплатам.\n',
                '/contact - Связь с разработчиком.\n')

msg_info = ''

msg_balance = text('<b>Доступный баланс:</b> %s BTC (%s руб).',
                   '\n\n<b>Невыплаченная прибыль:</b> %s BTC (%s руб).')

msg_stat = '<b>Текущая прибыльность:</b> %s BTC (%s руб).'

msg_rate = text('<b>Курс USD:</b> %s руб;',
                '\n<b>Курс BTC:</b> %s USD (%s руб).')

msg_contact = 'При возникновении вопросов обращайтесь: @redwh1te76'

msg_permission_denied = 'У Вас нет прав использования бота. \n Обратитесь к администратору: @redwh1te76'

msg_pays = text(
    '/pays_last - Вывести последние 12 выплат (за каждые 4 часа);',
    '\n/pays_days - Вывести ежедневные выплаты (последние 30);',
    '\n/pays_months - Вывести ежемесячные выплаты (последние 12).'
)

msg_pay_day = 'За последнюю неделю кровью и потом заработано: <b>%s</b> BTC (<b>%s</b> руб)!!!'
