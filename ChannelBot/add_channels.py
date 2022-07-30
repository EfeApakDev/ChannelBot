import asyncio.exceptions
from pyrogram import Client, filters
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChannelPrivate
from ChannelBot.database.users_sql import add_channel as uac, remove_channel
from ChannelBot.database.channel_sql import add_channel as cac, remove_channel, get_channel_info
from ChannelBot.settings import channel_settings
from pyrogram.types import InlineKeyboardMarkup


@Client.on_message((filters.regex(r'^\+ Add Channels \+$') | filters.command('add')) & filters.private)
async def _add_channels(bot: Client, msg):
    user_id = msg.from_user.id
    bot_id = (await bot.get_me()).id
    try:
        channel = await bot.ask(user_id,
                                "Lütfen beni istediğiniz kanala en az 'Mesaj Gönder' ve 'Başkalarının mesajını düzenle' haklarıyla **admin** olarak ekleyin "
                                "\n\nBundan sonra, kanaldan bir mesaj iletin. "
                                "\n\n/cancel kullanarak bu işlemi iptal edin. 5 dakika içinde cevap vermezlerse, işlem otomatik olarak iptal edilecektir..", timeout=300)
        while True:
            if channel.forward_from_chat:
                if channel.forward_from_chat.type == 'channel':
                    channel_id = channel.forward_from_chat.id
                    try:
                        chat_member = await bot.get_chat_member(channel_id, bot_id)
                        chat_member_user = await bot.get_chat_member(channel_id, user_id)
                        if chat_member.can_post_messages and chat_member.can_edit_messages:
                            if chat_member_user.status in ['creator', 'administrator']:  # Don't allow non-admins.
                                success, info = await get_channel_info(channel_id)
                                if success:
                                    try:
                                        admin_chat_member = await bot.get_chat_member(channel_id, info['admin_id'])
                                    except (ChatAdminRequired, UserNotParticipant, ChannelPrivate):
                                        await remove_channel(info['admin_id'], channel_id)
                                        admin_chat_member = None
                                else:
                                    admin_chat_member = None
                                if success and admin_chat_member and admin_chat_member.status in ['creator', 'administrator']:  # Already added channel and admin still admin.
                                    admin = await bot.get_users(info['admin_id'])
                                    text = f"Bu kanal zaten tarafından eklendi {admin.mention}"
                                    await channel.reply(text, quote=True)
                                else:
                                    await uac(user_id, channel_id)
                                    await cac(channel_id, user_id)
                                    await channel.reply("Beni seçtiğiniz için teşekkürler. Şimdi aşağıda gönderilen ayarları özelleştirerek bu kanalı yönetmeye başlayın.", quote=True)
                                    text, markup, _ = await channel_settings(channel_id, bot)
                                    if text:
                                        await msg.reply(text, reply_markup=InlineKeyboardMarkup(markup))
                                    else:
                                        await channel.reply('Kanal Bulunamadı. Lütfen tekrar ekleyin!')
                                        await remove_channel(channel_id)
                            else:
                                text = "Ben yöneticiyim ama sen orada yönetici değilsin. Buna izin veremem."
                                await channel.reply(text, quote=True)
                            break
                        else:
                            text = "Ben yöneticiyim ama gerekli hakların her ikisine de sahip değilim, 'Mesaj Gönder' ve 'Başkalarının mesajını düzenle'. \n\nLütfen tekrar yönlendirmeyi deneyin veya/cancel süreç ."
                            channel = await bot.ask(user_id, text, timeout=300, reply_to_message_id=channel.message_id)
                    except (ChatAdminRequired, UserNotParticipant, ChannelPrivate):
                        text = "Hala admin değilim. Lütfen yeniden yönlendirmeyi deneyin veya işlemi /Cancel  edin."
                        channel = await bot.ask(user_id, text, timeout=300, reply_to_message_id=channel.message_id)
                else:
                    text = 'Bu bir kanal mesajı değildir. Lütfen tekrar yönlendirmeyi deneyin veya işlemi /cancel edin.'
                    channel = await bot.ask(user_id, text, timeout=300, reply_to_message_id=channel.message_id)
            else:
                if channel.text.startswith('/'):
                    await channel.reply(' İptal edildi`Kanal Ekle` İşlemi !', quote=True)
                    break
                else:
                    text = 'Lütfen bir kanal mesajı iletin veya / cancel iptal edin.'
                    channel = await bot.ask(user_id, text, timeout=300, reply_to_message_id=channel.message_id, filters=~filters.me)
    except asyncio.exceptions.TimeoutError:
        await msg.reply('işlem otomatik olarak iptal edildi', quote=True)
