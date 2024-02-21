from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_callback_query(filters.regex('^add_products_ask$'))
async def show_products_ask(client, callback):
    user = client.database.get_user(callback.from_user.id)

    keyboard_menu = []
    keyboard_menu.append([InlineKeyboardButton(
                client.plate('add_product'), callback_data='add_product'
            )])
    keyboard_menu.append([InlineKeyboardButton(
                client.plate('add_by_excel'), callback_data='add_by_excel'
            )])
    await callback.edit_message_text(
                client.plate('how_to_add'),
                reply_markup=InlineKeyboardMarkup(keyboard_menu)
            )