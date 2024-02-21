from pyrogram.client import Client
from pyrogram import filters
import xlsxwriter
from PIL import ImageFont
import string


class CustomCache:
    def __init__(self, database):
        self.database = database
        self.products = {}
        self.users = {}

    def request(self, dict_type, type_id, value_requested):
        if dict_type == 'products':
            value = self.products
        elif dict_type == 'users':
            value = self.users
        else:
            raise ValueError(
                'This cache doesn\'t work with {}'.format(type(dict_type))
            )

        if data_requested := value.get(type_id):
            return data_requested[value_requested]
        else:
            value[type_id] = self.database.select(
                f'SELECT * FROM {dict_type} WHERE id = ?',
                (type_id,)
            ).fetchone()

            return value[type_id][value_requested]


@Client.on_message(filters.command('generate_excel')) # type: ignore
async def generate_excel(client, message):
    if int(client.config['bot']['admin_id']) != message.from_user.id:
        return

    # Setup excel file
    excel_path = 'transactions.xlsx'
    workbook = xlsxwriter.Workbook(excel_path)
    worksheet = workbook.add_worksheet()

    # Define fonts and styles
    font = ImageFont.truetype('MINGLIU.ttf', size=17)
    bold = workbook.add_format({'bold': True})

    # Define
    row = 1
    col = 0
    _cache = CustomCache(client.database)

    columns = {
        'A': {'title': 'ID', 'max_width': 0},
        'B': {'title': 'Product', 'max_width': 0},
        'C': {'title': 'Seller', 'max_width': 0},
        'D': {'title': 'Buyer', 'max_width': 0},
        'E': {'title': 'Cost', 'max_width': 0},
        'F': {'title': 'Is an offer?', 'max_width': 0}
    }

    i = 0
    for letter in string.ascii_uppercase[0:6]:
        worksheet.write(letter + '1', columns[letter]['title'], bold)
        left, top, right, bottom= font.getbbox(columns[letter]['title'])
        width = right - left
        height = top - bottom

        column_width = width*0.13953488372093023
        columns[letter]['max_width'] = column_width
        worksheet.set_column(i, i, column_width)

        i += 1

    # Setup variables and functions to use in the for loop
    def custom_cell_write(
        row,
        col,
        dict_type=None,
        type_id=None,
        value_requested=None,
        text=None
    ):
        if not text and dict_type and type_id and value_requested:
            text = _cache.request(dict_type, type_id, value_requested)

        worksheet.write(row, col, text)
        left, top, right, bottom = font.getbbox(text)
        width = right - left
        hight = top - bottom
        column_width = width*0.13953488372093023

        if columns[list(columns.keys())[col]]['max_width'] < column_width:
            worksheet.set_column(col, col, column_width)

    # Get the transactions
    transactions = client.database.get_transactions()

    # Write the transactions on the excel file
    for transaction in transactions:
        custom_cell_write(row, col, text=transaction.id)
        custom_cell_write(
            row, col+1, 'products', transaction.products_ids, 'name'
        )

        custom_cell_write(
            row, col+1, 'products', transaction.products_ids, 'name'
        )
        custom_cell_write(
            row, col+2, 'users', transaction.seller_id, 'name'
        )
        custom_cell_write(
            row, col+3, 'users', transaction.buyer_id, 'name'
        )
        custom_cell_write(row, col + 4, text=str(transaction.cost))
        custom_cell_write(
            row, col + 5, text='yes' if transaction.is_offer else 'no'
        )

        row += 1

    workbook.close()

    await message.reply_document(excel_path)
