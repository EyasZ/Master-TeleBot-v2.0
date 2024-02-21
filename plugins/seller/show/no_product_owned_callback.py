from pyrogram.client import Client
from pyrogram import filters


@Client.on_callback_query(filters.regex('^no_product_owned_explanation$'))
async def no_product_owned(client, callback):
    await callback.answer(
        client.plate('no_product_owned_explanation'),
        show_alert=True
    )
