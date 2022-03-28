from aiogram import types
from aiogram.dispatcher import FSMContext
import logging

from loader import dp
from utils.misc.check_number_correct import is_number
from handlers.users import give_get, course


@dp.message_handler(state="*")
async def go_buy(message: types.Message, state: FSMContext):
    if message.text == "Получить крипту":
        await give_get.get_crypto(message, state)
    elif message.text == "Отдать крипту":
        await give_get.give_crypto(message, state)
    elif message.text == "Курс крипты":
        await course.get_course(message, state)
    elif state is None:
        await bot_echo(message)
    else:
        current_state = await state.get_state()
        if current_state == "Buy":
            logging.info(f"Buying {message.text}")
            if await is_number(message.text):
                logging.info("Ok")
            else:
                await give_get.incorrect_give_get(message, state)

        elif current_state == "Sell":
            logging.info(f"Selling {message.text}")
            if await is_number(message.text):
                logging.info("Ok")
            else:
                await give_get.incorrect_give_get(message, state)

        else:
            await bot_echo_all(message, state)


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    await message.answer(f"Эхо без состояния."
                         f"Сообщение:\n"
                         f"{message.text}")


# Эхо хендлер, куда летят ВСЕ сообщения с указанным состоянием
@dp.message_handler(state="*", content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    state = await state.get_state()
    await message.answer(f"Эхо в состоянии <code>{state}</code>.\n"
                         f"\nСодержание сообщения:\n"
                         f"<code>{message}</code>")
