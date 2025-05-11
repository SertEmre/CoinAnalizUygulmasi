import requests
import time

def kullanici_para_birimi_sec():

    print("Coin verilerini hangi para biriminde görmek istersiniz?:'usd', 'try'")
    secim = input("Lütfen bir para birimi girin (usd / try): ").strip().lower()

    if secim not in ["usd", "try"]:
        print("\nGeçersiz giriş yapıldı. Varsayılan olarak USD seçildi.\n")
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
            cevap.raise_for_status()
            sayfa_verisi = cevap.json()

            if not sayfa_verisi:
                print(f"Sayfa {sayfa_numarasi} boş geldi.")
                break

            coin_listesi.extend(sayfa_verisi)
            print(f"Sayfa {sayfa_numarasi} verileri alındı.")

            time.sleep(1)  # API'yi çok hızlı çağırmamak için 1 yaptım

        except requests.exceptions.RequestException as hata:
            print(f"Sayfa {sayfa_numarasi} alınamadı: {hata}")
            break

    print(f"\nToplam {len(coin_listesi)} coin yüklendi.\n")
    return coin_listesi

def coin_bilgisi_yazdir(coin, birim):
    print(f"{coin['name']} ({coin['symbol'].upper()})")
    print(f"Anlık Fiyat: {birim}{coin['current_price']}")
    print(f"24 Saatlik Değişim: %{coin['price_change_percentage_24h']:.2f}")
    print("-" * 20)

def coinleri_yazdir(coin_listesi, adet=10, doviz="usd"):
    birim = "$" if doviz == "usd" else "₺"

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
    para_birimi = kullanici_para_birimi_sec()
    coin_verileri = coin_verilerini_getir(toplam_sayfa=3, doviz=para_birimi)
    coinleri_yazdir(coin_verileri, adet=10, doviz=para_birimi)

main()
