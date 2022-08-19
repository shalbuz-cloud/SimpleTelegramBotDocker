import random

from aiogram import types
from asyncpg import Connection, Record
from asyncpg.exceptions import UniqueViolationError

from load import bot, dp, db


class DBCommands:
    pool: Connection = db
    ADD_NEW_USER = "INSERT INTO users(chat_id, username, full_name) VALUES " \
                   "($1, $2, $3) RETURNING id"
    ADD_NEW_USER_REFERRAL = "INSERT INTO users(chat_id, username, full_name," \
                            " referral) VALUES ($1,  $2, $3, $4) RETURNING id"
    COUNT_USERS = "SELECT COUNT(*) FROM users"
    GET_ID = "SELECT id FROM users WHERE chat_id = $1"
    CHECK_REFERRALS = "SELECT chat_id FROM users WHERE referral=" \
                      "(SELECT id FROM users WHERE chat_id=$1)"
    CHECK_BALANCE = "SELECT balance FROM users WHERE chat_id=$1"
    ADD_MONEY = "UPDATE users SET balance=balance+$1 WHERE chat_id=$2"

    async def add_new_user(self, referral=None):
        """Добавляем нового пользователя"""
        user = types.User.get_current()

        chat_id = user.id
        username = user.username
        full_name = user.full_name
        args = chat_id, username, full_name

        if referral:
            args += (int(referral),)
            command = self.ADD_NEW_USER_REFERRAL
        else:
            command = self.ADD_NEW_USER

        try:
            record_id = await self.pool.fetchval(command, *args)
            return record_id
        except UniqueViolationError:
            pass

    async def count_users(self):
        record: Record = await self.pool.fetchval(self.COUNT_USERS)
        return record

    async def get_id(self):
        command = self.GET_ID
        user_id = types.User.get_current().id
        return await self.pool.fetchval(command, user_id)

    async def check_referrals(self):
        user_id = types.User.get_current().id
        command = self.CHECK_REFERRALS
        rows = await self.pool.fetch(command, user_id)
        text = ""
        for num, row in enumerate(rows):
            chat = await bot.get_chat(row['chat_id'])
            user_link = chat.get_mention(as_html=True)
            text += "%s. %s" % (num + 1, user_link)
        return text

    async def check_balance(self):
        command = self.CHECK_BALANCE
        user_id = types.User.get_current()
        return await self.pool.fetchval(command, user_id)

    async def add_money(self, money):
        command = self.ADD_MONEY
        user_id = types.User.get_current()
        return await self.pool.fetchval(command, money, user_id)


database = DBCommands()


@dp.message_handler(commands=['start'])
async def register_user(message: types.Message):
    chat_id = message.from_user.id
    referral = message.get_args()
    id_ = await database.add_new_user(referral=referral)
    count_users = await database.count_users()
    text = ""
    if not id_:
        id_ = await database.get_id()
    else:
        text = "Записал в базу"

    bot_username = (await bot.get_me()).username
    id_referral = id_
    bot_link = "https://t.me/%(bot_username)s?start=%(id_referral)s" % \
               {'bot_username': bot_username, 'id_referral': id_referral}

    balance = await database.check_balance()
    text += "Сейчас в базе %s человек!\n\n" \
            "Ваша реферальная ссылка:  %s\n" \
            "Проверить рефералов можно по команде:  /referrals\n\n" \
            "Ваш баланс: %.2f монет.\n" \
            "Добавить монет:  /add_money" % (count_users, bot_link, balance)
    await bot.send_message(chat_id, text)


@dp.message_handler(commands=['referrals'])
async def check_referrals(message: types.Message):
    referrals = await database.check_referrals()
    text = "Ваши рефералы:\n%s" % referrals
    await message.answer(text)


@dp.message_handler(commands=['add_money'])
async def add_money(message: types.Message):
    random_amount = random.randint(1, 100)
    await database.add_money(random_amount)
    balance = await database.check_balance()
    text = "Вам было добавлено %.2f.\nТеперь ваш баланс: %.2f" \
           % (random_amount, balance)
    await message.answer(text)
