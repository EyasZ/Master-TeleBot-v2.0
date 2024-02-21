from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_message(filters.command('transactions')) # type: ignore
async def transactions_command(client, message):
    user = client.database.get_user(message.from_user.id)
    if user is not None:
        user_transactions = client.database.get_transactions_by_user_id(
            message.from_user.id
        )

        if len(user_transactions) > 0:
            productsNames = ''
            for transaction in user_transactions:
                productsIds = transaction.products_ids.split
                for i in range(len(productsIds)):
                     productsNames = productsNames + '{}.{}'.format(i,client.get_product_by_id(id).name)
            await message.reply(
                client.plate('transactions'),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(
                        productsNames,
                        callback_data='show_transaction {}'.format(
                            transaction.id
                        )
                    )] for transaction in user_transactions
                ])
            )
        else:
            await message.reply(client.plate('no_transactions_found'))
    else:
        await message.reply(client.plate('user_not_valid'))
