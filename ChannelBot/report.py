from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_message(filters.regex(r'^Report a Problem$') | filters.command('report'))
async def _manage(_, msg):
    how = '**PROBLEMİ RAPOR ET** \n\n'
    how += "Eğer birşey **beklenmedik **bir sorun olursa bize bildirebilirsin . (Ayrıca özellikler önerebilirsiniz.)\n\n"
    how += '**adımlar ** \n'
    how += '1) ne yaptıysan tekrar dene. Aynı beklenmeyen şeyi gösteriyorsa, 2. adıma geçin \n'
    how += '2) Ziyaret etmek  @sancakbegi probleminizi admine anlatın **Tamamen **, yani, ne beklediğiniz ve bunun yerine ne oldu herşeyi anlatın.'
    how += "Cevap alamazsanız, bir admin etiketleyin. @muhabbetofkings"
    await msg.reply(
        how,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton('Support Group', url='https://t.me/muhabbetofkings')]
        ]),
        quote=True
    )
