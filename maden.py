import os
import random
from datetime import date, timedelta

# ─── KLASÖR AYARI ───────────────────────────
klasor = os.path.dirname(os.path.abspath(__file__))
rapor_klasor = os.path.join(klasor, "raporlar")
if not os.path.exists(rapor_klasor):
    os.makedirs(rapor_klasor)

# ─── SABİT VERİLER ──────────────────────────
KAPASITE      = 30
HEDEF_GUNLUK  = 1500
HEDEF_VARDIYA = 500
YAKIT_FIYATI  = 45

ARACLAR = {
    "34 ABC 001": "Mehmet Yılmaz",
    "34 ABC 002": "Ahmet Kaya",
    "34 ABC 003": "Hüseyin Demir",
    "34 ABC 004": "Mustafa Çelik",
    "34 ABC 005": "İbrahim Şahin"
}

VARDIYALAR = ["Sabah", "Öğle", "Gece"]

# ─── FONKSİYON 1: TEST VERİSİ ───────────────
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
        ariza = random.random() < 0.15  # %15 arıza ihtimali
        if ariza:
            tur = 0
            km  = 0
        else:
            tur = random.randint(3, 5)
            km  = round(random.uniform(18, 25), 1)

        ton           = tur * KAPASITE
        yakit_maliyet = km * YAKIT_FIYATI

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

# ─── FONKSİYON 2: VARDİYA RAPORU ───────────
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

# ─── FONKSİYON 3: GÜNLÜK RAPOR ──────────────
def gunluk_rapor_kaydet(tum_vardiyalar, tarih):
    tarih_str = tarih.strftime("%d%m%Y")
    dosya_adi = os.path.join(rapor_klasor, "gunluk_" + tarih_str + ".txt")

    gunluk_ton   = sum(v["toplam_ton"]            for v in tum_vardiyalar)
    gunluk_yakit = sum(v["toplam_yakit_maliyet"]  for v in tum_vardiyalar)

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
        fark = HEDEF_GUNLUK - gunluk_ton
        dosya.write("SONUC        : Hedef Tutturulamadi. Fark: " + str(fark) + " ton\n")

    dosya.write("════════════════════════════════\n")
    dosya.close()

    return {"tarih": tarih.strftime("%d.%m.%Y"), "ton": gunluk_ton, "yakit": gunluk_yakit}

# ─── FONKSİYON 4: HAFTALIK RAPOR ────────────
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
        durum = "✅" if g["ton"] >= HEDEF_GUNLUK else "❌"
        dosya.write(g["tarih"] + " : " + str(g["ton"]) + " ton " + durum + "\n")

    dosya.write("────────────────────────────────\n")
    dosya.write("HAFTALIK TON   : " + str(haftalik_ton) + " ton\n")
    dosya.write("HAFTALIK YAKIT : " + str(round(haftalik_yakit, 2)) + " TL\n")
    dosya.write("════════════════════════════════\n")
    dosya.close()
    print("✅ Haftalık rapor kaydedildi!")

# ─── ANA PROGRAM ────────────────────────────
print("✅ Soma Kömür Ocağı Sistemi Başlatıldı!")
print("Tarih       : " + date.today().strftime("%d.%m.%Y"))
print("Araç sayısı : " + str(len(ARACLAR)))
print("Günlük hedef: " + str(HEDEF_GUNLUK) + " ton\n")

gunluk_veriler = []
baslangic = date.today() - timedelta(days=6)

for gun in range(7):
    tarih = baslangic + timedelta(days=gun)
    tum_vardiyalar = []

    for vardiya_adi in VARDIYALAR:
        veri = test_vardiya_olustur(vardiya_adi, tarih)
        vardiya_raporu_kaydet(veri)
        tum_vardiyalar.append(veri)

    gunluk = gunluk_rapor_kaydet(tum_vardiyalar, tarih)
    gunluk_veriler.append(gunluk)
    print(tarih.strftime("%d.%m.%Y") + " → " + str(gunluk["ton"]) + " ton")

haftalik_rapor_kaydet(gunluk_veriler)
print("\n✅ Tüm raporlar tamamlandı!")
print("Raporlar klasörü: " + rapor_klasor)