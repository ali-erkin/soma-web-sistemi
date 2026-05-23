from veri_giris import sahte_vardiya_olustur
from sabit_veriler import ARACLAR

def test_vardiya_verisi_dolu_gelir():
    from datetime import date
    veri = sahte_vardiya_olustur("Sabah", date.today())
    assert veri["vardiya"] == "Sabah"
    assert veri["toplam_ton"] >= 0
    assert len(veri["araclar"]) == len(ARACLAR)

def test_toplam_ton_hesabi():
    from datetime import date
    veri = sahte_vardiya_olustur("Sabah", date.today())
    hesaplanan = sum(a["ton"] for a in veri["araclar"])
    assert hesaplanan == veri["toplam_ton"]