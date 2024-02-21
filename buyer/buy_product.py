from logging import config
from pyrogram import filters
from pyrogram.client import Client
from pyrogram.raw.types.input_web_document import InputWebDocument
from pyrogram.raw.types.data_json import DataJSON
from pyrogram.raw.types.labeled_price import LabeledPrice
from pyrogram.raw.types.input_media_invoice import InputMediaInvoice
from pyrogram.raw.types.invoice import Invoice
from pyrogram.raw.functions.messages.send_media import SendMedia


@Client.on_message(filters.regex(r'/start buy_(\S+)'))
async def start_use_offer(client, message):
    product_id = message.matches[0].group(1)
    product = client.database.get_product_by_id(product_id)

    if product is not None:
        seller = client.database.get_user(product.seller_id)

        invoice_raw = Invoice(
            currency=seller.currency,
            prices=[LabeledPrice(
                label=product.name, amount=int(product.cost * 100)
            )],  # type: ignore
            shipping_address_requested=True,
            test=True

        )
        payloadStr = 'p {product_id}'.format(product_id=product.id)
        invoiceMedia = InputMediaInvoice(
            title=product.name,
            description=client.plate('private_shop'),
            invoice=invoice_raw,  # type: ignore
            payload=payloadStr.encode('utf-8'),
            provider=client.config['bot']['stripe'],
            start_param='buy_{}'.format(product.id),
            provider_data=DataJSON(data='{"key": "value"}'),  # type: ignore
            photo=InputWebDocument(

                url=product.photo_link,
                size=0,
                mime_type="image/png",
                attributes=[]
            )  # type: ignore
        )
        await client.invoke(
            SendMedia(
                peer=await client.resolve_peer(message.chat.id),
                media=invoiceMedia,  # type: ignore
                random_id=client.rnd_id(),
                message=''

            ))



    else:
        await message.reply(client.plate('product_not_valid'))
