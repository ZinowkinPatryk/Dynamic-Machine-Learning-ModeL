import urllib.parse


def makeURL(marka, model, typNadwozia, rokProdukcji, cenaWidelki,
            paliwo, skrzyniaBiegow, przebieg, page=1):
    url_base = ["https://www.otomoto.pl/osobowe"]
    if marka: url_base.append(marka)
    if model: url_base.append(model)
    if typNadwozia: url_base.append(f"seg-{typNadwozia}")
    if rokProdukcji: url_base.append(f"od-{rokProdukcji[0]}")
    url_base = "/".join(url_base)
    params = {}
    if cenaWidelki[0]: params["search[filter_float_price:from]"] = cenaWidelki[0]
    if cenaWidelki[1]: params["search[filter_float_price:to]"] = cenaWidelki[1]
    if rokProdukcji[1]: params["search[filter_float_year:to]"] = rokProdukcji[1]
    if paliwo: params["search[filter_enum_fuel_type]"] = paliwo
    if skrzyniaBiegow: params["search[filter_enum_gearbox]"] = skrzyniaBiegow
    if przebieg[0]:
        params["search[filter_float_mileage:from]"] = przebieg[0]
    if przebieg[1]:
        params["search[filter_float_mileage:to]"] = przebieg[1]
    params["search[order]"] = "filter_float_price:asc"
    kolejkaString = urllib.parse.urlencode(params)
    url = f"{url_base}?page={page}&{kolejkaString}" if kolejkaString else url_base
    return url

