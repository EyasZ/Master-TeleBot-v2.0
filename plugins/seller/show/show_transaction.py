import json
from datetime import datetime, timezone
from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_callback_query(filters.regex(r'show_transaction (\S+)')) # type: ignore
async def show_product(client, callback):
    transaction = client.database.get_transaction_by_id(
        callback.matches[0].group(1)
    )

    if transaction is not None:
        if transaction.buyer_id == callback.from_user.id:
            address = json.loads(transaction.address)
            date = datetime.fromtimestamp(transaction.date, timezone.utc)

            await callback.answer()
            productsNames = ''
            productIds =  transaction.products_ids.split(',')
            for i in range(len(productIds)):
                product = client.database.get_product_by_id(productIds[i])
                if i == 0:
                    productsNames = productsNames +'{}.{}'.format(i,product.name)
                else:
                    productsNames = productsNames + '\n{}{}'.format( i,product.name)
            await callback.edit_message_text(
                client.plate(
                    'transaction_info',
                    date=date.strftime("%m/%d/%Y, %H:%M:%S"),
                    id=transaction.id,
                    product=productsNames,
                    buyer=(await client.get_users(
                        transaction.buyer_id
                    )).first_name,
                    cost=transaction.cost,
                    offer='yes' if transaction.is_offer else 'no',
                    street_line1=address['street_line1'],
                    street_line2=address['street_line2'],
                    city=address['city'],
                    state=address['state'],
                    post_code=address['post_code']
                ),
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
                    client.plate('back'), callback_data='show_transactions'
                )]])
            )
        else:
            await client.send_message(
                callback.from_user.id,
                client.plate('product_not_owned')
            )
    else:
        await client.send_message(
            callback.from_user.id,
            client.plate('product_not_valid')
        )
