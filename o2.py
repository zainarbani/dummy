from os import remove
from json import dump
from requests import post
from bs4 import BeautifulSoup
from datetime import datetime


def dt(x):
    y = datetime.fromtimestamp(x / 1000)
    return y.strftime("%Y-%m-%d %H:%M:%S")


def bs(x):
    y = BeautifulSoup(x, "html.parser")
    return y.text


def getOta(url, href, id):
    files = {"storeCode": (None, "us"), "phoneCode": (None, id)}
    r = post(url + href, files=files).json()
    model = r["data"][0]["phoneName"]
    x = {"model": model, "data": {"stable": [], "beta": []}}
    text = {
        "rel": r["data"][0]["versionNo"],
        "date": dt(r["data"][0]["versionReleaseTime"]),
        "size": r["data"][0]["versionSize"],
        "md5": r["data"][0]["versionSign"],
        "log": bs(r["data"][0]["versionLog"]),
        "url": r["data"][0]["versionLink"],
    }
    x["data"]["stable"].append(text)
    if "Open Beta" in str(r["data"]):
        text = {
            "rel": r["data"][1]["versionNo"],
            "date": dt(r["data"][1]["versionReleaseTime"]),
            "size": r["data"][1]["versionSize"],
            "md5": r["data"][1]["versionSign"],
            "log": bs(r["data"][1]["versionLog"]),
            "url": r["data"][1]["versionLink"],
        }
        x["data"]["beta"].append(text)
    data.append(x)


def getId(url, href):
    files = {"storeCode": (None, "us")}
    r = post(url + href, files=files).json()
    pid = []
    for i in r["data"]:
        pid.append(i["phoneCode"])
    return pid


def main():
    try:
        remove("o2.json")
    except OSError:
        pass

    url = "https://www.oneplus.com/xman/send-in-repair/find-phone-"
    href = "models"
    pid = getId(url, href)
    for id in pid:
        href = "systems"
        getOta(url, href, id)

    with open("o2.json", "w") as fvck:
        dump(data, fvck, indent=4)


if __name__ == "__main__":
    data = []
    main()
