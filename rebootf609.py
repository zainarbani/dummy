import requests
from hashlib import sha256
from random import randint
from re import findall


def rebootRouter(dom, stoken, ses):
    url = dom + "/getpage.gch?pid=1002&nextpage=manager_dev_conf_t.gch"
    dat = {
        "IF_ACTION": "devrestart",
        "IF_ERRORSTR": "SUCC",
        "IF_ERRORPARAM": "SUCC",
        "IF_ERRORTYPE": "-1",
        "flag": "1",
        "_SESSION_TOKEN": stoken[0],
    }
    req = ses[0]
    r = req.post(url, data=dat)
    res = findall(r"flag','(.*)'\)", r.text)
    if res[0] == "1":
        print("Reboot OK!")
    else:
        print("Reboot failed!")


def genSes(dom, pw):
    req = requests.Session()
    r = req.get(dom)
    flt = findall(r'"Frm_Logintoken", "(.*)"\)', r.text)
    flct = findall(r'"Frm_Loginchecktoken", "(.*)"\)', r.text)
    rnd = randint(10000000, 89999999)
    phash = sha256((pw + str(rnd)).encode()).hexdigest()
    return [req, flt[0], flct[0], rnd, phash]


def genTok(dom, un, ses):
    dat = {
        "action": "login",
        "Username": un,
        "Password": ses[4],
        "Frm_Logintoken": ses[1],
        "Frm_Loginchecktoken": ses[2],
        "UserRandomNum": ses[3],
    }
    req = ses[0]
    r = req.post(dom, data=dat, allow_redirects=False)
    if "Location" in r.headers:
        r = req.get(dom + "/template.gch")
        return findall(r'session_token = "(.*)";', r.text)
    else:
        print("Invalid username or password!")
        return False


if __name__ == "__main__":
    url = "http://192.168.1.1"
    usern = "admin"
    passw = "Telkomdso123"
    ses = genSes(url, passw)
    stoken = genTok(url, usern, ses)
    if stoken:
        print(stoken[0])
        rebootRouter(url, stoken, ses)
