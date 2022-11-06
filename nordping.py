#!/usr/bin/env python3
#

import argparse
from pythonping import ping
from requests import get


def ping_host(hosts):
    avg = 1000
    best = {}
    for host in hosts:
        try:
            ping_result = ping(target=host["host"], count=10, timeout=2)
            data = {
                "idx": host["idx"],
                "avg_latency": ping_result.rtt_avg_ms,
                "pkt_loss": ping_result.packet_loss,
            }
            if ping_result.rtt_avg_ms < avg:
                best.update(data)
                avg = ping_result.rtt_avg_ms
        except RuntimeError:
            pass
    return best


def get_host(srv_url, country):
    res = get(srv_url)
    if res.status_code == 200:
        print("\nPlease wait... ")
        hosts = []
        for idx, i in enumerate(res.json()):
            if i["locations"][0]["country"]["code"].lower() == country:
                hosts.append({"idx": idx, "host": i["hostname"]})
        bidx = ping_host(hosts)
        pub_key = ""
        identifier = ""
        status = ""
        for x in res.json()[bidx["idx"]]["technologies"]:
            if x["name"] == "Wireguard":
                pub_key = x["metadata"][0]["value"]
                identifier = x["identifier"]
                status = x["pivot"]["status"]
        data = (
            f"\n ip: {res.json()[bidx['idx']]['station']}\n"
            + f" hostname: {res.json()[bidx['idx']]['hostname']}\n"
            + f" average latency: {bidx['avg_latency']}ms\n"
            + f" packet loss: {bidx['pkt_loss']}\n"
            + f" methods:\n   identifier: {identifier}\n"
            + f"   public key: {pub_key}\n"
            + f"   status: {status}"
        )
        print(data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--country",
        "-c",
        dest="country",
        default="",
        action="store",
        help="designated country",
    )
    args = parser.parse_args()
    if args.country == "":
        print("\nUsage: nordping.py -c [country]")
        exit(0)
    srv_url = "https://api.nordvpn.com/v1/servers?limit=16384"
    get_host(srv_url, args.country)
    
