from requests_html import HTMLSession
from lxml import html
etree = html.etree
session = HTMLSession()
r = session.get('https://api.blockcypher.com/v1/btc/test3/addrs/mkZwNtbAYtp4zimgvm8ayvHD5dU3bkTYNd')
with open("txdata.txt","w",encoding='utf-8') as f:
    f.write(r.html.full_text)


