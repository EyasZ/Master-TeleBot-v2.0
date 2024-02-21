from pyrogram.client import Client
from pyrogram import filters
from pyrogram.raw.types.labeled_price import LabeledPrice


async def start_use_offer(client, message, offer_id):
    offer = client.database.get_offer_by_id(offer_id)

    if offer is not None:
        if offer.valid:
            if offer.buyer_id == message.from_user.id:
                product = client.database.get_product_by_id(
                    offer.product_id
                )
                seller = await client.get_users(offer.seller_id)

                await client.send_invoice(
                    chat_id=message.chat.id,
                    title=product.namme,
                    description=f'A {seller.first_name}\'s self',
                    currency='EUR',
                    prices=[LabeledPrice(
                        label=product.name, amount=int(offer.cost * 100)
                    )],
                    is_test=True,
                    payment_provider_token=client.config['bot']['stripe'],
                    payload=f'self {offer_id}',
                    start_param=f'use_offer_{offer_id}'
                )
            else:
                await message.reply(client.plate('offer_not_owned'))
        else:
            await message.reply(client.plate('offer_not_valid'))
    else:
        await message.reply(client.plate('offer_not_valid'))
