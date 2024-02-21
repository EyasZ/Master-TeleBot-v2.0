from logging import config
from pyrogram.client import Client
from pyrogram import filters
from pyrogram.raw.functions import payments
from pyrogram.raw.types.input_web_document import InputWebDocument
from pyrogram.raw.types.labeled_price import LabeledPrice
from pyrogram.raw.types.input_media_invoice import InputMediaInvoice
from pyrogram.raw.types.data_json import DataJSON
from pyrogram.raw.types.invoice import Invoice
from pyrogram.raw.functions.messages.send_media import SendMedia


# from pyrogram.raw.base import DataJSON


@Client.on_callback_query(filters.regex('^buy_cart$'))
async def buy_cart_products(client, callback):
    user = client.database.get_user(callback.from_user.id)

    cart = client.database.get_user_cart(callback.from_user.id)
    products_data = cart.products
    products_id_array = products_data.split(',')
    products = []
    products_names = ''
    sum = 0
    prices_array = []
    for i in range(len(products_id_array)):
        products_id_array[i] = products_id_array[i].replace('p ', '')
        products.append(client.database.get_product_by_id(products_id_array[i]))
        sum += products[i].cost
        if i == 0:
            if products[0] is not None:
                seller = client.database.get_user(products[0].seller_id)
        if products[i] is not None:
            prices_array.append(LabeledPrice(
                label=products[i].name, amount=int(products[i].cost * 100)))

    if products[0] is not None:

        invoice_raw = Invoice(

            currency=seller.currency,
            prices=prices_array,
            shipping_address_requested=True,
            test=True

        )

        invoiceMedia = InputMediaInvoice(
            title=client.plate('your_cart_checkout'),
            description=client.plate('private_shop'),
            invoice=invoice_raw,  # type: ignore
            payload=products_data.encode('utf-8'),
            provider=client.config['bot']['stripe'],
            start_param='unique-string',
            provider_data=DataJSON(data='{"key": "value"}'),  # type: ignore
            photo=InputWebDocument(

                url='https://i.imgur.com/hApVwg0.png',
                size=0,
                mime_type="image/png",
                attributes=[]
            )  # type: ignore

        )

        await client.invoke(
            SendMedia(
                peer=await client.resolve_peer(callback.from_user.id),
                media=invoiceMedia,  # type: ignore
                random_id=client.rnd_id(),
                message=''

            ))



    else:
        await client.send_message(user.id, client.plate('empty_cart'))
