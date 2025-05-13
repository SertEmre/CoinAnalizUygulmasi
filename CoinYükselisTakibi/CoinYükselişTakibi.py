import requests
import time
from datetime import datetime 

def kullanici_para_birimi_secimi():
    desteklenen_birimler = ["usd", "try", "eur", "gbp", "jpy", "btc"]
    print("Coin verilerini hangi para biriminde görmek istersiniz?")
    print(f"Desteklenen birimler: {', '.join(desteklenen_birimler)}")

    secim = input("Lütfen bir para birimi girin: ").strip().lower()

    if secim not in desteklenen_birimler:
        print("\nDesteklenmeyen para birimi. Varsayılan olarak USD seçildi.\n")
        secim = "usd"
    else:
        print(f"\n{secim.upper()} seçildi. Veriler bu para birimiyle gösterilecek.\n")

    return secim

def coin_verilerini_getir(toplam_sayfa=3, doviz="usd"):

    coin_listesi = []

    for sayfa_numarasi in range(1, toplam_sayfa + 1):
        url = "https://api.coingecko.com/api/v3/coins/markets"
        parametreler = {
            "vs_currency": doviz,
            "order": "market_cap_desc",
            "per_page": 250,
            "page": sayfa_numarasi,
            "sparkline": "false",
            "price_change_percentage": "24h"
        }

        try:
            cevap = requests.get(url, params=parametreler, timeout=10)
            cevap.raise_for_status() # hatayı bir HTTPError olarak yakalayıp programı durdurur
            sayfa_verisi = cevap.json()

            if not sayfa_verisi:
                break

            coin_listesi.extend(sayfa_verisi)
            print(f"Sayfa {sayfa_numarasi} verileri alındı.")

            time.sleep(1)  # API'yi çok hızlı çağırmamak için 1 yaptım

        except requests.exceptions.RequestException as hata:
            print(f"Sayfa {sayfa_numarasi} alınamadı: {hata}")
            break

    return coin_listesi

def coin_bilgisi_yazdir(coin, birim):
    print(f"{coin['name']} ({coin['symbol'].upper()})")
    print(f"Anlık Fiyat: {birim}{coin['current_price']}")
    print(f"24 Saatlik Değişim: %{coin['price_change_percentage_24h']:.2f}")
    print("-" * 20)

def coinleri_yazdir(coin_listesi, adet=10, doviz="usd"):
    semboller = {
        "usd": "$",
        "try": "₺",
        "eur": "€",
        "gbp": "£",
        "jpy": "¥",
        "btc": "₿"
    }

    birim = semboller.get(doviz, "")  # Bilinmeyen birim varsa boş bırakıyorum

    if not coin_listesi:
        print("Gösterilecek coin bulunamadı.")
        return

    yukselenler = sorted(
        coin_listesi,
        key=lambda c: c["price_change_percentage_24h"] or 0,
        reverse=True
    )

    print(f"\n24 Saatte En Çok Yükselen {adet} Coin ({doviz.upper()}):")
    print("-" * 20)
    for i, coin in enumerate(yukselenler[:adet], start=1):
        print(f"{i}.", end=" ")
        coin_bilgisi_yazdir(coin, birim)

    dusenler = sorted(
        coin_listesi,
        key=lambda c: c["price_change_percentage_24h"] or 0
    )

    print(f"\n24 Saatte En Çok Düşen {adet} Coin ({doviz.upper()}):")
    print("-" * 20)
    for i, coin in enumerate(dusenler[:adet], start=1):
        print(f"{i}.", end=" ")
        coin_bilgisi_yazdir(coin, birim)

def main():
    print("-"*20+"Coin Yükseliş & Düşüş Takip Aracı"+"-" * 20)
    para_birimi = kullanici_para_birimi_secimi()


    while True:
        su_an = datetime.now()
        tarih_zamah = su_an.strftime("%d/%m/%Y %H:%M:%S")
        coin_verileri = coin_verilerini_getir(toplam_sayfa=3, doviz=para_birimi)
        coinleri_yazdir(coin_verileri, adet=3, doviz=para_birimi)

        islem = input("Veri güncelemeye devam etmek için Enter'a, çıkmak için 'q' tuşuna basın: ").strip().lower()
        if islem == 'q':
            print("Program sonlandırıldı.")
            break

        print("5 Dakika sonra veriler tekrardan güncellenecek")
        time.sleep(300)        
main()
