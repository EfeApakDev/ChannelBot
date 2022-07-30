import asyncio.exceptions
from Data import Data
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import ButtonUrlInvalid
from ChannelBot.database.users_sql import remove_channel as urc
from ChannelBot.database.channel_sql import (
    remove_channel as crc,
    set_caption,
    set_buttons,
    set_sticker,
    set_position,
    set_edit_mode,
    toggle_webpage_preview,
    get_channel_info,
    get_sticker
)
from ChannelBot.manage import manage_channels
from ChannelBot.settings import channel_settings
from ChannelBot.string_to_buttons import string_to_buttons


# Callbacks
@Client.on_callback_query()
async def _callbacks(bot: Client, callback_query: CallbackQuery):
    user = await bot.get_me()
    user_id = callback_query.from_user.id
    mention = user["mention"]
    query = callback_query.data.lower()
    if query.startswith("home"):
        if query == 'home':
            chat_id = callback_query.from_user.id
            message_id = callback_query.message.message_id
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=Data.START.format(callback_query.from_user.mention, mention),
                reply_markup=InlineKeyboardMarkup(Data.buttons),
            )
        elif query == 'home+channel':
            success, buttons, text = await manage_channels(user_id, bot)
            if success:
                await callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(buttons))
            else:
                await callback_query.edit_message_text(text)
        elif query.startswith('home+'):
            channel_id = int(query.split("+")[-1])
            text, markup, sticker_id = await channel_settings(channel_id, bot)
            if text:
                await callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(markup), disable_web_page_preview=True)
    elif query == "about":
        chat_id = callback_query.from_user.id
        message_id = callback_query.message.message_id
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=Data.ABOUT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(Data.home_buttons),
        )
    elif query == "help":
        chat_id = callback_query.from_user.id
        message_id = callback_query.message.message_id
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="**İşte beni nasıl kullanacağınız**\n" + Data.HELP,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(Data.home_buttons),
        )
    elif query.startswith('settings'):
        channel_id = int(query.split('+')[1])
        text, markup, sticker_id = await channel_settings(channel_id, bot)
        if sticker_id:
            await callback_query.message.reply_sticker(sticker_id)
        if text:
            await callback_query.message.delete()
            await callback_query.message.reply(text, reply_markup=InlineKeyboardMarkup(markup), disable_web_page_preview=True)
        else:
            await callback_query.answer('Kanal Bulunamadı. Lütfen tekrar ekleyin!', show_alert=True)
            await crc(channel_id)
            await urc(user_id, channel_id)
            await callback_query.message.delete()
    elif query.startswith('change'):
        change = query.split('+')[1]
        channel_id = int(query.split('+')[2])
        success, info = await get_channel_info(channel_id)
        if success:
            buttons = info['buttons']
            caption = info['caption']
            # position = info['position']
            # webpage_preview = info['webpage_preview']
            sticker_id = info['sticker_id']
            if change == 'caption':
                if caption:
                    buttons = [
                        [InlineKeyboardButton('Altyazıyı değiştir ', callback_data=f'add+{change}+{channel_id}')],
                        [InlineKeyboardButton('Altyazıyı sil', callback_data=f'remove+{change}+{channel_id}')],
                        [InlineKeyboardButton('<-- KANAL AYARLARINA GERİ DÖN', callback_data=f'home+{channel_id}')]
                    ]
                    await callback_query.edit_message_text(f'Current Caption is : \n\n{caption} \n\nUse below buttons to change or remove it.', reply_markup=InlineKeyboardMarkup(buttons))
                else:
                    buttons = [
                        [InlineKeyboardButton('Altyazı ekle', callback_data=f'add+{change}+{channel_id}')],
                        [InlineKeyboardButton('<-- Kanal ayarlarina geri dön ', callback_data=f'home+{channel_id}')]
                    ]
                    await callback_query.edit_message_text(f'Altyazı ayarlanmadı  \n\nEklemek için aşağıdaki düğmeyi kullanın.', reply_markup=InlineKeyboardMarkup(buttons))
            elif change == 'buttons':
                if buttons:
                    _buttons = [
                        [InlineKeyboardButton('URL Düğmelerini Değiştir', callback_data=f'add+{change}+{channel_id}')],
                        [InlineKeyboardButton('url düğmelerini sil', callback_data=f'remove+{change}+{channel_id}')],
                        [InlineKeyboardButton('<-- kanal ayarlarına geri dön', callback_data=f'home+{channel_id}')]
                    ]
                    await callback_query.edit_message_text(f'Geçerli düğmeler  : \n\n`{buttons}` \n\nDeğiştirmek veya kaldırmak için aşağıdaki düğmeleri kullanın.', reply_markup=InlineKeyboardMarkup(_buttons))
                else:
                    _buttons = [
                        [InlineKeyboardButton('buton ekle', callback_data=f'add+{change}+{channel_id}')],
                        [InlineKeyboardButton('<-- kanal ayarlarına geri d9n', callback_data=f'home+{channel_id}')]
                    ]
                    await callback_query.edit_message_text(f'Hiçbir düğme ayarlanmadı \n\nBunları eklemek için aşağıdaki düğmeyi kullanın.', reply_markup=InlineKeyboardMarkup(_buttons))
            elif change == 'position':
                current_position = query.split('+')[3]
                if current_position == 'below':
                    new_position = 'above'
                elif current_position == 'above':
                    new_position = 'replace'
                else:
                    new_position = 'below'
                await set_position(channel_id, new_position)
                text, markup, __ = await channel_settings(channel_id, bot)
                if text:
                    await callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(markup), disable_web_page_preview=True)
                else:
                    await callback_query.answer("", show_alert=True)
                    await callback_query.message.delete()
            elif change == 'edit_mode':
                current_edit_mode = query.split('+')[3]
                if current_edit_mode == 'all':
                    new_edit_mode = 'media'
                else:
                    new_edit_mode = 'all'
                await set_edit_mode(channel_id, new_edit_mode)
                text, markup, __ = await channel_settings(channel_id, bot)
                if text:
                    await callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(markup), disable_web_page_preview=True)
                else:
                    await callback_query.answer("Veritabanında kanal yok", show_alert=True)
                    await callback_query.message.delete()
            elif change == 'sticker':
                if sticker_id:
                    buttons = [
                        [InlineKeyboardButton('Mevcut çıkartmayı göster ', callback_data=f'show+{channel_id}')],
                        [InlineKeyboardButton('Çıkartmayı değiştir ', callback_data=f'add+{change}+{channel_id}')],
                        [InlineKeyboardButton('Çıkartmayı sil', callback_data=f'remove+{change}+{channel_id}')],
                        [InlineKeyboardButton('<-- Kanal Ayarlarına geri dön', callback_data=f'home+{channel_id}')]
                    ]
                    await callback_query.edit_message_text(f'A sticker is already set. See it by tapping \'Show Current Sticker\' button \n\nUse below buttons to change or remove it.', reply_markup=InlineKeyboardMarkup(buttons))
                else:
                    buttons = [
                        [InlineKeyboardButton('Sticker ekle', callback_data=f'add+{change}+{channel_id}')],
                        [InlineKeyboardButton('<-- Kanal ayarlarına geri dön', callback_data=f'home+{channel_id}')]
                    ]
                    await callback_query.edit_message_text(f'Çıkartma seti yok  \n\nEklemek için aşağıdaki düğmeyi kullanın .', reply_markup=InlineKeyboardMarkup(buttons))
            elif change == 'webpage_preview':
                current = query.split('+')[3]
                if current.lower() == 'true':
                    new = False
                else:
                    new = True
                await toggle_webpage_preview(channel_id, new)
                text, markup, __ = await channel_settings(channel_id, bot)
                if text:
                    await callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(markup), disable_web_page_preview=True)
                else:
                    await callback_query.answer("Veritabanında kanal yok", show_alert=True)
                    await callback_query.message.delete()
    elif query.startswith('add'):
        add = query.split('+')[1]
        channel_id = int(query.split('+')[2])
        try:
            if add == 'caption':
                data = await bot.ask(user_id, 'Lütfen yeni başlığı gönderin veya işlemi /cancel edin. Şimdi göndereceğiniz her şey resim yazısı olarak ayarlanacak, bu yüzden dikkatli olun!', timeout=300)
                if data.text.lower() == '/cancel':
                    await data.reply('Cancelled', quote=True)
                else:
                    await set_caption(channel_id, data.text.markdown)
                    await data.reply('Altyazı başarıyla ayarlandı  !', quote=True)
                    text, markup, sticker_id = await channel_settings(channel_id, bot)
                    if sticker_id:
                        await callback_query.message.reply_sticker(sticker_id)
                    if text:
                        await callback_query.message.delete()
                        await callback_query.message.reply(text, reply_markup=InlineKeyboardMarkup(markup), disable_web_page_preview=True)
                    else:
                        await callback_query.answer(' Kanal Bulunamadı. lütfen tekrar ekleyin !', show_alert=True)
                        await crc(channel_id)
                        await urc(user_id, channel_id)
                        await callback_query.message.delete()
            elif add == 'buttons':
                data = await bot.ask(
                    user_id,
                    "**Buton Formatı:** \n\n"
                    "Bir düğmenin bir metni ve bir URL ile ayrılmış bir URL'si olmalıdır. '`-`'. \ntext - link\n"
                    "Örnek : \n`Google - google.com` \n\n"
                    "Tek bir satırdaki birden çok düğme için şunu kullanın: '`|`' bunları tek satırda yaz!!. \ntext1 - link1 | text2 - link2\n"
                    "Örnek: \n`Google - google.com | Telegram - telegram.org`. \n"
                    "Birden fazla satır için bunları farklı satırlara yazın. \ntext1 - link1\ntext2 - link2\n"
                    "Örnek: \n`Google - google.com \n"
                    "Telegram - telegram.org | Change - change.org \n"
                    "Wikipedia - wikipedia.org` \n\n\n"
                    "Şimdi lütfen  **düğmeleri gönder ** or /cancel Süreç . \n\n",
                    timeout=300
                )
                while True:
                    if data.text == '/cancel':
                        await data.reply('Cancelled', quote=True)
                        break
                    if "-" not in data.text:
                        data = await bot.ask(user_id, 'Düğmeler için Yanlış Biçim! Lütfen tekrar deneyin.',
                                             timeout=300)
                    else:
                        given_buttons = await string_to_buttons(data.text)
                        try:
                            await data.reply('nasıl görünecekler !', reply_markup=InlineKeyboardMarkup(given_buttons))
                            await set_buttons(channel_id, data.text)
                            await data.reply('Düğmeler başarıyla ayarlandı  !', quote=True)
                            text, markup, sticker_id = await channel_settings(channel_id, bot)
                            if sticker_id:
                                await callback_query.message.reply_sticker(sticker_id)
                            if text:
                                await callback_query.message.delete()
                                await callback_query.message.reply(text, reply_markup=InlineKeyboardMarkup(markup), disable_web_page_preview=True)
                            else:
                                await callback_query.answer('Kanal Bulunamadı. lütfen tekrar ekleyin !', show_alert=True)
                                await crc(channel_id)
                                await urc(user_id, channel_id)
                                await callback_query.message.delete()
                            break
                        except ButtonUrlInvalid:
                            data = await bot.ask(user_id, 'Düğmeler için Yanlış Biçim! Lütfen tekrar deneyin.', timeout=300)
            elif add == 'position':
                # Won't happen
                pass
            elif add == 'edit_mode':
                # Won't happen
                pass
            elif add == 'sticker':
                data = await bot.ask(user_id, 'Lütfen bir çıkartma gönderin .', timeout=300, filters=filters.sticker)
                await set_sticker(channel_id, data.sticker.file_id)
                await data.reply('Çıkartma başarıyla ayarlandı  !', quote=True)
                text, markup, sticker_id = await channel_settings(channel_id, bot)
                if sticker_id:
                    await callback_query.message.reply_sticker(sticker_id)
                if text:
                    await callback_query.message.delete()
                    await callback_query.message.reply(text, reply_markup=InlineKeyboardMarkup(markup), disable_web_page_preview=True)
                else:
                    await callback_query.answer(' Kanal Bulunamadı. lütfen tekrar ekleyin !', show_alert=True)
                    await crc(channel_id)
                    await urc(user_id, channel_id)
                    await callback_query.message.delete()
            elif add == 'webpage_preview':
                # Won't happen
                pass
        except asyncio.exceptions.TimeoutError:
            pass
    elif query.startswith('remove'):
        args = query.split('+')
        if len(args) == 2:
            channel_id = int(args[1])
            await crc(channel_id)
            await urc(user_id, channel_id)
            await callback_query.answer('Kanal Başarıyla Kaldırıldı', show_alert=True)
            success, buttons, text = await manage_channels(user_id, bot)
            if success:
                await callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(buttons))
            else:
                await callback_query.edit_message_text('Kanal Bulunamadı  ')
        else:
            remove = args[1]
            channel_id = int(args[2])
            if remove == 'caption':
                await set_caption(channel_id, None)
                await callback_query.answer('Altyazı başarıyla kaldırıldı !', show_alert=True)
                text, markup, sticker_id = await channel_settings(channel_id, bot)
                if sticker_id:
                    await callback_query.message.reply_sticker(sticker_id)
                if text:
                    await callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(markup), disable_web_page_preview=True)
                else:
                    await callback_query.answer(' Kanal Bulunamadı. lütfen tekrar ekleyin!', show_alert=True)
                    await crc(channel_id)
                    await urc(user_id, channel_id)
                    await callback_query.message.delete()
            elif remove == 'buttons':
                await set_buttons(channel_id, None)
                await callback_query.answer('Buton Başarıyla silindj !', show_alert=True)
                text, markup, sticker_id = await channel_settings(channel_id, bot)
                if sticker_id:
                    await callback_query.message.reply_sticker(sticker_id)
                if text:
                    await callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(markup), disable_web_page_preview=True)
                else:
                    await callback_query.answer('Kanal Bulunamadı. lütfen tekrar ekleyin !', show_alert=True)
                    await crc(channel_id)
                    await urc(user_id, channel_id)
                    await callback_query.message.delete()
            elif remove == 'position':
                # Won't happen
                pass
            elif remove == 'edit_mode':
                # Won't happen
                pass
            elif remove == 'sticker':
                await set_sticker(channel_id, None)
                await callback_query.answer('Sticker başarıyla silindi !', show_alert=True)
                text, markup, sticker_id = await channel_settings(channel_id, bot)
                if sticker_id:
                    await callback_query.message.reply_sticker(sticker_id)
                if text:
                    await callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(markup), disable_web_page_preview=True)
                else:
                    await callback_query.answer('Kanal Bulunamadı. lütfen tekrar ekleyin !', show_alert=True)
                    await crc(channel_id)
                    await urc(user_id, channel_id)
                    await callback_query.message.delete()
            elif remove == 'webpage_preview':
                # Won't happen
                pass
    elif query.startswith('show'):
        channel_id = int(query.split('+')[1])
        sticker_id = await get_sticker(channel_id)
        if sticker_id:
            sticker = await callback_query.message.reply_sticker(sticker_id)
            await sticker.reply('Bu mevcut çıkartma', quote=True)
        else:
            await callback_query.answer('Kanal Bulunamadı.', show_alert=True)
            await callback_query.message.delete()
