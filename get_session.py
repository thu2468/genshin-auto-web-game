import requests
import os

if not os.environ.get('COOKIE'):
    print('Cookie not set, exiting...')
    exit(1)

def get_session():
    indiv = os.environ['COOKIE'].split(';')
    pairs = [c.split('=') for c in indiv]
    pairs = [(k.strip(),v.strip()) for (k,v) in pairs]
    s = requests.Session()
    requests.utils.add_dict_to_cookiejar(s.cookies, dict(pairs))
    return s

SESSION = get_session()
