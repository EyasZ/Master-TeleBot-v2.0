from locale import currency
import re
from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import Update
from pyrogram.raw.functions.messages.set_bot_precheckout_results import SetBotPrecheckoutResults
from pyrogram.raw.types.message_action_payment_sent_me import  MessageActionPaymentSentMe
from pyrogram.raw.types.update_bot_precheckout_query import UpdateBotPrecheckoutQuery
from pyrogram.raw.types.update_new_message import UpdateNewMessage
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from telegram import EyezmiediaBot

@EyezmiediaBot.on_raw_update(group=1)
async def raw_update(client: Client, update: Update, users: dict, chats: dict):
    if isinstance(update, UpdateBotPrecheckoutQuery):
        success = True
        payload = update.payload.decode()
       
        buyer_id = users[update.user_id]
     

        if x := re.match(r'offer (\S+)', payload):
            offer_id = x.group(1)
            offer = client.database.get_offer_by_id(offer_id)

            if offer is not None:
                if not (offer.valid == 1 and offer.buyer_id == buyer_id):
                    success = False
        else:
          payload= payload.split(',')

        if x := re.match(r'p (\S+)', payload[0]):
            for i in range(0,len(payload)):
             x = re.match(r'p (\S+)', payload[i])
             product_id = x.group(1)
             product = client.database.get_product_by_id(product_id)

             if  product is None:
                 success = success and False
             

        await client.invoke(SetBotPrecheckoutResults(
            query_id=update.query_id,
            success=success
        ))

    if (
        isinstance(update, UpdateNewMessage)
        and hasattr(update.message, "action")
        and isinstance(update.message.action, MessageActionPaymentSentMe)
    ):
        payload = update.message.action.payload.decode()
        payload = payload.split(',')
        buyer = users[update.message.peer_id.user_id]
        amount = update.message.action.total_amount
        shipping_address = update.message.action.info.shipping_address

        if x := re.match(r'offer (\S+)', payload[0]):
            offer_id = x.group(1)
            offer = client.database.get_offer_by_id(offer_id)

            if offer is not None:
                if offer.valid == 1 and offer.buyer_id == buyer.id:
                    if offer.cost*100 == amount:
                        product = client.database.get_product_by_id(
                            offer.product_id
                        )
                        client.database.set_offer_valid(offer_id, 0)
                        client.database.insert_transaction(
                            offer.produt_id,
                            offer.seller_id,
                            offer.buyer_id,
                            offer.cost,
                            1,
                            str(shipping_address)
                        )

                        await client.send_message(
                            buyer.id, client.plate('payment_completed_buyer')
                        )

                        await client.send_message(
                            offer.seller_id,
                            client.plate(
                                'payment_completed_seller',
                                buyer=buyer.first_name ,
                                product=product.name,
                                cost=str(amount/100).replace('.0', ''),
                                currency=update.currency,
                                buy_type='offer',
                                street_line1=shipping_address.street_line1,
                                street_line2=shipping_address.street_line2,
                                city=shipping_address.city,
                                state=shipping_address.state,
                                post_code=shipping_address.post_code
                            )
                        )
        

        if x := re.match(r'p (\S+)', payload[0]):
            flag = True
            productsNames = ''
            productsIds = ''
            sum = 0
            product = None
            for i in range(0,len(payload)):
                x = re.match(r'p (\S+)', payload[i])
                product_id = x.group(1)
                product = client.database.get_product_by_id(product_id)

                if product is None:
                  flag = False

                productsNames = productsNames + '\n{}.{} \n'.format(i,product.name)
                if product.hidden_link:
                   productsNames = productsNames + 'link: {}\n code: {}'.format(product.hidden_link,product.product_code)
                if i==0:
                 productsIds = productsIds + '{}'.format(product.id)
                else:
                   productsIds = productsIds + ',{}'.format(product.id)
                   
                sum += product.cost
                

            if not client.database.insert_transaction(
                    productsIds,
                    product.seller_id,
                    buyer.id,
                    str(sum),
                    0,
                    str(shipping_address)
                ):
                flag =False
            if(flag):
              await client.send_message(
                    buyer.id, client.plate('payment_completed_buyer')
                )

              await client.send_message(
                    product.seller_id,
                    client.plate(
                        'payment_completed_seller',
                        buyer=buyer.first_name,
                        product=productsNames,
                        cost=str(amount/100).replace('.0', ''),
                        currency=client.plate(update.message.action.currency),
                        buy_type='product',
                        street_line1=shipping_address.street_line1,
                        street_line2=shipping_address.street_line2,
                        city=shipping_address.city,
                        state=shipping_address.state,
                        post_code=shipping_address.post_code
                    )
                    
            
                )
              client.database.update_balance(product.seller_id,sum)
            else:
                seller = client.get_users(product.seller_id)
                await client.send_message(
                    buyer.id, client.plate('transaction_error_user'),
                     reply_markup=InlineKeyboardMarkup(
                            [
                                [InlineKeyboardButton(
                                    '🗣 Speak to him',
                                    url=f't.me/{seller.username}'
                                )]])

                )
                await client.send_message(
                    seller.id, client.plate('transaction_registration_error')
                )

                  
