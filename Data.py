from pyrogram.types import InlineKeyboardButton


class Data:
    # Start Message
    START = """
Hey {}

MERHABA DOSTUM {}

TONLARCA ÖZELLİKLİ KANALLARI YÖNETMEK İÇİN BENİ KULLANABİLİRSİNİZ. DAHA FAZLA BİLGİ İÇİN AŞAĞIDAKİ BUTONLARI KULLANIN 

Bye @SancakBotlar
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
Bir kanal ekledikten sonra her şey açıklayıcıdır. Kanal eklemek için klavyedeki 'Kanal Ekle' düğmesini kullanın veya alternatif olarak kolaylık sağlamak için '/add' komutunu kullanın


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
