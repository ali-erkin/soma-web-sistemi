import tkinter as tk
from datetime import date, datetime
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "maden"))
from sabit_veriler import ARACLAR, HEDEF_GUNLUK, VARDIYALAR
from veri_giris import test_vardiya_olustur
from raporlama import vardiya_raporu_kaydet, gunluk_rapor_kaydet, haftalik_rapor_kaydet

# ─── VARDİYA TESPİT ─────────────────────────
def aktif_vardiya_bul():
    saat = datetime.now().hour
    if 7 <= saat < 15:
        return "Sabah", "15:00"
    elif 15 <= saat < 23:
        return "Öğle", "23:00"
    else:
        return "Gece", "07:00"

# ─── DURUM ÇUBUĞU GÜNCELLE ──────────────────
def durum_guncelle(mesaj):
    vardiya_adi, bitis = aktif_vardiya_bul()
    tarih = date.today().strftime("%d.%m.%Y")
    durum_label.config(text=mesaj + "  |  " + tarih + " | " + vardiya_adi + " Vardiyası | Bitiş: " + bitis)

# ─── VARDİYA RAPORU ─────────────────────────
def vardiya_olustur():
    sonuc_metin.config(state="normal")
    sonuc_metin.delete("1.0", tk.END)

    bugun = date.today()
    vardiya_adi, bitis = aktif_vardiya_bul()

    veri = test_vardiya_olustur(vardiya_adi, bugun)
    vardiya_raporu_kaydet(veri)

    sonuc_metin.insert(tk.END, "─── " + vardiya_adi.upper() + " VARDİYASI ───\n")
    for arac in veri["araclar"]:
        durum = "✅" if arac["durum"] == "Çalışıyor" else "⚠️"
        sonuc_metin.insert(tk.END, durum + " " + arac["plaka"] + " → " + str(arac["ton"]) + " ton\n")

    sonuc_metin.insert(tk.END, "─────────────────────────\n")
    sonuc_metin.insert(tk.END, "TOPLAM : " + str(veri["toplam_ton"]) + " ton\n")
    sonuc_metin.insert(tk.END, "YAKIT  : " + str(round(veri["toplam_yakit_maliyet"], 2)) + " TL\n")

    if veri["toplam_ton"] >= 500:
        sonuc_metin.insert(tk.END, "SONUÇ  : ✅ Hedef Aşıldı!\n")
    else:
        sonuc_metin.insert(tk.END, "SONUÇ  : ❌ Hedef Tutturulamadı!\n")

    sonuc_metin.config(state="disabled")
    durum_guncelle("Vardiya raporu oluşturuldu")

# ─── GÜNLÜK RAPOR ───────────────────────────
def gunluk_goster():
    sonuc_metin.config(state="normal")
    sonuc_metin.delete("1.0", tk.END)

    bugun = date.today()
    saat  = datetime.now().strftime("%H:%M")
    tum_vardiyalar = []

    for v in VARDIYALAR:
        veri = test_vardiya_olustur(v, bugun)
        vardiya_raporu_kaydet(veri)
        tum_vardiyalar.append(veri)

    gunluk = gunluk_rapor_kaydet(tum_vardiyalar, bugun)

    sonuc_metin.insert(tk.END, "─── GÜNLÜK RAPOR (" + saat + ") ───\n")
    for v in tum_vardiyalar:
        durum = "✅" if v["toplam_ton"] >= 500 else "❌"
        sonuc_metin.insert(tk.END, v["vardiya"] + " : " + str(v["toplam_ton"]) + " ton " + durum + "\n")

    sonuc_metin.insert(tk.END, "─────────────────────────\n")
    sonuc_metin.insert(tk.END, "GÜNLÜK TON   : " + str(gunluk["ton"]) + " ton\n")
    sonuc_metin.insert(tk.END, "GÜNLÜK YAKIT : " + str(round(gunluk["yakit"], 2)) + " TL\n")

    if gunluk["ton"] >= HEDEF_GUNLUK:
        sonuc_metin.insert(tk.END, "SONUÇ        : ✅ Hedef Aşıldı!\n")
    else:
        fark = HEDEF_GUNLUK - gunluk["ton"]
        sonuc_metin.insert(tk.END, "SONUÇ        : ❌ Fark: " + str(fark) + " ton\n")

    sonuc_metin.config(state="disabled")
    durum_guncelle("Günlük rapor oluşturuldu")

# ─── HAFTALIK RAPOR ─────────────────────────
def haftalik_goster():
    sonuc_metin.config(state="normal")
    sonuc_metin.delete("1.0", tk.END)

    from datetime import timedelta
    gunluk_veriler = []
    bugun = date.today()

    for gun in range(7):
        tarih = bugun - timedelta(days=6-gun)
        tum_vardiyalar = []
        for v in VARDIYALAR:
            veri = test_vardiya_olustur(v, tarih)
            tum_vardiyalar.append(veri)
        gunluk = gunluk_rapor_kaydet(tum_vardiyalar, tarih)
        gunluk_veriler.append(gunluk)

    haftalik_rapor_kaydet(gunluk_veriler)

    haftalik_ton   = sum(g["ton"]   for g in gunluk_veriler)
    haftalik_yakit = sum(g["yakit"] for g in gunluk_veriler)

    sonuc_metin.insert(tk.END, "─── HAFTALIK RAPOR ───\n")
    for g in gunluk_veriler:
        durum = "✅" if g["ton"] >= HEDEF_GUNLUK else "❌"
        sonuc_metin.insert(tk.END, g["tarih"] + " : " + str(g["ton"]) + " ton " + durum + "\n")

    sonuc_metin.insert(tk.END, "─────────────────────────\n")
    sonuc_metin.insert(tk.END, "HAFTALIK TON   : " + str(haftalik_ton) + " ton\n")
    sonuc_metin.insert(tk.END, "HAFTALIK YAKIT : " + str(round(haftalik_yakit, 2)) + " TL\n")

    sonuc_metin.config(state="disabled")
    durum_guncelle("Haftalık rapor oluşturuldu")

# ─── PENCERE ────────────────────────────────
pencere = tk.Tk()
pencere.title("Soma Kömür Ocağı Yönetim Sistemi")
pencere.geometry("620x560")

baslik = tk.Label(pencere, text="⛏️ SOMA KÖMÜR OCAĞI", font=("Arial", 20, "bold"))
baslik.pack(pady=15)

btn_vardiya = tk.Button(pencere, text="📋 Vardiya Raporu Oluştur",
                        width=30, height=2, command=vardiya_olustur)
btn_vardiya.pack(pady=5)

btn_gunluk = tk.Button(pencere, text="📅 Günlük Rapor Görüntüle",
                       width=30, height=2, command=gunluk_goster)
btn_gunluk.pack(pady=5)

btn_haftalik = tk.Button(pencere, text="📊 Haftalık Rapor Görüntüle",
                         width=30, height=2, command=haftalik_goster)
btn_haftalik.pack(pady=5)

btn_cikis = tk.Button(pencere, text="❌ Çıkış",
                      width=30, height=2, command=pencere.destroy)
btn_cikis.pack(pady=5)

sonuc_metin = tk.Text(pencere, height=10, width=55, state="disabled")
sonuc_metin.pack(pady=10)

# ─── DURUM ÇUBUĞU ───────────────────────────
durum_label = tk.Label(pencere, text="", font=("Arial", 9), anchor="e")
durum_label.pack(side="bottom", fill="x", padx=10, pady=5)

durum_guncelle("Sistem hazır")

pencere.mainloop()