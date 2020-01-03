#!/usr/bin/env python3.7

import requests
import json
import os
from git import Repo
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

def git_push():
    git_user = ''#gh username
    git_pass = ''#gh userpass
    repo_name = 'dummy'#gh repo
    remote_url = f'https://{git_user}:{git_pass}@github.com/{git_user}/{repo_name}.git'
    repo = Repo('.git')

    if 'modified' in repo.git.status(['mirom.json']):
        print('New update found !')
        repo.index.add(['mirom.json'])
        repo.index.commit('mirom: ' + datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
        repo.git.push(remote_url, 'master')
    else:
        print('No update found !')

def miui(pid):
    url = f'http://c.mi.com/oc/rom/getdevicelist?phone_id={pid}'
    res = requests.get(url).json()

    for device in res['data']['device_data']['device_list']:
        rom = res['data']['device_data']['device_list'][f'{device}']['stable_rom']['rom_url']
        with open('mirom.json', 'a+') as f:
            json.dump({'device': device, 'url': rom}, f, indent=1)
            f.write(',\n')

def main():
    try:
        os.remove('mirom.json')
    except OSError:
        pass
    
    print("Fetching update, started at:", datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
    url = 'https://c.mi.com/oc/rom/getphonelist'
    res = requests.get(url).json()

    for device in res['data']['phone_data']['phone_list']:
        pid = device['id']
        miui(pid)

    git_push()
    print("Fetching update done\n")

if __name__ == '__main__':
    main()
    scheduler = BlockingScheduler()
    scheduler.add_job(main, 'interval', minutes=30)
    scheduler.start()
