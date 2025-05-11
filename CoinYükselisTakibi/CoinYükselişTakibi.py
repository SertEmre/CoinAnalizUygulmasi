import requests

def tum_coinleri_getir(sayfa_sayisi=5):
    tum_coinler = []

    for sayfa in range(1, sayfa_sayisi + 1):
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 250,
            "page": sayfa,
            "sparkline": "false",
            "price_change_percentage": "24h"
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            tum_coinler.extend(response.json())
        else:
            print(f"Hata oluştu! Sayfa: {sayfa}")
            break

    return tum_coinler

def en_cok_yukselenleri_yazdir(coin_listesi, adet=10):
    sirali = sorted(
        coin_listesi,
        key=lambda x: x["price_change_percentage_24h"] or 0,
        reverse=True
    )

    print(f"\nEn Çok Yükselen İlk {adet} Coin (24 Saatlik):\n")
    for i, coin in enumerate(sirali[:adet], 1):
        print(f"{i}. {coin['name']} ({coin['symbol'].upper()})")
        print(f"   Fiyat: ${coin['current_price']}")
        print(f"   24s Değişim: %{coin['price_change_percentage_24h']:.2f}")
        print()

coinler = tum_coinleri_getir(sayfa_sayisi=3) 
en_cok_yukselenleri_yazdir(coinler, adet=10)
