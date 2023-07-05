from bit import PrivateKeyTestnet
my_key = PrivateKeyTestnet('cSNYdM5m5mE1EUmwimp7wZHfoAZo4aKU3aNALzdVuTBiANo8BgfG')
tx_hash = my_key.send([('mkZwNtbAYtp4zimgvm8ayvHD5dU3bkTYNd', 1, 'usd')])
print(tx_hash)