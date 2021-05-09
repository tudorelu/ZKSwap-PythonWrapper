from ZKSwapClient import ZKSwapClient
from pprint import pprint
import json
# TESTING CLASS

client = ZKSwapClient(network = 1, address = '000x0')

print("Get price of 1000 ZKS in ETH")
print(client.get_amount_out(1000, 'ZKS', 'ETH'))

print("Get price of 1000 ZKS in USDT")
print(client.get_amount_out(1000, 'ZKS', 'USDT'))