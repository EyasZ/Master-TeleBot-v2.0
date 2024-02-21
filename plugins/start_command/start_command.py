from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from telegram import EyezmiediaBot
import use_offer
from plugins import add_to_cart, view_collection


@EyezmiediaBot.on_message(filters.command("start"), group=0)
async def start_command(client, message):
    # m = client.get_messages(message.chat_id, 12345)
    # print(m.date.year, m.date.month, m.date.day)
    payload = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else ""
    if payload.startswith("use_offer_"):
        offer_id = payload.split('_')[2]
        await use_offer.start_use_offer(client, message, offer_id)
        return
    elif payload.startswith("add2cart_"):
        product_id = payload.split('_')[1]
        await add_to_cart.start_add_to_cart(client, message, product_id)
        return
    elif payload.startswith("view_collection_"):
        collection_id = payload.split('_')[2]
        await view_collection.view_collection(client, message, collection_id)
        return
    user = client.database.get_user(message.from_user.id)
    if user is not None:
        user.status = 'start'
        client.database.set_user_status(user.id, 'start')
    if user.is_seller:
        await message.reply(
            client.plate('welcome_back', name=message.from_user.first_name, reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    client.plate('show_seller_menu'),
                    callback_data='seller_menu'
                )]])),
        )
        if user.currency == '':
            await client.send_message(chat_id=message.chat.id,
                                      text=client.plate('choose_currency'),
                                      reply_markup=InlineKeyboardMarkup([[
                                          InlineKeyboardButton(
                                              client.plate('bank_note_EUR'),
                                              callback_data='set_currency ' + 'EUR'
                                          ),
                                          InlineKeyboardButton(
                                              client.plate('bank_note_USD'),
                                              callback_data='set_currency '
                                                            + 'USD'
                                          ),
                                          InlineKeyboardButton(
                                              client.plate('bank_note_GBP'),
                                              callback_data='set_currency '
                                                            + 'GBP'
                                          )
                                      ]])
                                      )





    else:
        await message.reply(
            client.plate('start_message', name=message.from_user.first_name),
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    client.plate('become_a_seller'),
                    url='https://eyas12ez.wixsite.com/my-site-2'
                )]
            ])
        )
