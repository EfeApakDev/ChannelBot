from pyrogram.types import InlineKeyboardButton


class Data:
    # Start Message
    START = """
Hey {}

Welcome to {}

You can use me to manage channels with tons of features. Use below buttons to learn more !

By @StarkBots
    """

    # Home Button
    home_buttons = [
        [InlineKeyboardButton(text="🏠 Eve dön  🏠", callback_data="home")],
    

    # Rest Buttons
    buttons = [
        [InlineKeyboardButton("✨ DİĞER BOTLARIM ✨", url="https://t.me/sancakbotlar/7")],
        [
            InlineKeyboardButton(" ❔"NASIL KULLANILIR , callback_data="help"),
            InlineKeyboardButton("🎪 HAKKINDA  🎪", callback_data="about")
        ],
        [InlineKeyboardButton("♥ DAHA MUHTEŞEM BOTLAR  ♥", url="https://t.me/SancakBotlar")],
        [InlineKeyboardButton("🎨 Support GRUBU 🎨", url="https://t.me/muhabbetofkings")],
    ]

    # Help Message
    HELP = """
Everything is self explanatory after you add a channel.
To add a channel use keyboard button 'Add Channels' or alternatively for ease, use `/add` command

✨ **Kullanılabilir komutlar * ✨

/about - BOT HAKKINDA
/help - YARDIM KOMUTU
/start - BOTU BAŞLATIR

Alternatif Komutlar
/channels - Eklenen kanalları listele 
/add - Kanal Ekle
/report - Problemi Rapor Et
    """

    # About Message
    ABOUT = """
**BOT HAKKINDA** 

@SancakBotlar 'dan bir Telegram kanal otomasyon botu

Ka
ADMİNİN HESABİ: Click Here](https://t.me/sancakbegi)

PYROGRAM: [Pyrogram](docs.pyrogram.org)

DIL : [Python](www.python.org)

Developer : @sancakbegi
    """
