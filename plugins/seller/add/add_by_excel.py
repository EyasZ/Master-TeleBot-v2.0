from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_callback_query(filters.regex('^add_by_excel$'))
async def show_product(client, callback):
    user = client.database.get_user(callback.from_user.id)

    if user is not None:
        if user.is_seller:
            if user.currency != '':
              if client.database.set_user_status(
                callback.from_user.id,
                'add_by_excel'
            ):
                await callback.edit_message_text(
                    client.plate('ready_to_add_by_excel'),
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(
                            client.plate('back'),
                            callback_data='show_products'
                        )]
                    ])
                )
            else:
                
                await callback.edit_message_text( 
                                text=client.plate('choose_currency'),
                                reply_markup=InlineKeyboardMarkup([[
                                    InlineKeyboardButton(
                                        client.plate('bank_note_EUR'),
                                        callback_data='set_currency '+'EUR'
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
            await client.send_message(
                callback.from_user.id,
                client.plate('not_seller_error'),
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton(
                        client.plate('become_a_seller'),
                        url='https://eyas12ez.wixsite.com/my-site-2'
                    )
                ]])
            )