from ZKSwapClient import ZKSwapClient
from pprint import pprint
import json
# TESTING CLASS

client = ZKSwapClient(network = 1, address = '000x0')

pprint(client.pairs_by_id[128])
pprint(client.tokens_by_id[1])

pprint(client.get_complete_info_all_pairs())
info = client.get_complete_info_pair(128)
pprint(info)

# GET CONTRACT ADDRESS
print('get_contact_address '); print(client.get_contact_address())
print('get_token_list '); print(client.get_token_list())
print('get_pairs_prices'); print(client.get_pairs_prices())
print('get_account_balance'); print(client.get_account_balance())
print('get_account_info'); print(client.get_account_info())
print('get_account_fee'); print(client.get_account_fee())
print('get_transaction_list'); print(client.get_transaction_list())
print('get_transaction'); print(client.get_transaction(tx_hash = '000x0'))
print('post_submit_transaction'); print(client.post_submit_transaction())

print("client.get_amount_out(1000, 'ZKS', 'ETH')")
print(client.get_amount_out(1000, 'ZKS', 'ETH'))
print("client.get_amount_out(1000, 'ETH', 'ZKS')")
print(client.get_amount_out(1000, 'ETH', 'ZKS'))