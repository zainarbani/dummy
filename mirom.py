import os

from git import Repo
from json import dump
from requests import get
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler


def git_push():
    git_user = ""  # github username
    git_pass = ""  # github userpass
    repo_name = "dummy"  # github repo
    remote_url = f"https://{git_user}:{git_pass}@github.com/{git_user}/{repo_name}.git"
    repo = Repo(".git")

    if "modified" in repo.git.status(["mirom.json"]):
        print("New update found !")
        repo.index.add(["mirom.json"])
        repo.index.commit("mirom: " + datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
        repo.git.push(remote_url, "master")
    else:
        print("No update found !")


def miui(pid):
    url = f"http://c.mi.com/oc/rom/getdevicelist"
    res = get(url, params={"phone_id": pid}).json()
    for x in res["data"]["device_data"]["device_list"]:
        url = res["data"]["device_data"]["device_list"][f"{x}"]["stable_rom"]["rom_url"]
        data.append({"phone": x, "url": {"global": url, "ru": url, "id": url}})


def main():
    try:
        os.remove("mirom.json")
    except OSError:
        pass

    print("Fetching update, started at:", datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
    url = "https://c.mi.com/oc/rom/getphonelist"
    res = get(url).json()
    for x in res["data"]["phone_data"]["phone_list"]:
        pid = x["id"]
        miui(pid)

    with open("mirom.json", "w") as f:
        dump(data, f, indent=2)

    git_push()
    print("Fetching update done\n")


if __name__ == "__main__":
    data = []
    main()
    scheduler = BlockingScheduler()
    scheduler.add_job(main, "interval", minutes=30)
    scheduler.start()
