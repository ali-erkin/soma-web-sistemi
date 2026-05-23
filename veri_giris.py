import random
from datetime import date
from sabit_veriler import ARACLAR, KAPASITE, VARDIYALAR

def sahte_vardiya_olustur(vardiya_adi, tarih):
    vardiya_verisi = {
        "tarih"               : tarih.strftime("%d.%m.%Y"),
        "vardiya"             : vardiya_adi,
        "sorumlu"             : random.choice(["Ali", "Veli", "Hasan"]),
        "araclar"             : [],
        "toplam_ton"          : 0,
        "toplam_km"           : 0,
        "toplam_yakit_maliyet": 0
    }

    for plaka, sofor in ARACLAR.items():
        ariza = random.random() < 0.15
        if ariza:
            tur = 0
            km  = 0
        else:
            tur = random.randint(3, 5)
            km  = round(random.uniform(18, 25), 1)

        ton           = tur * KAPASITE
        yakit_maliyet = km * 45

        arac_verisi = {
            "plaka"        : plaka,
            "sofor"        : sofor,
            "durum"        : "Arıza" if ariza else "Çalışıyor",
            "tur"          : tur,
            "ton"          : ton,
            "km"           : km,
            "yakit_maliyet": yakit_maliyet
        }

        vardiya_verisi["araclar"].append(arac_verisi)
        vardiya_verisi["toplam_ton"]            += ton
        vardiya_verisi["toplam_km"]             += km
        vardiya_verisi["toplam_yakit_maliyet"]  += yakit_maliyet

    return vardiya_verisi