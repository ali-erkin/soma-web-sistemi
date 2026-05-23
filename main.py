import os
from veritabani import veritabani_baslat, vardiya_kaydet, gunluk_ozet, haftalik_ozet
from datetime import date, timedelta
from sabit_veriler import ARACLAR, HEDEF_GUNLUK, VARDIYALAR
from veri_giris import sahte_vardiya_olustur
from raporlama    import vardiya_raporu_kaydet, gunluk_rapor_kaydet, haftalik_rapor_kaydet
veritabani_baslat()
# ─── SİSTEM BAŞLAT ──────────────────────────
print("✅ Soma Kömür Ocağı Sistemi Başlatıldı!")
print("Tarih       : " + date.today().strftime("%d.%m.%Y"))
print("Araç sayısı : " + str(len(ARACLAR)))
print("Günlük hedef: " + str(HEDEF_GUNLUK) + " ton\n")

# ─── 7 GÜNLÜK VERİ ──────────────────────────
gunluk_veriler = []
baslangic = date.today() - timedelta(days=6)

for gun in range(7):
    tarih = baslangic + timedelta(days=gun)
    tum_vardiyalar = []

    for vardiya_adi in VARDIYALAR:
        veri = sahte_vardiya_olustur(vardiya_adi, tarih)
        vardiya_raporu_kaydet(veri)
        vardiya_kaydet(veri)
        tum_vardiyalar.append(veri)

    gunluk = gunluk_rapor_kaydet(tum_vardiyalar, tarih)
    gunluk_veriler.append(gunluk)
    print(tarih.strftime("%d.%m.%Y") + " → " + str(gunluk["ton"]) + " ton")

# ─── HAFTALIK RAPOR ─────────────────────────
haftalik_rapor_kaydet(gunluk_veriler)
print("\n✅ Tüm raporlar tamamlandı!")