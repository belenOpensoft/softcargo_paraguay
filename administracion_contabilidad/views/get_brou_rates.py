from django.http import JsonResponse
import requests
from bs4 import BeautifulSoup
import unicodedata


def brou_rates():
    brou_url = "https://www.brou.com.uy/c/portal/render_portlet?p_l_id=20593&p_p_id=cotizacionfull_WAR_broutmfportlet_INSTANCE_otHfewh1klyS"
    response = requests.get(brou_url)

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")

    rates = {}

    for row in table.find_all("tr")[1:]:  # saltamos encabezado
        cols = row.find_all("td")
        if not cols:
            continue

        currency = cols[0].find("p", class_="moneda").get_text(strip=True)
        bid = cols[2].find("p", class_="valor").get_text(strip=True)
        ask = cols[4].find("p", class_="valor").get_text(strip=True)
        spread_bid = cols[6].find("p", class_="valor").get_text(strip=True)
        spread_ask = cols[8].find("p", class_="valor").get_text(strip=True)

        # Normalizar (similar a I18n.transliterate)
        currency = unicodedata.normalize("NFKD", currency).encode("ASCII", "ignore").decode("utf-8")
        currency = currency.replace(" ", "_").lower()

        rates[currency] = {
            "bid": bid,
            "ask": ask,
            "spread_bid": spread_bid,
            "spread_ask": spread_ask,
        }
    return JsonResponse(rates)