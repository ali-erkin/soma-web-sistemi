import os
from dotenv import load_dotenv
load_dotenv()

DB_BAGLANTI = {
    "host"    : os.getenv("DB_HOST"),
    "port"    : int(os.getenv("DB_PORT", 6543)),
    "database": os.getenv("DB_NAME", "postgres"),
    "user"    : os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}

def baglanti_ac():
    return psycopg2.connect(**DB_BAGLANTI)

# ─── TABLOLARI OLUŞTUR ──────────────────────
def veritabani_baslat():
    baglanti = baglanti_ac()
    imleç = baglanti.cursor()

    imleç.execute("""
        CREATE TABLE IF NOT EXISTS vardiyalar (
            id           SERIAL PRIMARY KEY,
            tarih        VARCHAR(20),
            vardiya      VARCHAR(20),
            sorumlu      VARCHAR(50),
            toplam_ton   REAL,
            toplam_km    REAL,
            toplam_yakit REAL,
            created_at   TIMESTAMP DEFAULT NOW()
        )
    """)

    imleç.execute("""
        CREATE TABLE IF NOT EXISTS kullanicilar (
            id            SERIAL PRIMARY KEY,
            kullanici_adi VARCHAR(50) UNIQUE,
            sifre         VARCHAR(100),
            rol           VARCHAR(20)
        )
    """)

    imleç.execute("""
        INSERT INTO kullanicilar (kullanici_adi, sifre, rol)
        VALUES (%s, %s, %s)
        ON CONFLICT (kullanici_adi) DO NOTHING
    """, ("abc", "123", "admin"))

    imleç.execute("""
        CREATE TABLE IF NOT EXISTS araclar (
            id            SERIAL PRIMARY KEY,
            vardiya_id    INTEGER REFERENCES vardiyalar(id),
            plaka         VARCHAR(20),
            sofor         VARCHAR(50),
            durum         VARCHAR(20),
            tur           INTEGER,
            ton           REAL,
            km            REAL,
            yakit_maliyet REAL
        )
    """)

    baglanti.commit()
    baglanti.close()
    print("✅ Veritabanı hazır!")

# ─── VARDİYA KAYDET ─────────────────────────
def vardiya_kaydet(vardiya_verisi):
    baglanti = baglanti_ac()
    imleç = baglanti.cursor()

    imleç.execute("""
        INSERT INTO vardiyalar (tarih, vardiya, sorumlu, toplam_ton, toplam_km, toplam_yakit)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (tarih, vardiya) DO NOTHING
        RETURNING id
    """, (
        vardiya_verisi["tarih"],
        vardiya_verisi["vardiya"],
        vardiya_verisi["sorumlu"],
        vardiya_verisi["toplam_ton"],
        vardiya_verisi["toplam_km"],
        vardiya_verisi["toplam_yakit_maliyet"]
    ))

    sonuc = imleç.fetchone()
    if sonuc is None:
        baglanti.close()
        return

    vardiya_id = sonuc[0]

    for arac in vardiya_verisi["araclar"]:
        imleç.execute("""
            INSERT INTO araclar (vardiya_id, plaka, sofor, durum, tur, ton, km, yakit_maliyet)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            vardiya_id,
            arac["plaka"],
            arac["sofor"],
            arac["durum"],
            arac["tur"],
            arac["ton"],
            arac["km"],
            arac["yakit_maliyet"]
        ))

    baglanti.commit()
    baglanti.close()

# ─── GÜNLÜK ÖZET ────────────────────────────
def gunluk_ozet(tarih):
    baglanti = baglanti_ac()
    imleç = baglanti.cursor()

    imleç.execute("""
        SELECT vardiya, toplam_ton, toplam_yakit
        FROM vardiyalar
        WHERE tarih = %s
        ORDER BY id
    """, (tarih,))

    satirlar = imleç.fetchall()
    baglanti.close()
    return satirlar

# ─── HAFTALIK ÖZET ──────────────────────────
def haftalik_ozet():
    baglanti = baglanti_ac()
    imleç = baglanti.cursor()

    imleç.execute("""
        SELECT tarih, SUM(toplam_ton), SUM(toplam_yakit)
        FROM vardiyalar
        GROUP BY tarih
        ORDER BY tarih
    """)

    satirlar = imleç.fetchall()
    baglanti.close()
    return satirlar

# ─── KULLANICI KONTROL ───────────────────────
def kullanici_kontrol(kullanici_adi, sifre):
    baglanti = baglanti_ac()
    imleç = baglanti.cursor()

    imleç.execute("""
        SELECT * FROM kullanicilar
        WHERE kullanici_adi = %s AND sifre = %s
    """, (kullanici_adi, sifre))

    kullanici = imleç.fetchone()
    baglanti.close()

    if kullanici:
        return True
    else:
        return False

# ─── TEST ───────────────────────────────────
if __name__ == "__main__":
    veritabani_baslat()

    baglanti = baglanti_ac()
    imleç = baglanti.cursor()

    imleç.execute("SELECT COUNT(*) FROM vardiyalar")
    print("Vardiya sayısı: " + str(imleç.fetchone()[0]))

    imleç.execute("SELECT COUNT(*) FROM araclar")
    print("Araç kaydı sayısı: " + str(imleç.fetchone()[0]))

    imleç.execute("SELECT tarih, vardiya, toplam_ton FROM vardiyalar LIMIT 5")
    print("\nİlk 5 kayıt:")
    for satir in imleç.fetchall():
        print(satir)

    baglanti.close()
