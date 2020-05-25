from os import remove
from re import findall
from json import dump
from requests import get
from bs4 import BeautifulSoup as bs


headers = {"User-Agent": "Mozilla/5.0"}

def getOta(device):
    url = f"https://www.vivo.com.cn/upgrade/detail"
    r = get(url, params={"modelId": device["id"]}, headers=headers,)
    soup = bs(r.text, "html.parser")
    info = soup.find_all("div", attrs={"class": "pack-info"})
    cl = soup.find_all("div", attrs={"class": "upgrade-logs"})
    c = findall("li>(.*)</li", str(cl))
    d = findall("p>.*: (.*)</p", str(info))[0]
    s = findall("p>.*: (.*)</p", str(info))[1]
    u = findall('href="(.*)" id', str(info))[0]
    data.append(
        {"device": device["name"], "date": d, "size": s, "url": u, "cl": "\n".join(c)}
    )


def getId():
    """ R.I.P zh-CN """
    url = "https://www.vivo.com.cn/upgrade/getModels"
    r = get(url, headers=headers).json()
    devices = []
    for i in r["data"]:
        for x in i["products"]:
            id = x["id"]
            name = x["name"].encode("utf-8")
            devices.append({"id": id, "name": name.decode("ascii", "ignore")})
    return devices


def main():
    try:
        remove("bibo.json")
    except OSError:
        pass

    devices = getId()
    for device in devices:
        if device["name"] in str(data):
            pass
        else:
            print(f"Fetching update: {device['name']}...")
            getOta(device)

    with open("bibo.json", "w") as fvck:
        dump(data, fvck, indent=4)


if __name__ == "__main__":
    data = []
    main()
