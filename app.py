import os
import sys
from datetime import date, datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, session

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "maden"))
from sabit_veriler import ARACLAR, HEDEF_GUNLUK, VARDIYALAR
from veri_giris import test_vardiya_olustur
from raporlama import vardiya_raporu_kaydet, gunluk_rapor_kaydet, haftalik_rapor_kaydet
from veritabani import gunluk_ozet, haftalik_ozet, kullanici_kontrol
from grafik import grafik_olustur

app = Flask(__name__)
app.secret_key = "soma_gizli_anahtar"

# ─── KULLANICI BİLGİLERİ ────────────────────
@app.route("/", methods=["GET", "POST"])
def giris():
    hata = ""
    if request.method == "POST":
        kullanici = request.form["kullanici"]
        sifre     = request.form["sifre"]
        if kullanici_kontrol(kullanici, sifre):
            session["kullanici"] = kullanici
            return redirect(url_for("ana_sayfa"))
        else:
            hata = "Kullanıcı adı veya şifre yanlış!"
    return render_template("giris.html", hata=hata)

# ─── ANA SAYFA ──────────────────────────────
@app.route("/ana")
def ana_sayfa():
    if "kullanici" not in session:
        return redirect(url_for("giris"))
    return render_template("ana_sayfa.html", kullanici=session["kullanici"])

# ─── ÇIKIŞ ──────────────────────────────────
@app.route("/cikis")
def cikis():
    session.clear()
    return redirect(url_for("giris"))
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "maden"))
from sabit_veriler import ARACLAR, HEDEF_GUNLUK, VARDIYALAR
from veri_giris import test_vardiya_olustur
from raporlama import vardiya_raporu_kaydet, gunluk_rapor_kaydet, haftalik_rapor_kaydet
from datetime import date, datetime, timedelta
import os

@app.route("/vardiya")
def vardiya():
    if "kullanici" not in session:
        return redirect(url_for("giris"))
    
    bugun = date.today()
    vardiya_adi, bitis = aktif_vardiya_bul()
    veri = test_vardiya_olustur(vardiya_adi, bugun)
    vardiya_raporu_kaydet(veri)
    
    mesaj = "─── " + vardiya_adi.upper() + " VARDİYASI ───\n"
    for arac in veri["araclar"]:
        durum = "✅" if arac["durum"] == "Çalışıyor" else "⚠️"
        mesaj += durum + " " + arac["plaka"] + " | " + arac["sofor"] + " → " + str(arac["ton"]) + " ton\n"
    mesaj += "─────────────────────────\n"
    mesaj += "TOPLAM TON : " + str(veri["toplam_ton"]) + " ton\n"
    mesaj += "YAKIT      : " + str(round(veri["toplam_yakit_maliyet"], 2)) + " TL\n"
    mesaj += "SONUÇ      : " + ("✅ Hedef Aşıldı!" if veri["toplam_ton"] >= 500 else "❌ Hedef Tutturulamadı!")
    
    return render_template("rapor.html", baslik="Vardiya Raporu", mesaj=mesaj)


@app.route("/gunluk")
def gunluk():
    if "kullanici" not in session:
        return redirect(url_for("giris"))

    bugun = date.today().strftime("%d.%m.%Y")
    satirlar = gunluk_ozet(bugun)

    mesaj = "─── GÜNLÜK RAPOR ───\n"
    toplam_ton   = 0
    toplam_yakit = 0

    for satir in satirlar:
        durum = "✅" if satir[1] >= 500 else "❌"
        mesaj += satir[0] + " : " + str(satir[1]) + " ton " + durum + "\n"
        toplam_ton   += satir[1]
        toplam_yakit += satir[2]

    mesaj += "─────────────────────────\n"
    mesaj += "GÜNLÜK TON   : " + str(toplam_ton) + " ton\n"
    mesaj += "GÜNLÜK YAKIT : " + str(round(toplam_yakit, 2)) + " TL\n"
    mesaj += "SONUÇ        : " + ("✅ Hedef Aşıldı!" if toplam_ton >= HEDEF_GUNLUK else "❌ Hedef Tutturulamadı!")

    return render_template("rapor.html", baslik="Günlük Rapor", mesaj=mesaj)


@app.route("/haftalik")
def haftalik():
    if "kullanici" not in session:
        return redirect(url_for("giris"))

    satirlar = haftalik_ozet()

    mesaj = "─── HAFTALIK RAPOR ───\n"
    haftalik_ton   = 0
    haftalik_yakit = 0

    for satir in satirlar:
        durum = "✅" if satir[1] >= HEDEF_GUNLUK else "❌"
        mesaj += satir[0] + " : " + str(satir[1]) + " ton " + durum + "\n"
        haftalik_ton   += satir[1]
        haftalik_yakit += satir[2]

    mesaj += "─────────────────────────\n"
    mesaj += "HAFTALIK TON   : " + str(haftalik_ton) + " ton\n"
    mesaj += "HAFTALIK YAKIT : " + str(round(haftalik_yakit, 2)) + " TL\n"

    return render_template("rapor.html", baslik="Haftalık Rapor", mesaj=mesaj)

@app.route("/grafik")
def grafik():
    if "kullanici" not in session:
        return redirect(url_for("giris"))
    grafik_olustur()
    return render_template("grafik.html")

def aktif_vardiya_bul():
    saat = datetime.now().hour
    if 7 <= saat < 15:
        return "Sabah", "15:00"
    elif 15 <= saat < 23:
        return "Öğle", "23:00"
    else:
        return "Gece", "07:00"
if __name__ == "__main__":
    app.run(debug=True)