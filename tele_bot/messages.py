start_message = '*Добрый день, {name}! С помощью этого бота вы можете пополнить ваш кошелек в asiastream!*\n/addmoney - пополнить кошелек'

addmoney_message = '_Для пополнения баланса введите имя вашего пользователя:_'

addmoney_info = '_Выберите сумму пополнения, либо введите ее с клавиатуры (максимальная сумма пополнения 50000):_'

incorrect_input = '_Введите /addmoney чтобы пополнить кошелек:_'

pre_buy_demo_alert = '''\
Для оплаты используйте данные тестовой карты: 1111 1111 1111 1026, 12/22, CVC 000.
Счёт для оплаты:
'''

successful_payment = '''
Платеж на сумму `{total_amount} {currency}` совершен успешно!
'''

MESSAGES = {
    'start': start_message,
    'addmoney': addmoney_message,
    'money_info': addmoney_info,
    'help': incorrect_input,
    'pre_buy_demo_alert': pre_buy_demo_alert,
    'successful_payment': successful_payment,
}