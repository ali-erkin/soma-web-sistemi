import matplotlib
matplotlib.use('Agg')  # ← Ekran açmadan kaydetmek için
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
import os

DB_YOLU = os.path.join(os.path.dirname(__file__), "..", "maden", "maden.db")

def grafik_olustur():
    baglanti = sqlite3.connect(DB_YOLU)
    df = pd.read_sql("SELECT tarih, SUM(toplam_ton) as ton FROM vardiyalar GROUP BY tarih", baglanti)
    baglanti.close()

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    ax1.plot(df["tarih"], df["ton"], marker="o", color="blue", linewidth=2)
    ax1.axhline(y=1500, color="red", linestyle="--", linewidth=1.5)
    ax1.set_title("Günlük Üretim Trendi")
    ax1.set_ylabel("Ton")
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(True)

    renkler = ["green" if ton >= 1500 else "red" for ton in df["ton"]]
    ax2.bar(df["tarih"], df["ton"], color=renkler)
    ax2.axhline(y=1500, color="black", linestyle="--", linewidth=1.5)
    ax2.set_title("Hedef Karşılaştırması")
    ax2.set_ylabel("Ton")
    ax2.tick_params(axis='x', rotation=45)

    plt.tight_layout()

    grafik_yolu = os.path.join(os.path.dirname(__file__), "static", "grafik.png")
    plt.savefig(grafik_yolu, dpi=150)
    plt.close()