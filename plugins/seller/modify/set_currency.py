
from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_callback_query(filters.regex(r'set_currency (\S+)'))
async def set_currency(client,callback):
    currency = callback.matches[0].group(1)
    user_id = callback.from_user.id
    user = (client.database.get_user(user_id))
    if user is not None:
      if user.is_seller:
        client.database.set_currency(currency,user_id)
        await callback.answer()
        await callback.edit_message_text( client.plate('currency_updated_sucessfully',title =(user.currency)),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(
                        client.plate('back'),
                        callback_data='seller_menu'
                    )]
                    
                    ]))

        
    else:
        await callback.send_message(callback.from_user.id, client.plate('not_seller_error'))
        