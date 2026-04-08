import urllib.parse


def makeURL(marka, model, page=1):
    url_base = ["https://www.otomoto.pl/osobowe"]
    if marka: url_base.append(marka)
    if model: url_base.append(model)
    url_base = "/".join(url_base)
    params = {}
    params["search[order]"] = "filter_float_price:asc"
    kolejkaString = urllib.parse.urlencode(params)
    url = f"{url_base}?page={page}&{kolejkaString}" if kolejkaString else url_base
    return url

