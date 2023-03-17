import asyncio
import logging

from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types.message import ContentType
from config import TOKEN, PAYMENTS_PROVIDER_TOKEN, db, PAYMENT_IMAGE_URL
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from messages import MESSAGES

storage = MemoryStorage()


logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.INFO)

loop = asyncio.get_event_loop()
bot = Bot(token = TOKEN, parse_mode = types.ParseMode.MARKDOWN)
dp = Dispatcher(bot, loop=loop, storage=storage)


button_cancel = KeyboardButton('/cancel')

button_100 = KeyboardButton('100')
button_300 = KeyboardButton('300')
button_500 = KeyboardButton('500')
button_1000 = KeyboardButton('1000')
kb_prices = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_prices.add(button_100)
kb_prices.add(button_300)
kb_prices.add(button_500)
kb_prices.add(button_1000)
kb_prices.add(button_cancel)

kb_cancel = ReplyKeyboardMarkup(resize_keyboard=True).add(button_cancel)

kb_addmoney = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/addmoney'))


class ClientStatesGroup(StatesGroup):
    user = State()
    money = State()


@dp.message_handler(commands=['start'])
async def process_start_command(message):
    await message.reply(MESSAGES['start'].format(name=message.chat.first_name), reply=False)

@dp.message_handler(commands=['cancel'], state='*')
async def cmd_start(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    await message.reply('_Отменил_', reply=False, reply_markup=kb_addmoney)
    await state.finish()


@dp.message_handler(commands=['addmoney'])
async def process_addmoney_command(message):
    await ClientStatesGroup.user.set()
    await message.reply(MESSAGES['addmoney'], reply=False, reply_markup=kb_cancel)


@dp.message_handler(state=ClientStatesGroup.user)
async def get_user(message, state):
    db.connect()
    cursor = db.cursor()
    cursor.execute(f"SELECT id FROM useraccount_customuser WHERE username='{message.text}'")
    user_id = cursor.fetchall()
    db.close()

    if user_id:
        async with state.proxy() as data:
            data['user'] = message.text
            await ClientStatesGroup.next()
            await message.reply(MESSAGES['money_info'],  reply=False, reply_markup=kb_prices)
    else:
        return await message.reply('_Вы неправильно ввели имя пользователя!_', reply=False)


@dp.message_handler(state=ClientStatesGroup.money)
async def get_money(message, state):
    async with state.proxy() as data:
        data['money'] = message.text
        user = data['user']

    if message.text.isdigit() and (money:=int(message.text)) > 0 and money <= 50000:
        await state.finish()
        money *= 100
        if PAYMENTS_PROVIDER_TOKEN.split(':')[1] == 'TEST':
            await bot.send_message(message.from_user.id, MESSAGES['pre_buy_demo_alert'], reply_markup=ReplyKeyboardRemove())

        await bot.send_invoice(message.from_user.id,
                               title=user,
                               description='Счет для пополнения баланса кошелька!',
                               provider_token=PAYMENTS_PROVIDER_TOKEN,
                               currency='rub',
                               photo_url=PAYMENT_IMAGE_URL,
                               photo_height=512,
                               photo_width=512,
                               photo_size=512,
                               need_email=True,
                               need_phone_number=False,
                               need_shipping_address=False,
                               is_flexible=False,
                               prices=[types.LabeledPrice(label=user, amount=money)],
                               start_parameter='invoice',
                               payload=f'{user}'
        )

    else:
        return await message.reply('_Неправильно введенная сумма!_', reply=False)
    

@dp.pre_checkout_query_handler(lambda query: True)
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: types.Message):
    print('successful_payment:')

    user=message.successful_payment.invoice_payload
    money=message.successful_payment.total_amount // 100

    db.connect()
    cursor=db.cursor()
    cursor.execute(f"SELECT money FROM useraccount_wallet WHERE user_id=(SELECT id FROM useraccount_customuser WHERE username='{user}')")
    wallet = cursor.fetchall()[0][0]
    amount = int(money) + int(wallet)
    cursor.execute(f"UPDATE useraccount_wallet set money = '{amount}' WHERE user_id=(SELECT id FROM useraccount_customuser WHERE username='{user}')")
    db.commit()
    db.close()

    pmnt = message.successful_payment.to_python()
    for key, val in pmnt.items():
        print(f'{key} = {val}')

    await bot.send_message(
        message.chat.id,
        MESSAGES['successful_payment'].format(
            total_amount=money,
            currency=message.successful_payment.currency
        )
    )



# @dp.message_handler()
# async def process_find_user(message, state):
#     db.connect()
#     cursor = db.cursor()
#     cursor.execute(f"SELECT id FROM useraccount_customuser WHERE username='{message.text}'")
#     user_id = cursor.fetchall()
#     db.close()

#     if user_id:
#         # print(user_id[0][0])
#         # await state.update_data(message_text=message.text)
#         # await MyStates.message.set()
#         await message.reply('Выберите сумму пополнения, либо введите ее с клавиатуры (максимальная сумма пополнения 100 000):',  reply=False, reply_markup=kb_prices)
#         # await bot.register_next_step_handler(message, amount, user_id)

#     else:
#         print('Не найден')
#         await message.reply('_Вы неправильно ввели имя ползователя!_', reply=False)
    
@dp.message_handler()
async def process_help_command(message):
    await message.reply(MESSAGES['help'], reply=False, reply_markup=kb_addmoney)



if __name__ == '__main__':
    executor.start_polling(dp, loop=loop)






