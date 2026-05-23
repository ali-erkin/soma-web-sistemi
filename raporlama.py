import os
from sabit_veriler import HEDEF_VARDIYA, HEDEF_GUNLUK

klasor = os.path.dirname(os.path.abspath(__file__))
rapor_klasor = os.path.join(klasor, "raporlar")
if not os.path.exists(rapor_klasor):
    os.makedirs(rapor_klasor)

def vardiya_raporu_kaydet(vardiya_verisi):
    tarih     = vardiya_verisi["tarih"].replace(".", "")
    vardiya   = vardiya_verisi["vardiya"]
    dosya_adi = os.path.join(rapor_klasor, "vardiya_" + vardiya + "_" + tarih + ".txt")

    dosya = open(dosya_adi, "w", encoding="utf-8")
    dosya.write("════════════════════════════════\n")
    dosya.write("  SOMA KÖMÜR OCAĞI - VARDİYA RAPORU\n")
    dosya.write("════════════════════════════════\n")
    dosya.write("Tarih    : " + vardiya_verisi["tarih"] + "\n")
    dosya.write("Vardiya  : " + vardiya + "\n")
    dosya.write("Sorumlu  : " + vardiya_verisi["sorumlu"] + "\n")
    dosya.write("────────────────────────────────\n")

    for arac in vardiya_verisi["araclar"]:
        dosya.write("Araç     : " + arac["plaka"] + " | " + arac["sofor"] + "\n")
        dosya.write("Durum    : " + arac["durum"] + "\n")
        dosya.write("Tur      : " + str(arac["tur"]) + "\n")
        dosya.write("Tonaj    : " + str(arac["ton"]) + " ton\n")
        dosya.write("Km       : " + str(arac["km"]) + " km\n")
        dosya.write("Yakit    : " + str(round(arac["yakit_maliyet"], 2)) + " TL\n")
        dosya.write("────────────────────────────────\n")

    dosya.write("TOPLAM TON   : " + str(vardiya_verisi["toplam_ton"]) + " ton\n")
    dosya.write("TOPLAM KM    : " + str(round(vardiya_verisi["toplam_km"], 1)) + " km\n")
    dosya.write("TOPLAM YAKIT : " + str(round(vardiya_verisi["toplam_yakit_maliyet"], 2)) + " TL\n")

    if vardiya_verisi["toplam_ton"] >= HEDEF_VARDIYA:
        dosya.write("SONUC        : Hedef Asildi!\n")
    else:
        fark = HEDEF_VARDIYA - vardiya_verisi["toplam_ton"]
        dosya.write("SONUC        : Hedef Tutturulamadi. Fark: " + str(fark) + " ton\n")

    dosya.write("════════════════════════════════\n")
    dosya.close()

def gunluk_rapor_kaydet(tum_vardiyalar, tarih):
    tarih_str = tarih.strftime("%d%m%Y")
    dosya_adi = os.path.join(rapor_klasor, "gunluk_" + tarih_str + ".txt")

    gunluk_ton   = sum(v["toplam_ton"]           for v in tum_vardiyalar)
    gunluk_yakit = sum(v["toplam_yakit_maliyet"] for v in tum_vardiyalar)

    dosya = open(dosya_adi, "w", encoding="utf-8")
    dosya.write("════════════════════════════════\n")
    dosya.write("  SOMA KÖMÜR OCAĞI - GÜNLÜK RAPOR\n")
    dosya.write("════════════════════════════════\n")
    dosya.write("Tarih         : " + tarih.strftime("%d.%m.%Y") + "\n")
    dosya.write("────────────────────────────────\n")

    for v in tum_vardiyalar:
        durum = "Hedef Asildi!" if v["toplam_ton"] >= HEDEF_VARDIYA else "Hedef Tutturulamadi!"
        dosya.write(v["vardiya"] + " : " + str(v["toplam_ton"]) + " ton → " + durum + "\n")

    dosya.write("────────────────────────────────\n")
    dosya.write("GÜNLÜK TON   : " + str(gunluk_ton) + " ton\n")
    dosya.write("GÜNLÜK YAKIT : " + str(round(gunluk_yakit, 2)) + " TL\n")

    if gunluk_ton >= HEDEF_GUNLUK:
        dosya.write("SONUC        : Gunluk Hedef Asildi!\n")
    else:
        fark = HEDEF_GUNLUK
        dosya.write("════════════════════════════════\n")
    dosya.close()

    return {"tarih": tarih.strftime("%d.%m.%Y"), "ton": gunluk_ton, "yakit": gunluk_yakit}

def haftalik_rapor_kaydet(gunluk_veriler):
    dosya_adi = os.path.join(rapor_klasor, "haftalik_rapor.txt")

    haftalik_ton   = sum(g["ton"]   for g in gunluk_veriler)
    haftalik_yakit = sum(g["yakit"] for g in gunluk_veriler)

    dosya = open(dosya_adi, "w", encoding="utf-8")
    dosya.write("════════════════════════════════\n")
    dosya.write("  SOMA KÖMÜR OCAĞI - HAFTALIK RAPOR\n")
    dosya.write("════════════════════════════════\n")
    dosya.write("Dönem : " + gunluk_veriler[0]["tarih"] + " - " + gunluk_veriler[-1]["tarih"] + "\n")
    dosya.write("────────────────────────────────\n")

    for g in gunluk_veriler:
        durum = "Hedef Asildi!" if g["ton"] >= HEDEF_GUNLUK else "Hedef Tutturulamadi!"
        dosya.write(g["tarih"] + " : " + str(g["ton"]) + " ton → " + durum + "\n")

    dosya.write("────────────────────────────────\n")
    dosya.write("HAFTALIK TON   : " + str(haftalik_ton) + " ton\n")
    dosya.write("HAFTALIK YAKIT : " + str(round(haftalik_yakit, 2)) + " TL\n")
    dosya.write("════════════════════════════════\n")
    dosya.close()
    print("✅ Haftalık rapor kaydedildi!")